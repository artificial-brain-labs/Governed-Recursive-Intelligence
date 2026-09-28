# Change 0020 — Persistent Cognition Relevance Retrieval Model v0.1

**Status:** Implemented on feature branch  
**Date:** 2026-09-28

## Summary

Formalizes the Persistent Cognition Relevance Retrieval Model (PCRRM) as the architectural layer that identifies which PCG structures should participate in an interaction before Internal Cognition Sufficiency Evaluation.

## Decisions

- Retrieval is requirement-relative and demand-driven.
- Retrieval is distinct from sufficiency and truth evaluation.
- Retrieval begins from explicit or established interaction-derived seeds.
- Direct, relational, goal, dimension, evidence, temporal, and contextual relevance are recognized.
- Similarity may discover candidates but does not itself establish cognitive relevance.
- Relationship-aware retrieval is bounded and controlled.
- Retrieval completeness is relative to the current evaluation scope, not the entire PCG.
- No relevant cognition found is distinct from retrieval failure, ambiguity, and access restriction.
- Identity ambiguity must remain explicit.
- Retrieval is non-mutating.
- Retrieved PCG references preserve state/version context and retrieval provenance.
- ICSM consumes retrieval results and may trigger additional controlled retrieval.
- Routing, not retrieval, determines whether frontier delegation is required.
- Relevant but unauthorized cognition must not cross an access boundary.

## Architectural Principle

> GRI should not retrieve everything it knows. It should retrieve what the current cognitive requirement gives it reason to consider—and it must preserve why that cognition was considered relevant.

## Files Added

- docs/PERSISTENT_COGNITION_RELEVANCE_RETRIEVAL_MODEL_v0.1.md
- docs/changes/0020-persistent-cognition-relevance-retrieval-model-v0.1.md
