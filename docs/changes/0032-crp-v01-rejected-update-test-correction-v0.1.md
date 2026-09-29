# Change 0032 — CRP v0.1 Rejected-Update Test Correction

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## Purpose

Correct the CRP v0.1 semantic test so that it actually exercises the invariant it asserts.

The v0.1 semantic rule is:

`rejected governance + cognitive updates -> semantic error`

The previous test changed governance to `rejected` while leaving `cognitive_updates` empty. Under the implemented rule, there was therefore no unauthorized update to reject.

## Change

The test now inserts a valid cognitive update before setting/validating rejected governance.

No validator semantics were changed.

## Architectural Impact

None. This is a test-contract correction only.

It preserves the distinction:

**Governance Rejection -> No Authorized Cognitive Update**

and avoids treating the mere presence of a rejected governance status as an error when no cognitive update is being attempted.

## Verification

Before this correction:

**43 passed, 1 failed**

The remaining failure was isolated to this test.

A full-suite run is required after pulling this change.
