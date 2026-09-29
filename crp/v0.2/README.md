# CRP v0.2

CRP v0.2 is the structured representation layer derived from the GRI Cognitive
State Transition Model v0.1 and Cognitive State Transition Record v0.1.

## Architectural boundary

Experience → CRP Candidate → Structural Validation → Semantic Validation
→ Cognitive Proposal → Governance → Cognitive Kernel → State Transition → CSTR

CRP is not the Cognitive State Transition Record.

CRP represents the information required to evaluate a possible cognitive
transition. CSTR records the authoritative transition that actually occurred.

## New v0.2 concepts

- state_context — predecessor cognitive state reference.
- evidence — first-class, traceable evidence objects.
- proposal — explicit proposal separated from commitment.
- governance — governance evaluation context.
- transition_reference — reference to a resulting CSTR when one exists.
- richer provenance for interpreter and reasoning components.

## No-guessing

The representation preserves:

Observed != Interpreted != Inferred != Believed

and:

No Evidence -> No Cognitive Commitment

An inference must reference evidence. A proposal must reference evidence.
Evidence does not automatically authorize a persistent change.

## Transition boundary

A CRP candidate may produce:

- no proposal
- a proposal awaiting governance
- a rejected proposal
- a null transition
- a committed transition

A committed transition reference requires approved governance.

The actual state change remains the responsibility of the GRI Cognitive Kernel.

## Validation

CRP v0.2 uses:

1. JSON Schema Draft 2020-12 for structural validation.
2. Deterministic semantic validation for cross-field integrity.

The v0.2 schema is intentionally not a state-delta or PCG schema.
