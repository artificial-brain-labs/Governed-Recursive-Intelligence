# Change Record 0004 — Cognitive Kernel v0.1

**Date:** 2026-09-28  
**Area:** GRI cognitive architecture / execution  
**Status:** Proposed / documented  
**Branch:** feature/crp-v0.1

## Context

The GRI architecture now defines the Cognitive State Transition Model, CSTR, and CRP v0.2.

The next missing architectural boundary is the executable mechanism that applies an authorized proposal to persistent cognitive state.

## Decision

Introduce a minimal Cognitive Kernel v0.1.

The kernel is the only component permitted to commit persistent state changes in the initial implementation.

It consumes:

- current cognitive state
- proposal
- evidence references
- governance authorization
- interaction/provenance context

It produces:

- successor state
- CSTR

or:

- unchanged state
- null-transition CSTR

## Implementation Boundary

The kernel intentionally does not define the final PCG ontology.

Its initial state container exposes generic stores for:

- PCG
- dimensions
- goals
- relationships
- learning
- history

This allows transition execution to be tested before the full persistent cognitive ontology is finalized.

## Key Invariants

- no commit without approved governance
- no commit without evidence
- predecessor state is immutable
- proposal is distinct from commitment
- every evaluated transition produces a traceable CSTR
- null transition is a valid result

## Consequence

GRI now has an executable boundary for the state-transition function without prematurely freezing belief mathematics, relationship mathematics, goal conflict resolution, or PCG graph semantics.

The next implementation work should exercise the kernel with controlled transition scenarios and then connect governance as a distinct component.
