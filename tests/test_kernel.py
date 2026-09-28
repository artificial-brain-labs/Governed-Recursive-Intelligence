from kernel import CognitiveState, apply_transition


def base_state():
    return CognitiveState(
        state_id="STATE-001",
        state_version=1,
        pcg={"belief-1": {"claim": "existing"}},
    )


def test_create_commits_only_with_approval_and_evidence():
    state = base_state()
    proposal = {
        "proposal_id": "PROP-1",
        "target_type": "belief",
        "target_id": "belief-2",
        "operation": "create",
        "value": {"claim": "new"},
    }

    successor, record = apply_transition(
        state,
        proposal,
        interaction_id="INT-1",
        governance_status="approved",
        governance_reason="authorized",
        governance_version="GOV-1",
        evidence_ids=["E-1"],
        timestamp="2026-09-28T10:00:00+00:00",
    )

    assert successor.state_version == 2
    assert successor.pcg["belief-2"]["claim"] == "new"
    assert record["outcome"] == "committed"
    assert state.state_version == 1
    assert "belief-2" not in state.pcg


def test_no_governance_means_null_transition():
    state = base_state()
    proposal = {
        "proposal_id": "PROP-1",
        "target_type": "belief",
        "target_id": "belief-2",
        "operation": "create",
    }

    successor, record = apply_transition(
        state,
        proposal,
        interaction_id="INT-1",
        governance_status="pending",
        governance_reason=None,
        governance_version="GOV-1",
        evidence_ids=["E-1"],
    )

    assert successor.state_version == state.state_version
    assert successor.pcg == state.pcg
    assert record["outcome"] == "null"


def test_no_evidence_means_null_transition():
    state = base_state()
    proposal = {
        "proposal_id": "PROP-1",
        "target_type": "belief",
        "target_id": "belief-2",
        "operation": "create",
    }

    successor, record = apply_transition(
        state,
        proposal,
        interaction_id="INT-1",
        governance_status="approved",
        governance_reason="authorized",
        governance_version="GOV-1",
        evidence_ids=[],
    )

    assert successor.state_version == state.state_version
    assert record["outcome"] == "null"
    assert record["null_reason"] == "no evidence"


def test_null_transition_does_not_mutate_predecessor():
    state = base_state()
    proposal = {
        "proposal_id": "PROP-1",
        "target_type": "belief",
        "target_id": "missing",
        "operation": "modify",
    }

    successor, record = apply_transition(
        state,
        proposal,
        interaction_id="INT-1",
        governance_status="approved",
        governance_reason="authorized",
        governance_version="GOV-1",
        evidence_ids=["E-1"],
    )

    assert successor.state_version == state.state_version
    assert successor.pcg == state.pcg
    assert record["outcome"] == "null"


def test_remove_creates_successor_state():
    state = base_state()
    proposal = {
        "proposal_id": "PROP-1",
        "target_type": "belief",
        "target_id": "belief-1",
        "operation": "remove",
    }

    successor, record = apply_transition(
        state,
        proposal,
        interaction_id="INT-1",
        governance_status="approved",
        governance_reason="authorized",
        governance_version="GOV-1",
        evidence_ids=["E-1"],
    )

    assert successor.state_version == 2
    assert "belief-1" not in successor.pcg
    assert record["outcome"] == "committed"
