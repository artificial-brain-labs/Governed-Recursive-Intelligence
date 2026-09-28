# Change 0039 — PCG Relevance Retrieval Runtime v0.1

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## Summary

Change 0039 introduces the first executable reference implementation of the Persistent Cognition Relevance Retrieval Model (PCRRM) specified by `PERSISTENT_COGNITION_RELEVANCE_RETRIEVAL_MODEL_v0.1.md`.

The implementation is deliberately bounded and read-only.

## Added

- `retrieval/retriever.py`
- `retrieval/__init__.py`
- `tests/test_pcrrm.py`

## Implemented Semantics

The runtime supports:

- explicit retrieval seeds;
- direct PCG retrieval;
- bounded relationship expansion;
- retrieval provenance;
- unresolved retrieval candidates;
- access-restricted results;
- explicit retrieval-status distinctions;
- immutable/read-only retrieval over `CognitiveState`.

The implementation does not use embeddings, similarity scoring, or inferred identity resolution as authoritative retrieval rules.

## Status Distinctions

The runtime preserves:

- complete;
- partial;
- no_relevant_cognition_found;
- ambiguous;
- retrieval_failure;
- access_restricted.

In particular:

```
No Relevant Cognition Found != Retrieval Failure
Retrieval Failure != Unknown
```

## Authority Boundaries

PCRRM does not:

- mutate PCG;
- establish truth;
- evaluate sufficiency;
- authorize frontier delegation;
- create identities;
- create relationships;
- create beliefs or proposals.

Its output is temporary retrieval context for the Cognitive Instance.

## Current Scope

The implementation maps onto the current executable `CognitiveState` representation while preserving the ontology's separation between current persistent cognition and retrieval processing.

The following remain intentionally deferred:

- full requirement decomposition;
- learned relevance ranking;
- semantic similarity as a candidate-generation mechanism;
- multi-hop controlled expansion beyond the initial bounded implementation;
- temporal adequacy evaluation;
- goal/dimension relevance algorithms;
- advanced evidence/provenance indexing;
- production graph storage;
- concurrency and snapshot semantics;
- full Cognitive Instance integration;
- ICSM integration.

## No-Guessing Properties Tested

The test suite verifies:

1. direct retrieval does not mutate state;
2. relationship expansion follows established relationships;
3. missing seeds do not invent identities;
4. absence of a seed is not classified as retrieval failure;
5. retrieval does not claim sufficiency or truth;
6. restricted cognition is not exposed;
7. similarity is not treated as the retrieval authority.

## Architectural Position

The intended dependency chain is now:

```
Cognitive Instance
-> Requirement Context
-> PCRRM
-> Relevant Persistent Cognition
-> ICSM
-> Gap Identification
-> Routing
```

The next dependency is Internal Cognition Sufficiency Model (ICSM).
