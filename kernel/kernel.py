"""Minimal executable Cognitive Kernel for GRI v0.1."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

SUPPORTED_TARGETS = {"belief": "pcg", "concept": "pcg", "relationship": "relationships", "goal": "goals", "dimension": "dimensions", "learning_state": "learning"}
SUPPORTED_OPERATIONS = {"create", "modify", "reinforce", "weaken", "remove", "no_change"}


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
        return CognitiveState(self.state_id, state_version, deepcopy(self.pcg), deepcopy(self.dimensions), deepcopy(self.goals), deepcopy(self.relationships), deepcopy(self.learning), list(self.history))


def _target_store(state: CognitiveState, target_type: str) -> dict[str, Any]:
    return getattr(state, SUPPORTED_TARGETS[target_type])


def apply_transition(state: CognitiveState, proposal: dict[str, Any] | None, *, interaction_id: str, governance_decision: dict[str, Any] | None, evidence_ids: list[str], timestamp: str | None = None) -> tuple[CognitiveState, dict[str, Any]]:
    """Execute exactly one state-bound authorization against an immutable predecessor."""
    timestamp = timestamp or datetime.now(timezone.utc).isoformat()
    transition_id = f"TR-{uuid4().hex[:12]}"
    authorization = deepcopy(governance_decision) if governance_decision else {
        "status": "rejected", "proposal_id": proposal.get("proposal_id", "") if proposal else "",
        "state_id": state.state_id, "state_version": state.state_version,
        "governance_version": "unknown", "reason": "missing authorization decision",
    }
    base_cstr = {
        "transition_id": transition_id, "timestamp": timestamp, "interaction_id": interaction_id,
        "state_before": {"state_id": state.state_id, "state_version": str(state.state_version)},
        "proposal": deepcopy(proposal), "evidence": list(evidence_ids),
        "governance": authorization,
        "provenance": {"kernel": "gri-cognitive-kernel-v0.1", "interaction_id": interaction_id},
    }

    def null(reason: str, status: str = "execution_failure"):
        successor = state.clone(state_version=state.state_version)
        return successor, {**base_cstr, "outcome": "null", "execution_status": status, "null_reason": reason,
            "state_after": {"state_id": successor.state_id, "state_version": str(successor.state_version)}, "state_change": []}

    if proposal is None:
        return null("no cognitive proposal", "no_proposal")
    if authorization.get("status") != "approved":
        return null(f"governance not approved: {authorization.get('status')}", "governance_not_approved")
    if authorization.get("proposal_id") != proposal.get("proposal_id"):
        return null("authorization does not match proposal", "authorization_invalidated")
    if authorization.get("state_id") != state.state_id:
        return null("authorization predecessor state_id mismatch", "stale_state")
    try:
        authorized_version = int(authorization.get("state_version"))
    except (TypeError, ValueError):
        return null("authorization predecessor state_version is invalid", "authorization_invalidated")
    if authorized_version != state.state_version:
        return null("authorization predecessor state is stale", "stale_state")
    if not evidence_ids:
        return null("no evidence", "evidence_missing")

    target_type, operation, target_id = proposal.get("target_type"), proposal.get("operation"), proposal.get("target_id")
    if target_type not in SUPPORTED_TARGETS:
        return null(f"unsupported target type: {target_type}", "unsupported_operation")
    if operation not in SUPPORTED_OPERATIONS:
        return null(f"unsupported operation: {operation}", "unsupported_operation")
    if operation == "no_change":
        successor = state.clone(state_version=state.state_version)
        return successor, {**base_cstr, "outcome": "null", "execution_status": "explicit_no_change", "null_reason": "explicit_no_change",
            "state_after": {"state_id": successor.state_id, "state_version": str(successor.state_version)}, "state_change": []}
    if not target_id:
        return null("target_id is required", "target_precondition_failed")

    store = _target_store(state, target_type)
    if operation == "create":
        if target_id in store:
            return null("create target already exists", "target_precondition_failed")
        value = deepcopy(proposal.get("value", {"operation": "create"}))
        successor = state.clone(state_version=state.state_version + 1)
        _target_store(successor, target_type)[target_id] = value
    elif operation == "modify":
        if target_id not in store:
            return null("modify target does not exist", "target_precondition_failed")
        successor = state.clone(state_version=state.state_version + 1)
        _target_store(successor, target_type)[target_id] = deepcopy(proposal.get("value"))
    elif operation in {"reinforce", "weaken"}:
        if target_id not in store:
            return null(f"{operation} target does not exist", "target_precondition_failed")
        successor = state.clone(state_version=state.state_version + 1)
        current = deepcopy(store[target_id])
        if not isinstance(current, dict):
            current = {"value": current}
        current["last_operation"] = operation
        current["reinforcement_count"] = current.get("reinforcement_count", 0) + (1 if operation == "reinforce" else 0)
        current["weakening_count"] = current.get("weakening_count", 0) + (1 if operation == "weaken" else 0)
        _target_store(successor, target_type)[target_id] = current
    else:
        if target_id not in store:
            return null("remove target does not exist", "target_precondition_failed")
        successor = state.clone(state_version=state.state_version + 1)
        del _target_store(successor, target_type)[target_id]

    successor.history.append(transition_id)
    return successor, {**base_cstr, "outcome": "committed", "execution_status": "success", "null_reason": None,
        "state_after": {"state_id": successor.state_id, "state_version": str(successor.state_version)},
        "state_change": [{"target_type": target_type, "target_id": target_id, "operation": operation}]}
