# Change Record 0011 — Interaction-Scoped Curiosity and Cognitive Graph Instances

**Date:** 2026-09-28  
**Area:** GRI interaction architecture  
**Status:** Proposed / documented  
**Branch:** feature/crp-v0.1

## Decision

Every new conversation creates a new interaction context and activates the
Curiosity cognitive dimension as the initial cognitive orientation.

The intended initial lifecycle is:

New Conversation
-> Interaction Instance
-> Curiosity Activation
-> Perception / Interpretation
-> Salience
-> Relevant Dimensions
-> Evidence / Proposal
-> Governance
-> Cognitive Transition

Curiosity is therefore a first-stage cognitive dimension rather than an
optional late-stage feature.

Curiosity must not convert unknown information into assumed facts. Its role is
to identify what should be explored, clarified, examined, or understood.

## Interaction-Scoped Cognitive Instance

Each interaction receives a distinct cognitive-processing instance.

The instance operates over persistent cognition and interaction-specific
context. It is not an isolated intelligence and does not replace the
persistent PCG.

Conceptually:

Persistent PCG_(n-1)
-> Cognitive Instance_n
-> governed transition
-> Persistent PCG_n

The interaction instance may contain its own active dimensions, relevant
objects, relationship paths, reasoning context, and candidate changes.

## Interaction PCG Graph

Each interaction may create a processing graph instance containing the
cognitive structures relevant to that interaction.

This graph instance is analogous to neuroplasticity at the architectural level:
interaction can activate, strengthen, weaken, connect, or propose new cognitive
structures.

The analogy does not claim biological equivalence.

Only governed consequences are consolidated into persistent PCG.

## Curiosity and Human-Like Decision Formation

"Curiosity must decide like a human" is defined as a research requirement for
contextual, goal-aware, relationship-aware, and governed exploration.

Curiosity can contribute decisions about:

- what is unknown
- what is worth investigating
- what clarification is needed
- what information may reduce uncertainty
- what experience may be valuable for learning

It cannot invent missing facts.

## Architectural Consequence

The PCG architecture now has two related scopes:

1. **Interaction-scoped cognitive graph instance** — temporary working cognitive
   structure for the current interaction.
2. **Persistent PCG** — governed cognitive consequences consolidated across
   interactions.

TCM remains the transient communication layer, while the interaction graph is
the cognitive working structure for that interaction.

The exact lifecycle, memory boundaries, graph merge/consolidation rules, and
curiosity decision algorithm remain open for subsequent formalization.
