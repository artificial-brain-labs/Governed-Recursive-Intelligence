# Change 0029 — Persistence and Execution Contract Hardening v0.1

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## 1. Purpose

Change 0029 closes the remaining implementation/documentation mismatches identified while continuing the Change 0028 execution-alignment work.

## 2. Changes

### 2.1 JSONL null-transition durability fix

The file-backed state store previously appended an escaped newline sequence when recording null transitions. This was corrected to append an actual newline so each transition remains a separate valid JSONL record.

### 2.2 Durable execution state freshness

The durable pipeline now verifies that the caller-supplied state matches the store's current `state_id` and `state_version` before running Governance and Kernel.

This prevents Governance from evaluating a stale in-memory state and then attempting to persist against a different store state.

The store retains its own optimistic version check at commit time.

### 2.3 Specification alignment

The Cognitive State Transition Execution Model now explicitly documents:
- state-bound authorization,
- durable-pipeline freshness validation,
- the current JSONL persistence behavior,
- the distinction between the reference file-backed store and a future transactional storage implementation.

The Governance Decision & Authorization Model now explicitly documents the executable authorization shape and state binding.

## 3. Invariants Reinforced

1. Governance evaluates the actual predecessor state intended for execution.
2. Authorization is bound to proposal and predecessor state.
3. A stale caller state cannot silently enter the durable execution route.
4. Null transitions remain durably traceable.
5. Persistence format must preserve record boundaries.
6. File-backed durability is not represented as equivalent to full transactional storage.

## 4. Verification

Source-level verification was performed by fetching the updated repository files after commit.

The full repository test suite was not executed in this environment because the environment cannot clone/access GitHub over the network. No full-test-pass claim is made.

## 5. Remaining Open Work

The following remain intentionally open:
- fully transactional state+CSTR atomicity,
- advanced concurrency,
- multi-target atomic transitions,
- production database/graph persistence,
- exact cognitive reinforcement/weakening mathematics,
- machine-readable constitutional policy execution,
- final end-to-end test execution when repository access is available.

## 6. Architectural Conclusion

Change 0029 does not alter GRI's cognitive theory. It hardens the execution/persistence boundary and keeps the implementation explicitly aligned with the existing governance-native architecture.
