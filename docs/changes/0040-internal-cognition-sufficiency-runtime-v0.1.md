# Change 0040 — Internal Cognition Sufficiency Runtime v0.1

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## Summary

Change 0040 introduces the first executable reference implementation of the Internal Cognition Sufficiency Model (ICSM) specified by `INTERNAL_COGNITION_SUFFICIENCY_MODEL_v0.1.md`.

ICSM is a non-mutating evaluation layer between relevant PCG retrieval and routing.

## Added

- `sufficiency/icsm.py`
- `sufficiency/__init__.py`
- `tests/test_icsm.py`

## Implemented Semantics

The runtime evaluates:

- requirement-relative cognitive coverage;
- retrieval status;
- evidence state;
- temporal/freshness adequacy;
- consistency/conflict;
- identity/context resolution;
- native capability availability;
- knowledge gaps;
- capability gaps;
- combined gaps;
- internal recovery options.

It exposes the architectural sufficiency states:

- sufficient;
- partially_sufficient;
- insufficient;
- unknown;
- ambiguous;
- retrieval_failure;
- conflict.

## Authority Boundaries

ICSM does not:

- determine objective truth;
- guarantee certainty;
- select a routing destination;
- authorize frontier delegation;
- mutate PCG;
- create beliefs or facts;
- turn evaluation into learning.

The intended boundary remains:

```
PCG / Retrieval
-> ICSM
-> Gap Identification
-> Routing
```

## No-Guessing Properties

The runtime preserves the distinctions:

```
Sufficiency != Truth
Retrieval Failure != Unknown
PCG Absence != Falsity
Knowledge Gap != Capability Gap
Conflict != Resolved Truth
Stale Cognition != False Cognition
```

A missing retrieval result may produce an explicit unknown state with recovery options rather than an automatic frontier route.

## Current Scope

The implementation intentionally avoids:

- numeric confidence thresholds;
- probabilistic sufficiency scoring;
- learned routing policy;
- semantic similarity as an authority;
- automatic identity resolution;
- automatic conflict resolution;
- direct frontier invocation;
- PCG mutation.

Those remain separate research/implementation concerns.

## Verification Scope

Dedicated tests cover:

1. sufficient cognition;
2. partial retrieval;
3. no relevant cognition;
4. retrieval failure;
5. conflict;
6. ambiguous identity;
7. capability gap;
8. combined gap;
9. stale/temporally inadequate cognition;
10. separation of sufficiency evaluation from truth and routing.

A full repository test run must be performed after pulling the change.

## Architectural Position

The executable dependency chain is now:

```
Cognitive Instance
-> Retrieval Context
-> PCRRM
-> Relevant Persistent Cognition
-> ICSM
-> Gap Identification
-> Routing
```

The next layer is the Cognitive Routing Decision Model runtime, which will consume ICSM results without allowing routing to become a truth or persistence mechanism.
