# Change 0028 — Governed Execution and Persistence Alignment v0.1

**Status:** Implemented on branch `feature/crp-v0.1`

## Purpose

Align the reference implementation with the Cognitive State Transition Execution Model v0.1 and establish one explicit durable execution boundary.

## Changes

### 1. State-bound GovernanceDecision

Governance decisions now carry decision_id, proposal_id, state_id, state_version, status, governance version, reason, and constraint evaluations. The Kernel verifies that authorization corresponds to both the proposal and actual predecessor state.

### 2. Kernel execution gates

The Kernel now explicitly rejects/null-transitions for missing authorization, non-approved authorization, proposal/authorization mismatch, predecessor state mismatch, stale authorization, missing evidence, unsupported target/operation, and invalid target preconditions. No stale proposal is silently rebased.

### 3. Explicit no_change

`no_change` is now part of the executable operation vocabulary. It produces unchanged state, a CSTR, `outcome = null`, and `execution_status = explicit_no_change`. This remains distinct from execution failure.

### 4. Execution status

CSTR preserves the architectural distinction between the two transition outcomes (`committed`, `null`) and the reason/status explaining the result.

### 5. Persistence boundary

`execute_and_persist_transition()` provides the single reference path: Governance -> Kernel -> Persistence. Committed transitions use `commit_transition()`. Null transitions use `record_transition()`. Persistence remains downstream of the Kernel and does not create an alternate mutation path.

### 6. Tests

Added coverage for state-bound authorization, stale authorization, authorization/proposal mismatch, explicit no_change, durable committed transition, and durable null transition.

## Remaining limitations

This change does not claim production-grade transactional durability, distributed concurrency, multi-target atomicity, or final cognitive update mathematics. Those remain explicitly open.

## Architectural decision

The Kernel is now the execution authority for an exact, state-bound authorization, and persistence records exactly the result produced by that execution boundary.
