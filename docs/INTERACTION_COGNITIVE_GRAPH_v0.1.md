# GRI Interaction Cognitive Graph Model v0.1

Status: Foundational architecture specification
Version: 0.1

## Purpose

The Interaction Cognitive Graph (ICG) is the temporary cognitive workspace created for one interaction. It is distinct from TCM, PCG, CCA, and CSTR.

TCM records temporary communication and experience. ICG represents structures participating in the current interaction. CCA evaluates consolidation. PCG stores persistent cognition. CSTR records transition history.

## Core Model

ICG_i = (nodes, relationships, activations, evidence, candidates, context)

Each interaction receives a distinct cognitive-processing instance operating over the preceding persistent state:

PCG_(i-1) -> Cognitive Instance_i -> ICG_i -> CCA -> Governance -> Kernel -> PCG_i

The ICG is not an independent intelligence and cannot directly mutate PCG.

## Node Classes

1. Persistent Reference Node — reference to an existing PCG object and state version.
2. Candidate Node — temporary cognitive structure without persistent authority.
3. Evidence Node — explicit evidence with source and provenance.
4. Interpretation Node — cognitive interpretation, distinct from observation and evidence.
5. Context Node — interaction-specific context such as goals, task context, uncertainty, or salience context.

## Candidate Dimensions

An ICG may reference an existing dimension, activate it for the interaction, and construct a candidate update. A candidate update is not a persistent dimension version.

Persistent Dimension -> ICG Reference -> Candidate Update -> Proposal -> Governance -> Possible Persistent Update

## Relationships

Temporary ICG relationships may represent observed association, interpreted association, candidate relationship, influence candidate, evidence support, relevance, activation dependency, goal relevance, or reasoning dependency.

A temporary relationship does not automatically become a PCG relationship.

Relationship influence never directly mutates its target.

## Activation and Salience

Activation describes participation in the current interaction. Salience describes processing priority. Neither establishes truth.

Activation may contain active state, salience, reason, and source.

## Curiosity

Every new interaction begins with Curiosity activation.

Curiosity identifies unknowns, seeks clarification, explores relevant information, examines relationships, and tests whether evidence is sufficient.

Unknown -> Curiosity -> Investigation

not Unknown -> Curiosity -> Assumed Fact.

Curiosity cannot manufacture external-world facts.

## Evidence and Candidates

Evidence remains distinct from interpretation. Candidates remain distinct from persistent cognition.

Candidate -> Proposal -> Governance -> Cognitive Kernel -> PCG

The ICG never bypasses Governance or the Kernel.

## Persistent Reference and Identity

A reference appearing in an interaction is not automatically an established persistent identity. Ambiguous identity resolution remains unresolved or requires clarification/review.

## Working Graph

The ICG is not a copy of the entire PCG. Relevant persistent structures are referenced or activated as needed. The graph may expand when additional relevant structures are identified, but graph expansion does not imply persistence.

Temporary nodes may be consolidated, discarded, unresolved, or retained only as explicitly governed historical references.

## No-Guessing Invariants

1. Observation != Interpretation.
2. Interpretation != Evidence.
3. Evidence != Belief.
4. Candidate != Persistent Object.
5. Salience != Truth.
6. Curiosity != Knowledge.
7. Proposal != Commitment.
8. Reference != Identity.
9. Relationship Influence != Target Mutation.
10. Unknown remains unknown.
11. Missing information is not silently inferred.

## Lifecycle

created -> curiosity_active -> processing -> proposal_ready -> consolidating -> closed/discarded

Lifecycle state describes processing status, not truth or persistence.

## Closure

When the interaction closes, committed consequences remain in PCG and transition history remains in CSTR. Temporary ICG state may be discarded. Discarding ICG cannot erase committed cognition.

## Technology Boundary

This document defines semantic architecture, not JSON serialization or database technology. Storage decisions must follow the cognitive model.

## Open Questions

Exact ICG serialization, activation mathematics, salience function, graph expansion limits, candidate deduplication, identity resolution, candidate conflict resolution, proposal grouping, concurrent interaction isolation, retention/security policy, recursive-reflection retention, and storage technology remain open.

## Architectural Principle

The interaction graph may explore and construct candidate cognition, but only governed transition execution can make cognition persistent.
