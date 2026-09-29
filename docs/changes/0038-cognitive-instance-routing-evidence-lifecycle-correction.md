# Change 0038 — Cognitive Instance Routing-to-Evidence Lifecycle Correction

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## Summary

The first execution of the Cognitive Instance runtime exposed a lifecycle-table omission:

```
routing -> evidence_evaluation
```

is a valid architectural path when routing has completed without requiring another processing or frontier-delegation cycle.

The runtime transition table originally omitted this edge, causing the canonical lifecycle test to fail even though the architecture specification explicitly permits processing to reach evidence evaluation after routing.

## Correction

Updated `cognitive_instance/instance.py` so `ROUTING` may transition to:

- `PROCESSING`
- `DELEGATED_PROCESSING`
- `EVIDENCE_EVALUATION`
- `CLARIFICATION_REQUIRED`
- `BLOCKED`

Added a dedicated regression test confirming that routing can proceed directly to evidence evaluation without a frontier call.

## Architectural Interpretation

This correction does not broaden Cognitive Instance authority.

It only makes the executable state machine conform to the previously specified lifecycle:

```
processing
-> routing
-> evidence_evaluation
-> proposal_ready OR null_ready
-> consolidation_ready
```

The existing boundaries remain unchanged:

- routing does not authorize persistent change;
- evidence evaluation does not commit cognition;
- CCA handoff still requires consolidation readiness;
- Governance remains the authorization boundary;
- Cognitive Kernel remains the persistent-state execution boundary.

## Verification

The repository's previous run reported:

```
60 passed, 1 failed
```

with the sole failure caused by this omitted transition.

A fresh full-suite run is required after pulling the correction.
