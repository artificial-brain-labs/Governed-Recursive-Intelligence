# Change 0035 — Execution Evidence Binding

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## 1. Finding

The first end-to-end adversarial run exposed a subtle evidence-boundary defect.

The proposal contained evidence references, but the execution call supplied `evidence_ids=[]`. The pipeline copied the proposal's existing evidence field into the Governance input because it used `setdefault()`.

As a result, `require_evidence` approved the proposal even though no evidence had been supplied to that execution attempt.

## 2. Change

The governed pipeline now explicitly overwrites the Governance input's evidence field with the execution-supplied `evidence_ids`.

Therefore:

```
Proposal Evidence Metadata != Execution Evidence
```

and Governance can authorize only against evidence actually presented at the execution boundary.

## 3. Architectural Principle Reinforced

This restores the intended invariant:

```
Evidence Before Commitment
```

and:

```
No Evidence -> No Authorized Cognitive Change
```

A proposal cannot self-authorize merely by carrying evidence references in its own metadata.

## 4. Scope

No changes were made to:

- Governance decision semantics
- Cognitive Kernel execution semantics
- PCG ontology
- CSTR model
- CRP schema

The change is confined to the pipeline's construction of the Governance evaluation context.

## 5. Verification

Before this fix, the new end-to-end suite reported:

**51 passed, 1 failed**

The remaining failure was:

`test_no_evidence_cannot_commit`

because Governance incorrectly received the proposal's embedded evidence references.

A full-suite run is required after pulling this change.
