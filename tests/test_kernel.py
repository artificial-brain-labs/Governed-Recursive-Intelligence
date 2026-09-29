from kernel import CognitiveState, apply_transition


def auth(proposal_id, state, status="approved"):
    return {"decision_id": "D1", "proposal_id": proposal_id, "state_id": state.state_id, "state_version": state.state_version, "status": status, "reason": "authorized", "governance_version": "GOV-1"}


def base_state():
    return CognitiveState(state_id="STATE-001", state_version=1, pcg={"belief-1": {"claim": "existing"}})


def test_create_commits_only_with_approval_and_evidence():
    state = base_state()
    proposal = {"proposal_id": "PROP-1", "target_type": "belief", "target_id": "belief-2", "operation": "create", "value": {"claim": "new"}}
    successor, record = apply_transition(state, proposal, interaction_id="INT-1", governance_decision=auth("PROP-1", state), evidence_ids=["E-1"], timestamp="2026-09-28T10:00:00+00:00")
    assert successor.state_version == 2
    assert successor.pcg["belief-2"]["claim"] == "new"
    assert record["outcome"] == "committed"
    assert record["execution_status"] == "success"
    assert state.state_version == 1
    assert "belief-2" not in state.pcg


def test_no_governance_means_null_transition():
    state = base_state()
    proposal = {"proposal_id": "PROP-1", "target_type": "belief", "target_id": "belief-2", "operation": "create"}
    successor, record = apply_transition(state, proposal, interaction_id="INT-1", governance_decision=auth("PROP-1", state, "pending"), evidence_ids=["E-1"])
    assert successor.state_version == state.state_version
    assert record["outcome"] == "null"
    assert record["execution_status"] == "governance_not_approved"


def test_no_evidence_means_null_transition():
    state = base_state()
    proposal = {"proposal_id": "PROP-1", "target_type": "belief", "target_id": "belief-2", "operation": "create"}
    successor, record = apply_transition(state, proposal, interaction_id="INT-1", governance_decision=auth("PROP-1", state), evidence_ids=[])
    assert successor.state_version == state.state_version
    assert record["outcome"] == "null"
    assert record["execution_status"] == "evidence_missing"


def test_null_transition_does_not_mutate_predecessor():
    state = base_state()
    proposal = {"proposal_id": "PROP-1", "target_type": "belief", "target_id": "missing", "operation": "modify"}
    successor, record = apply_transition(state, proposal, interaction_id="INT-1", governance_decision=auth("PROP-1", state), evidence_ids=["E-1"])
    assert successor.state_version == state.state_version
    assert record["outcome"] == "null"
    assert record["execution_status"] == "target_precondition_failed"


def test_remove_creates_successor_state():
    state = base_state()
    proposal = {"proposal_id": "PROP-1", "target_type": "belief", "target_id": "belief-1", "operation": "remove"}
    successor, record = apply_transition(state, proposal, interaction_id="INT-1", governance_decision=auth("PROP-1", state), evidence_ids=["E-1"])
    assert successor.state_version == 2
    assert "belief-1" not in successor.pcg
    assert record["outcome"] == "committed"


def test_stale_authorization_does_not_commit():
    state = base_state()
    proposal = {"proposal_id": "PROP-1", "target_type": "belief", "target_id": "belief-2", "operation": "create"}
    stale = auth("PROP-1", state)
    state.state_version = 2
    successor, record = apply_transition(state, proposal, interaction_id="INT-1", governance_decision=stale, evidence_ids=["E-1"])
    assert successor.state_version == 2
    assert record["outcome"] == "null"
    assert record["execution_status"] == "stale_state"


def test_mismatched_authorization_does_not_commit():
    state = base_state()
    proposal = {"proposal_id": "PROP-2", "target_type": "belief", "target_id": "belief-2", "operation": "create"}
    successor, record = apply_transition(state, proposal, interaction_id="INT-1", governance_decision=auth("PROP-1", state), evidence_ids=["E-1"])
    assert record["outcome"] == "null"
    assert record["execution_status"] == "authorization_invalidated"


def test_no_change_is_explicit_null():
    state = base_state()
    proposal = {"proposal_id": "PROP-1", "target_type": "belief", "target_id": "belief-1", "operation": "no_change"}
    successor, record = apply_transition(state, proposal, interaction_id="INT-1", governance_decision=auth("PROP-1", state), evidence_ids=["E-1"])
    assert successor.state_version == 1
    assert record["outcome"] == "null"
    assert record["execution_status"] == "explicit_no_change"
    assert record["null_reason"] == "explicit_no_change"
