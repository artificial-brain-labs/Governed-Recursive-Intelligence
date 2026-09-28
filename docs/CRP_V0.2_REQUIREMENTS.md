# CRP v0.2 Requirements Derived from CSTR v0.1

**Status:** Foundational representation specification  
**Version:** 0.2  
**Depends on:** GRI Cognitive State Transition Model v0.1 and CSTR v0.1

## 1. Purpose

CRP v0.2 defines the minimum structured representation required to carry an experience through cognitive interpretation and proposal generation toward a governed GRI state transition.

It is derived from the Cognitive State Transition Model and Cognitive State Transition Record.

CRP remains an interface representation.

It is not:

- the GRI cognitive architecture
- the Cognitive Kernel
- the Persistent Cognitive Graph
- the Cognitive State Transition Record
- a reasoning engine
- a truth oracle
- a serialization-specific theory of cognition

## 2. Architectural Position

The v0.2 pipeline is:

Experience
-> CRP Candidate
-> Structural Validation
-> Semantic Validation
-> Cognitive Interpretation
-> Cognitive Proposal
-> Governance
-> Cognitive Kernel
-> State Transition
-> CSTR
-> Persistent Cognitive State

CRP therefore represents information required before and during transition evaluation.

CSTR records the authoritative transition after governance and state-transition execution.

## 3. What Changes from v0.1

CRP v0.1 represented a cognitive event but did not explicitly represent the state-transition context required by CSTR.

CRP v0.2 introduces five architectural concepts:

1. **state_context** — identifies the persistent state against which the experience was interpreted.
2. **evidence** — gives evidence first-class identity and provenance rather than relying only on strings.
3. **proposal** — explicitly separates a proposed cognitive transition from an eventual cognitive update.
4. **governance context** — records evaluation status without treating CRP as the final state-transition authority.
5. **transition_reference** — provides a traceable link to a resulting CSTR when one exists, without embedding the CSTR into CRP.

## 4. State Context

CRP v0.2 must identify the relevant predecessor cognitive state.

Minimum concepts:

- state_id
- state_version

The CRP candidate therefore has an explicit relationship to S_t.

CRP does not contain the complete persistent state by default.

## 5. Observation

Observation remains explicitly separated from interpretation, inference, and belief.

An observation may contain:

- raw input
- explicit or observed facts
- linguistic/structural observations

Unknown information must remain unknown.

An unknown observation cannot contain facts presented as observed.

## 6. Interpretation

Interpretation contains structured semantic candidates.

It may include:

- entities
- events
- relationships
- contextual observations
- hypotheses
- uncertainty

Interpretation is not belief.

## 7. Evidence

Evidence is now a first-class object.

Every evidence item must have:

- evidence_id
- type
- claim
- source reference

Evidence types are deliberately open enough to support future research, but v0.2 distinguishes at least:

- observation
- interpretation
- external_source
- system_state
- historical_transition

Evidence does not itself authorize a cognitive change.

## 8. Inference

Inferences remain hypotheses rather than facts.

Every inference must identify the evidence IDs supporting it.

Therefore:

Inference -> Evidence

and not:

Inference -> Observation by implicit promotion.

## 9. Cognitive Proposal

CRP v0.2 explicitly represents a proposal.

A proposal contains:

- proposal_id
- target type
- target reference
- operation
- evidence references
- rationale
- status

Proposal status describes the lifecycle of the proposal within representation processing.

At minimum:

- proposed
- withdrawn
- superseded

Governance authorization is represented separately.

Proposal != Commitment

## 10. Governance

Governance remains a separate architectural layer.

CRP v0.2 may carry governance evaluation metadata:

- status
- constraints checked
- reason
- governance version

However, a CRP message must not claim persistent commitment merely because a foundation model or interpreter marked something approved.

The Cognitive Kernel remains authoritative for state transition execution.

## 11. Transition Reference

When a proposal results in a state-transition record, CRP may carry a transition reference containing:

- transition_id
- outcome

This is a reference, not the CSTR itself.

The CSTR remains the authoritative historical record.

## 12. Provenance

Provenance must support the causal chain:

interaction
-> interpretation
-> evidence
-> proposal
-> governance
-> transition

The v0.2 representation therefore identifies:

- source interaction
- interpreter
- reasoning component where applicable
- schema version
- originating model/system where applicable

## 13. Semantic Rules

CRP v0.2 must enforce at least:

1. provenance.source_interaction == interaction_id
2. state_context.state_version is required
3. unknown observations cannot contain observed facts
4. every inference basis must reference an evidence_id
5. every evidence item must have a valid source reference
6. every proposal evidence reference must resolve to evidence
7. every proposal target must have a valid target type
8. rejected governance cannot authorize a committed proposal
9. a transition reference must not claim committed outcome when governance is not approved
10. CRP cannot declare persistent state changed without a transition reference
11. interpretation must not be represented as belief merely by field placement
12. unknown information must remain explicitly unknown

## 14. No-Guessing Rule

The v0.2 representation must preserve:

Observed != Interpreted != Inferred != Believed

and:

No Evidence -> No Cognitive Commitment

Evidence does not automatically imply commitment.

The representation must never silently promote an inference into a fact.

## 15. CRP vs CSTR

The distinction is explicit:

**CRP asks:**

> What information, interpretation, evidence, and proposal are being presented for cognitive evaluation?

**CSTR asks:**

> What governed transition actually occurred?

Therefore:

CRP Candidate != CSTR

A CRP candidate may result in:

- committed transition
- null transition
- rejected proposal
- pending review
- no proposal

## 16. What v0.2 Does Not Define

The following remain outside CRP v0.2:

- belief confidence mathematics
- evidence thresholds
- trust equations
- goal conflict resolution
- learning-rate update equations
- PCG graph algorithms
- state-delta encoding standard
- concurrency model
- recursive reflection algorithm
- cryptographic transition signing

These belong to later architecture or experimental work.

## 17. Migration Principle

Existing CRP v0.1 remains valid as a historical protocol version.

CRP v0.2 is not a silent mutation of v0.1.

A v0.1 event must not be interpreted as containing v0.2 state-transition semantics unless explicitly migrated.

## 18. Architectural Sequence

The authoritative sequence remains:

GRI Cognitive Theory
-> Cognitive State Transition Model
-> Cognitive State Transition Record
-> CRP v0.2
-> Cognitive Kernel
-> Experimental Evaluation

CRP v0.2 is therefore derived from architecture rather than defining it.
