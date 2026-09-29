# Change 0042 — Cognitive Routing Decision Runtime v0.1

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## Summary

Change 0042 introduces the first executable reference implementation of the Cognitive Routing Decision Model (CRDM) v0.1.

The router consumes Internal Cognition Sufficiency results and determines a processing route without becoming a truth evaluator, evidence authority, governance layer, or persistent-state writer.

## Added

- `routing/router.py`
- `routing/__init__.py`
- `tests/test_routing.py`

## Primary Routing Outcomes

The runtime supports:

- `gri_native`
- `frontier_delegated`
- `hybrid`
- `clarification_required`
- `blocked`

## Decision Principles

The runtime enforces:

1. Sufficient cognition routes to GRI-native processing.
2. Missing PCG cognition does not automatically trigger frontier delegation.
3. Internal recovery is considered before external delegation.
4. Retrieval failure remains distinct from knowledge absence.
5. Ambiguity may require clarification.
6. Conflict is preserved rather than resolved by selecting a winner.
7. External capability gaps require explicit authorization.
8. Security restrictions can block an otherwise available route.
9. Delegation scope is bounded to the identified missing requirement.
10. Routing does not authorize persistent cognitive change.

## Selective Delegation

When frontier delegation is selected, the runtime returns:

- the missing requirement;
- a bounded delegation scope;
- the selected authorized capability.

The router does not invoke a frontier provider itself.

This preserves the architectural separation:

```
Routing Decision
-> Delegation Context Selection
-> Authorization / Access Check
-> Frontier Processor
```

Provider integration remains a separate boundary.

## No-Guessing Invariants

The implementation preserves:

```
PCG Not Found != Frontier Required
Retrieval Failure != Knowledge Absence
Routing != Truth
Routing != Evidence
Routing != Governance
Frontier Output != Persistent Belief
```

## Current Scope

This runtime intentionally does not implement:

- frontier provider invocation;
- capability registry persistence;
- learned routing;
- model-quality ranking;
- cost/latency optimization;
- context minimization implementation;
- frontier response re-entry execution;
- recursive routing limits;
- governance policy execution for delegation;
- CCA integration.

Those remain separate implementation layers.

## Verification Scope

Tests cover:

- native routing;
- internal recovery before delegation;
- unknown cognition;
- capability-gap delegation;
- hybrid routing;
- clarification;
- conflict preservation;
- retrieval failure;
- unauthorized capability blocking;
- security blocking;
- truth/governance boundary;
- bounded delegation scope.

A full repository test run is required after pulling this change.

## Architectural Position

The executable chain now reaches:

```
Cognitive Instance
-> PCG Relevance Retrieval
-> Internal Cognition Sufficiency
-> Gap Identification
-> Cognitive Routing Decision
-> GRI-Native / Frontier / Hybrid / Clarification / Blocked
```

The next implementation should connect this routing decision to the existing Cognitive Instance lifecycle and then implement the frontier communication/re-entry boundary, rather than allowing the router to call a foundation model directly.
