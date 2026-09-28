"""End-to-end governed transition pipeline for GRI v0.1."""

from __future__ import annotations

from typing import Any, Callable

from governance import GovernanceDecision, evaluate_governance
from kernel import CognitiveState, apply_transition


def execute_governed_transition(
    state: CognitiveState,
    proposal: dict[str, Any] | None,
    *,
    interaction_id: str,
    local_constraints: list[Callable] | None = None,
    global_constraints: list[Callable] | None = None,
    evidence_ids: list[str] | None = None,
    timestamp: str | None = None,
) -> tuple[CognitiveState, GovernanceDecision, dict[str, Any]]:
    """Evaluate governance, then execute exactly that authorization in the kernel."""

    evidence_ids = list(evidence_ids or [])

    governance_input = dict(proposal or {})
    if proposal is not None and "evidence" not in governance_input:
        governance_input["evidence"] = list(evidence_ids)

    decision = evaluate_governance(
        governance_input,
        local_constraints=local_constraints,
        global_constraints=global_constraints,
    )

    successor, cstr = apply_transition(
        state,
        proposal,
        interaction_id=interaction_id,
        governance_status=decision.status,
        governance_reason=decision.reason,
        governance_version=decision.governance_version,
        evidence_ids=evidence_ids,
        timestamp=timestamp,
    )

    cstr["governance"] = decision.as_dict()
    return successor, decision, cstr
