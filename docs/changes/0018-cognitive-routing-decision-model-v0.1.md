# Change 0018 — Cognitive Routing Decision Model v0.1

**Status:** Implemented on feature branch  
**Date:** 2026-09-28

## Summary

Formalizes the Cognitive Routing Decision as a distinct GRI orchestration process between internal cognition evaluation and external/frontier delegation.

## Decisions

- GRI evaluates relevant internal cognition before external delegation.
- The router identifies the actual missing requirement before selecting a frontier route.
- Missing PCG information is not itself sufficient reason to invoke a frontier model.
- Additional internal retrieval, ICG processing, dimension activation, evidence evaluation, or clarification may occur before delegation.
- Routing outcomes are GRI-native, frontier-delegated, hybrid, clarification-required, or blocked.
- Delegation is selective rather than automatically applying to the complete interaction.
- Frontier context is minimized and authorization-checked.
- Frontier capability selection may use an authorized capability registry.
- Every frontier response is treated as new information and re-enters the same GRI cognitive process.
- Routing is distinct from evidence, truth, governance, and persistent cognitive change.
- Routing history remains temporary unless separately governed for persistence.

## Architectural Principle

> GRI thinks first, determines what is missing, and only then decides whether external intelligence is required.

## Files Added

- docs/COGNITIVE_ROUTING_DECISION_MODEL_v0.1.md
- docs/changes/0018-cognitive-routing-decision-model-v0.1.md
