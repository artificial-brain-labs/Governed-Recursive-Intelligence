"""Semantic validation rules for CRP v0.2.

Structural validation is performed by JSON Schema. These rules enforce
cross-field integrity without deciding external-world truth.
"""

from __future__ import annotations

from typing import Any


def validate_semantics(event: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    interaction_id = event.get("interaction_id")
    provenance = event.get("provenance", {})
    if provenance.get("source_interaction") != interaction_id:
        errors.append("provenance.source_interaction must equal interaction_id")

    observation = event.get("observation", {})
    facts = observation.get("facts", [])
    if observation.get("status") == "unknown" and facts:
        errors.append("an unknown observation cannot contain facts")

    evidence = event.get("evidence", [])
    evidence_ids = {item.get("evidence_id") for item in evidence}

    for inference in event.get("inferences", []):
        for basis in inference.get("basis", []):
            if basis not in evidence_ids:
                errors.append(
                    f"inference basis '{basis}' does not reference an evidence item"
                )

    proposal = event.get("proposal")
    governance = event.get("governance", {})
    transition = event.get("transition_reference")

    if proposal is not None:
        for evidence_ref in proposal.get("evidence", []):
            if evidence_ref not in evidence_ids:
                errors.append(
                    f"proposal evidence '{evidence_ref}' does not reference an evidence item"
                )

    if transition is not None and transition.get("outcome") == "committed":
        if governance.get("status") != "approved":
            errors.append("a committed transition reference requires approved governance")
        if proposal is None:
            errors.append("a committed transition reference requires a cognitive proposal")

    if transition is not None and proposal is None:
        errors.append("a transition reference requires a cognitive proposal")

    if governance.get("status") == "rejected" and transition is not None:
        errors.append("rejected governance cannot authorize a transition")

    return errors


def is_semantically_valid(event: dict[str, Any]) -> bool:
    return not validate_semantics(event)
