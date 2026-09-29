"""Deterministic two-layer governance evaluator for GRI v0.1."""
from dataclasses import dataclass, asdict
from typing import Callable, Any
from uuid import uuid4


@dataclass(frozen=True)
class ConstraintResult:
    constraint_id: str
    layer: str
    status: str
    reason: str


@dataclass(frozen=True)
class GovernanceDecision:
    decision_id: str
    proposal_id: str
    state_id: str
    state_version: int
    status: str
    local: tuple[ConstraintResult, ...]
    global_: tuple[ConstraintResult, ...]
    reason: str
    governance_version: str = "GRI-GOV-0.1"

    def as_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["global"] = result.pop("global_")
        return result


Constraint = Callable[[dict[str, Any]], ConstraintResult]


def evaluate_governance(proposal: dict[str, Any], *, state_id: str = "", state_version: int = 0, local_constraints=None, global_constraints=None, governance_version="GRI-GOV-0.1") -> GovernanceDecision:
    local = tuple(c(proposal) for c in (local_constraints or []))
    global_results = tuple(c(proposal) for c in (global_constraints or []))
    if any(r.status == "fail" for r in global_results):
        status, reason = "rejected", "mandatory global governance constraint failed"
    elif any(r.status == "fail" for r in local):
        status, reason = "rejected", "mandatory local governance constraint failed"
    elif any(r.status == "review" for r in local + global_results):
        status, reason = "requires_review", "governance review is required"
    else:
        status, reason = "approved", "all applicable governance constraints passed"
    return GovernanceDecision(f"GOV-{uuid4().hex[:12]}", proposal.get("proposal_id", ""), state_id, state_version, status, local, global_results, reason, governance_version)


def require_evidence(proposal):
    ok = bool(proposal.get("evidence"))
    return ConstraintResult("GOV-EVIDENCE-001", "local", "pass" if ok else "fail",
                            "proposal contains evidence references" if ok else "proposal contains no evidence references")


def prohibit_goal_removal_without_review(proposal):
    review = proposal.get("target_type") == "goal" and proposal.get("operation") == "remove"
    return ConstraintResult("GOV-GOAL-001", "global", "review" if review else "pass",
                            "goal removal requires explicit review" if review else "proposal is not an unrestricted goal removal")
