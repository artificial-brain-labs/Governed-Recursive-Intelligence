# Change Record 0002 — Cognitive State Transition Record

**Date:** 2026-09-28  
**Area:** GRI cognitive architecture  
**Status:** Proposed / documented  
**Branch:** feature/crp-v0.1

## Context

The GRI Cognitive State Transition Model v0.1 established the formal transition:

S_(t+1) = T(S_t, E_t, I_t, X_t, P_t, A_t)

The architecture now requires an explicit historical representation of each evaluated transition so persistent cognitive evolution remains auditable and traceable.

## Decision

Introduce the Cognitive State Transition Record (CSTR) v0.1 as an implementation-independent historical record of cognitive state transitions.

CSTR records:

- originating experience
- previous state reference
- interpretation
- evidence
- cognitive proposal
- governance decision
- actual transition outcome
- successor state reference
- provenance
- explicit reasons for null transitions

## Architectural Boundaries

CSTR is:

- not persistent cognitive state
- not PCG
- not TCM
- not CRP
- not a reasoning engine
- not a truth oracle
- not a serialization format

CSTR records the governed transition that changes, or explicitly does not change, persistent cognition.

## Key Invariants

1. Committed cognitive changes must be traceable.
2. Committed changes require governance authorization.
3. Proposal does not equal commitment.
4. Null transitions are valid and must be explainable.
5. Unknown, interpreted, and inferred information must not silently become facts.
6. Foundation models cannot directly write persistent cognitive state.
7. Transition history must remain distinguishable from persistent cognitive consequences.

## Consequence

CRP v0.2 should be derived after CSTR is stable.

The architectural sequence is:

Cognitive Theory
-> State Transition Model
-> Transition Record
-> CRP
-> Kernel Implementation

## Related Specification

See docs/COGNITIVE_STATE_TRANSITION_RECORD_v0.1.md.

## Open Work

The next stage is to derive the minimum CRP v0.2 representation requirements from the CSTR model and then implement the corresponding validation and transition-record tests.
