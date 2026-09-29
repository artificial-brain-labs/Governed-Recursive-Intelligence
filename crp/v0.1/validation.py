"""Semantic validation rules for CRP v0.1.

JSON Schema validates representation structure. This module validates
cross-field cognitive integrity rules that require inspecting the complete
Cognitive Event.
"""

from __future__ import annotations

from typing import Any


def validate_semantics(event: dict[str, Any]) -> list[str]:
    """Return deterministic semantic validation errors."""
    errors: list[str] = []

    interaction_id = event.get("interaction_id")
    provenance = event.get("provenance", {})
    if provenance.get("source_interaction") != interaction_id:
        errors.append("provenance.source_interaction must equal interaction_id")

    observation = event.get("observation", {})
    facts = observation.get("facts", [])
    fact_ids = {fact.get("fact_id") for fact in facts}

    if observation.get("status") == "unknown" and facts:
        errors.append("an unknown observation cannot contain facts")

    for inference in event.get("inferences", []):
        for basis in inference.get("basis", []):
            if basis not in fact_ids:
                errors.append(
                    f"inference basis '{basis}' does not reference an observed fact"
                )

    governance_status = event.get("governance", {}).get("status")
    updates = event.get("cognitive_updates", [])

    if governance_status == "rejected" and updates:
        errors.append("rejected governance cannot authorize cognitive updates")

    return errors


def is_semantically_valid(event: dict[str, Any]) -> bool:
    """Return True when the event passes semantic integrity checks."""
    return not validate_semantics(event)
