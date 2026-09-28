# Change 0041 — ICSM Result-Constructor Branch Fix

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## Summary

The first execution of the ICSM runtime exposed a constructor mismatch in two explicit evaluation branches:

- `conflict`
- `ambiguous identity/context`

Both branches correctly selected the intended sufficiency state but failed at runtime because the shared result constructor requires explicit `knowledge_gaps` and `capability_gaps` collections.

## Correction

Both branches now pass explicit empty gap lists where no knowledge/capability gap was being asserted by that branch.

This preserves the semantic distinction between:

- conflict as a consistency condition;
- ambiguity as an identity/context resolution condition;
- knowledge gaps;
- capability gaps.

No new inference or evaluation rule was introduced.

## Architectural Impact

The correction is implementation-only.

The ICSM contract remains:

```
Requirement + Relevant Cognition
-> Sufficiency Evaluation
-> Gap Identification
-> Routing
```

ICSM remains non-mutating and does not:

- establish truth;
- choose a route;
- authorize delegation;
- mutate PCG;
- create persistent cognition.

## Verification

Before this correction the user-run repository suite reported:

```
77 passed, 2 failed
```

Both failures were the same class of `TypeError` in the ICSM result-construction path.

A fresh full-suite run is required after pulling this correction.
