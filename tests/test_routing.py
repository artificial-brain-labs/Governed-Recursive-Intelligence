from routing import CognitiveRouter, RoutingContext, RoutingOutcome


def ctx(**overrides):
    base = dict(
        interaction_id="INT-ROUTE-1",
        instance_id="CI-ROUTE-1",
        requirement={"task": "answer"},
        sufficiency_state="sufficient",
        missing_requirements=(),
        knowledge_gaps=(),
        capability_gaps=(),
        internal_recovery_options=(),
        security_context={},
        available_capabilities=("native_reasoning",),
        clarification_available=True,
        internal_recovery_available=True,
        frontier_allowed=False,
        frontier_capabilities=(),
    )
    base.update(overrides)
    return RoutingContext(**base)


def test_sufficient_routes_native():
    result = CognitiveRouter().decide(ctx())
    assert result.outcome == RoutingOutcome.GRI_NATIVE
    assert result.selected_capability is None


def test_missing_pcg_does_not_automatically_route_frontier():
    result = CognitiveRouter().decide(ctx(
        sufficiency_state="unknown",
        knowledge_gaps=("missing_current_information",),
        internal_recovery_options=("additional_retrieval",),
        frontier_allowed=True,
        frontier_capabilities=("frontier-reasoning",),
    ))
    assert result.outcome == RoutingOutcome.GRI_NATIVE


def test_internal_recovery_precedes_frontier():
    result = CognitiveRouter().decide(ctx(
        sufficiency_state="insufficient",
        knowledge_gaps=("missing_context",),
        internal_recovery_options=("additional_retrieval",),
        frontier_allowed=True,
        frontier_capabilities=("frontier-reasoning",),
    ))
    assert result.outcome == RoutingOutcome.GRI_NATIVE


def test_capability_gap_can_route_frontier_when_authorized():
    result = CognitiveRouter().decide(ctx(
        sufficiency_state="insufficient",
        capability_gaps=("specialized_reasoning",),
        internal_recovery_options=(),
        frontier_allowed=True,
        frontier_capabilities=("specialized-frontier",),
    ))
    assert result.outcome == RoutingOutcome.FRONTIER_DELEGATED
    assert result.selected_capability == "specialized-frontier"
    assert result.delegation_scope == ("specialized_reasoning",)


def test_knowledge_and_capability_gap_can_be_hybrid():
    result = CognitiveRouter().decide(ctx(
        sufficiency_state="partially_sufficient",
        knowledge_gaps=("current_external_information",),
        capability_gaps=("specialized_reasoning",),
        internal_recovery_options=(),
        frontier_allowed=True,
        frontier_capabilities=("specialized-frontier",),
    ))
    assert result.outcome == RoutingOutcome.HYBRID


def test_ambiguous_context_requires_clarification():
    result = CognitiveRouter().decide(ctx(
        sufficiency_state="ambiguous",
        clarification_available=True,
    ))
    assert result.outcome == RoutingOutcome.CLARIFICATION_REQUIRED


def test_conflict_does_not_select_a_winner():
    result = CognitiveRouter().decide(ctx(
        sufficiency_state="conflict",
        clarification_available=True,
    ))
    assert result.outcome == RoutingOutcome.CLARIFICATION_REQUIRED


def test_retrieval_failure_is_not_unknown():
    result = CognitiveRouter().decide(ctx(
        sufficiency_state="retrieval_failure",
        internal_recovery_available=True,
        internal_recovery_options=("retry_retrieval",),
        frontier_allowed=True,
        frontier_capabilities=("frontier-reasoning",),
    ))
    assert result.outcome == RoutingOutcome.GRI_NATIVE


def test_unauthorized_external_capability_is_blocked():
    result = CognitiveRouter().decide(ctx(
        sufficiency_state="insufficient",
        capability_gaps=("specialized_reasoning",),
        internal_recovery_options=(),
        frontier_allowed=False,
        frontier_capabilities=("specialized-frontier",),
    ))
    assert result.outcome == RoutingOutcome.BLOCKED


def test_security_block_overrides_route():
    result = CognitiveRouter().decide(ctx(
        sufficiency_state="sufficient",
        security_context={"delegation": "blocked"},
        frontier_allowed=True,
        frontier_capabilities=("frontier-reasoning",),
    ))
    assert result.outcome == RoutingOutcome.BLOCKED


def test_routing_does_not_claim_truth_or_governance():
    result = CognitiveRouter().decide(ctx())
    assert result.provenance["routing_is_not_truth"] is True
    assert result.provenance["routing_is_not_governance"] is True


def test_delegation_scope_is_bounded():
    result = CognitiveRouter().decide(ctx(
        sufficiency_state="insufficient",
        capability_gaps=("specialized_reasoning",),
        knowledge_gaps=("unrelated_context",),
        internal_recovery_options=(),
        frontier_allowed=True,
        frontier_capabilities=("specialized-frontier",),
    ))
    assert len(result.delegation_scope) == 1
