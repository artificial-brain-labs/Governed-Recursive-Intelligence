# Change 0015 — Cognitive Instance Lifecycle v0.1

**Status:** Implemented on feature branch  
**Date:** 2026-09-28

## Summary

Formalizes the **GRI Cognitive Instance** as the bounded orchestration unit for processing an interaction from normalized communication through cognitive evaluation and consolidation handoff.

The Cognitive Instance is now explicitly positioned between the Interaction Communication & Routing Layer (ICRL) and the Cognitive Consolidation Architecture (CCA).

## Decisions

- Every new interaction creates a bounded cognitive-processing context.
- Interaction ID and Cognitive Instance ID are distinct concepts.
- Curiosity is the first cognitive dimension activated for a new interaction.
- Curiosity has the highest initial dimension weight under the current architecture.
- Curiosity may activate related dimensions through relationships.
- PCG retrieval is demand-driven rather than full-graph loading.
- The Cognitive Instance owns the temporary interaction orchestration context and ICG.
- Frontier models are delegated processors, not persistent-state owners.
- Frontier outputs must re-enter GRI before influencing persistent cognition.
- Multiple frontier calls may occur within one Cognitive Instance.
- The Cognitive Instance may terminate with an explicit null cognitive outcome.
- Processing completion is defined by a consolidation-readiness boundary rather than by message receipt.
- The Cognitive Instance hands control to CCA only at consolidation readiness.
- The Cognitive Instance cannot directly mutate PCG.
- Persistent mutation remains restricted to Governance + Cognitive Kernel.
- Processing failure must remain distinct from a valid null cognitive outcome.
- Unknown and missing information must remain explicit rather than being silently inferred.

## Architectural Position

The canonical lifecycle is:

External Environment
-> Communication Reception
-> GRI Communication Envelope
-> Interaction Identification
-> Cognitive Instance
-> Curiosity
-> PCG Retrieval / ICG
-> Cognitive Routing
-> GRI-native / Frontier / Hybrid
-> Frontier Output Re-entry
-> Evidence Evaluation
-> Proposal or Explicit Null
-> CCA
-> Governance
-> Cognitive Kernel
-> PCG + CSTR

## Files Added

- docs/COGNITIVE_INSTANCE_LIFECYCLE_v0.1.md
- docs/changes/0015-cognitive-instance-lifecycle-v0.1.md
