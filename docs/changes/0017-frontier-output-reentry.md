# Change 0017 — Frontier Output Re-enters the Same GRI Process

**Status:** Implemented on feature branch  
**Date:** 2026-09-28

## Summary

Formalizes the rule that every output received from a frontier model is treated as new information entering GRI and is processed through the same cognitive process as other incoming information.

## Decision

A frontier response follows:

Frontier Model
-> Frontier Response Envelope
-> New Information Re-entry
-> Curiosity / Context Evaluation
-> Relevant PCG Retrieval
-> Internal Cognition Sufficiency Evaluation
-> Interpretation / Evidence Classification
-> ICG
-> Routing if Required
-> Proposal / Explicit Null

## Core Rule

> Frontier output is new information to GRI, not automatically accepted cognition.

The fact that GRI requested a frontier response does not increase the truth status of that response.

## Consequences

A returned frontier response may be:

- already known;
- useful information;
- ambiguous;
- conflicting with existing cognition;
- insufficiently evidenced;
- a trigger for additional internal retrieval;
- a trigger for another frontier call;
- a clarification requirement;
- input to a cognitive proposal;
- or produce no persistent cognitive consequence.

## Boundary

Frontier Model -> New Information -> Same GRI Process -> Governed Cognitive Consequence if justified

## Files Updated

- docs/COGNITIVE_INSTANCE_LIFECYCLE_v0.1.md

## Files Added

- docs/changes/0017-frontier-output-reentry.md
