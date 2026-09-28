# CRP v0.1

The Cognitive Representation Protocol (CRP) is the structured representation
layer between foundation-model interpretation and the GRI cognitive kernel.

## Architectural boundary

Foundation Model → CRP Candidate → Structural Validation → Semantic Validation
→ Governance → Cognitive Kernel → Persistent Cognitive Graph

CRP is a representation protocol, not a reasoning engine and not a truth oracle.

## Core distinctions

- Observation: explicit information available to the system.
- Interpretation: structured semantic representation.
- Inference: non-explicit hypothesis grounded in evidence.
- Uncertainty: unknown or ambiguous information.
- Cognitive update: proposed change to persistent cognition.
- Governance: authorization state.
- Provenance: traceability back to the source interaction.

## No-guessing rule

Missing information must not silently become an observation or confirmed belief.

Evidence used by an inference must itself be represented explicitly. For
example, if the word "again" is used as evidence for a recurrence hypothesis,
the linguistic observation must be represented as a fact before the inference
can reference it.

## Validation layers

CRP uses two gates:

1. **Structural validation** — JSON Schema Draft 2020-12.
2. **Semantic validation** — deterministic cross-field integrity rules.

See SEMANTIC_VALIDATION.md for the current semantic rules.

A CRP candidate that fails either validation layer must not be written directly
to the Persistent Cognitive Graph.

## v0.1 scope

v0.1 defines the Cognitive Event envelope, core objects, and semantic
integrity validation. Belief decay, richer dimension ontology, temporal state
transitions, goal conflict resolution, and full semantic governance remain
future work.
