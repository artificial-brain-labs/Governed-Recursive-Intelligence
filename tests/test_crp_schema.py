import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "crp" / "v0.1" / "cognitive-event.schema.json"
VALID = ROOT / "crp" / "v0.1" / "examples" / "john-cancelled-meeting.json"
INVALID = ROOT / "crp" / "v0.1" / "examples" / "invalid-guessing.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def validator():
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())

def test_valid_event():
    assert list(validator().iter_errors(load(VALID))) == []

def test_unknown_root_field_rejected():
    event = load(VALID)
    event["unexpected_field"] = True
    assert list(validator().iter_errors(event))

def test_cognitive_update_requires_evidence():
    errors = list(validator().iter_errors(load(INVALID)))
    assert any(
        error.validator == "minItems" and
        error.absolute_path[-1:] == ["evidence"]
        for error in errors
    )
