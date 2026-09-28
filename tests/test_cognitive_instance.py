import pytest

from cognitive_instance import CognitiveInstance, CognitiveInstanceError, ProcessingState


def new_instance():
    return CognitiveInstance(
        interaction_id="INT-CI-001",
        communication={"payload": "John cancelled the meeting."},
    )


def test_new_interaction_creates_distinct_cognitive_instance():
    first = new_instance()
    second = new_instance()

    assert first.interaction_id == second.interaction_id
    assert first.instance_id != second.instance_id
    assert first.state == "created"


def test_canonical_lifecycle_reaches_cca_handoff():
    ci = new_instance()

    ci.transition(ProcessingState.ENVELOPE_READY)
    ci.transition(ProcessingState.INTERACTION_IDENTIFIED)
    ci.activate_curiosity()
    ci.transition(ProcessingState.CONTEXT_EVALUATION)
    ci.transition(ProcessingState.PROCESSING)
    ci.transition(ProcessingState.ROUTING)
    ci.transition(ProcessingState.EVIDENCE_EVALUATION)

    ci.add_evidence("EVID-001", {"claim": "John cancelled the meeting."})
    ci.add_candidate("CAND-001", {"type": "relationship"})
    ci.add_proposal("PROP-001", {"proposal_id": "PROP-001"})

    ci.mark_proposal_ready()
    ci.mark_consolidation_ready()
    ci.handoff_to_cca()
    assert ci.state == "handed_to_cca"


def test_null_is_valid_and_distinct_from_failure():
    ci = new_instance()

    for state in (
        ProcessingState.ENVELOPE_READY,
        ProcessingState.INTERACTION_IDENTIFIED,
        ProcessingState.CURIOSITY_ACTIVE,
        ProcessingState.CONTEXT_EVALUATION,
        ProcessingState.PROCESSING,
        ProcessingState.EVIDENCE_EVALUATION,
    ):
        ci.transition(state)

    ci.mark_null_ready()
    ci.mark_consolidation_ready()

    assert ci.state == "consolidation_ready"
    assert "null_ready" in ci.lifecycle_history


def test_unknown_does_not_create_fact():
    ci = new_instance()
    ci.uncertainty["unknowns"] = ["reason_for_cancellation"]

    assert ci.uncertainty["unknowns"] == ["reason_for_cancellation"]
    assert ci.icg.evidence == {}
    assert ci.candidates == {}


def test_frontier_output_is_recorded_without_persistence():
    ci = new_instance()
    ci.record_frontier_output({
        "source": "frontier-model",
        "claim": "John intentionally cancelled the meeting.",
    })

    assert len(ci.frontier_history) == 1
    assert ci.proposals == {}
    assert ci.icg.persistent_references == {}


def test_persistent_reference_is_not_candidate_ownership():
    ci = new_instance()
    ci.add_persistent_reference("REL-001", {"state_version": 1})

    assert "REL-001" in ci.icg.persistent_references
    assert "REL-001" not in ci.candidates


def test_invalid_lifecycle_transition_is_rejected():
    ci = new_instance()

    with pytest.raises(CognitiveInstanceError):
        ci.transition(ProcessingState.CONSOLIDATION_READY)


def test_cca_cannot_receive_instance_before_readiness():
    ci = new_instance()

    with pytest.raises(CognitiveInstanceError, match="consolidation readiness"):
        ci.handoff_to_cca()


def test_closed_instance_cannot_reenter_processing():
    ci = new_instance()
    ci.transition(ProcessingState.ENVELOPE_READY)
    ci.transition(ProcessingState.INTERACTION_IDENTIFIED)
    ci.activate_curiosity()
    ci.transition(ProcessingState.CLARIFICATION_REQUIRED)
    ci.close()

    assert ci.state == "closed"

    with pytest.raises(CognitiveInstanceError):
        ci.transition(ProcessingState.PROCESSING)
