# Change 0043 — Unified Cognitive Interaction Flow Runtime v0.1

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## Summary

Change 0043 introduces the first executable orchestration layer connecting the existing GRI v0.1 runtimes:

```
Cognitive Instance
-> PCG Relevance Retrieval
-> Internal Cognition Sufficiency
-> Cognitive Routing Decision
```

The flow is deliberately bounded. It does not become a frontier provider, Governance, Cognitive Kernel, PCG writer, or CSTR writer.

## Added

- `interaction_flow/flow.py`
- `interaction_flow/__init__.py`
- `tests/test_interaction_flow.py`

## Runtime Responsibilities

The flow:

1. creates a new Cognitive Instance;
2. activates Curiosity;
3. retrieves relevant persistent cognition through PCRRM;
4. evaluates internal cognition sufficiency through ICSM;
5. routes through CRDM;
6. records the routing decision in the interaction-scoped instance;
7. stops at the appropriate delegation, clarification, blocked, evidence, or consolidation boundary;
8. accepts frontier output only through an explicit re-entry method;
9. treats frontier output as new information;
10. prepares a temporary proposal or explicit null without committing persistent cognition.

## Explicit Boundaries

`InteractionFlow` does **not**:

- invoke a frontier provider;
- decide truth;
- create evidence automatically from model output;
- authorize persistent cognitive change;
- invoke Governance;
- invoke the Cognitive Kernel;
- mutate PCG;
- write CSTR.

Those remain downstream boundaries.

## Frontier Re-entry

A frontier response can enter the runtime only after a routing decision selected delegation.

The response is recorded in the Cognitive Instance and re-enters at validation/processing. It is not automatically treated as evidence, belief, or truth.

The re-entry boundary preserves:

```
Frontier Output
-> New Information
-> GRI Processing
-> Evidence / Proposal / Explicit Null
```

## Adversarial Coverage

Tests verify:

- native routing;
- explicit null;
- unknown cognition does not automatically trigger frontier delegation;
- capability-gap delegation;
- no provider invocation by the flow;
- frontier output re-entry;
- frontier output does not directly become persistent cognition;
- temporary proposal formation does not bypass Governance/Kernel;
- security blocking;
- unknown remains unknown;
- empty requirements are not silently invented.

## Architectural Position

The executable v0.1 path now reaches:

```
Interaction
-> Cognitive Instance
-> Curiosity
-> PCG Relevance Retrieval
-> Internal Cognition Sufficiency
-> Gap Identification
-> Cognitive Routing
-> Native / Frontier / Hybrid / Clarification / Blocked
```

For delegated processing, the next boundary remains external frontier communication followed by GRI re-entry. For persistent consequences, the existing CCA -> Governance -> Kernel -> PCG/CSTR path remains authoritative.

## Verification

The first integrated test run after this change exposed a test-fixture mismatch: the capability-only scenario also carried a knowledge gap because the retrieval stage had no seed. The router therefore correctly selected `hybrid`, matching the CRDM contract.

The fixture was corrected to represent a genuine capability-only gap, and a separate integration test now explicitly preserves the hybrid route when knowledge and capability gaps coexist.

A fresh full repository test run is required after this correction.


## Second Verification Correction

A second fixture issue was identified after the first correction: ICSM correctly classifies unspecified evidence and freshness as unresolved knowledge gaps. The capability-only integration scenario therefore now explicitly supplies supported evidence and adequate freshness, isolating the intended capability gap without changing ICSM or CRDM behavior.
