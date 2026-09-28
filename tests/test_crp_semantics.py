import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location(
    "gri_crp_v01_test_validation", ROOT / "crp" / "v0.1" / "validation.py"
)
_module = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_module)
validate_semantics = _module.validate_semantics

VALID = ROOT / "crp" / "v0.1" / "examples" / "john-cancelled-meeting.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_valid_event_has_valid_provenance():
    event = load(VALID)
    assert validate_semantics(event) == []


def test_provenance_must_match_interaction():
    event = load(VALID)
    event["provenance"]["source_interaction"] = "different-interaction"

    errors = validate_semantics(event)

    assert any("source_interaction" in error for error in errors)


def test_inference_basis_must_reference_observed_fact():
    event = load(VALID)
    event["inferences"][0]["basis"] = ["invented-fact-id"]

    errors = validate_semantics(event)

    assert any("does not reference an observed fact" in error for error in errors)


def test_unknown_observation_cannot_contain_facts():
    event = load(VALID)
    event["observation"]["status"] = "unknown"

    errors = validate_semantics(event)

    assert any("unknown observation" in error for error in errors)


def test_rejected_governance_cannot_authorize_updates():
    event = load(VALID)
    event["governance"]["status"] = "rejected"

    errors = validate_semantics(event)

    assert any("rejected governance" in error for error in errors)
