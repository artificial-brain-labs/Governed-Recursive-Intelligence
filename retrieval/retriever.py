"""Reference implementation of PCG relevance retrieval for GRI v0.1.

This module is intentionally read-only. It implements explicit-seed and
relationship-aware retrieval over the current CognitiveState representation
without treating similarity, absence, or inferred identity as fact.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping
from uuid import uuid4

from kernel import CognitiveState


class RetrievalStatus(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    NO_RELEVANT_COGNITION_FOUND = "no_relevant_cognition_found"
    AMBIGUOUS = "ambiguous"
    RETRIEVAL_FAILURE = "retrieval_failure"
    ACCESS_RESTRICTED = "access_restricted"


@dataclass(frozen=True)
class RetrievalSeed:
    """Explicitly established retrieval reference."""

    seed_id: str
    target_type: str
    target_id: str
    reason: str = "explicit_requirement_reference"


@dataclass(frozen=True)
class RetrievalContext:
    interaction_id: str
    instance_id: str
    requirement: Any
    goal_context: Mapping[str, Any] = field(default_factory=dict)
    active_dimensions: Mapping[str, Any] = field(default_factory=dict)
    current_entities: tuple[str, ...] = ()
    current_concepts: tuple[str, ...] = ()
    current_relationships: tuple[str, ...] = ()
    temporal_requirements: Mapping[str, Any] = field(default_factory=dict)
    evidence_requirements: Mapping[str, Any] = field(default_factory=dict)
    processing_history: tuple[Mapping[str, Any], ...] = ()
    security_context: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class RetrievalResult:
    retrieval_id: str
    requirement_reference: Any
    selected_objects: dict[str, Any] = field(default_factory=dict)
    selected_relationships: dict[str, Any] = field(default_factory=dict)
    selected_dimensions: dict[str, Any] = field(default_factory=dict)
    supporting_evidence_references: dict[str, Any] = field(default_factory=dict)
    unresolved_candidates: list[dict[str, Any]] = field(default_factory=list)
    ambiguities: list[dict[str, Any]] = field(default_factory=list)
    retrieval_status: RetrievalStatus = RetrievalStatus.NO_RELEVANT_COGNITION_FOUND
    expansion_history: list[dict[str, Any]] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)


class PCRRM:
    """Bounded, non-mutating persistent-cognition retrieval."""

    def __init__(self, *, max_expansion_depth: int = 1):
        if max_expansion_depth < 0:
            raise ValueError("max_expansion_depth must be >= 0")
        self.max_expansion_depth = max_expansion_depth

    @staticmethod
    def _object_store(state: CognitiveState, target_type: str) -> dict[str, Any] | None:
        mapping = {
            "belief": state.pcg,
            "concept": state.pcg,
            "identity": state.pcg,
            "goal": state.goals,
            "dimension": state.dimensions,
            "relationship": state.relationships,
            "learning_state": state.learning,
        }
        return mapping.get(target_type)

    @staticmethod
    def _access_allowed(reference: Any, context: RetrievalContext) -> bool:
        restricted = context.security_context.get("restricted_object_ids", ())
        if isinstance(reference, Mapping):
            object_id = reference.get("object_id") or reference.get("id")
            if object_id in restricted:
                return False
        return True

    def retrieve(
        self,
        state: CognitiveState,
        context: RetrievalContext,
        *,
        seeds: list[RetrievalSeed] | tuple[RetrievalSeed, ...] = (),
    ) -> RetrievalResult:
        retrieval_id = f"RET-{uuid4().hex[:12]}"
        result = RetrievalResult(
            retrieval_id=retrieval_id,
            requirement_reference=context.requirement,
            provenance={
                "retrieval": "gri-pcrrm-v0.1",
                "interaction_id": context.interaction_id,
                "instance_id": context.instance_id,
                "state_id": state.state_id,
                "state_version": state.state_version,
                "seed_ids": [seed.seed_id for seed in seeds],
            },
        )

        if not seeds:
            result.retrieval_status = RetrievalStatus.NO_RELEVANT_COGNITION_FOUND
            result.unresolved_candidates.append({
                "reason": "no_explicit_retrieval_seed",
                "requirement": context.requirement,
            })
            return result

        selected_ids: set[str] = set()
        for seed in seeds:
            store = self._object_store(state, seed.target_type)
            if store is None:
                result.unresolved_candidates.append({
                    "seed_id": seed.seed_id,
                    "target_type": seed.target_type,
                    "target_id": seed.target_id,
                    "reason": "unsupported_target_type",
                })
                continue
            if seed.target_id not in store:
                result.unresolved_candidates.append({
                    "seed_id": seed.seed_id,
                    "target_type": seed.target_type,
                    "target_id": seed.target_id,
                    "reason": "target_not_found",
                })
                continue

            reference = store[seed.target_id]
            if not self._access_allowed(reference, context):
                result.ambiguities.append({
                    "seed_id": seed.seed_id,
                    "target_id": seed.target_id,
                    "status": RetrievalStatus.ACCESS_RESTRICTED.value,
                })
                continue

            selected_ids.add(seed.target_id)
            bucket = {
                "goal": result.selected_objects,
                "dimension": result.selected_dimensions,
                "relationship": result.selected_relationships,
            }.get(seed.target_type, result.selected_objects)
            bucket[seed.target_id] = {
                "target_type": seed.target_type,
                "target_id": seed.target_id,
                "value": reference,
                "retrieval_reason": seed.reason,
            }
            result.expansion_history.append({
                "layer": 1,
                "seed_id": seed.seed_id,
                "target_id": seed.target_id,
                "reason": seed.reason,
            })

        if self.max_expansion_depth >= 1 and result.selected_objects:
            self._expand_relationships(state, context, result, selected_ids)

        if result.ambiguities and not result.selected_objects and not result.selected_relationships and not result.selected_dimensions:
            result.retrieval_status = RetrievalStatus.ACCESS_RESTRICTED
        elif result.selected_objects or result.selected_relationships or result.selected_dimensions:
            result.retrieval_status = (
                RetrievalStatus.PARTIAL if result.unresolved_candidates else RetrievalStatus.COMPLETE
            )
        else:
            result.retrieval_status = RetrievalStatus.NO_RELEVANT_COGNITION_FOUND

        return result

    def _expand_relationships(
        self,
        state: CognitiveState,
        context: RetrievalContext,
        result: RetrievalResult,
        selected_ids: set[str],
    ) -> None:
        relationships = state.relationships
        target_ids = set(context.current_relationships)
        for relationship_id, relationship in relationships.items():
            if not isinstance(relationship, Mapping):
                continue
            source = relationship.get("source_id") or relationship.get("source")
            target = relationship.get("target_id") or relationship.get("target")
            relation_id = relationship.get("relationship_id") or relationship.get("id") or relationship_id
            if not ({source, target} & selected_ids) and relation_id not in target_ids:
                continue
            if not self._access_allowed(relationship, context):
                result.ambiguities.append({
                    "relationship_id": relation_id,
                    "status": RetrievalStatus.ACCESS_RESTRICTED.value,
                })
                continue
            result.selected_relationships[relation_id] = {
                "target_type": "relationship",
                "target_id": relation_id,
                "value": relationship,
                "retrieval_reason": "established_relationship_expansion",
            }
            result.expansion_history.append({
                "layer": 2,
                "relationship_id": relation_id,
                "source_id": source,
                "target_id": target,
                "reason": "established_relationship_expansion",
            })

            for neighbor_id in (source, target):
                if neighbor_id in selected_ids:
                    continue
                if neighbor_id in state.pcg:
                    result.selected_objects[neighbor_id] = {
                        "target_type": "identity_or_pcg_object",
                        "target_id": neighbor_id,
                        "value": state.pcg[neighbor_id],
                        "retrieval_reason": "relationship_neighbor",
                    }
