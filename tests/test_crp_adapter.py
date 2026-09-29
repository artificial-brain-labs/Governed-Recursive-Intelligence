import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "adapters"))

from adapter import CRPAdapterError, adapt_crp_to_pipeline
from governance import ConstraintResult, require_evidence
from kernel import CognitiveState

EVENT = ROOT / "crp" / "v0.2" / "examples" / "john-cancelled-meeting.json"

def load():
    return json.loads(EVENT.read_text(encoding="utf-8"))

def state():
    return CognitiveState(
        state_id="STATE-001",
        state_version=1,
        relationships={"REL-JOHN-MEETING": {"trust": "unmodified"}},
    )

def test_valid_crp_enters_pipeline_and_commits():
    successor, decision, cstr = adapt_crp_to_pipeline(
        load(), state(), local_constraints=[require_evidence]
    )
    assert decision["status"] == "approved"
    assert cstr["outcome"] == "committed"
    assert successor.state_version == 2

def test_crp_embedded_governance_is_not_authoritative():
    event = load()
    event["governance"]["status"] = "approved"
    event["proposal"]["operation"] = "remove"
    successor, decision, cstr = adapt_crp_to_pipeline(
        event, state(), local_constraints=[require_evidence]
    )
    assert decision["status"] == "approved"
    assert cstr["outcome"] == "committed"
    assert "REL-JOHN-MEETING" not in successor.relationships

def test_global_governance_stops_commitment():
    def reject(_):
        return ConstraintResult("GLOBAL-TEST", "global", "fail", "constitutional restriction")
    successor, decision, cstr = adapt_crp_to_pipeline(
        load(), state(), local_constraints=[require_evidence], global_constraints=[reject]
    )
    assert decision["status"] == "rejected"
    assert cstr["outcome"] == "null"
    assert successor.state_version == 1

def test_state_context_mismatch_is_blocked():
    event = load()
    event["state_context"]["state_version"] = "999"
    try:
        adapt_crp_to_pipeline(event, state(), local_constraints=[require_evidence])
    except CRPAdapterError as exc:
        assert "state_context.state_version" in str(exc)
    else:
        raise AssertionError("expected state context mismatch")

def test_invalid_crp_never_reaches_kernel():
    event = load()
    event["proposal"]["evidence"] = ["INVENTED"]
    try:
        adapt_crp_to_pipeline(event, state(), local_constraints=[require_evidence])
    except CRPAdapterError:
        pass
    else:
        raise AssertionError("expected invalid CRP to be rejected")
