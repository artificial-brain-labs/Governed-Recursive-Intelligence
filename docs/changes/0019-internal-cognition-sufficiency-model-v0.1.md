# Change 0019 — Internal Cognition Sufficiency Model v0.1

**Status:** Implemented on feature branch  
**Date:** 2026-09-28

## Summary

Formalizes the Internal Cognition Sufficiency Model (ICSM) as the non-mutating evaluation layer between relevant PCG retrieval and Cognitive Routing.

## Decisions

- Sufficiency is always evaluated relative to an explicit interaction requirement.
- Sufficiency is not a truth judgment or certainty guarantee.
- GRI distinguishes sufficient, partially sufficient, insufficient, unknown, ambiguous, retrieval-failure, and conflict states.
- Knowledge gaps and capability gaps are separate architectural conditions.
- PCG absence does not automatically justify frontier delegation.
- Retrieval failure is not evidence of knowledge absence.
- Stale cognition is not automatically false; temporal adequacy is requirement-dependent.
- Conflicting cognition remains explicitly conflicting until an appropriate resolution process acts.
- Internal recovery options are considered before external delegation where applicable.
- ICSM is non-mutating and cannot authorize frontier delegation or persistent cognitive change.
- Frontier responses re-enter the same ICSM process as new information.
- Sufficiency evaluation itself is not learning and does not become persistent cognition.

## Architectural Principle

> GRI does not ask only “Do I have this information?” It asks “Given the current requirement, what relevant cognition do I have, what is established, what is missing, what is unresolved, and what capability is actually required?”

## Files Added

- docs/INTERNAL_COGNITION_SUFFICIENCY_MODEL_v0.1.md
- docs/changes/0019-internal-cognition-sufficiency-model-v0.1.md
