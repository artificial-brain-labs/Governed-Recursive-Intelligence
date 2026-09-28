from governance import prohibit_goal_removal_without_review, require_evidence
from kernel import CognitiveState
from pipeline import execute_governed_transition


def test_approved_governance_reaches_kernel_and_commits():
    state = CognitiveState(state_id="S", state_version=1)
    proposal = {
        "proposal_id": "P1",
        "target_type": "belief",
        "target_id": "B1",
        "operation": "create",
        "value": {"claim": "explicitly supported"},
    }

    successor, decision, cstr = execute_governed_transition(
        state,
        proposal,
        interaction_id="I1",
        local_constraints=[require_evidence],
        evidence_ids=["E1"],
        timestamp="2026-09-28T10:00:00+00:00",
    )

    assert decision.status == "approved"
    assert cstr["outcome"] == "committed"
    assert successor.state_version == 2
    assert successor.pcg["B1"]["claim"] == "explicitly supported"


def test_global_review_stops_kernel_commit():
    state = CognitiveState(state_id="S", state_version=1)
    proposal = {
        "proposal_id": "P1",
        "target_type": "goal",
        "target_id": "G1",
        "operation": "remove",
    }

    successor, decision, cstr = execute_governed_transition(
        state,
        proposal,
        interaction_id="I1",
        local_constraints=[require_evidence],
        global_constraints=[prohibit_goal_removal_without_review],
        evidence_ids=["E1"],
    )

    assert decision.status == "requires_review"
    assert cstr["outcome"] == "null"
    assert successor.state_version == 1


def test_governance_rejection_is_recorded_in_cstr():
    state = CognitiveState(state_id="S", state_version=1)
    proposal = {
        "proposal_id": "P1",
        "target_type": "belief",
        "target_id": "B1",
        "operation": "create",
    }

    successor, decision, cstr = execute_governed_transition(
        state,
        proposal,
        interaction_id="I1",
        local_constraints=[require_evidence],
        evidence_ids=[],
    )

    assert decision.status == "rejected"
    assert cstr["outcome"] == "null"
    assert cstr["governance"]["status"] == "rejected"
    assert successor.pcg == {}


def test_pipeline_does_not_allow_proposal_to_bypass_governance():
    state = CognitiveState(state_id="S", state_version=1)
    proposal = {
        "proposal_id": "P1",
        "target_type": "belief",
        "target_id": "B1",
        "operation": "create",
        "value": {"claim": "x"},
    }

    successor, decision, cstr = execute_governed_transition(
        state,
        proposal,
        interaction_id="I1",
        local_constraints=[require_evidence],
        evidence_ids=[],
    )

    assert decision.status == "rejected"
    assert "B1" not in successor.pcg
    assert cstr["state_change"] == []
