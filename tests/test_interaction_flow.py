from kernel import CognitiveState
from interaction_flow import (
    InteractionFlow,
    InteractionFlowError,
    InteractionFlowStatus,
)
from retrieval import RetrievalSeed
from routing import RoutingOutcome


def state():
    return CognitiveState(
        state_id="STATE-FLOW-1",
        state_version=1,
        pcg={
            "ID-X": {"object_id": "ID-X", "object_type": "identity", "name": "X"},
        },
        dimensions={},
        goals={},
        relationships={},
        learning={},
        history=[],
    )


def test_native_route_composes_ci_retrieval_sufficiency_and_routing():
    result = InteractionFlow().start(
        state=state(),
        interaction_id="INT-FLOW-1",
        communication={"text": "Tell me about X."},
        requirement={"task": "explain", "subject": "ID-X"},
        retrieval_seeds=(RetrievalSeed("SEED-1", "identity", "ID-X"),),
        evidence_state="supported",
        freshness_state="adequate",
        consistency_state="no_detected_conflict",
        identity_context_state="resolved",
        native_capability_state="available",
    )

    assert result.status == InteractionFlowStatus.ROUTED
    assert result.routing.outcome == RoutingOutcome.GRI_NATIVE
    assert result.instance.state == "evidence_evaluation"
    assert result.instance.icg.persistent_references["ID-X"]["target_id"] == "ID-X"


def test_native_route_can_reach_consolidation_boundary_with_explicit_null():
    result = InteractionFlow().start(
        state=state(),
        interaction_id="INT-FLOW-2",
        communication={"text": "Tell me about X."},
        requirement={"task": "explain", "subject": "ID-X"},
        retrieval_seeds=(RetrievalSeed("SEED-1", "identity", "ID-X"),),
        evidence_state="supported",
        freshness_state="adequate",
        consistency_state="no_detected_conflict",
        identity_context_state="resolved",
    )
    final = InteractionFlow().finalize_native(result)

    assert final.status == InteractionFlowStatus.CONSOLIDATION_READY
    assert final.instance.state == "consolidation_ready"
    assert final.proposal is None


def test_unknown_does_not_automatically_delegate_when_internal_recovery_exists():
    result = InteractionFlow().start(
        state=state(),
        interaction_id="INT-FLOW-3",
        communication={"text": "What is happening now?"},
        requirement={"task": "investigate", "subject": "current"},
        retrieval_seeds=(),
        frontier_allowed=True,
        frontier_capabilities=("web-research",),
    )

    assert result.sufficiency.requirement_state.value == "unknown"
    assert result.routing.outcome == RoutingOutcome.GRI_NATIVE
    assert result.status == InteractionFlowStatus.ROUTED


def test_capability_gap_creates_delegation_boundary_without_invoking_provider():
    result = InteractionFlow().start(
        state=state(),
        interaction_id="INT-FLOW-4",
        communication={"text": "Perform specialist analysis."},
        requirement={"task": "evaluate", "subject": "specialist"},
        retrieval_seeds=(),
        native_capability_state="insufficient",
        frontier_allowed=True,
        frontier_capabilities=("specialist-model",),
        internal_recovery_available=False,
        evidence_state="supported",
        freshness_state="adequate",
    )

    assert result.status == InteractionFlowStatus.DELEGATION_REQUIRED
    assert result.routing.outcome == RoutingOutcome.FRONTIER_DELEGATED
    assert result.instance.state == "delegated_processing"
    assert result.instance.frontier_history == []


def test_capability_and_knowledge_gaps_produce_hybrid_route():
    result = InteractionFlow().start(
        state=state(),
        interaction_id="INT-FLOW-4B",
        communication={"text": "Use specialist analysis with current context."},
        requirement={"task": "evaluate", "subject": "specialist"},
        retrieval_seeds=(),
        native_capability_state="insufficient",
        frontier_allowed=True,
        frontier_capabilities=("specialist-model",),
        internal_recovery_available=False,
    )

    assert result.status == InteractionFlowStatus.DELEGATION_REQUIRED
    assert result.routing.outcome == RoutingOutcome.HYBRID


def test_frontier_output_reenters_as_new_information_and_can_end_in_null():
    flow = InteractionFlow()
    result = flow.start(
        state=state(),
        interaction_id="INT-FLOW-5",
        communication={"text": "Perform specialist analysis."},
        requirement={"task": "evaluate", "subject": "specialist"},
        retrieval_seeds=(),
        native_capability_state="insufficient",
        frontier_allowed=True,
        frontier_capabilities=("specialist-model",),
        internal_recovery_available=False,
    )

    reentered = flow.reenter_frontier_output(
        result,
        {"answer": "Specialist output", "claim": "X has a new property."},
    )

    assert reentered.status == InteractionFlowStatus.CONSOLIDATION_READY
    assert reentered.instance.state == "consolidation_ready"
    assert reentered.proposal is None
    assert len(reentered.instance.frontier_history) == 1
    assert reentered.provenance["frontier_output_is_new_information"] is True
    assert reentered.provenance["frontier_output_is_not_direct_persistence"] is True


def test_frontier_output_can_supply_temporary_proposal_but_not_commit_it():
    flow = InteractionFlow()
    result = flow.start(
        state=state(),
        interaction_id="INT-FLOW-6",
        communication={"text": "Perform specialist analysis."},
        requirement={"task": "evaluate", "subject": "specialist"},
        retrieval_seeds=(),
        native_capability_state="insufficient",
        frontier_allowed=True,
        frontier_capabilities=("specialist-model",),
        internal_recovery_available=False,
    )

    proposal = {
        "proposal_id": "PROP-FLOW-1",
        "target": {"target_type": "concept", "target_id": "CONCEPT-1"},
        "op": "create",
        "evidence": ["EVID-FLOW-1"],
    }
    reentered = flow.reenter_frontier_output(
        result,
        {"answer": "Specialist output"},
        evidence_ids=("EVID-FLOW-1",),
        proposal=proposal,
    )

    assert reentered.status == InteractionFlowStatus.CONSOLIDATION_READY
    assert reentered.proposal == proposal
    assert reentered.instance.proposals["PROP-FLOW-1"] == proposal
    assert reentered.provenance["frontier_output_is_not_direct_persistence"] is True


def test_frontier_response_cannot_be_reentered_without_delegation_boundary():
    flow = InteractionFlow()
    result = flow.start(
        state=state(),
        interaction_id="INT-FLOW-7",
        communication={"text": "Tell me about X."},
        requirement={"task": "explain", "subject": "ID-X"},
        retrieval_seeds=(RetrievalSeed("SEED-1", "identity", "ID-X"),),
        evidence_state="supported",
        freshness_state="adequate",
    )

    try:
        flow.reenter_frontier_output(result, {"answer": "unexpected"})
        assert False
    except InteractionFlowError as exc:
        assert "delegation-required" in str(exc)


def test_proposal_does_not_bypass_governance_or_kernel():
    flow = InteractionFlow()
    result = flow.start(
        state=state(),
        interaction_id="INT-FLOW-8",
        communication={"text": "Tell me about X."},
        requirement={"task": "explain", "subject": "ID-X"},
        retrieval_seeds=(RetrievalSeed("SEED-1", "identity", "ID-X"),),
        evidence_state="supported",
        freshness_state="adequate",
    )

    final = flow.finalize_native(
        result,
        evidence_ids=("EVID-FLOW-2",),
        proposal={
            "proposal_id": "PROP-FLOW-2",
            "target": {"target_type": "concept", "target_id": "CONCEPT-1"},
            "op": "create",
            "evidence": ["EVID-FLOW-2"],
        },
    )

    assert final.status == InteractionFlowStatus.CONSOLIDATION_READY
    assert final.instance.state == "consolidation_ready"
    assert final.provenance["persistent_state_mutation"] is False


def test_security_block_prevents_delegation():
    result = InteractionFlow().start(
        state=state(),
        interaction_id="INT-FLOW-9",
        communication={"text": "Perform specialist analysis."},
        requirement={"task": "evaluate"},
        native_capability_state="insufficient",
        frontier_allowed=True,
        frontier_capabilities=("specialist-model",),
        internal_recovery_available=False,
        security_context={"delegation": "blocked"},
    )

    assert result.status == InteractionFlowStatus.BLOCKED
    assert result.routing.outcome == RoutingOutcome.BLOCKED
    assert result.instance.state == "blocked"


def test_unknown_remains_unknown_when_no_retrieval_seed_exists():
    result = InteractionFlow().start(
        state=state(),
        interaction_id="INT-FLOW-10",
        communication={"text": "Who is Z?"},
        requirement={"task": "remember", "subject": "Z"},
    )

    assert result.sufficiency.requirement_state.value == "unknown"
    assert result.routing.outcome == RoutingOutcome.GRI_NATIVE
    assert result.instance.icg.persistent_references == {}


def test_empty_requirement_is_not_silently_invented():
    result = InteractionFlow().start(
        state=state(),
        interaction_id="INT-FLOW-11",
        communication={"text": "Something happened."},
        requirement={},
    )

    assert result.requirement == {}
    assert result.instance.icg.evidence == {}
    assert result.instance.candidates == {}
