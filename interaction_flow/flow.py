"""Unified executable cognitive interaction flow for GRI v0.1.

This module composes existing bounded runtimes without becoming a new
persistent-state authority, governance layer, or frontier provider.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from cognitive_instance import CognitiveInstance, ProcessingState
from kernel import CognitiveState
from retrieval import PCRRM, RetrievalContext, RetrievalSeed, RetrievalResult
from routing import CognitiveRouter, RoutingContext, RoutingDecision, RoutingOutcome
from sufficiency import ICSM, SufficiencyContext, SufficiencyEvaluation


class InteractionFlowError(RuntimeError):
    """Raised when the unified interaction flow cannot advance safely."""


class InteractionFlowStatus(str, Enum):
    ROUTED = "routed"
    DELEGATION_REQUIRED = "delegation_required"
    REENTRY_REQUIRED = "reentry_required"
    CONSOLIDATION_READY = "consolidation_ready"
    CLARIFICATION_REQUIRED = "clarification_required"
    BLOCKED = "blocked"


@dataclass
class InteractionFlowResult:
    status: InteractionFlowStatus
    instance: CognitiveInstance
    retrieval: RetrievalResult
    sufficiency: SufficiencyEvaluation
    routing: RoutingDecision
    requirement: Any
    frontier_response: Mapping[str, Any] | None = None
    evidence_ids: tuple[str, ...] = ()
    proposal: Mapping[str, Any] | None = None
    provenance: dict[str, Any] = field(default_factory=dict)


class InteractionFlow:
    """Compose CI -> PCRRM -> ICSM -> Routing for one interaction.

    The flow owns temporary orchestration only. Persistent cognition remains
    owned by the supplied CognitiveState and its downstream governed pipeline.
    """

    def __init__(
        self,
        *,
        retriever: PCRRM | None = None,
        sufficiency: ICSM | None = None,
        router: CognitiveRouter | None = None,
    ) -> None:
        self.retriever = retriever or PCRRM()
        self.sufficiency = sufficiency or ICSM()
        self.router = router or CognitiveRouter()

    def start(
        self,
        *,
        state: CognitiveState,
        interaction_id: str,
        communication: Any,
        requirement: Any,
        retrieval_seeds: tuple[RetrievalSeed, ...] = (),
        goal_context: Mapping[str, Any] | None = None,
        active_dimensions: Mapping[str, Any] | None = None,
        security_context: Mapping[str, Any] | None = None,
        evidence_state: str = "unknown",
        freshness_state: str = "unknown",
        consistency_state: str = "no_detected_conflict",
        identity_context_state: str = "resolved",
        native_capability_state: str = "available",
        clarification_available: bool = True,
        internal_recovery_available: bool = True,
        frontier_allowed: bool = False,
        frontier_capabilities: tuple[str, ...] = (),
    ) -> InteractionFlowResult:
        """Run one bounded interaction through retrieval, sufficiency, routing."""

        if not interaction_id:
            raise InteractionFlowError("interaction_id is required")

        ci = CognitiveInstance(
            interaction_id=interaction_id,
            communication=communication,
        )
        ci.transition(ProcessingState.ENVELOPE_READY)
        ci.transition(ProcessingState.INTERACTION_IDENTIFIED)
        ci.activate_curiosity()
        ci.transition(ProcessingState.CONTEXT_EVALUATION)
        ci.transition(ProcessingState.PROCESSING)

        retrieval_context = RetrievalContext(
            interaction_id=interaction_id,
            instance_id=ci.instance_id,
            requirement=requirement,
            goal_context=goal_context or {},
            active_dimensions=active_dimensions or {},
            security_context=security_context or {},
        )
        retrieval = self.retriever.retrieve(
            state,
            retrieval_context,
            seeds=retrieval_seeds,
        )

        ci.retrieval_context = {
            "retrieval_id": retrieval.retrieval_id,
            "status": retrieval.retrieval_status.value,
            "state_id": state.state_id,
            "state_version": state.state_version,
        }

        for object_id, reference in retrieval.selected_objects.items():
            ci.add_persistent_reference(object_id, reference)
        for relationship_id, reference in retrieval.selected_relationships.items():
            ci.add_persistent_reference(relationship_id, reference)
        for dimension_id, reference in retrieval.selected_dimensions.items():
            ci.add_persistent_reference(dimension_id, reference)

        if retrieval.retrieval_status.value == "retrieval_failure":
            retrieval_state = "retrieval_failure"
        elif retrieval.retrieval_status.value == "ambiguous":
            retrieval_state = "ambiguous"
        elif retrieval.retrieval_status.value == "access_restricted":
            retrieval_state = "access_restricted"
        else:
            retrieval_state = retrieval.retrieval_status.value

        relevant_cognition = {}
        relevant_cognition.update(retrieval.selected_objects)
        relevant_cognition.update(retrieval.selected_relationships)
        relevant_cognition.update(retrieval.selected_dimensions)

        sufficiency_context = SufficiencyContext(
            interaction_id=interaction_id,
            instance_id=ci.instance_id,
            requirement=requirement,
            relevant_cognition=relevant_cognition,
            retrieval_status=retrieval_state,
            evidence_state=evidence_state,
            freshness_state=freshness_state,
            consistency_state=consistency_state,
            identity_context_state=identity_context_state,
            native_capability_state=native_capability_state,
        )
        sufficiency = self.sufficiency.evaluate(sufficiency_context)

        routing_context = RoutingContext(
            interaction_id=interaction_id,
            instance_id=ci.instance_id,
            requirement=requirement,
            sufficiency_state=sufficiency.requirement_state.value,
            missing_requirements=tuple(sufficiency.unresolved_questions),
            knowledge_gaps=tuple(sufficiency.knowledge_gaps),
            capability_gaps=tuple(sufficiency.capability_gaps),
            internal_recovery_options=tuple(sufficiency.internal_recovery_options),
            evidence_state=sufficiency.evidence_state,
            security_context=security_context or {},
            available_capabilities=(
                ("native_reasoning",)
                if native_capability_state == "available"
                else ()
            ),
            clarification_available=clarification_available,
            internal_recovery_available=internal_recovery_available,
            frontier_allowed=frontier_allowed,
            frontier_capabilities=frontier_capabilities,
        )
        routing = self.router.decide(routing_context)
        ci.record_routing({
            "routing_id": routing.routing_id,
            "outcome": routing.outcome.value,
            "reason": routing.reason,
            "delegation_scope": list(routing.delegation_scope),
        })

        if routing.outcome == RoutingOutcome.FRONTIER_DELEGATED:
            ci.transition(ProcessingState.ROUTING)
            ci.transition(ProcessingState.DELEGATED_PROCESSING)
            status = InteractionFlowStatus.DELEGATION_REQUIRED
        elif routing.outcome == RoutingOutcome.HYBRID:
            ci.transition(ProcessingState.ROUTING)
            ci.transition(ProcessingState.DELEGATED_PROCESSING)
            status = InteractionFlowStatus.DELEGATION_REQUIRED
        elif routing.outcome == RoutingOutcome.CLARIFICATION_REQUIRED:
            ci.transition(ProcessingState.ROUTING)
            ci.transition(ProcessingState.CLARIFICATION_REQUIRED)
            status = InteractionFlowStatus.CLARIFICATION_REQUIRED
        elif routing.outcome == RoutingOutcome.BLOCKED:
            ci.transition(ProcessingState.ROUTING)
            ci.transition(ProcessingState.BLOCKED)
            status = InteractionFlowStatus.BLOCKED
        else:
            ci.transition(ProcessingState.ROUTING)
            ci.transition(ProcessingState.EVIDENCE_EVALUATION)
            status = InteractionFlowStatus.ROUTED

        return InteractionFlowResult(
            status=status,
            instance=ci,
            retrieval=retrieval,
            sufficiency=sufficiency,
            routing=routing,
            requirement=requirement,
            provenance={
                "flow": "gri-unified-interaction-flow-v0.1",
                "interaction_id": interaction_id,
                "instance_id": ci.instance_id,
                "state_id": state.state_id,
                "state_version": state.state_version,
                "persistent_state_mutation": False,
            },
        )

    def reenter_frontier_output(
        self,
        result: InteractionFlowResult,
        response: Mapping[str, Any],
        *,
        evidence_ids: tuple[str, ...] = (),
        proposal: Mapping[str, Any] | None = None,
        evidence_state: str = "unknown",
        freshness_state: str = "unknown",
        consistency_state: str = "no_detected_conflict",
        identity_context_state: str = "resolved",
        native_capability_state: str = "available",
    ) -> InteractionFlowResult:
        """Re-enter frontier output as new information.

        The response is recorded in the interaction context and is never
        promoted directly to evidence, belief, or persistent cognition.
        """

        if result.status != InteractionFlowStatus.DELEGATION_REQUIRED:
            raise InteractionFlowError(
                "frontier re-entry requires a prior delegation-required result"
            )
        if result.instance.processing_state != ProcessingState.DELEGATED_PROCESSING:
            raise InteractionFlowError(
                "instance is not awaiting frontier output"
            )

        result.instance.record_frontier_output(dict(response))
        result.instance.transition(ProcessingState.REENTRY_VALIDATION)
        result.instance.transition(ProcessingState.PROCESSING)

        relevant_cognition = dict(result.sufficiency.relevant_cognition)
        sufficiency_context = SufficiencyContext(
            interaction_id=result.instance.interaction_id,
            instance_id=result.instance.instance_id,
            requirement=result.requirement,
            relevant_cognition=relevant_cognition,
            retrieval_status="complete" if relevant_cognition else "no_relevant_cognition_found",
            evidence_state=evidence_state,
            freshness_state=freshness_state,
            consistency_state=consistency_state,
            identity_context_state=identity_context_state,
            native_capability_state=native_capability_state,
        )
        sufficiency = self.sufficiency.evaluate(sufficiency_context)

        result.instance.transition(ProcessingState.EVIDENCE_EVALUATION)

        if proposal is not None:
            proposal_id = str(proposal.get("proposal_id", ""))
            if not proposal_id:
                raise InteractionFlowError("proposal_id is required for a proposal")
            result.instance.add_proposal(proposal_id, dict(proposal))
            result.instance.mark_proposal_ready()
            result.instance.mark_consolidation_ready()
            status = InteractionFlowStatus.CONSOLIDATION_READY
        else:
            result.instance.mark_null_ready()
            result.instance.mark_consolidation_ready()
            status = InteractionFlowStatus.CONSOLIDATION_READY

        return InteractionFlowResult(
            status=status,
            instance=result.instance,
            retrieval=result.retrieval,
            sufficiency=sufficiency,
            routing=result.routing,
            requirement=result.requirement,
            frontier_response=dict(response),
            evidence_ids=tuple(evidence_ids),
            proposal=dict(proposal) if proposal is not None else None,
            provenance={
                **result.provenance,
                "frontier_reentry": True,
                "frontier_output_is_new_information": True,
                "frontier_output_is_not_direct_persistence": True,
            },
        )

    def finalize_native(
        self,
        result: InteractionFlowResult,
        *,
        evidence_ids: tuple[str, ...] = (),
        proposal: Mapping[str, Any] | None = None,
    ) -> InteractionFlowResult:
        """Complete a native route at the consolidation boundary.

        This method prepares a proposal or explicit null outcome. It does not
        invoke Governance, the Kernel, or the persistence store.
        """

        if result.routing.outcome != RoutingOutcome.GRI_NATIVE:
            raise InteractionFlowError("finalize_native requires a GRI-native route")
        if result.instance.processing_state != ProcessingState.EVIDENCE_EVALUATION:
            raise InteractionFlowError("native route is not at evidence evaluation")

        if proposal is None:
            result.instance.mark_null_ready()
            result.instance.mark_consolidation_ready()
            status = InteractionFlowStatus.CONSOLIDATION_READY
        else:
            proposal_id = str(proposal.get("proposal_id", ""))
            if not proposal_id:
                raise InteractionFlowError("proposal_id is required for a proposal")
            result.instance.add_proposal(proposal_id, dict(proposal))
            result.instance.mark_proposal_ready()
            result.instance.mark_consolidation_ready()
            status = InteractionFlowStatus.CONSOLIDATION_READY

        return InteractionFlowResult(
            status=status,
            instance=result.instance,
            retrieval=result.retrieval,
            sufficiency=result.sufficiency,
            routing=result.routing,
            requirement=result.requirement,
            evidence_ids=tuple(evidence_ids),
            proposal=dict(proposal) if proposal is not None else None,
            provenance={
                **result.provenance,
                "native_finalization": True,
                "persistent_state_mutation": False,
            },
        )
