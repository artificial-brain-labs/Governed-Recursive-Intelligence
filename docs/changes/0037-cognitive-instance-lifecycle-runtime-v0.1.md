# Change 0037 — Cognitive Instance Lifecycle Runtime v0.1

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## 1. Purpose

Change 0037 implements the first executable runtime for the GRI Cognitive Instance (CI) lifecycle specified in `COGNITIVE_INSTANCE_LIFECYCLE_v0.1.md`.

The Cognitive Instance is the bounded orchestration context for one cognitive-processing occurrence.

It is explicitly **not** persistent cognition.

## 2. Runtime Components

Added:

- `cognitive_instance/instance.py`
- `cognitive_instance/__init__.py`
- `tests/test_cognitive_instance.py`

## 3. Implemented Lifecycle

The runtime represents the specified processing states, including:

- created
- envelope_ready
- interaction_identified
- curiosity_active
- context_evaluation
- processing
- routing
- delegated_processing
- reentry_validation
- evidence_evaluation
- proposal_ready
- null_ready
- consolidation_ready
- handed_to_cca
- closed
- clarification_required
- blocked
- terminated
- delegation_failed

Invalid lifecycle transitions are rejected.

## 4. Cognitive Instance / ICG Boundary

The runtime contains an interaction-scoped ICG workspace with:

- persistent references
- candidates
- evidence
- interpretations
- context
- activations
- temporary relationships

Persistent references remain references; they are not owned copies of PCG objects.

Candidates and proposals remain interaction-scoped.

## 5. Curiosity

A new instance can activate Curiosity as the first cognitive dimension.

Curiosity activation is represented as temporary instance state and does not create persistent knowledge.

## 6. Frontier Output Boundary

Frontier responses can be recorded in the instance's temporary history.

Recording a frontier response does not:

- create a belief;
- create persistent PCG state;
- create CSTR;
- authorize a proposal.

The output must still pass through subsequent GRI processing.

## 7. Consolidation Boundary

The runtime requires:

```
PROPOSAL_READY OR NULL_READY
-> CONSOLIDATION_READY
-> HANDED_TO_CCA
```

CCA cannot receive an instance before consolidation readiness.

Handoff does not imply Governance approval.

## 8. Persistent-State Ownership

The Cognitive Instance has no persistent-state writer.

The existing boundary remains:

```
Proposal
-> Governance
-> Cognitive Kernel
-> Persistent State
```

CSTR remains the authoritative transition history.

## 9. No-Guessing Invariants

The runtime preserves:

- unknown information remains uncertainty;
- frontier output is not automatically cognition;
- persistent references are not candidate ownership;
- candidate is not commitment;
- lifecycle state is not truth;
- null is distinct from processing failure.

## 10. Scope Deliberately Deferred

This change does not implement:

- PCG relevance retrieval algorithms;
- requirement decomposition engine;
- internal cognition sufficiency engine;
- routing policy;
- frontier provider integration;
- CCA consolidation engine;
- identity resolution;
- salience mathematics;
- persistent graph storage.

Those remain separate architectural components and should be implemented against this lifecycle boundary.

## 11. Verification

The new runtime has dedicated tests covering:

- distinct instance identity;
- canonical lifecycle;
- valid null outcome;
- unknown handling;
- frontier-output non-persistence;
- persistent-reference separation;
- invalid transitions;
- CCA readiness enforcement;
- closed-instance protection.

The complete repository suite must be executed after pulling this change before declaring the new baseline.

## 12. Conclusion

Change 0037 converts the Cognitive Instance from architecture specification into an executable bounded orchestration primitive without expanding its authority into persistent cognition.
