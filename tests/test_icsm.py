from sufficiency import (
    GapType,
    ICSM,
    SufficiencyContext,
    SufficiencyState,
)


def ctx(**overrides):
    base = dict(
        interaction_id="INT-ICSM-1",
        instance_id="CI-ICSM-1",
        requirement={"task": "explain", "subject": "ID-X"},
        relevant_cognition={"ID-X": {"object_type": "identity"}},
        retrieval_status="complete",
        evidence_state="supported",
        freshness_state="adequate",
        consistency_state="no_detected_conflict",
        identity_context_state="resolved",
        native_capability_state="available",
    )
    base.update(overrides)
    return SufficiencyContext(**base)


def test_sufficient_when_relevant_cognition_and_native_capability_are_adequate():
    result = ICSM().evaluate(ctx())

    assert result.requirement_state == SufficiencyState.SUFFICIENT
    assert result.gap_type is None
    assert result.knowledge_gaps == []
    assert result.capability_gaps == []


def test_partial_retrieval_is_partially_sufficient():
    result = ICSM().evaluate(ctx(retrieval_status="partial"))

    assert result.requirement_state == SufficiencyState.PARTIALLY_SUFFICIENT
    assert result.gap_type == GapType.KNOWLEDGE


def test_no_relevant_cognition_is_unknown_not_frontier():
    result = ICSM().evaluate(
        ctx(relevant_cognition={}, retrieval_status="no_relevant_cognition_found")
    )

    assert result.requirement_state == SufficiencyState.UNKNOWN
    assert result.gap_type == GapType.KNOWLEDGE
    assert "additional_retrieval" in result.internal_recovery_options


def test_retrieval_failure_is_distinct_from_unknown():
    result = ICSM().evaluate(
        ctx(relevant_cognition={}, retrieval_status="retrieval_failure")
    )

    assert result.requirement_state == SufficiencyState.RETRIEVAL_FAILURE
    assert result.requirement_state != SufficiencyState.UNKNOWN


def test_conflict_is_preserved():
    result = ICSM().evaluate(ctx(consistency_state="conflict"))

    assert result.requirement_state == SufficiencyState.CONFLICT
    assert "evaluate_conflict" in result.internal_recovery_options


def test_ambiguous_identity_is_preserved():
    result = ICSM().evaluate(ctx(identity_context_state="ambiguous"))

    assert result.requirement_state == SufficiencyState.AMBIGUOUS
    assert "clarify" in result.internal_recovery_options


def test_capability_gap_is_distinct():
    result = ICSM().evaluate(ctx(native_capability_state="insufficient"))

    assert result.requirement_state == SufficiencyState.INSUFFICIENT
    assert result.gap_type == GapType.CAPABILITY
    assert result.knowledge_gaps == []


def test_combined_gap_is_detected():
    result = ICSM().evaluate(
        ctx(
            retrieval_status="partial",
            native_capability_state="insufficient",
        )
    )

    assert result.requirement_state == SufficiencyState.PARTIALLY_SUFFICIENT
    assert result.gap_type == GapType.COMBINED


def test_stale_information_is_not_marked_false():
    result = ICSM().evaluate(ctx(freshness_state="stale"))

    assert result.requirement_state == SufficiencyState.INSUFFICIENT
    assert "temporal_adequacy_not_established" in result.knowledge_gaps


def test_icse_does_not_claim_truth_or_routing():
    result = ICSM().evaluate(ctx())

    assert "truth" not in result.provenance
    assert "routing" not in result.provenance
    assert "route" not in result.provenance
