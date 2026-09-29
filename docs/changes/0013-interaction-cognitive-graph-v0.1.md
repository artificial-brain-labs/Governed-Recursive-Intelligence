# Change 0013 — Interaction Cognitive Graph Model v0.1

Status: Implemented on feature branch
Date: 2026-09-28

## Summary

Formalizes the Interaction Cognitive Graph (ICG) as the temporary cognitive workspace created for each interaction.

## Decisions

- ICG is temporary and interaction-scoped.
- ICG is not PCG and cannot directly mutate PCG.
- Existing PCG objects are referenced rather than owned by ICG.
- Candidate identities, concepts, beliefs, relationships, dimension updates, and goal effects have no persistent authority.
- Curiosity activates first for every new interaction.
- Activation and salience describe participation and priority, not truth.
- Evidence is first-class and remains distinct from interpretation.
- Candidate cognition becomes a proposal before entering consolidation/governance.
- The only persistent commitment path remains ICG -> CCA -> Governance -> Cognitive Kernel -> PCG.
- CSTR remains the historical record of evaluated transitions.
- Missing information must not be silently inferred.

## Invariants Added

Reference is not identity.

Candidate is not persistent cognition.

Activation is not truth.

Curiosity is not knowledge.

Graph expansion is not persistence.

ICG disposal cannot erase committed cognition.

## Deferred Work

No JSON schema, graph database schema, activation equation, salience algorithm, identity-resolution algorithm, candidate-merging algorithm, or concurrency model is fixed by this change.
