# Cognitive State Transition Record (CSTR) v0.1

**Status:** Foundational specification  
**Version:** 0.1  
**Depends on:** GRI Cognitive State Transition Model v0.1  
**Scope:** Conceptual model, independent of JSON, CRP, foundation models, and implementation language

## 1. Purpose

The Cognitive State Transition Record (CSTR) defines the authoritative record of a change, or explicitly non-change, in GRI persistent cognitive state.

The Cognitive State Transition Model defines how cognition may transition. CSTR defines how each evaluated transition is represented as an auditable historical event.

CSTR preserves the distinction between what was experienced, what was interpreted, what evidence was available, what cognitive change was proposed, what governance authorized or rejected, and what state actually changed.

CSTR is therefore a transition-history model, not a reasoning protocol and not a serialization format.

## 2. Core Principle

> A cognitive transition is not complete until the transition itself is traceable.

For every evaluated experience, GRI must be able to answer:

1. What experience caused this evaluation?
2. What persistent state existed before evaluation?
3. What interpretation and evidence were used?
4. What cognitive change was proposed?
5. What governance decision was made?
6. What transition operation was authorized?
7. What persistent state resulted?
8. What evidence and provenance support the transition?
9. If no change occurred, why was the transition null?

## 3. Relationship to the Cognitive State Transition Model

The state-transition model defines:

S_(t+1) = T(S_t, E_t, I_t, X_t, P_t, A_t)

Where:

- S_t = previous persistent cognitive state
- E_t = experience
- I_t = cognitive interpretation
- X_t = evidence
- P_t = cognitive proposal
- A_t = governance authorization
- S_(t+1) = resulting persistent cognitive state

CSTR records the evaluated execution of this transition.

Conceptually:

CSTR_t = Record(S_t, E_t, I_t, X_t, P_t, A_t, S_(t+1))

CSTR therefore sits after transition evaluation but within persistent cognitive history.

## 4. Transition Record vs Cognitive State

A CSTR is not itself persistent cognitive state.

Persistent cognitive state is represented conceptually as:

S_t = (PCG_t, D_t, G_t, R_t, H_t)

Where:

- PCG_t = Persistent Cognitive Graph
- D_t = current cognitive dimension states
- G_t = active goals and goal relationships
- R_t = persistent relationships, trust, and relevance
- H_t = learning and historical transition record

CSTR contributes to the historical component H_t, while actual cognitive consequences are represented in the corresponding PCG, dimension, goal, relationship, or other persistent state.

This distinction is fundamental:

- CSTR: what transition was evaluated and what happened.
- PCG: what persistent cognition now exists because of it.

## 5. Transition Identity

Every transition receives a unique transition_id.

The transition_id identifies the transition record itself.

The originating experience retains its own interaction_id or equivalent experience identifier.

These identifiers must not be conflated.

Conceptually:

interaction_id != transition_id

A single interaction may produce:

- no transition,
- one transition,
- or multiple governed cognitive transitions where the architecture explicitly permits decomposition.

## 6. Required Conceptual Components

A CSTR contains the following logical components.

### 6.1 Transition Identity

Identifies the transition.

Minimum concepts:

- transition identifier
- transition timestamp
- transition sequence or version where required
- originating interaction or experience identifier

### 6.2 Previous State Reference

Identifies the persistent cognitive state from which the transition was evaluated.

The record should reference the relevant state version rather than requiring the complete state to be duplicated in every record.

Conceptually:

StateReference_t -> S_t

### 6.3 Experience Reference

Identifies the experience that triggered evaluation.

Experience may originate from:

- user interaction
- system event
- environment
- agent
- sensor
- external document
- another explicitly permitted source

The record should reference the original experience rather than silently reconstructing it from interpretation.

### 6.4 Interpretation Reference

Identifies the cognitive interpretation used during evaluation.

Interpretation is not observation.

The record must preserve:

Observed != Interpreted

### 6.5 Evidence Set

Identifies the evidence used to support the proposal.

Evidence must be traceable to available observations or explicitly permitted evidence sources.

The CSTR must not convert an inference into an observation merely because the inference was used during reasoning.

### 6.6 Cognitive Proposal

Records the proposed cognitive operation.

A proposal may target:

- belief
- concept
- relationship
- goal
- cognitive dimension
- another explicitly defined persistent cognitive structure

Possible operations include:

- create
- modify
- reinforce
- weaken
- remove

The proposal is not equivalent to an authorized transition.

Proposal != Commitment

### 6.7 Governance Decision

Records the governance outcome applied to the proposal.

At minimum:

- approved
- rejected
- pending
- requires review

Where applicable, the record should preserve:

- local constraints evaluated
- global constitutional constraints evaluated
- authorization rationale
- governance version or policy reference

Governance must precede persistent cognitive commitment.

Proposal -> Governance -> Transition

### 6.8 Transition Outcome

Records what actually happened.

Fundamental outcome categories:

- committed
- null

A committed transition means an authorized change was applied.

A null transition means:

S_(t+1) = S_t

A null transition is a valid architectural outcome and must not be treated as an error.

### 6.9 State Change

For a committed transition, the record must identify the affected persistent state.

Conceptually:

Delta S_t = S_(t+1) - S_t

The implementation may represent this as a structured set of operations rather than mathematical subtraction.

A state change must identify:

- target
- operation
- previous value or state where required
- resulting value or state where required
- evidence reference
- governance authorization

### 6.10 Null Transition Reason

When the transition is null, the record must explain why no persistent cognitive change occurred.

Examples:

- insufficient evidence
- unresolved ambiguity
- low salience
- redundant information
- governance rejection
- proposal not justified
- experience not cognitively relevant
- required review not completed

The reason must describe the transition outcome, not invent an explanation for the external event.

## 7. Evidence and No-Guessing Invariant

CSTR inherits the GRI no-guessing principle.

The record must never promote:

- unknown -> observed
- interpreted -> observed
- inferred -> observed
- proposed -> committed

without an explicit architectural transition that authorizes that transformation.

The following remains mandatory:

No Evidence -> No Cognitive Commitment

However:

Evidence -> Commitment does not automatically follow.

Evidence produces a basis for evaluation. Governance and the transition mechanism determine whether persistent cognition changes.

## 8. Governance Is Part of the Record

Governance cannot be omitted from a committed transition.

A committed cognitive transition must be traceable to an authorization decision.

Conceptually:

A_t = LocalGovernance(P_t) intersection GlobalGovernance(P_t)

Therefore:

CommittedTransition -> GovernanceAuthorization

A rejected proposal may still produce a CSTR because rejection itself is part of the system's cognitive history.

## 9. Null Transitions

GRI must explicitly record valid non-learning outcomes.

Examples:

### Insufficient evidence

S_(t+1) = S_t

because the evidence did not justify commitment.

### Ambiguity

S_(t+1) = S_t

because the interpretation remained unresolved.

### Governance rejection

S_(t+1) = S_t

because the proposed change was not authorized.

### Redundant experience

S_(t+1) = S_t

because the persistent state already represented the relevant information.

Null transitions preserve the distinction between processing an experience and learning from an experience.

## 10. Provenance

Every CSTR must preserve sufficient provenance to reconstruct the causal chain:

Experience -> Interpretation -> Evidence -> Proposal -> Governance -> Transition

At minimum, provenance should support identification of:

- originating interaction
- interpreter or reasoning component
- evidence sources
- proposal source
- governance decision
- transition executor
- relevant architecture or version

The objective is reproducibility and auditability, not merely logging.

## 11. Transition Causality

A CSTR must not claim that an experience caused a cognitive change unless the transition mechanism records that relationship.

The authoritative internal chain is:

E_t -> I_t -> X_t -> P_t -> A_t -> S_(t+1)

External-world causality may remain unknown.

For example, if a person cancels a meeting, GRI may record that the cancellation was observed. It must not record the person's reason or intention unless that information is explicitly available or separately established through valid evidence.

## 12. Multiple Changes From One Experience

One experience may produce more than one authorized cognitive change.

For example, a sufficiently evidenced interaction could produce separate governed updates to:

- a concept
- a relationship
- a cognitive dimension

These are logically distinct state changes even when they share the same originating interaction.

Each resulting change must remain individually traceable.

A future implementation may group them under one transition evaluation while preserving separate target-level operations.

## 13. Ordering and State Continuity

Persistent cognitive transitions require ordered state progression.

Conceptually:

S_0 -> S_1 -> S_2 -> ... -> S_n

A transition record must identify the state version before and after the transition where the implementation supports explicit state versioning.

The architecture must prevent two independent transitions from silently claiming the same predecessor state unless concurrency semantics explicitly authorize that behavior.

Concurrency control remains an implementation research topic and is not fixed by CSTR v0.1.

## 14. Failed and Rejected Evaluations

Not every evaluated proposal becomes a committed transition.

CSTR should preserve rejected and non-committed outcomes when they are meaningful to cognitive history.

This allows GRI to distinguish:

- no proposal generated
- proposal generated but rejected
- proposal awaiting review
- proposal approved and committed
- proposal evaluated but resulting in a null transition

This distinction is important for recursive reflection and future learning about the system's own cognitive processes.

## 15. Recursive Reflection

CSTR provides historical material for recursive cognition.

A later cognitive process may evaluate prior transitions to determine:

- whether repeated patterns exist
- whether prior learning produced expected goal effects
- whether a dimension is adapting appropriately
- whether governance repeatedly blocks a particular class of proposals
- whether prior transitions should influence future interpretation

Historical records are evidence about prior system behavior. They must not automatically become beliefs about the external world.

## 16. Relationship to TCM

TCM and CSTR serve different purposes.

TCM answers:

> What happened in the recent communication?

CSTR answers:

> What cognitive transition did GRI evaluate and what persistent consequence resulted?

TCM is temporary.

CSTR is persistent historical record.

PCG contains persistent cognitive consequences.

Therefore:

TCM != CSTR != PCG

The three components form complementary layers of persistence.

## 17. Relationship to CRP

CSTR is upstream of CRP v0.2 conceptually.

CRP should represent the information required to support cognitive processing and transition proposals.

CSTR records the authoritative transition after governance and state-transition execution.

Therefore:

Experience -> CRP -> Cognitive Evaluation -> CSTR

This does not mean CRP defines CSTR.

The Cognitive State Transition Model defines the requirements that CRP and CSTR must satisfy.

Theory drives representation; representation does not define the theory.

## 18. Relationship to Foundation Models

Foundation models may contribute:

- interpretation candidates
- extracted observations
- hypotheses
- semantic structures
- reasoning proposals

A foundation model must not directly write persistent cognitive state.

Therefore:

FoundationModel -X-> PCG

and:

FoundationModel -X-> committed CSTR

The model may contribute evidence or proposals, but the Cognitive Kernel and Governance architecture determine whether a persistent transition is authorized and recorded as committed.

## 19. Minimal Conceptual Record

A minimal CSTR can be described as:

CSTR = (
  transition_id,
  interaction_id,
  state_before,
  experience,
  interpretation,
  evidence,
  proposal,
  governance,
  outcome,
  state_after,
  provenance
)

For a null transition:

state_after = state_before

and:

outcome = null

with a required null-transition reason.

For a committed transition:

outcome = committed

and the resulting state reference must identify the successor state.

## 20. Conceptual Lifecycle

The complete lifecycle becomes:

External Experience
↓
Perception
↓
TCM
↓
Cognitive Interpretation
↓
Evidence Formation
↓
Cognitive Proposal
↓
Local Governance
↓
Global Constitutional Governance
↓
Cognitive State Transition
↓
CSTR
↓
PCG / Dimension / Goal / Relationship Update
↓
Recursive Reflection
↓
Learning
↓
Future Cognition

CSTR provides the historical bridge between a governed transition and persistent cognitive evolution.

## 21. Architectural Invariants

CSTR v0.1 establishes:

1. Every committed cognitive change is traceable to a transition record.
2. Every committed cognitive change has governance authorization.
3. Proposal and commitment are distinct states.
4. Unknown information remains unknown unless valid evidence changes its status.
5. Interpretation cannot silently become observation.
6. Inference cannot silently become fact.
7. A null transition is a valid transition outcome.
8. Null transitions must preserve a reason.
9. Previous and resulting persistent state must be distinguishable.
10. Transition provenance must remain traceable.
11. CSTR is historical record, not persistent cognition itself.
12. CSTR does not replace PCG.
13. CSTR does not replace TCM.
14. CRP does not define CSTR.
15. Foundation models cannot bypass governance or the Cognitive Kernel.
16. Recursive reflection may use transition history but must not silently convert historical interpretation into external-world fact.

## 22. Open Questions for v0.2+

The following are intentionally unresolved:

- exact state versioning mechanism
- exact representation of state deltas
- whether one CSTR may contain multiple target-level operations
- concurrency and conflict resolution
- cryptographic integrity and signing requirements
- retention and archival policy
- whether rejected proposals require the same retention period as committed transitions
- exact recursive-reflection interface
- exact mapping between CSTR and future CRP v0.2 fields
- whether transition records should support reversible operations or compensating transitions

These questions must be resolved through architecture and experimentation rather than prematurely fixed in v0.1.

## 23. Research Direction

The architecture sequence is:

GRI Cognitive Theory
-> Cognitive State Transition Model v0.1
-> Cognitive State Transition Record v0.1
-> CRP v0.2
-> Cognitive Kernel Implementation
-> Experimental Evaluation

CSTR v0.1 is intentionally implementation-independent.

The next representation work should derive the minimum CRP v0.2 requirements from this transition record rather than adding fields opportunistically.
