# Change Record 0010 — Persistent Cognitive Graph Ontology v0.1

**Date:** 2026-09-28  
**Area:** GRI persistent cognition  
**Status:** Proposed / documented  
**Branch:** feature/crp-v0.1

## Context

GRI now has:

- a cognitive state-transition model
- CSTR transition history
- governed transition execution
- persistent state storage
- a unified cognitive-dimension model

The next required architectural step was to define what the Persistent
Cognitive Graph actually contains before storage technology is expanded.

## Decision

Define PCG as the ontology of **current persistent cognition**, independent of
database technology.

PCG consists conceptually of:

PCG = (Objects, Dimensions, Relationships)

### Persistent Cognitive Objects

Initial canonical object categories:

- identity
- concept
- belief
- goal
- relationship
- cognitive dimension

Not every object is a dimension.

### Cognitive Dimensions

Dimensions use:

D = (value, weight, state, constraints, relationships, learning_rate)

Trust is a normal cognitive-dimension instance, not a special subsystem.

### Relationships

Relationships are first-class cognitive structures rather than anonymous
database edges.

They identify source, target, relationship type, direction, semantics, and
applicable constraints.

Relationship influence is not automatic mutation.

Cross-dimension influence must pass through proposal, governance, and kernel
execution.

## Key Boundaries

PCG:
What persistent cognition exists now?

CSTR:
What governed transition produced or preserved that cognition?

TCM:
What recent communication or experience occurred?

These remain separate.

## Belief Boundary

A concept is not a belief.

An inference is not a belief.

A belief is committed persistent cognition resulting from evidence, evaluation,
governance, and transition execution.

## Learning Boundary

Current learning state required for future cognition may be represented in PCG.

Historical learning events remain in CSTR/H_t.

## No-Guessing Boundary

The ontology does not permit:

- interpretation -> automatic belief
- inference -> automatic fact
- relationship impact -> automatic target mutation
- TCM content -> automatic PCG persistence

## Architectural Consequence

The storage implementation must now be treated as an implementation of the PCG
ontology rather than a source of its definition.

Database selection, graph representation, indexing, identity resolution, belief
revision, contradiction handling, and exact object schemas remain open research
questions.

## Next Research Direction

The next work should formalize the **canonical PCG object model** and the
minimum invariants for identities, concepts, beliefs, goals, relationships, and
dimension instances before implementing graph-specific persistence.
