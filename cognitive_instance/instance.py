"""Bounded Cognitive Instance lifecycle for GRI v0.1."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class CognitiveInstanceError(RuntimeError):
    """Raised when a Cognitive Instance lifecycle transition is invalid."""


class ProcessingState(str, Enum):
    CREATED = "created"
    ENVELOPE_READY = "envelope_ready"
    INTERACTION_IDENTIFIED = "interaction_identified"
    CURIOSITY_ACTIVE = "curiosity_active"
    CONTEXT_EVALUATION = "context_evaluation"
    PROCESSING = "processing"
    ROUTING = "routing"
    DELEGATED_PROCESSING = "delegated_processing"
    REENTRY_VALIDATION = "reentry_validation"
    EVIDENCE_EVALUATION = "evidence_evaluation"
    PROPOSAL_READY = "proposal_ready"
    NULL_READY = "null_ready"
    CONSOLIDATION_READY = "consolidation_ready"
    HANDED_TO_CCA = "handed_to_cca"
    CLOSED = "closed"
    CLARIFICATION_REQUIRED = "clarification_required"
    BLOCKED = "blocked"
    TERMINATED = "terminated"
    DELEGATION_FAILED = "delegation_failed"


_TERMINAL = {
    ProcessingState.CLOSED,
    ProcessingState.TERMINATED,
}

_ALLOWED = {
    ProcessingState.CREATED: {ProcessingState.ENVELOPE_READY},
    ProcessingState.ENVELOPE_READY: {ProcessingState.INTERACTION_IDENTIFIED},
    ProcessingState.INTERACTION_IDENTIFIED: {ProcessingState.CURIOSITY_ACTIVE},
    ProcessingState.CURIOSITY_ACTIVE: {
        ProcessingState.CONTEXT_EVALUATION,
        ProcessingState.CLARIFICATION_REQUIRED,
        ProcessingState.BLOCKED,
    },
    ProcessingState.CONTEXT_EVALUATION: {
        ProcessingState.PROCESSING,
        ProcessingState.CLARIFICATION_REQUIRED,
        ProcessingState.BLOCKED,
    },
    ProcessingState.PROCESSING: {
        ProcessingState.ROUTING,
        ProcessingState.EVIDENCE_EVALUATION,
        ProcessingState.TERMINATED,
    },
    ProcessingState.ROUTING: {
        ProcessingState.PROCESSING,
        ProcessingState.DELEGATED_PROCESSING,
        ProcessingState.EVIDENCE_EVALUATION,
        ProcessingState.CLARIFICATION_REQUIRED,
        ProcessingState.BLOCKED,
    },
    ProcessingState.DELEGATED_PROCESSING: {
        ProcessingState.REENTRY_VALIDATION,
        ProcessingState.DELEGATION_FAILED,
    },
    ProcessingState.REENTRY_VALIDATION: {
        ProcessingState.CONTEXT_EVALUATION,
        ProcessingState.PROCESSING,
        ProcessingState.EVIDENCE_EVALUATION,
        ProcessingState.CLARIFICATION_REQUIRED,
        ProcessingState.BLOCKED,
    },
    ProcessingState.EVIDENCE_EVALUATION: {
        ProcessingState.PROPOSAL_READY,
        ProcessingState.NULL_READY,
    },
    ProcessingState.PROPOSAL_READY: {ProcessingState.CONSOLIDATION_READY},
    ProcessingState.NULL_READY: {ProcessingState.CONSOLIDATION_READY},
    ProcessingState.CONSOLIDATION_READY: {ProcessingState.HANDED_TO_CCA},
    ProcessingState.HANDED_TO_CCA: {ProcessingState.CLOSED},
    ProcessingState.CLARIFICATION_REQUIRED: {ProcessingState.CLOSED},
    ProcessingState.BLOCKED: {ProcessingState.CLOSED},
    ProcessingState.DELEGATION_FAILED: {
        ProcessingState.ROUTING,
        ProcessingState.CLARIFICATION_REQUIRED,
        ProcessingState.BLOCKED,
        ProcessingState.CLOSED,
    },
    ProcessingState.TERMINATED: {ProcessingState.CLOSED},
    ProcessingState.CLOSED: set(),
}


@dataclass
class InteractionCognitiveGraph:
    """Temporary interaction-scoped graph state.

    This is deliberately a lightweight runtime container. It is not PCG.
    """

    persistent_references: dict[str, Any] = field(default_factory=dict)
    candidates: dict[str, Any] = field(default_factory=dict)
    evidence: dict[str, Any] = field(default_factory=dict)
    interpretations: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    activations: dict[str, Any] = field(default_factory=dict)
    relationships: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class CognitiveInstance:
    """Temporary orchestration context for one cognitive-processing lifecycle."""

    interaction_id: str
    communication: Any
    instance_id: str = field(default_factory=lambda: f"CI-{uuid4().hex[:12]}")
    processing_state: ProcessingState = ProcessingState.CREATED
    icg: InteractionCognitiveGraph = field(default_factory=InteractionCognitiveGraph)
    active_dimensions: dict[str, Any] = field(default_factory=dict)
    retrieval_context: dict[str, Any] = field(default_factory=dict)
    routing_history: list[dict[str, Any]] = field(default_factory=list)
    frontier_history: list[dict[str, Any]] = field(default_factory=list)
    candidates: dict[str, Any] = field(default_factory=dict)
    proposals: dict[str, Any] = field(default_factory=dict)
    uncertainty: dict[str, Any] = field(default_factory=dict)
    lifecycle_history: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.interaction_id:
            raise CognitiveInstanceError("interaction_id is required")
        self.lifecycle_history.append(self.processing_state.value)

    @property
    def state(self) -> str:
        return self.processing_state.value

    @property
    def closed(self) -> bool:
        return self.processing_state == ProcessingState.CLOSED

    def transition(self, new_state: ProcessingState | str) -> None:
        target = ProcessingState(new_state)
        if target == self.processing_state:
            raise CognitiveInstanceError(
                f"invalid lifecycle transition: already in {target.value}"
            )
        if target not in _ALLOWED[self.processing_state]:
            raise CognitiveInstanceError(
                f"invalid lifecycle transition: "
                f"{self.processing_state.value} -> {target.value}"
            )
        self.processing_state = target
        self.lifecycle_history.append(target.value)

    def activate_curiosity(self) -> None:
        self.transition(ProcessingState.CURIOSITY_ACTIVE)
        self.active_dimensions.setdefault(
            "curiosity",
            {"active": True, "initial_activation": True},
        )

    def add_persistent_reference(self, reference_id: str, reference: Any) -> None:
        if not reference_id:
            raise CognitiveInstanceError("reference_id is required")
        if reference_id in self.icg.persistent_references:
            raise CognitiveInstanceError(
                f"persistent reference already exists: {reference_id}"
            )
        self.icg.persistent_references[reference_id] = reference

    def add_evidence(self, evidence_id: str, evidence: Any) -> None:
        if not evidence_id:
            raise CognitiveInstanceError("evidence_id is required")
        self.icg.evidence[evidence_id] = evidence

    def add_candidate(self, candidate_id: str, candidate: Any) -> None:
        if not candidate_id:
            raise CognitiveInstanceError("candidate_id is required")
        self.icg.candidates[candidate_id] = candidate
        self.candidates[candidate_id] = candidate

    def add_proposal(self, proposal_id: str, proposal: Any) -> None:
        if not proposal_id:
            raise CognitiveInstanceError("proposal_id is required")
        self.proposals[proposal_id] = proposal

    def record_routing(self, decision: dict[str, Any]) -> None:
        self.routing_history.append(dict(decision))

    def record_frontier_output(self, response: dict[str, Any]) -> None:
        # Recording is not endorsement. The response remains interaction-scoped
        # until it re-enters GRI's validation/evaluation process.
        self.frontier_history.append(dict(response))

    def mark_proposal_ready(self) -> None:
        self.transition(ProcessingState.PROPOSAL_READY)

    def mark_null_ready(self) -> None:
        self.transition(ProcessingState.NULL_READY)

    def mark_consolidation_ready(self) -> None:
        if self.processing_state not in {
            ProcessingState.PROPOSAL_READY,
            ProcessingState.NULL_READY,
        }:
            raise CognitiveInstanceError(
                "consolidation requires proposal_ready or null_ready"
            )
        self.transition(ProcessingState.CONSOLIDATION_READY)

    def handoff_to_cca(self) -> None:
        if self.processing_state != ProcessingState.CONSOLIDATION_READY:
            raise CognitiveInstanceError(
                "CCA handoff requires consolidation readiness"
            )
        self.transition(ProcessingState.HANDED_TO_CCA)

    def close(self) -> None:
        if self.processing_state not in {
            ProcessingState.HANDED_TO_CCA,
            ProcessingState.CLARIFICATION_REQUIRED,
            ProcessingState.BLOCKED,
            ProcessingState.TERMINATED,
            ProcessingState.DELEGATION_FAILED,
        }:
            raise CognitiveInstanceError(
                "instance cannot close before a valid terminal boundary"
            )
        self.transition(ProcessingState.CLOSED)

    def assert_not_persistent_owner(self) -> None:
        """Document the runtime boundary: CI has no persistent-state writer."""
        if hasattr(self, "pcg") or hasattr(self, "cstr"):
            raise CognitiveInstanceError(
                "Cognitive Instance must not own persistent cognition or CSTR"
            )
