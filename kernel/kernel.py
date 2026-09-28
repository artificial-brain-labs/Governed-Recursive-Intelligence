"""Minimal executable Cognitive Kernel for GRI v0.1.

The kernel is intentionally independent of CRP serialization. It executes
already-structured proposals against a persistent state and emits a
Cognitive State Transition Record (CSTR).
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


SUPPORTED_TARGETS = {
    "belief": "pcg",
    "concept": "pcg",
    "relationship": "relationships",
    "goal": "goals",
    "dimension": "dimensions",
    "learning_state": "learning",
}
SUPPORTED_OPERATIONS = {"create", "modify", "reinforce", "weaken", "remove"}


@dataclass
class CognitiveState:
    state_id: str
    state_version: int
    pcg: dict[str, Any] = field(default_factory=dict)
    dimensions: dict[str, Any] = field(default_factory=dict)
    goals: dict[str, Any] = field(default_factory=dict)
    relationships: dict[str, Any] = field(default_factory=dict)
    learning: dict[str, Any] = field(default_factory=dict)
    history: list[str] = field(default_factory=list)

    def clone(self, *, state_version: int) -> "CognitiveState":
        return CognitiveState(
            state_id=self.state_id,
            state_version=state_version,
            pcg=deepcopy(self.pcg),
            dimensions=deepcopy(self.dimensions),
            goals=deepcopy(self.goals),
            relationships=deepcopy(self.relationships),
            learning=deepcopy(self.learning),
            history=list(self.history),
        )


def _target_store(state: CognitiveState, target_type: str) -> dict[str, Any]:
    store_name = SUPPORTED_TARGETS[target_type]
    return getattr(state, store_name)


def apply_transition(
    state: CognitiveState,
    proposal: dict[str, Any] | None,
    *,
    interaction_id: str,
    governance_status: str,
    governance_reason: str | None,
    governance_version: str,
    evidence_ids: list[str],
    timestamp: str | None = None,
) -> tuple[CognitiveState, dict[str, Any]]:
    """Apply one governed proposal and return (successor_state, CSTR)."""

    timestamp = timestamp or datetime.now(timezone.utc).isoformat()
    transition_id = f"TR-{uuid4().hex[:12]}"

    base_cstr = {
        "transition_id": transition_id,
        "timestamp": timestamp,
        "interaction_id": interaction_id,
        "state_before": {
            "state_id": state.state_id,
            "state_version": str(state.state_version),
        },
        "proposal": deepcopy(proposal),
        "evidence": list(evidence_ids),
        "governance": {
            "status": governance_status,
            "reason": governance_reason,
            "version": governance_version,
        },
        "provenance": {
            "kernel": "gri-cognitive-kernel-v0.1",
            "interaction_id": interaction_id,
        },
    }

    def null(reason: str) -> tuple[CognitiveState, dict[str, Any]]:
        successor = state.clone(state_version=state.state_version)
        record = {
            **base_cstr,
            "outcome": "null",
            "null_reason": reason,
            "state_after": {
                "state_id": successor.state_id,
                "state_version": str(successor.state_version),
            },
            "state_change": [],
        }
        return successor, record

    if proposal is None:
        return null("no cognitive proposal")

    if governance_status != "approved":
        return null(f"governance not approved: {governance_status}")

    if not evidence_ids:
        return null("no evidence")

    target_type = proposal.get("target_type")
    operation = proposal.get("operation")
    target_id = proposal.get("target_id")

    if target_type not in SUPPORTED_TARGETS:
        return null(f"unsupported target type: {target_type}")

    if operation not in SUPPORTED_OPERATIONS:
        return null(f"unsupported operation: {operation}")

    if not target_id and operation != "create":
        return null("target_id is required for non-create operations")

    store = _target_store(state, target_type)

    if operation == "create":
        if not target_id:
            return null("target_id is required for create")
        if target_id in store:
            return null("create target already exists")
        value = deepcopy(proposal.get("value", {"operation": "create"}))
        successor = state.clone(state_version=state.state_version + 1)
        _target_store(successor, target_type)[target_id] = value

    elif operation == "modify":
        if target_id not in store:
            return null("modify target does not exist")
        successor = state.clone(state_version=state.state_version + 1)
        _target_store(successor, target_type)[target_id] = deepcopy(
            proposal.get("value")
        )

    elif operation in {"reinforce", "weaken"}:
        if target_id not in store:
            return null(f"{operation} target does not exist")
        successor = state.clone(state_version=state.state_version + 1)
        current = deepcopy(store[target_id])
        if not isinstance(current, dict):
            current = {"value": current}
        current["last_operation"] = operation
        current["reinforcement_count"] = current.get("reinforcement_count", 0) + (
            1 if operation == "reinforce" else 0
        )
        current["weakening_count"] = current.get("weakening_count", 0) + (
            1 if operation == "weaken" else 0
        )
        _target_store(successor, target_type)[target_id] = current

    else:  # remove
        if target_id not in store:
            return null("remove target does not exist")
        successor = state.clone(state_version=state.state_version + 1)
        del _target_store(successor, target_type)[target_id]

    successor.history.append(transition_id)
    record = {
        **base_cstr,
        "outcome": "committed",
        "null_reason": None,
        "state_after": {
            "state_id": successor.state_id,
            "state_version": str(successor.state_version),
        },
        "state_change": [{
            "target_type": target_type,
            "target_id": target_id,
            "operation": operation,
        }],
    }
    return successor, record
