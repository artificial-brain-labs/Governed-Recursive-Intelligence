"""Reference Internal Cognition Sufficiency Model (ICSM) for GRI v0.1.

ICSM evaluates whether currently retrieved cognition and available native
capability are sufficient for a requirement. It is non-mutating and does not
make truth judgments or choose a routing destination.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping
from uuid import uuid4


class SufficiencyState(str, Enum):
    SUFFICIENT = "sufficient"
    PARTIALLY_SUFFICIENT = "partially_sufficient"
    INSUFFICIENT = "insufficient"
    UNKNOWN = "unknown"
    AMBIGUOUS = "ambiguous"
    RETRIEVAL_FAILURE = "retrieval_failure"
    CONFLICT = "conflict"


class GapType(str, Enum):
    KNOWLEDGE = "knowledge_gap"
    CAPABILITY = "capability_gap"
    COMBINED = "combined_gap"


@dataclass(frozen=True)
class SufficiencyContext:
    interaction_id: str
    instance_id: str
    requirement: Any
    relevant_cognition: Mapping[str, Any] = field(default_factory=dict)
    retrieval_status: str | None = None
    evidence_state: str | None = None
    freshness_state: str | None = None
    consistency_state: str | None = None
    identity_context_state: str | None = None
    native_capability_state: str | None = None
    icg_context: Mapping[str, Any] = field(default_factory=dict)
    uncertainty_state: Mapping[str, Any] = field(default_factory=dict)
    available_native_capabilities: tuple[str, ...] = ()


@dataclass
class SufficiencyEvaluation:
    evaluation_id: str
    requirement_state: SufficiencyState
    relevant_cognition: dict[str, Any]
    coverage: str
    evidence_state: str
    freshness_state: str
    consistency_state: str
    identity_context_state: str
    native_capability_state: str
    knowledge_gaps: list[str] = field(default_factory=list)
    capability_gaps: list[str] = field(default_factory=list)
    internal_recovery_options: list[str] = field(default_factory=list)
    unresolved_questions: list[str] = field(default_factory=list)
    gap_type: GapType | None = None
    provenance: dict[str, Any] = field(default_factory=dict)


class ICSM:
    """Non-mutating sufficiency evaluation reference implementation."""

    def evaluate(self, context: SufficiencyContext) -> SufficiencyEvaluation:
        status = (context.retrieval_status or "").strip().lower()
        evidence = (context.evidence_state or "unresolved").strip().lower()
        freshness = (context.freshness_state or "unresolved").strip().lower()
        consistency = (context.consistency_state or "no_detected_conflict").strip().lower()
        identity = (context.identity_context_state or "resolved").strip().lower()
        capability = (context.native_capability_state or "available").strip().lower()

        knowledge_gaps: list[str] = []
        capability_gaps: list[str] = []
        recovery: list[str] = []
        unresolved: list[str] = []

        # Operational retrieval failure is kept distinct from knowledge absence.
        if status == "retrieval_failure":
            return self._result(
                context,
                SufficiencyState.RETRIEVAL_FAILURE,
                coverage="unresolved",
                evidence=evidence,
                freshness=freshness,
                consistency=consistency,
                identity=identity,
                capability=capability,
                knowledge_gaps=knowledge_gaps,
                capability_gaps=capability_gaps,
                recovery=["retry_retrieval", "alternate_retrieval_mechanism"],
                unresolved=["retrieval could not be completed reliably"],
            )

        if consistency in {"conflict", "unresolved_conflict"}:
            return self._result(
                context,
                SufficiencyState.CONFLICT,
                coverage="conflicted",
                evidence=evidence,
                freshness=freshness,
                consistency=consistency,
                identity=identity,
                capability=capability,
                recovery=["retrieve_provenance", "evaluate_conflict", "clarify"],
                unresolved=["relevant persistent cognition is conflicting"],
            )

        if identity in {"ambiguous", "unresolved"}:
            return self._result(
                context,
                SufficiencyState.AMBIGUOUS,
                coverage="unresolved",
                evidence=evidence,
                freshness=freshness,
                consistency=consistency,
                identity=identity,
                capability=capability,
                recovery=["resolve_reference", "clarify"],
                unresolved=["required identity/context is not uniquely resolved"],
            )

        if status == "access_restricted":
            return self._result(
                context,
                SufficiencyState.INSUFFICIENT,
                coverage="inaccessible",
                evidence=evidence,
                freshness=freshness,
                consistency=consistency,
                identity=identity,
                capability=capability,
                recovery=["request_authorized_access", "use_permitted_context"],
                unresolved=["relevant cognition is inaccessible"],
            )

        selected = bool(context.relevant_cognition)
        no_relevant = status in {
            "",
            "no_relevant_cognition_found",
        } and not selected

        if no_relevant:
            knowledge_gaps.append("no_established_relevant_cognition")
            unresolved.append("required relevant cognition has not been established")
            gap = GapType.KNOWLEDGE
            if capability in {"unavailable", "insufficient"}:
                capability_gaps.append("required_native_capability_unavailable")
                gap = GapType.COMBINED
            return self._result(
                context,
                SufficiencyState.UNKNOWN,
                coverage="absent",
                evidence=evidence,
                freshness=freshness,
                consistency=consistency,
                identity=identity,
                capability=capability,
                knowledge_gaps=knowledge_gaps,
                capability_gaps=capability_gaps,
                recovery=["additional_retrieval", "investigate", "clarify"],
                unresolved=unresolved,
                gap_type=gap,
            )

        coverage = "sufficient"
        if status == "partial":
            coverage = "partial"
        elif status not in {"complete", "partial"}:
            coverage = "unresolved"

        if coverage == "partial":
            knowledge_gaps.append("retrieval_scope_is_partial")
            recovery.extend(["additional_retrieval", "evaluate_missing_requirements"])

        if evidence in {"insufficient", "missing", "unresolved"}:
            knowledge_gaps.append("evidence_state_not_adequate")
            recovery.append("inspect_additional_evidence")

        if freshness in {"stale", "inadequate", "unresolved"}:
            knowledge_gaps.append("temporal_adequacy_not_established")
            recovery.append("retrieve_temporally_appropriate_information")

        if capability in {"unavailable", "insufficient"}:
            capability_gaps.append("required_native_capability_unavailable")
            recovery.append("select_authorized_external_or_native_capability")

        if knowledge_gaps and capability_gaps:
            gap = GapType.COMBINED
        elif capability_gaps:
            gap = GapType.CAPABILITY
        elif knowledge_gaps:
            gap = GapType.KNOWLEDGE
        else:
            gap = None

        if coverage == "partial":
            result_state = SufficiencyState.PARTIALLY_SUFFICIENT
        elif knowledge_gaps and not unresolved:
            result_state = SufficiencyState.INSUFFICIENT
        elif capability_gaps and not knowledge_gaps:
            result_state = SufficiencyState.INSUFFICIENT
        elif knowledge_gaps or capability_gaps:
            result_state = SufficiencyState.INSUFFICIENT
        else:
            result_state = SufficiencyState.SUFFICIENT

        return self._result(
            context,
            result_state,
            coverage=coverage,
            evidence=evidence,
            freshness=freshness,
            consistency=consistency,
            identity=identity,
            capability=capability,
            knowledge_gaps=knowledge_gaps,
            capability_gaps=capability_gaps,
            recovery=list(dict.fromkeys(recovery)),
            unresolved=unresolved,
            gap_type=gap,
        )

    @staticmethod
    def _result(
        context: SufficiencyContext,
        state: SufficiencyState,
        *,
        coverage: str,
        evidence: str,
        freshness: str,
        consistency: str,
        identity: str,
        capability: str,
        knowledge_gaps: list[str],
        capability_gaps: list[str],
        recovery: list[str],
        unresolved: list[str],
        gap_type: GapType | None = None,
    ) -> SufficiencyEvaluation:
        return SufficiencyEvaluation(
            evaluation_id=f"ICS-{uuid4().hex[:12]}",
            requirement_state=state,
            relevant_cognition=dict(context.relevant_cognition),
            coverage=coverage,
            evidence_state=evidence,
            freshness_state=freshness,
            consistency_state=consistency,
            identity_context_state=identity,
            native_capability_state=capability,
            knowledge_gaps=knowledge_gaps,
            capability_gaps=capability_gaps,
            internal_recovery_options=list(dict.fromkeys(recovery)),
            unresolved_questions=unresolved,
            gap_type=gap_type,
            provenance={
                "icsm": "gri-icsm-v0.1",
                "interaction_id": context.interaction_id,
                "instance_id": context.instance_id,
                "evaluation_type": "sufficiency",
            },
        )
