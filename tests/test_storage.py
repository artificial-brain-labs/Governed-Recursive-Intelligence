import json

import pytest

from kernel import CognitiveState
from storage import JsonJournalStateStore, StaleStateError


def make_state():
    return CognitiveState(
        state_id="STATE-1",
        state_version=1,
        pcg={"B1": {"claim": "existing"}},
    )


def make_cstr():
    return {
        "transition_id": "TR-1",
        "state_before": {"state_id": "STATE-1", "state_version": "1"},
        "state_after": {"state_id": "STATE-1", "state_version": "2"},
        "outcome": "committed",
    }


def test_initialize_and_recover(tmp_path):
    store = JsonJournalStateStore(tmp_path)
    store.initialize(make_state())
    assert store.read_current_state().state_version == 1


def test_commit_persists_successor_and_cstr(tmp_path):
    store = JsonJournalStateStore(tmp_path)
    store.initialize(make_state())

    successor = make_state().clone(state_version=2)
    successor.pcg["B2"] = {"claim": "new"}
    cstr = make_cstr()

    store.commit_transition(
        expected_state_version=1,
        successor=successor,
        cstr=cstr,
    )

    recovered = JsonJournalStateStore(tmp_path)
    assert recovered.read_current_state().state_version == 2
    assert recovered.read_current_state().pcg["B2"]["claim"] == "new"
    assert recovered.read_transition("TR-1")["transition_id"] == "TR-1"


def test_stale_writer_cannot_overwrite_newer_state(tmp_path):
    store = JsonJournalStateStore(tmp_path)
    store.initialize(make_state())
    successor = make_state().clone(state_version=2)
    store.commit_transition(expected_state_version=1, successor=successor, cstr=make_cstr())

    stale = make_state().clone(state_version=2)
    with pytest.raises(StaleStateError):
        store.commit_transition(expected_state_version=1, successor=stale, cstr=make_cstr())


def test_null_transition_history_is_persisted_without_state_change(tmp_path):
    store = JsonJournalStateStore(tmp_path)
    store.initialize(make_state())
    cstr = {"transition_id": "TR-NULL", "outcome": "null", "null_reason": "governance rejection"}

    store.record_transition(cstr)

    recovered = JsonJournalStateStore(tmp_path)
    assert recovered.read_current_state().state_version == 1
    assert recovered.read_transition("TR-NULL")["outcome"] == "null"
    assert len(recovered.list_transitions()) == 1
