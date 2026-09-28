# Change 0031 — CRP v0.2 Validation and Test Isolation Alignment

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## 1. Purpose

Change 0031 resolves the CRP-related failures exposed by the first full repository test run after the durable pipeline export fix.

The failures were implementation/test-contract mismatches rather than Cognitive Kernel or Governance architecture failures.

## 2. Changes

### 2.1 CRP v0.2 state-context fixture

The canonical v0.2 example used `state_version: "42"` while the adapter tests supplied predecessor state version `1`.

The fixture is aligned to the test's intended predecessor state version:

`state_version = "1"`

This preserves the invariant that CRP state context must match the supplied predecessor state.

### 2.2 Versioned validator isolation

CRP v0.1 and v0.2 both contain a module named `validation.py`.

The tests previously imported both under the same top-level Python module name `validation`. Python module caching could therefore cause the v0.2 tests to execute the v0.1 validator.

The tests now load each validator under a version-specific module name:

- `gri_crp_v01_test_validation`
- `gri_crp_v02_test_validation`

This makes test behavior independent of collection order.

### 2.3 Rejected governance semantic guard

CRP v0.2 now reports a semantic error when rejected governance is combined with a proposal or transition reference.

This reinforces:

**Rejected Governance != Authorization**

and prevents a rejected governance status from being represented as an authorizing transition context.

### 2.4 jsonschema path assertion compatibility

The v0.1 schema test previously attempted slicing directly on `ValidationError.absolute_path`.

The jsonschema API exposes the path as a sequence/deque, so the test now explicitly converts it to a list before slicing.

No schema semantics were changed.

## 3. Architectural Impact

No changes were made to:

- Cognitive Kernel authority
- Governance architecture
- PCG semantics
- CSTR semantics
- state-transition mathematics
- CRP architectural position

The changes align fixtures, validation semantics, and test isolation with the existing GRI v0.1/v0.2 contracts.

## 4. Verification

The repository previously reached:

**33 passed, 11 failed**

after the public pipeline export was corrected.

A new full-suite execution is required in the Codespace after pulling Change 0031. No new full-test-pass claim is made until that execution is observed.

## 5. Expected Result

The next full test run should specifically verify:

1. CRP v0.2 adapter enters the governed pipeline with matching state context.
2. Embedded CRP governance remains non-authoritative.
3. Global governance rejection prevents commitment.
4. v0.1 and v0.2 semantic validators execute independently.
5. CRP v0.2 proposal/evidence/transition-reference rules are enforced.
6. The schema test works with the installed jsonschema API.

## 6. Conclusion

Change 0031 is a CRP protocol/test-harness alignment change. It does not alter the foundational GRI cognitive architecture.
