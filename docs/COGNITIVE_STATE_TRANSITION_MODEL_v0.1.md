# GRI Cognitive State Transition Model v0.1

## Status

Foundational architecture specification.

This document defines the conceptual state-transition model of Governed
Recursive Intelligence (GRI). It is deliberately independent of JSON, CRP,
specific foundation models, and implementation language.

CRP is expected to serialize parts of this model later. CRP MUST NOT define
the underlying cognitive theory.

## 1. Purpose

GRI is designed as a persistent cognitive system rather than a stateless
prediction system.

The fundamental transformation is:

Experience → Interpretation → Evidence → Cognitive Proposal → Governance → Cognitive State Transition

The important unit is therefore not merely an output response. It is the
governed evolution of persistent cognitive state.

## 2. Cognitive State

Let the persistent cognitive state at time t be:

S_t = (PCG_t, D_t, G_t, R_t, H_t)

where:

- PCG_t = Persistent Cognitive Graph
- D_t = current states of cognitive dimensions
- G_t = active goals and goal relationships
- R_t = persistent relationships, including trust and relevance
- H_t = learning and historical transition record

TCM is intentionally NOT part of persistent cognitive state.

TCM stores transient experience and communication context. It may provide
evidence for a transition, but its contents do not automatically become
persistent cognition.

## 3. Experience

An experience is an interaction or event available to the system.

Represent it conceptually as:

E_t = (input, source, context, timestamp, provenance)

An experience is not yet cognition.

The system must first distinguish what was actually observed from what was
interpreted or inferred.

## 4. Cognitive Interpretation

The Cognitive Interpreter transforms experience into a structured candidate:

I_t = Interpret(E_t, S_t)

The interpretation may contain:

- observations
- entities
- events
- relationships
- linguistic or structural observations
- hypotheses
- uncertainty
- contextual relevance

Interpretation is not equivalent to belief.

A foundation model may produce an interpretation candidate, but the GRI kernel
retains authority over persistent cognitive change.

## 5. Evidence

Evidence is information explicitly available to support a cognitive proposal.

Let:

X_t = Evidence(E_t, I_t, S_t)

Evidence MUST retain provenance.

The following distinction is mandatory:

Observed ≠ Interpreted ≠ Inferred ≠ Believed

An inference may use an observation as evidence, but an inference MUST NOT be
silently promoted to a belief.

Unknown information remains unknown.

## 6. Cognitive Proposal

The interpreter or reasoning system may propose a change:

P_t = Propose(S_t, E_t, I_t, X_t, Goals_t)

A proposal may target:

- belief
- concept
- relationship
- goal
- cognitive dimension
- learning state

A proposal is NOT a state change.

This is a critical architectural boundary.

Proposal ≠ Commitment

The proposal must pass governance before it can modify persistent cognition.

## 7. Governance

Governance evaluates whether a proposed transition is permitted:

A_t = Govern(P_t, S_t, Constitution, Constraints_t)

Governance operates at two levels:

### Local governance

Constraints associated with the affected cognitive dimension or subsystem.

### Global governance

Constitutional, ethical, safety, and system-wide constraints.

The effective authorization is:

A_t = LocalGovernance(P_t) ∩ GlobalGovernance(P_t)

A proposal is committed only when the applicable governance requirements are
satisfied.

## 8. State Transition

The GRI cognitive transition function is:

S_(t+1) = T(S_t, E_t, I_t, X_t, P_t, A_t)

The transition function is the authoritative mechanism that changes persistent
cognition.

It MUST NOT be replaced by direct writes from a foundation model.

Conceptually:

S_t → Proposal → Governance → T → S_(t+1)

## 9. Null Transition

Not every interaction should change persistent cognition.

Therefore:

T(S_t, ...) = S_t

is a valid and important outcome.

Examples include:

- insufficient evidence
- ambiguous information
- redundant information
- rejected proposal
- low-salience experience
- governance failure
- information that does not materially affect any cognitive dimension

This prevents forced learning.

Experience does not imply cognitive change.

## 10. Allowed Cognitive Transition Operations

At the conceptual level, GRI supports at least:

### Create

A previously absent persistent cognitive object is introduced.

### Modify

An existing cognitive object changes state or attributes.

### Reinforce

Existing cognition becomes stronger because additional evidence supports it.

### Weaken

Existing cognition loses strength because evidence reduces support.

### Remove

An existing cognitive object is removed when governance and transition rules
permit removal.

These operations are not themselves proof that a change is justified. Evidence
and governance remain mandatory.

## 11. Evidence Threshold

A cognitive transition must have an explicit evidence basis.

The minimum principle is:

No Evidence → No Cognitive Commitment

However:

Evidence → Cognitive Commitment

does NOT automatically follow.

Instead:

Evidence → Proposal → Governance → Possible Commitment

This preserves the distinction between evidence and authorization.

## 12. Belief Formation

A belief is not created from a single unexamined inference merely because an
interpreter is confident.

Conceptually:

Repeated or sufficient evidence
→ hypothesis
→ evaluation
→ governed belief formation

The exact evidence threshold is intentionally left open at this stage.

This prevents premature mathematical assumptions about belief confidence,
probability, or repetition.

## 13. Relationship and Trust Evolution

Relationships are persistent cognitive structures.

A relationship may evolve through repeated observed interactions.

For example:

Interaction
→ Observed Pattern
→ Observed Goal Effect
→ Relationship Evaluation
→ Governed Trust Update

The system must not infer a stable relationship property from an unsupported
single event.

## 14. Goal Interaction

Goals participate in state transitions in two ways.

First, existing goals affect salience and interpretation:

Goal → Salience → Interpretation

Second, experience may provide evidence relevant to goal evaluation:

Experience → Observed Goal Effect → Goal Evaluation

A goal may be proposed for creation, modification, suspension, or evolution,
but goal evolution remains subject to constitutional governance.

No emergent goal automatically overrides higher-level governance.

## 15. Cognitive Dimensions

Each cognitive dimension is represented conceptually as:

D = (value, weight, state, constraints, relationships, learning_rate)

The learning rate is persistent state.

It is initialized when the dimension is created and may evolve through governed
learning.

A dimension update therefore changes part of S_t, rather than creating a
separate ad-hoc learning mechanism.

## 16. Salience

Not every experience deserves equal cognitive processing.

A salience mechanism may determine:

Salience(E_t, S_t, Goals_t, D_t) → priority

Salience influences which experiences receive deeper interpretation and
possible consolidation.

Salience MUST NOT convert uncertainty into certainty.

High salience means "worth processing", not "true".

## 17. Recursive Cognition

After a state transition, GRI may evaluate the consequences of its own
cognitive change:

S_t
→ Transition
→ S_(t+1)
→ Reflection
→ Evaluation
→ Possible governed adjustment

This recursive loop is central to GRI.

However, recursion does not imply unrestricted self-modification.

Every persistent modification remains bounded by governance.

## 18. Learning

Learning is therefore defined as governed state evolution:

Learning_t = S_(t+1) - S_t

This is conceptual rather than numerical. Not every state component needs a
scalar representation.

Learning can involve changes to:

- beliefs
- concepts
- relationships
- trust
- goals
- dimensions
- learning rates
- contextual associations

The system should preserve the causal and provenance relationship between the
experience and the resulting state change.

## 19. Complete Cognitive Lifecycle

The model can therefore be expressed as:

External Experience
→ Perception
→ TCM
→ Cognitive Interpretation
→ Evidence Formation
→ Cognitive Proposal
→ Local Governance
→ Global Constitutional Governance
→ Cognitive State Transition
→ PCG
→ Recursive Reflection
→ Learning
→ Future Cognition

TCM is transient context.

PCG is persistent cognitive consequence.

## 20. Core Invariants

The following invariants should guide future GRI implementation.

### Invariant 1 — No Guess Promotion

An inference MUST NOT automatically become an observation or belief.

### Invariant 2 — No Direct Foundation-Model State Writes

Foundation models may generate proposals, but persistent cognition can only be
changed by the governed GRI transition mechanism.

### Invariant 3 — Evidence Before Commitment

Every persistent cognitive change requires an explicit evidence basis.

### Invariant 4 — Governance Before Commitment

A proposed persistent change must pass the applicable governance layers.

### Invariant 5 — Unknown Remains Unknown

Missing information must not be silently synthesized into confirmed cognition.

### Invariant 6 — No Forced Learning

An interaction may produce no persistent state change.

### Invariant 7 — Persistent Learning Is Traceable

A cognitive change must be traceable to the experience, interpretation,
evidence, proposal, and governance decision that produced it.

### Invariant 8 — Governance Is Constitutional

Governance is part of the cognitive architecture, not merely an external
post-processing safety filter.

### Invariant 9 — Goal Evolution Is Governed

Goals may evolve only within constitutional constraints.

### Invariant 10 — Recursive Modification Is Bounded

Self-evaluation may produce new proposals, but recursive cognition cannot bypass
governance.

## 21. Architectural Boundary

The final separation is:

Foundation Model
produces interpretation and reasoning candidates.

CRP
represents those candidates in a structured, model-independent form.

Cognitive Interpreter
constructs cognitively meaningful representations.

Governance
determines whether proposed cognitive changes are permitted.

Cognitive Kernel
executes authorized state transitions.

PCG
stores persistent cognitive consequences.

Therefore:

CRP is not GRI.

CRP is an interface representation used by GRI.

And:

JSON is not CRP.

JSON is only one possible serialization of CRP.

## 22. Research Direction

The next formalization should define the internal structure of a
Cognitive State Transition Record independently of JSON.

Only after that definition is stable should CRP v0.2 serialize it.

The intended sequence is:

GRI Cognitive Theory
→ Cognitive State Transition Model
→ Transition Record
→ CRP v0.2
→ Kernel Implementation
→ Experimental Evaluation

This preserves the architectural principle that the theory of cognition must
drive the representation protocol, rather than the representation protocol
driving the theory.
