# Change 0021 — Cognitive Requirement Identification & Decomposition Model v0.1

**Status:** Implemented on feature branch  
**Date:** 2026-09-28

## Summary

Formalizes the Cognitive Requirement Identification & Decomposition Model (CRIDM) as the temporary semantic layer that establishes what the current interaction requires before PCG relevance retrieval.

## Decisions

- Requirement identification precedes PCG relevance retrieval.
- A requirement is distinct from user intent, interpretation, cognition, and truth.
- Explicit, context-derived, inferred, and unresolved requirement elements remain distinguishable.
- Ambiguity is a first-class state and must not be silently resolved by assumption.
- Complex interactions may be decomposed into dependent sub-requirements.
- Requirement completeness is stage-dependent.
- Temporal, evidence, output, constraint, and capability requirements may be represented explicitly.
- Requirement identification is non-mutating.
- Requirement representation does not authorize actions or persistent cognitive change.
- Frontier output re-enters requirement evaluation and may revise the requirement when justified.
- Multiple requirements may progress independently where dependencies permit.

## Architectural Principle

> Before GRI asks “What do I know?”, it must establish “What am I being asked to determine or accomplish?”

## Files Added

- docs/COGNITIVE_REQUIREMENT_IDENTIFICATION_DECOMPOSITION_v0.1.md
- docs/changes/0021-cognitive-requirement-identification-decomposition-v0.1.md
