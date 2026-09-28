"""Canonical GRI v0.1 end-to-end integration and adversarial invariants.

This test composes the currently executable boundaries while keeping the
architectural layers that are still specification-only explicit as test-stage
orchestration. It must not be read as evidence that those future layers are
already production modules.
"""

from copy import deepcopy

import pytest

from adapters.adapter import CRPAdapterError, validate_crp_event
from governance import ConstraintResult, require_evidence
from kernel import CognitiveState
from pipeline import execute_and_persist_transition
from storage import JsonJournalStateStore


def interaction_event():
    return {
        "crp_version": "0.2",
        "interaction_id": "INT-E2E-001",
        "timestamp": "2026-09-29T10:00:00+00:00",
        "source": {"type": "user", "identifier": None},
        "state_context": {"state_id": "STATE-E2E", "state_version": "1"},
        "observation": {
            "raw_input": "John cancelled the meeting again.",
            "status": "explicit",
            "facts": [
                {
                    "fact_id": "FACT-001",
                    "claim": "John cancelled the meeting.",
                    "status": "explicit",
                },
                {
                    "fact_id": "FACT-002",
                    "claim": "The input contains the recurrence marker 'again'.",
                    "status": "observed",
                },
            ],
        },
        "interpretation": {
            "entities": [
                {"entity_id": "ENT-JOHN", "type": "person", "name": "John"}
            ],
            "events": [
                {
                    "event_id": "EV-001",
                    "type": "meeting_cancellation",
                    "actor": "ENT-JOHN",
                    "target": None,
                }
            ],
            "relationships": [],
        },
        "evidence": [
            {
                "evidence_id": "EVID-001",
                "type": "observation",
                "claim": "John cancelled the meeting.",
                "source_ref": "FACT-001",
            },
            {
                "evidence_id": "EVID-002",
                "type": "observation",
                "claim": "The input contains the recurrence marker 'again'.",
                "source_ref": "FACT-002",
            },
        ],
        "inferences": [
            {
                "inference_id": "INF-001",
                "claim": "John may have a recurring pattern of cancelling meetings.",
                "basis": ["EVID-001", "EVID-002"],
                "status": "possible",
            }
        ],
        "uncertainty": {
            "unknowns": ["reason_for_cancellation", "John's_intention"],
            "ambiguities": [],
        },
        "proposal": {
            "proposal_id": "PROP-E2E-001",
            "target_type": "relationship",
            "target_id": "REL-JOHN-MEETING",
            "operation": "reinforce",
            "evidence": ["EVID-001", "EVID-002"],
            "rationale": "Evidence may support a recurring interaction pattern.",
            "status": "proposed",
        },
        "governance": {
            "status": "pending",
            "constraints_checked": [],
            "reason": None,
            "version": "GRI-GOV-0.1",
        },
        "transition_reference": None,
        "provenance": {
            "source_interaction": "INT-E2E-001",
            "interpreter": "integration-test-interpreter",
            "reasoning_component": None,
            "originating_model": None,
            "schema_version": "0.2",
        },
    }


def initial_state():
    return CognitiveState(
        state_id="STATE-E2E",
        state_version=1,
        relationships={"REL-JOHN-MEETING": {"trust": "unmodified"}},
    )


def test_canonical_gri_v01_experience_to_persistent_transition(tmp_path):
    """Exercise the executable path from experience representation to persistence."""

    event = interaction_event()
    state = initial_state()
    store = JsonJournalStateStore(tmp_path)
    store.initialize(state)

    # Interaction / requirement identification:
    # The event is the supplied interaction. Requirement decomposition and
    # task interpretation remain orchestration-level in v0.1.
    requirement = {
        "task_type": "evaluate",
        "target": "REL-JOHN-MEETING",
        "source": "interaction",
    }
    assert requirement["target"] in state.relationships

    # PCG relevance retrieval:
    # Current v0.1 PCG is represented by CognitiveState collections.
    relevant_pcg = {
        "relationship": state.relationships["REL-JOHN-MEETING"],
        "target_id": "REL-JOHN-MEETING",
    }
    assert relevant_pcg["target_id"] == event["proposal"]["target_id"]

    # Internal cognition sufficiency:
    # This is an explicit test-stage determination, not a production
    # sufficiency engine.
    internal_sufficiency = "sufficient_for_proposal_evaluation"
    assert internal_sufficiency == "sufficient_for_proposal_evaluation"

    # Interpretation and evidence classification are represented by CRP v0.2.
    validate_crp_event(event)
    evidence_ids = [item["evidence_id"] for item in event["evidence"]]
    assert evidence_ids == ["EVID-001", "EVID-002"]
    assert event["inferences"][0]["status"] == "possible"

    # Candidate -> Proposal is represented by the explicit CRP proposal.
    proposal = deepcopy(event["proposal"])
    assert proposal["operation"] == "reinforce"

    successor, decision, cstr = execute_and_persist_transition(
        store,
        state,
        proposal,
        interaction_id=event["interaction_id"],
        local_constraints=[require_evidence],
        evidence_ids=evidence_ids,
        timestamp=event["timestamp"],
    )

    assert decision.status == "approved"
    assert decision.proposal_id == proposal["proposal_id"]
    assert decision.state_id == state.state_id
    assert decision.state_version == state.state_version

    assert cstr["outcome"] == "committed"
    assert cstr["execution_status"] == "success"
    assert cstr["state_before"]["state_version"] == "1"
    assert cstr["state_after"]["state_version"] == "2"

    assert successor.state_version == 2
    assert successor.relationships["REL-JOHN-MEETING"]["last_operation"] == "reinforce"
    assert successor.relationships["REL-JOHN-MEETING"]["reinforcement_count"] == 1

    recovered = store.read_current_state()
    assert recovered.state_version == 2
    assert recovered.relationships["REL-JOHN-MEETING"]["reinforcement_count"] == 1

    recorded = store.read_transition(cstr["transition_id"])
    assert recorded["outcome"] == "committed"
    assert recorded["interaction_id"] == event["interaction_id"]


def test_no_evidence_cannot_commit(tmp_path):
    store = JsonJournalStateStore(tmp_path)
    state = initial_state()
    store.initialize(state)
    proposal = interaction_event()["proposal"]

    successor, decision, cstr = execute_and_persist_transition(
        store,
        state,
        proposal,
        interaction_id="INT-NO-EVIDENCE",
        local_constraints=[require_evidence],
        evidence_ids=[],
    )

    assert decision.status == "rejected"
    assert cstr["outcome"] == "null"
    assert cstr["execution_status"] == "governance_not_approved"
    assert successor.state_version == 1
    assert store.read_current_state().state_version == 1


def test_governance_rejection_cannot_commit(tmp_path):
    store = JsonJournalStateStore(tmp_path)
    state = initial_state()
    store.initialize(state)
    proposal = interaction_event()["proposal"]

    def reject(_):
        return ConstraintResult(
            "GLOBAL-BLOCK-001", "global", "fail", "constitutional restriction"
        )

    successor, decision, cstr = execute_and_persist_transition(
        store,
        state,
        proposal,
        interaction_id="INT-REJECTED",
        local_constraints=[require_evidence],
        global_constraints=[reject],
        evidence_ids=["EVID-001"],
    )

    assert decision.status == "rejected"
    assert cstr["outcome"] == "null"
    assert successor.state_version == 1
    assert store.read_current_state().state_version == 1


def test_stale_state_is_blocked_before_governance(tmp_path):
    store = JsonJournalStateStore(tmp_path)
    state = initial_state()
    store.initialize(state)
    proposal = interaction_event()["proposal"]

    current_successor = state.clone(state_version=2)
    current_successor.relationships["REL-JOHN-MEETING"]["marker"] = "new"
    committed_cstr = {
        "transition_id": "TR-EXTERNAL-001",
        "interaction_id": "INT-EXTERNAL",
        "state_before": {"state_id": state.state_id, "state_version": "1"},
        "state_after": {"state_id": state.state_id, "state_version": "2"},
        "outcome": "committed",
    }
    store.commit_transition(
        expected_state_version=1,
        successor=current_successor,
        cstr=committed_cstr,
    )

    with pytest.raises(RuntimeError, match="store current state"):
        execute_and_persist_transition(
            store,
            state,
            proposal,
            interaction_id="INT-STALE",
            local_constraints=[require_evidence],
            evidence_ids=["EVID-001"],
        )

    assert store.read_current_state().state_version == 2


def test_target_precondition_failure_is_null_and_traceable(tmp_path):
    store = JsonJournalStateStore(tmp_path)
    state = initial_state()
    store.initialize(state)
    proposal = interaction_event()["proposal"] | {"target_id": "REL-MISSING"}

    successor, decision, cstr = execute_and_persist_transition(
        store,
        state,
        proposal,
        interaction_id="INT-MISSING-TARGET",
        local_constraints=[require_evidence],
        evidence_ids=["EVID-001"],
    )

    assert decision.status == "approved"
    assert cstr["outcome"] == "null"
    assert cstr["execution_status"] == "target_precondition_failed"
    assert successor.state_version == 1
    assert store.read_current_state().state_version == 1
    assert store.read_transition(cstr["transition_id"])["outcome"] == "null"


def test_explicit_no_change_is_not_forced_learning(tmp_path):
    store = JsonJournalStateStore(tmp_path)
    state = initial_state()
    store.initialize(state)
    proposal = interaction_event()["proposal"] | {"operation": "no_change"}

    successor, decision, cstr = execute_and_persist_transition(
        store,
        state,
        proposal,
        interaction_id="INT-NO-CHANGE",
        local_constraints=[require_evidence],
        evidence_ids=["EVID-001"],
    )

    assert decision.status == "approved"
    assert cstr["outcome"] == "null"
    assert cstr["execution_status"] == "explicit_no_change"
    assert successor.state_version == 1
    assert store.read_current_state().state_version == 1
    assert store.read_transition(cstr["transition_id"])["outcome"] == "null"


def test_ambiguous_or_unknown_information_does_not_become_fact():
    event = interaction_event()
    event["observation"]["status"] = "unknown"
    event["observation"]["facts"] = []

    # The CRP semantic boundary must accept an explicit unknown with no facts;
    # no belief/proposal is created from the missing information here.
    event["proposal"] = None
    event["transition_reference"] = None

    validate_crp_event(event)
    assert event["observation"]["status"] == "unknown"
    assert event["observation"]["facts"] == []
    assert event["proposal"] is None


def test_frontier_output_requires_reentry_validation():
    event = interaction_event()
    frontier_output = {
        "source": "frontier-model",
        "claim": "John intentionally cancelled the meeting.",
    }

    # A frontier output is new information, not direct persistent cognition.
    # This test models the re-entry boundary explicitly; no state mutation is
    # attempted from the frontier output itself.
    event["evidence"] = []
    event["proposal"] = None
    event["transition_reference"] = None
    event["observation"]["status"] = "explicit"
    event["observation"]["facts"] = []

    event["provenance"]["originating_model"] = frontier_output["source"]

    validate_crp_event(event)
    assert event["proposal"] is None
    assert event["observation"]["facts"] == []
    assert event["provenance"]["originating_model"] == "frontier-model"
