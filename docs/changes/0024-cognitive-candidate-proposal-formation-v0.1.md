# Change Record 0024 — Cognitive Candidate & Proposal Formation Model v0.1

**Date:** 2026-09-28
**Branch:** feature/crp-v0.1
**Status:** Proposed / documented

## 1. Decision

Introduce the Cognitive Candidate & Proposal Formation Model (CCPFM) v0.1 as the explicit architectural boundary between evaluated evidence and a request for persistent cognitive change.

## 2. Core Decision

GRI must distinguish:

Candidate != Proposal != Commitment

The canonical path is:

Evidence -> Candidate -> Proposal -> Governance -> Cognitive Kernel -> PCG

## 3. Why This Change Is Required

The architecture now has explicit interpretation and evidence layers.

A missing boundary remained between:

“What does the evidence suggest GRI should consider?”

and:

“What persistent cognitive change should be requested for authorization?”

Without this layer, evidence could silently become a state-change instruction.

## 4. Candidate

A candidate is temporary interaction-scoped cognition representing a possible persistent consequence.

It may concern:
- belief;
- concept;
- relationship;
- goal;
- cognitive dimension;
- identity;
- learning state;
- reconciliation.

A candidate can remain unresolved, conflicted, redundant, or be discarded without producing a proposal.

## 5. Proposal

A proposal is a structurally complete request for possible persistent cognitive transition.

It identifies:
- target;
- operation;
- evidence;
- rationale;
- predecessor context;
- provenance;
- unresolved conditions where relevant.

Proposal formation does not authorize execution.

## 6. Reconciliation

Candidate formation must consider relevant existing PCG cognition.

Possible outcomes include:
- genuinely new;
- modify existing;
- reinforce;
- weaken;
- redundant;
- contradictory;
- unresolved.

Retrieval failure must not be interpreted as target absence.

## 7. Conflict

Multiple candidates may coexist.

GRI must not silently select one candidate merely because it is convenient.

Identity ambiguity, competing relationships, and competing dimension changes remain explicit until appropriately resolved.

## 8. Persistent Boundary

CCPFM introduces no direct persistence route.

The persistent boundary remains:

Proposal -> Governance -> Cognitive Kernel -> PCG

CSTR records the resulting committed or null transition.

## 9. Frontier Integration

Frontier output remains new information:

Frontier Output
-> Interpretation
-> Evidence Evaluation
-> Candidate Re-evaluation
-> Proposal / No Change

The frontier model does not receive proposal or persistence authority.

## 10. No-Guessing Impact

CCPFM reinforces:
- candidate is not evidence;
- candidate is not truth;
- proposal is not commitment;
- unresolved target remains unresolved;
- candidate conflict remains explicit;
- no-change is valid;
- retrieval failure is not absence;
- candidate/proposal formation does not mutate PCG.

## 11. Consequences

Positive:
- prevents evidence-to-state shortcuts;
- makes cognitive change candidates explicit;
- supports competing hypotheses/candidates;
- provides a clean interface to Governance;
- improves traceability through CSTR.

Tradeoffs:
- candidate ontology must be formalized further;
- proposal semantics require target-specific rules;
- conflict and merging require future design;
- candidate support should not be prematurely reduced to a single confidence number.

## 12. Open Questions

Formal candidate ontology, proposal schema, scoring/support semantics, identity resolution, relationship reconciliation, belief thresholds, reinforcement equations, conflict resolution, proposal merging, concurrency, recursive proposal generation, retention, and cryptographic provenance remain open.

## 13. Repository Principle

This change is architectural documentation only.

No production candidate/proposal engine is claimed to exist.

Future implementation must preserve the separation:

Evidence -> Candidate -> Proposal -> Governance -> Kernel -> Persistent Cognition.
