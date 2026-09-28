from governance import evaluate_governance, require_evidence, prohibit_goal_removal_without_review, ConstraintResult

def test_approved_when_all_constraints_pass():
    d = evaluate_governance({"proposal_id": "P1", "evidence": ["E1"]}, local_constraints=[require_evidence])
    assert d.status == "approved"

def test_missing_evidence_is_rejected():
    d = evaluate_governance({"proposal_id": "P1", "evidence": []}, local_constraints=[require_evidence])
    assert d.status == "rejected"

def test_global_failure_overrides_local_pass():
    def fail(_):
        return ConstraintResult("GLOBAL-1", "global", "fail", "constitutional restriction")
    d = evaluate_governance({"proposal_id": "P1", "evidence": ["E1"]}, local_constraints=[require_evidence], global_constraints=[fail])
    assert d.status == "rejected"

def test_review_does_not_authorize_commitment():
    p = {"proposal_id": "P1", "target_type": "goal", "operation": "remove", "evidence": ["E1"]}
    d = evaluate_governance(p, local_constraints=[require_evidence], global_constraints=[prohibit_goal_removal_without_review])
    assert d.status == "requires_review"

def test_governance_does_not_mutate_proposal():
    p = {"proposal_id": "P1", "evidence": ["E1"]}
    before = p.copy()
    evaluate_governance(p, local_constraints=[require_evidence])
    assert p == before
