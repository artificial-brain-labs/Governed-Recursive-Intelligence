# Change 0016 — Internal Cognition Before Frontier Delegation

**Status:** Implemented on feature branch  
**Date:** 2026-09-28

## Summary

Formalizes the requirement that GRI must inspect and evaluate relevant internal persistent cognition before sending information or a task to a frontier model.

## Decision

The canonical routing sequence is:

Interaction -> Curiosity -> Relevant PCG Retrieval -> Internal Cognition Sufficiency Evaluation -> Routing Decision

Only after this internal evaluation may GRI choose frontier delegation.

## Core Rule

> Internal Cognition Before External Delegation: GRI must evaluate relevant internal cognition before delegating to a frontier model and must delegate only when additional external capability or information is justified by the current interaction.

## Important Distinction

Not Found in PCG != Automatically Send to Frontier

An initially missing item may represent:

- information resolvable through additional PCG retrieval;
- retrieval failure;
- unresolved identity or ambiguity;
- genuinely unknown information;
- a requirement for external knowledge;
- a requirement for specialized reasoning or transformation.

These cases must remain distinguishable.

## Architectural Consequence

The frontier model is not the first fallback whenever GRI lacks an immediately available answer. GRI first determines what it already knows, what is missing, whether it can resolve the missing requirement internally, and only then whether external delegation is justified.

## Files Updated

- docs/COGNITIVE_INSTANCE_LIFECYCLE_v0.1.md
- docs/GRI_INTERACTION_COMMUNICATION_ROUTING_v0.1.md

## Files Added

- docs/changes/0016-internal-cognition-before-frontier-delegation.md