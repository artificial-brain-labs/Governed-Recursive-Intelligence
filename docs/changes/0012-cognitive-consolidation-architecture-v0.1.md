# Change 0012 — Cognitive Consolidation Architecture v0.1

**Status:** Proposed / implemented on feature branch  
**Date:** 2026-09-28  
**Scope:** GRI cognitive architecture

## 1. Change Summary

This change formalizes the **Cognitive Consolidation Architecture (CCA) v0.1** as the bridge between interaction-scoped cognition and persistent cognition.

The architecture introduces the **Interaction Cognitive Graph (ICG)** as a temporary working graph for each interaction.

The new model is:

`New Conversation
-> New Interaction Instance
-> Curiosity
-> Interaction Cognitive Graph
-> Evidence / Proposal
-> CCA Consolidation Evaluation
-> Governance
-> Cognitive Kernel
-> Persistent PCG`

CSTR remains the authoritative historical record of the evaluated transition.

## 2. Motivation

Previous architecture decisions established:

- TCM for temporary communication
- PCG for persistent cognition
- CSTR for transition history
- governed transition pipeline for commitment
- Curiosity as the first dimension activated by a new conversation
- a distinct cognitive instance for every interaction

A formal consolidation layer was required to define how these pieces relate without allowing temporary interaction cognition to become persistent state automatically.

## 3. Architectural Decisions

### 3.1 Interaction Cognitive Graph

Each interaction may create a temporary ICG containing:

- activated persistent structures
- active dimensions
- relevant relationships
- interaction context
- evidence
- interpretations
- candidate structures
- candidate changes
- reasoning paths
- unresolved questions

The ICG is not the persistent PCG.

### 3.2 Curiosity First

A new conversation begins with Curiosity activation.

Curiosity is an orientation toward exploration, clarification, uncertainty reduction, and potentially valuable learning.

It must not convert unknown information into facts.

### 3.3 Interaction-Scoped Cognitive Instance

Each interaction receives its own cognitive-processing instance operating over persistent cognition.

Conceptually:

`PCG_(n-1) -> Cognitive Instance_n -> governed transition -> PCG_n`

This instance is temporary and contextual.

### 3.4 Consolidation Boundary

CCA determines which interaction-scoped candidates may become explicit cognitive proposals.

CCA does not authorize commitment.

Governance remains the authorization layer.

The Cognitive Kernel remains the only persistent-state execution authority.

### 3.5 Null Consolidation

CCA explicitly supports no-change outcomes.

`PCG_(t+1) = PCG_t`

A processed interaction does not necessarily produce learning.

Where a transition evaluation occurs, CSTR preserves the evaluation and reason for non-commitment.

### 3.6 No-Guessing Preservation

CCA must preserve:

- observation vs interpretation
- evidence vs inference
- candidate vs persistent cognition
- proposal vs commitment
- salience vs truth
- curiosity vs knowledge

No component may silently promote an unknown or inferred item into persistent fact.

## 4. Relationship to Existing Components

| Component | Responsibility |
|---|---|
| TCM | Temporary communication and raw experience context |
| ICG | Temporary interaction-scoped cognitive working graph |
| CCA | Consolidation/reconciliation boundary |
| Governance | Authorization of proposed persistent change |
| Cognitive Kernel | Execution of authorized state transition |
| PCG | Current persistent cognitive state |
| CSTR | Persistent history of transition evaluation |

## 5. Architectural Invariant Added

The following invariant is now explicit:

> An interaction may change cognition, but an interaction does not automatically become persistent cognition.

Only a governed and traceable transition may consolidate interaction consequences into PCG.

## 6. Consequences

This decision provides a formal place for:

- interaction-level cognitive processing
- curiosity activation
- temporary graph formation
- candidate cognition
- PCG reconciliation
- consolidation decisions
- null learning
- transition traceability

It also prevents TCM, interaction working memory, and PCG from collapsing into one undifferentiated memory system.

## 7. Deferred Work

CCA v0.1 does not define:

- exact ICG data structures
- graph database selection
- curiosity equations
- salience algorithms
- evidence thresholds
- identity-resolution algorithms
- PCG merge algorithms
- concurrent interaction handling
- distributed consolidation
- cryptographic transition integrity

These remain explicit research/implementation questions.

## 8. Files Added

- `docs/COGNITIVE_CONSOLIDATION_ARCHITECTURE_v0.1.md`
- `docs/changes/0012-cognitive-consolidation-architecture-v0.1.md`

No existing governance, kernel, storage, CRP, or PCG implementation was changed by this architectural documentation update.
