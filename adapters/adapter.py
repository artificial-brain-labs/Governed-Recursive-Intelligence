"""Strict adapter from validated CRP v0.2 events to the governed pipeline."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator, FormatChecker
from kernel import CognitiveState
from pipeline import execute_governed_transition

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "crp" / "v0.2" / "cognitive-event.schema.json"
VALIDATION_PATH = ROOT / "crp" / "v0.2" / "validation.py"

_spec = importlib.util.spec_from_file_location("gri_crp_v02_validation", VALIDATION_PATH)
_module = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_module)
validate_semantics = _module.validate_semantics


class CRPAdapterError(ValueError):
    """Raised when a CRP event cannot enter the governed pipeline."""


def _validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_crp_event(event: dict[str, Any]) -> None:
    structural = sorted(_validator().iter_errors(event), key=lambda error: list(error.path))
    semantic = validate_semantics(event)
    errors = [f"structural: {error.message}" for error in structural]
    errors.extend(f"semantic: {error}" for error in semantic)
    if errors:
        raise CRPAdapterError("; ".join(errors))


def adapt_crp_to_pipeline(
    event: dict[str, Any],
    state: CognitiveState,
    *,
    local_constraints: list[Callable] | None = None,
    global_constraints: list[Callable] | None = None,
) -> tuple[CognitiveState, dict[str, Any], dict[str, Any]]:
    """Validate CRP, re-run governance, then execute through the kernel."""
    validate_crp_event(event)

    context = event["state_context"]
    if context["state_id"] != state.state_id:
        raise CRPAdapterError("CRP state_context.state_id does not match supplied state")
    if str(context["state_version"]) != str(state.state_version):
        raise CRPAdapterError("CRP state_context.state_version does not match supplied state")

    proposal = event.get("proposal")
    evidence_ids = [item["evidence_id"] for item in event.get("evidence", [])]

    # CRP governance is metadata only. It is never execution authorization.
    successor, decision, cstr = execute_governed_transition(
        state,
        proposal,
        interaction_id=event["interaction_id"],
        local_constraints=local_constraints,
        global_constraints=global_constraints,
        evidence_ids=evidence_ids,
        timestamp=event["timestamp"],
    )

    cstr["crp"] = {
        "crp_version": event["crp_version"],
        "interaction_id": event["interaction_id"],
        "state_context": context,
        "source": event["source"],
        "provenance": event["provenance"],
    }
    return successor, decision.as_dict(), cstr
