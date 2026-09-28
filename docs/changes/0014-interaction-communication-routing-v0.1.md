# Change 0014 — Interaction Communication and Routing Layer v0.1

**Status:** Implemented on feature branch  
**Date:** 2026-09-28

## Summary

Introduces the GRI Interaction Communication & Routing Layer (ICRL) as the architectural boundary between external communication, GRI cognition, and third-party frontier-model delegation.

## Decisions

- Normalize every external interaction into a structured communication envelope before cognitive interpretation.
- Treat JSON as serialization, not as cognition.
- Keep communication protocol distinct from CRP, which remains a cognitive representation protocol.
- Create the interaction-scoped cognitive instance after interaction identification.
- Activate Curiosity first.
- Use demand-driven PCG retrieval rather than loading the complete persistent graph.
- Permit GRI-native, frontier-delegated, hybrid, clarification-required, and blocked routing outcomes.
- Send only authorized relevant context to frontier models.
- Treat frontier output as external model output that must re-enter GRI validation.
- Never allow a frontier model to write PCG directly.
- Allow multiple frontier calls within one interaction instance.
- Hand control from the interaction instance to CCA at explicit consolidation readiness.
- Permit explicit null consolidation when no persistent cognitive consequence is justified.

## Evidence Position

Model routing and semantic routing are established mechanisms. MCP establishes standardized model/context/tool communication. The GRI-specific combination of persistent cognitive ownership, selective delegation, output re-entry, and governed consolidation is documented as an architectural hypothesis to be validated rather than asserted as wholly unprecedented.

## Files Added

- docs/GRI_INTERACTION_COMMUNICATION_ROUTING_v0.1.md
- docs/changes/0014-interaction-communication-routing-v0.1.md
