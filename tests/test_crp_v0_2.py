import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location(
    "gri_crp_v02_test_validation", ROOT / "crp" / "v0.2" / "validation.py"
)
_module = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_module)
validate_semantics = _module.validate_semantics

SCHEMA = ROOT / "crp" / "v0.2" / "cognitive-event.schema.json"
VALID = ROOT / "crp" / "v0.2" / "examples" / "john-cancelled-meeting.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validator():
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def test_schema_is_valid():
    assert list(validator().iter_errors(load(VALID))) == []


def test_provenance_must_match_interaction():
    event = load(VALID)
    event["provenance"]["source_interaction"] = "different"
    assert any("source_interaction" in e for e in validate_semantics(event))


def test_inference_basis_must_reference_evidence():
    event = load(VALID)
    event["inferences"][0]["basis"] = ["invented-evidence"]
    assert any("does not reference an evidence item" in e for e in validate_semantics(event))


def test_proposal_evidence_must_reference_evidence():
    event = load(VALID)
    event["proposal"]["evidence"] = ["invented-evidence"]
    assert any("proposal evidence" in e for e in validate_semantics(event))


def test_committed_transition_requires_approved_governance():
    event = load(VALID)
    event["transition_reference"] = {"transition_id": "TR-001", "outcome": "committed"}
    assert any("approved governance" in e for e in validate_semantics(event))


def test_rejected_governance_cannot_authorize_transition():
    event = load(VALID)
    event["governance"]["status"] = "rejected"
    event["transition_reference"] = {"transition_id": "TR-001", "outcome": "null"}
    assert any("rejected governance" in e for e in validate_semantics(event))


def test_no_proposal_is_valid_without_transition():
    event = load(VALID)
    event["proposal"] = None
    event["transition_reference"] = None
    assert validate_semantics(event) == []


def test_committed_transition_requires_proposal():
    event = load(VALID)
    event["proposal"] = None
    event["governance"]["status"] = "approved"
    event["transition_reference"] = {"transition_id": "TR-001", "outcome": "committed"}
    assert any("requires a cognitive proposal" in e for e in validate_semantics(event))
