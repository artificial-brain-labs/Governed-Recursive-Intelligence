"""Reference Cognitive Routing Decision Model for GRI v0.1.

Routing selects a processing path. It does not establish truth, authorize
persistent cognition, or directly invoke a frontier provider.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping
from uuid import uuid4


class RoutingOutcome(str, Enum):
    GRI_NATIVE = "gri_native"
    FRONTIER_DELEGATED = "frontier_delegated"
    HYBRID = "hybrid"
    CLARIFICATION_REQUIRED = "clarification_required"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class RoutingContext:
    interaction_id: str
    instance_id: str
    requirement: Any
    sufficiency_state: str
    missing_requirements: tuple[str, ...] = ()
    knowledge_gaps: tuple[str, ...] = ()
    capability_gaps: tuple[str, ...] = ()
    internal_recovery_options: tuple[str, ...] = ()
    evidence_state: str | None = None
    security_context: Mapping[str, Any] = field(default_factory=dict)
    available_capabilities: tuple[str, ...] = ()
    processing_history: tuple[Mapping[str, Any], ...] = ()
    clarification_available: bool = True
    internal_recovery_available: bool = True
    frontier_allowed: bool = False
    frontier_capabilities: tuple[str, ...] = ()


@dataclass(frozen=True)
class RoutingDecision:
    routing_id: str
    outcome: RoutingOutcome
    missing_requirements: tuple[str, ...]
    delegation_scope: tuple[str, ...]
    selected_capability: str | None
    reason: str
    provenance: Mapping[str, Any]


class CognitiveRouter:
    """Deterministic reference router preserving GRI's v0.1 boundaries."""

    _CLARIFICATION_STATES = {"ambiguous"}
    _RECOVERABLE_STATES = {"unknown", "insufficient", "partially_sufficient"}
    _BLOCKED_SECURITY = {"blocked", "denied", "prohibited"}

    def decide(self, context: RoutingContext) -> RoutingDecision:
        state = context.sufficiency_state.strip().lower()
        missing = tuple(dict.fromkeys(context.missing_requirements))
        knowledge_gaps = tuple(dict.fromkeys(context.knowledge_gaps))
        capability_gaps = tuple(dict.fromkeys(context.capability_gaps))
        all_missing = tuple(dict.fromkeys(missing + knowledge_gaps + capability_gaps))

        if self._security_blocked(context):
            return self._decision(
                context, RoutingOutcome.BLOCKED, all_missing,
                (), None, "processing or delegation is prohibited by security constraints",
            )

        if state == "retrieval_failure":
            if context.internal_recovery_available:
                return self._decision(
                    context, RoutingOutcome.GRI_NATIVE, all_missing,
                    (), None, "retrieval failed; recover internally before considering external delegation",
                )
            return self._decision(
                context, RoutingOutcome.BLOCKED, all_missing,
                (), None, "retrieval failed and no permitted internal recovery path is available",
            )

        if state == "conflict":
            if context.clarification_available:
                return self._decision(
                    context, RoutingOutcome.CLARIFICATION_REQUIRED, all_missing,
                    (), None, "conflicting persistent cognition requires resolution or clarification",
                )
            if context.internal_recovery_available:
                return self._decision(
                    context, RoutingOutcome.GRI_NATIVE, all_missing,
                    (), None, "conflicting cognition requires internal conflict evaluation",
                )
            return self._decision(
                context, RoutingOutcome.BLOCKED, all_missing,
                (), None, "conflicting cognition cannot be safely resolved with available paths",
            )

        if state == "ambiguous":
            if context.clarification_available:
                return self._decision(
                    context, RoutingOutcome.CLARIFICATION_REQUIRED, all_missing,
                    (), None, "required identity or context is ambiguous",
                )
            if context.internal_recovery_available:
                return self._decision(
                    context, RoutingOutcome.GRI_NATIVE, all_missing,
                    (), None, "ambiguous context requires internal resolution before delegation",
                )
            return self._decision(
                context, RoutingOutcome.BLOCKED, all_missing,
                (), None, "ambiguous context cannot be resolved with available paths",
            )

        if state == "sufficient":
            return self._decision(
                context, RoutingOutcome.GRI_NATIVE, (),
                (), None, "relevant cognition and native capability are sufficient",
            )

        # Unknown/partial/insufficient: identify the missing requirement before
        # selecting an external route.
        if context.internal_recovery_available and context.internal_recovery_options:
            return self._decision(
                context, RoutingOutcome.GRI_NATIVE, all_missing,
                (), None, "internal recovery is available and must be evaluated before frontier delegation",
            )

        if capability_gaps and context.frontier_allowed and context.frontier_capabilities:
            capability = context.frontier_capabilities[0]
            scope = self._minimal_scope(all_missing or capability_gaps)
            outcome = RoutingOutcome.HYBRID if context.knowledge_gaps else RoutingOutcome.FRONTIER_DELEGATED
            return self._decision(
                context, outcome, all_missing, scope, capability,
                "an authorized external capability addresses the identified missing requirement",
            )

        if capability_gaps and not context.frontier_allowed:
            return self._decision(
                context, RoutingOutcome.BLOCKED, all_missing,
                (), None, "required external capability is not authorized",
            )

        if state in {"unknown", "insufficient", "partially_sufficient"}:
            if context.clarification_available and not context.frontier_allowed:
                return self._decision(
                    context, RoutingOutcome.CLARIFICATION_REQUIRED, all_missing,
                    (), None, "the missing requirement cannot be resolved internally and requires clarification",
                )
            if context.frontier_allowed and context.frontier_capabilities:
                capability = context.frontier_capabilities[0]
                scope = self._minimal_scope(all_missing or ("unresolved_requirement",))
                return self._decision(
                    context, RoutingOutcome.FRONTIER_DELEGATED, all_missing,
                    scope, capability, "the identified requirement requires authorized external information or capability",
                )

        return self._decision(
            context, RoutingOutcome.BLOCKED, all_missing,
            (), None, "no permitted processing route satisfies the identified requirement",
        )

    @classmethod
    def _security_blocked(cls, context: RoutingContext) -> bool:
        security = {str(v).lower() for v in context.security_context.values()}
        return bool(security & cls._BLOCKED_SECURITY)

    @staticmethod
    def _minimal_scope(requirements: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(requirements[:1]) if requirements else ("identified_missing_requirement",)

    @staticmethod
    def _decision(
        context: RoutingContext,
        outcome: RoutingOutcome,
        missing: tuple[str, ...],
        scope: tuple[str, ...],
        capability: str | None,
        reason: str,
    ) -> RoutingDecision:
        return RoutingDecision(
            routing_id=f"ROUTE-{uuid4().hex[:12]}",
            outcome=outcome,
            missing_requirements=missing,
            delegation_scope=scope,
            selected_capability=capability,
            reason=reason,
            provenance={
                "routing": "gri-routing-v0.1",
                "interaction_id": context.interaction_id,
                "instance_id": context.instance_id,
                "sufficiency_state": context.sufficiency_state,
                "routing_is_not_truth": True,
                "routing_is_not_governance": True,
            },
        )
