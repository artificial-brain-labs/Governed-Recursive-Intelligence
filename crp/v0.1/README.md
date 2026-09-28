# CRP v0.1

The Cognitive Representation Protocol (CRP) is the structured representation layer between foundation-model interpretation and the GRI cognitive kernel.

## Architectural boundary

Foundation Model -> CRP Candidate -> Validation -> Cognitive Kernel -> Governance -> Persistent Cognitive Graph

CRP is a representation protocol, not a reasoning engine and not a truth oracle.

## Core distinctions

- Observation: explicit information available to the system.
- Interpretation: structured semantic representation.
- Inference: non-explicit hypothesis.
- Uncertainty: unknown or ambiguous information.
- Cognitive update: proposed change to persistent cognition.
- Governance: authorization state.
- Provenance: traceability back to the source interaction.

## No-guessing rule

Missing information must not silently become an observation or confirmed belief.

## v0.1 scope

v0.1 defines the Cognitive Event envelope and core objects only. Belief decay, richer dimension ontology, temporal state transitions, goal conflict resolution, and full semantic governance are future work.
