# GRI Cognitive Dimension Model v0.1

**Status:** Foundational architecture specification  
**Version:** 0.1

## 1. Purpose

GRI represents cognitive characteristics as persistent **cognitive dimensions**.

A cognitive dimension is a governed, stateful cognitive object whose value may
evolve over time and whose evolution may influence, and be influenced by, other
dimensions in the Persistent Cognitive Graph (PCG).

The unified model is:

D = (value, weight, state, constraints, relationships, learning_rate)

This model applies to dimensions such as Trust, Curiosity, Relevance, and
future explicitly defined cognitive dimensions.

## 2. Trust as a Cognitive Dimension

Trust is a concrete instance of the unified cognitive-dimension model.

Trust = (value, weight, state, constraints, relationships, learning_rate)

Trust therefore does not require a separate primitive architecture.

Its value may increase or decrease as governed evidence produces authorized
updates:

Trust.value_t -> Trust.value_(t+1)

A single interaction does not necessarily change Trust. Evidence, proposal,
governance, and the transition mechanism remain mandatory.

## 3. Value

**Value** is the current numerical state of the dimension.

For the initial Trust model, value is an integer and may move in both positive
and negative directions:

value ∈ Z

Positive and negative values represent opposite directions of accumulated
dimension state; zero represents a neutral value.

The exact range, saturation, normalization, and interpretation remain open for
experimental definition.

A value change is a persistent cognitive state transition and must be traceable
through CSTR.

## 4. Weight

**Weight** represents the externally assigned importance or priority of the
dimension.

It answers:

> How important is this dimension to the current cognitive system?

Weight is distinct from value.

Weight does not mean truth, confidence, or evidence strength.

Because weight is externally assigned, its authority and modification rules
remain governed. External assignment must not silently become persistent
cognition without the appropriate transition mechanism.

The exact numerical representation remains open.

## 5. State

**State** indicates whether a dimension is active or inactive for a particular
PCG update event.

state ∈ {active, inactive}

Inactive does not mean deleted, weakened, or false. It means the dimension is
not participating in that particular update evaluation.

A dimension may therefore remain persistently present while being inactive for
one update and active for another.

## 6. Constraints

**Constraints** define local governance conditions applicable to the dimension.

For Trust, constraints may govern:

- what evidence types may modify Trust
- what operations are permitted
- whether Trust may increase or decrease under particular evidence
- whether a proposed change requires review
- whether a change is bounded by a maximum rate or range

Constraints are part of the dimension's governance structure and remain
subordinate to Global Constitutional Governance.

## 7. Relationships

**Relationships** define how a dimension connects to other persistent
cognitive dimensions or cognitive objects in the PCG.

A relationship must contain more than a simple connection. It should represent:

1. related target
2. direction of influence
3. relationship type
4. possible impact of source change on target
5. constraints governing that impact

Conceptually:

D_i --relationship/impact--> D_j

For example:

Trust --influences--> RelationshipStability

or:

Trust --influences--> Cooperation

A relationship does **not** mean that changing Trust automatically changes the
target.

Instead:

Change(D_i)
-> Relationship Evaluation
-> Proposed Effect(D_j)
-> Governance
-> Possible Update(D_j)

This preserves the distinction between influence and commitment.

### 7.1 Relationship as a Graph Property

A dimension is a persistent PCG node/object.

A relationship is a typed, potentially directed edge carrying cognitive-impact
semantics.

This allows interacting dimensions to form a cognitive graph without requiring
every dependency to be hard-coded inside individual dimension implementations.

### 7.2 Relationship Impact

At v0.1, impact remains conceptual rather than being forced into a specific
equation.

The relationship must answer:

> If this source dimension changes, what possible cognitive effect should be
> evaluated for the connected target dimension?

The effect becomes a proposal, not an automatic mutation.

## 8. Learning Rate

**Learning rate** controls how quickly a dimension is permitted to update its
value in response to governed learning.

A high learning rate permits faster adaptation.

A low learning rate permits slower adaptation.

Learning rate is persistent dimension state. It is initialized when the
dimension is created and may itself evolve only through governed learning.

Learning rate therefore controls **how fast** a dimension changes; it does not
determine **whether** the dimension is allowed to change.

Authorization belongs to evidence, proposal, and governance.

## 9. Dimension Update

A dimension update follows:

D_t -> Evidence -> Proposal -> Governance -> D_(t+1)

For Trust:

Trust_t -> Evidence -> TrustProposal -> Governance -> Trust_(t+1)

The result may be:

- increase
- decrease
- no change

No change is a valid outcome.

## 10. Learning-Rate-Constrained Update

Learning rate should constrain the magnitude or speed of value adaptation,
rather than directly deciding the target value.

Conceptually:

Delta(value) = GovernedUpdate(evidence, proposal, learning_rate)

The exact equation is intentionally not fixed in v0.1.

## 11. Activation During PCG Updates

A dimension can be persistently present but inactive during a particular update.

state(D, update_t) ∈ {active, inactive}

Activation may depend on:

- relevance to the experience
- relationships affected by the proposal
- active goals
- salience
- governance requirements
- other explicitly defined cognitive conditions

Activation means:

> This dimension participates in this update evaluation.

It does not mean:

> This dimension is true.

## 12. Dimension Interactions

A single experience may activate multiple dimensions.

For example:

Experience -> Activated Dimensions -> Dimension Proposals
-> Relationship Evaluation -> Governance -> Persistent Update

Each dimension remains an independently governed cognitive object.

The architecture must not collapse multiple dimensions into one opaque score.

## 13. PCG Representation

The PCG should represent at least two distinct concepts.

### Dimension Node

Contains the current persistent state of a cognitive dimension:

- dimension identity
- dimension type
- value
- weight
- state
- constraints reference
- learning rate
- provenance/state-version metadata

### Dimension Relationship Edge

Contains:

- source dimension
- target dimension
- relationship type
- direction
- impact semantics
- relationship constraints
- provenance/version metadata where required

The exact storage representation remains implementation-independent.

A graph database is not required by this specification.

## 14. Trust Example

An interaction produces evidence relevant to Trust.

Lifecycle:

Experience
-> Evidence
-> Trust Proposal
-> Local Trust Constraints
-> Global Governance
-> Trust Value Update
-> CSTR
-> PCG

Example committed update:

Trust.value: 4 -> 5

The system must preserve:

- why the update was proposed
- what evidence supported it
- what governance authorized it
- previous value
- resulting value
- transition identity

If evidence does not justify the change:

Trust.value: 4 -> 4

This is a valid null transition.

## 15. No-Guessing Requirements

The dimension model inherits GRI's no-guessing invariants.

In particular:

- an inferred event cannot silently become a Trust fact
- an interpretation cannot silently become a Trust update
- a proposal cannot silently become a Trust commitment
- an unknown external state cannot be encoded as a confirmed Trust value
- a relationship impact cannot automatically mutate its target

All persistent changes require explicit evidence, proposal, governance, and
transition execution.

## 16. Dimension Identity and Persistence

A cognitive dimension has persistent identity across updates.

For example:

Trust_0 -> Trust_1 -> Trust_2 -> ... -> Trust_n

The dimension identity remains stable while its state changes.

Each update should remain associated with the relevant interaction and
transition identifiers through CSTR/provenance.

## 17. Relationship to CSTR

A dimension update is a persistent cognitive transition:

DimensionUpdate -> CSTR -> PCG

CSTR records historical transition.

PCG stores resulting current dimension state.

A null dimension update may produce CSTR history without changing the PCG value.

## 18. Relationship to the Cognitive State Model

The existing state model remains:

S_t = (PCG_t, D_t, G_t, R_t, H_t)

The dimension model gives D_t a precise common structure.

PCG contains persistent dimension objects and their relationships.
CSTR contributes to H_t.

TCM remains outside persistent cognitive state.

## 19. Open Questions

The following remain deliberately open:

- exact Trust value range
- whether value should be bounded
- exact weight representation
- exact learning-rate representation
- mathematical learning-rate update equation
- relationship impact equations
- whether impact is linear, nonlinear, conditional, or symbolic
- conflict resolution when multiple dimensions propose interacting updates
- activation/salience algorithm
- persistent versus event-scoped activation semantics
- exact provenance granularity
- relationship semantic versioning

These should be resolved experimentally rather than prematurely fixed.

## 20. Core Principles

1. Every cognitive dimension uses the unified dimension structure.
2. Trust is a cognitive dimension, not a special-case subsystem.
3. Value represents current dimension state and may change in both directions.
4. Weight represents externally assigned importance/priority and is distinct from value.
5. State determines participation in a particular PCG update event.
6. Constraints define local governance for the dimension.
7. Relationships represent typed, directional cognitive dependencies and possible impact.
8. Relationship influence produces proposals, not automatic mutations.
9. Learning rate controls permitted adaptation speed, not authorization.
10. Every persistent dimension change is evidence-based, governed, and traceable.
11. Null dimension updates are valid.
12. PCG stores current cognitive dimension state; CSTR stores transition history.
13. The model remains independent of database technology.
14. No dimension may bypass the GRI governed transition pipeline.

## 21. Conversation-Scoped Curiosity Activation

A new conversation creates a new interaction context. The first cognitive
dimension activated by that interaction is **Curiosity**.

This is an architectural rule for the initial GRI interaction lifecycle:

New Conversation
-> New Interaction Instance
-> Curiosity Activation
-> Perception / Interpretation
-> Salience
-> Other Relevant Dimensions
-> Evidence / Proposal
-> Governance
-> Cognitive Transition

Curiosity is therefore not merely another optional dimension that may happen
to activate later. It is the initial cognitive orientation for a new
conversation.

Curiosity does not mean that the system assumes anything about the user or
the external world. Its role is to determine what should be explored,
clarified, examined, or understood.

A curiosity activation must therefore preserve the distinction:

Curiosity -> Question / Exploration
not:
Curiosity -> Assumption

The exact curiosity-value update equation remains open.

## 22. Interaction-Scoped Cognitive Instance

Every new interaction receives a distinct interaction-scoped cognitive
execution instance.

Conceptually:

Interaction I_n
-> Cognitive Instance CI_n
-> PCG Instance / Cognitive Graph Context PCG_n

The instance contains the cognitive state required to process that interaction
while remaining connected to the persistent identity and learning history of
the overall GRI system.

This does **not** mean that every interaction creates an entirely isolated
intelligence with no continuity.

Instead, the interaction creates a new cognitive-processing instance that
operates over persistent cognition and can produce governed changes to the
persistent PCG.

Conceptually:

Persistent PCG_(n-1)
        |
        +----> Cognitive Instance CI_n
        |          |
        |          +--> TCM_n
        |          +--> Curiosity_n
        |          +--> Active Dimensions_n
        |          +--> Reasoning_n
        |          +--> Governance_n
        |
        +<---- Governed Cognitive Transition
        |
Persistent PCG_n

## 23. PCG Graph Instance and Neuroplasticity Analogy

Each interaction may create a new **PCG processing graph instance** representing
the cognitive structures activated for that interaction.

This is analogous to neuroplasticity at the architectural level: interaction
can activate existing structures, establish new relationships, strengthen
existing relationships, weaken relationships, or create new persistent
cognitive structures through governed learning.

The analogy is architectural, not a claim that GRI reproduces biological
neural mechanisms.

The interaction-scoped graph may contain:

- activated dimensions
- relevant identities
- relevant concepts
- relevant beliefs
- active goals
- relationship paths
- candidate new cognitive objects
- candidate impact paths

The interaction graph is not automatically equivalent to permanent PCG.

Only governed cognitive consequences are consolidated into persistent PCG.

## 24. Curiosity as the Initial Cognitive Trigger

The initial sequence is therefore:

New Conversation
-> Interaction Instance
-> Curiosity Activation
-> Curiosity Evaluation
-> Salience / Exploration
-> Relevant Dimension Activation
-> Cognitive Interpretation
-> Evidence
-> Proposal
-> Governance
-> Kernel
-> PCG Transition

Curiosity may activate other dimensions through relationships and salience.

For example:

Curiosity
-> Explore unfamiliar information
-> Activate Relevance
-> Activate Concept Formation
-> Evaluate Trust where applicable

These downstream activations remain context-dependent and must not be
assumed merely because Curiosity is active.

## 25. Human-Like Decision Requirement

The phrase "Curiosity must decide like a human" is interpreted architecturally
as a requirement that Curiosity participate in **contextual, goal-aware,
relationship-aware, governed decision formation**, rather than behaving as a
random question generator or fixed rule.

Curiosity may contribute:

- what is unknown
- what is worth investigating
- what clarification is needed
- what relationship is relevant
- what information could reduce uncertainty
- what experience may be valuable for learning

Curiosity must not manufacture missing facts.

Therefore:

Unknown -> Curiosity -> Investigation

not:

Unknown -> Curiosity -> Assumed Fact

The exact human-like curiosity decision mechanism remains a research question
and is not fixed as a simple formula in v0.1.
