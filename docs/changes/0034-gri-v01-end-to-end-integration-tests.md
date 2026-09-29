# Change 0034 — GRI v0.1 End-to-End Integration and Invariant Tests

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## 1. Purpose

Change 0034 introduces the first canonical end-to-end integration test for the executable GRI v0.1 boundaries and a focused adversarial invariant suite.

## 2. Canonical Path

The integration test composes:

```
Interaction
-> Requirement representation
-> PCG relevance retrieval
-> Internal cognition sufficiency stage
-> CRP interpretation/evidence
-> Candidate/Proposal
-> Governance
-> Cognitive Kernel
-> Successor State
-> CSTR
-> Persistent Store
```

The requirement, PCG retrieval, and internal sufficiency stages are explicitly represented as test-stage orchestration because dedicated production modules for these architectural layers have not yet been implemented.

The test does not claim that those layers are already production components.

## 3. Verified Invariants Covered

The new tests cover:

1. Valid evidence-backed proposal commits through Governance and Kernel.
2. Missing evidence cannot commit.
3. Global governance rejection cannot commit.
4. Stale persistent state is rejected before durable execution.
5. Missing target produces a null, traceable transition.
6. Explicit `no_change` does not force learning.
7. Unknown information remains without facts/proposal.
8. Frontier-model output is represented as new information and does not directly mutate persistent cognition.

## 4. Persistence Boundary

The canonical test verifies both:

- successor state recovery from the persistent store
- CSTR recovery for the committed transition

This demonstrates the current executable separation:

`PCG/current state != CSTR/history`

## 5. Architectural Boundary

This change does not implement the still-specification-level:

- Requirement Identification engine
- PCG Relevance Retrieval engine
- Internal Cognition Sufficiency engine
- Cognitive Instance lifecycle runtime
- CCA runtime
- frontier routing runtime

It establishes tests that will become integration anchors as those components are implemented.

## 6. No-Guessing Boundary

The tests preserve:

```
Observation != Interpretation != Evidence != Inference != Proposal != Commitment
```

and:

```
Unknown != Fact
Frontier Output != Persistent Cognition
```

## 7. Verification

The existing baseline before this change was:

**44 passed**

The new integration suite must be executed in the Codespace after pulling this change. No new test-pass claim is made until the execution result is observed.

## 8. Conclusion

Change 0034 establishes the first system-level executable acceptance boundary for GRI v0.1 while explicitly distinguishing implemented runtime components from architectural layers that remain to be implemented.
