# GRI Persistent Cognitive Graph Ontology v0.1

**Status:** Foundational architecture specification  
**Version:** 0.1  
**Depends on:** Cognitive State Transition Model v0.1, Cognitive Dimension Model v0.1, CSTR v0.1

## 1. Purpose

The Persistent Cognitive Graph (PCG) represents the current persistent cognitive
state of GRI.

PCG answers:

> What persistent cognition exists now?

It does not answer:

> What was the original conversation?

That responsibility belongs to TCM.

And it does not answer:

> What transition produced this state?

That responsibility belongs to CSTR.

Therefore:

TCM != PCG != CSTR

PCG is the persistent cognitive consequence layer.

## 2. Ontology Principle

The PCG ontology must be derived from GRI cognitive theory rather than from a
particular database technology.

The logical architecture is:

Persistent Cognitive Objects
+
Cognitive Dimensions
+
Typed Cognitive Relationships
=
Persistent Cognitive Graph

A graph database is not required.

The ontology may later be serialized into relational, graph, document, or
other storage technologies without changing its cognitive meaning.

## 3. Persistent Cognitive Object

A **Persistent Cognitive Object (PCO)** is an identifiable unit of persistent
cognition represented in the PCG.

A PCO has persistent identity across state transitions.

Conceptually:

PCO = (object_id, object_type, state, provenance, version)

The object identity remains stable while its cognitive state evolves.

Examples include:

- entity identity
- concept
- belief
- goal
- relationship
- cognitive dimension

Not every PCO is a dimension.

A dimension is a specific class of persistent cognitive object with the unified
dimension structure:

D = (value, weight, state, constraints, relationships, learning_rate)

## 4. Canonical PCG Object Types

v0.1 defines the following initial logical object categories.

### 4.1 Identity

Identity represents a persistent referent recognized by GRI.

An identity may represent:

- a person
- organization
- system
- object
- place
- other explicitly established entity

Identity is not a personality model and is not inferred merely because an
entity name appears in an interaction.

An identity must retain provenance for how it became persistent.

Unknown identity information remains unknown.

### 4.2 Concept

A concept represents a persistent abstraction formed or maintained by GRI.

Examples may include:

- "meeting"
- "reliability"
- "customer"
- "deadline"

A concept is not automatically a belief.

A concept answers approximately:

> What persistent abstraction does the system recognize?

A concept may be connected to beliefs, identities, goals, and dimensions.

### 4.3 Belief

A belief represents governed persistent cognition that GRI has accepted as a
belief about an explicitly defined target or proposition.

A belief must not be created merely because an interpreter produced an
inference.

Conceptually:

Evidence
-> Hypothesis/Proposal
-> Evaluation
-> Governance
-> Belief Commitment

A belief must preserve provenance and evidence references sufficient to trace
its formation or modification.

Belief strength/confidence is intentionally not defined as an automatic
synonym for Trust or dimension value.

### 4.4 Goal

A goal represents a persistent purpose or objective relevant to GRI cognition.

Goals influence:

Goal -> Salience -> Interpretation

and experience may provide:

Experience -> Observed Goal Effect -> Goal Evaluation

Goal evolution is governed and cannot bypass constitutional constraints.

A goal may be connected to dimensions, concepts, identities, beliefs, and other
goals.

### 4.5 Cognitive Dimension

A cognitive dimension is a persistent cognitive object using the unified model:

D = (value, weight, state, constraints, relationships, learning_rate)

Examples:

- Trust
- Curiosity
- Relevance
- other explicitly defined dimensions

Trust is therefore a dimension object, not a special graph primitive.

### 4.6 Relationship

A relationship represents a persistent cognitive relation between identified
PCG objects.

It is distinct from a raw graph edge because it has cognitive semantics.

Conceptually:

Relationship = (source, target, type, direction, semantics, constraints)

A relationship may connect:

- identity -> identity
- identity -> concept
- belief -> identity
- goal -> concept
- dimension -> dimension
- dimension -> identity
- dimension -> relationship
- and other explicitly governed combinations

The allowed combinations must be constrained by the ontology.

## 5. Cognitive Dimension vs Relationship

These concepts must remain distinct.

A dimension stores a changing cognitive characteristic:

Trust.value = 5

A relationship expresses a connection and possible influence:

Trust --influences--> Cooperation

The relationship does not itself become the Trust value.

Likewise, the relationship does not automatically mutate its target.

Cross-dimension influence follows:

Source Dimension Change
-> Relationship Evaluation
-> Target Proposal
-> Governance
-> Possible Target Update

## 6. Trust Representation

Trust is a dimension.

The ontology therefore permits a structure such as:

Identity(A)
    |
    | associated-with
    v
Trust Dimension(A,B)
    |
    | influences
    v
Cooperation Dimension(A,B)

The exact attachment semantics remain open.

The important architectural point is that Trust's value is stored in the Trust
dimension object, while its relationships are represented separately.

Trust may therefore be:

- increased
- decreased
- unchanged

through governed transitions.

## 7. Dimension Instance Identity

A dimension type and a dimension instance are different concepts.

For example:

Dimension type = Trust

Dimension instance =
"Trust of GRI toward Identity-X"

The instance has its own persistent identity.

This permits the same dimension type to exist across multiple relevant
cognitive contexts without collapsing all Trust into one global scalar.

Conceptually:

DimensionInstance =
(dimension_id, dimension_type, subject, optional_target, D)

The exact subject/target cardinality remains open and must be defined per
dimension type.

## 8. Dimension State

The persistent dimension state is:

D = (value, weight, state, constraints, relationships, learning_rate)

Important distinction:

- value = persistent cognitive value
- weight = assigned importance/priority
- state = participation state for an update evaluation
- constraints = local governance
- relationships = graph connections/impact semantics
- learning_rate = adaptation speed

The state field must not be interpreted as the existence of the dimension
itself.

A dimension can persist while being inactive during a particular update.

## 9. Relationships as First-Class Cognitive Structures

PCG relationships are first-class logical structures.

A relationship should minimally identify:

- relationship_id
- source_object_id
- target_object_id
- relationship_type
- direction
- relationship semantics
- constraints
- provenance/version metadata where required

A relationship may itself become the target of a cognitive dimension.

This allows dimensions such as Trust to be associated with a relationship
rather than forcing Trust to be attached only to an identity.

For example:

Identity-A
    |
    +--- works-with ---> Identity-B
                 |
                 +--- Trust Dimension ---> value

This remains conceptual; the exact attachment representation is an open
implementation question.

## 10. Cognitive Impact

A relationship may define potential impact semantics.

For example:

Trust
--influences-->
Cooperation

The impact semantics describe what should be evaluated when Trust changes.

They do not authorize a target mutation.

The evaluation chain remains:

Impact Detection
-> Target Proposal
-> Local Governance
-> Global Governance
-> Kernel
-> Target State Transition

This prevents graph relationships from becoming hidden mutation paths.

## 11. Belief and Evidence Boundary

PCG stores the committed belief.

It does not replace the evidence or transition history that justified it.

Therefore:

Evidence != Belief

The evidence remains traceable through CSTR and its provenance.

A belief must retain sufficient references to its supporting transition/evidence
history to allow later cognitive evaluation.

Historical evidence must not automatically be interpreted as current external
truth.

## 12. Concept and Belief Boundary

A concept and belief are different.

Example:

Concept:
"Meeting cancellation"

Belief:
"Identity-X cancelled the meeting."

The concept is an abstraction.

The belief is a governed proposition about a target.

The existence of a concept does not imply the truth of any belief associated
with that concept.

## 13. Goal and Belief Boundary

Goals and beliefs are also distinct.

A goal expresses a desired objective.

A belief expresses persistent cognition about a proposition.

For example:

Goal:
"Maintain reliable collaboration."

Belief:
"Identity-X has repeatedly cancelled scheduled meetings."

A belief may influence goal evaluation, but it does not automatically redefine
the goal.

Goal evolution remains governed.

## 14. Identity and Observation Boundary

An identity in PCG is not equivalent to a name extracted from TCM.

The system must distinguish:

Observed reference
!=
Established persistent identity

An identity becomes persistent only through the appropriate governed cognitive
process.

This preserves the no-guessing invariant.

## 15. Learning State

Learning history belongs primarily to the transition-history component H_t and
CSTR.

PCG may retain current **learning state** required for future cognition, but it
must not duplicate the complete transition history as cognitive state.

Examples of current learning state may include:

- current learning rate
- dimension adaptation state
- governed learning parameters
- references to relevant historical transitions

Historical transitions remain CSTR.

Therefore:

Current Learning State -> PCG

Historical Learning Events -> CSTR/H_t

## 16. Provenance

Every persistent cognitive object must retain sufficient provenance to answer:

- when it was created
- what transition created it
- what transition last modified it
- what interaction initiated the relevant evaluation
- what evidence supported the change
- what governance decision authorized it

Provenance does not turn an interpretation into an observation.

It records the origin and history of the committed cognitive state.

## 17. Versioning

Every persistent cognitive object participates in state-version continuity.

A state transition conceptually produces:

PCG_t -> PCG_(t+1)

An individual object may therefore have:

object_version_t -> object_version_(t+1)

The exact object-version implementation remains open.

Global state versioning remains authoritative for transition continuity.

## 18. Null Transition Behavior

A null transition does not mutate PCG.

Therefore:

PCG_(t+1) = PCG_t

The CSTR records that the experience was evaluated and why no persistent
cognitive change occurred.

Examples:

- insufficient evidence
- ambiguity
- redundant information
- low salience
- governance rejection

This is fundamental to preventing forced learning.

## 19. Creation, Modification, Reinforcement, Weakening, Removal

PCG objects may be changed only through the governed transition mechanism.

Supported conceptual operations remain:

- create
- modify
- reinforce
- weaken
- remove

For dimensions, these operations may affect value, weight, activation state,
constraints, relationships, or learning rate where governance permits.

For beliefs, they may affect the proposition's persistent status or associated
cognitive attributes.

For concepts, relationships, goals, and identities, the applicable operations
must be defined by their object semantics.

## 20. PCG Integrity Rules

The PCG must enforce the following architectural rules.

1. No direct foundation-model writes.
2. No direct arbitrary storage writes.
3. Every committed change has evidence.
4. Every committed change has governance authorization.
5. Every committed change has CSTR provenance.
6. Unknown information remains unknown.
7. Interpretation cannot silently become belief.
8. Inference cannot silently become fact.
9. Relationship influence cannot silently mutate a target.
10. Null transitions do not modify PCG.
11. Dimension values change only through governed transitions.
12. Learning rate controls adaptation speed, not authorization.
13. Weight is not truth or confidence.
14. TCM content does not automatically become PCG.
15. CSTR remains historical record and does not become PCG.
16. PCG represents current persistent cognition.

## 21. Canonical PCG Structure

Conceptually:

PCG = (Objects, Dimensions, Relationships)

where:

Objects =
  identities
  concepts
  beliefs
  goals
  other governed cognitive objects

Dimensions =
  persistent instances of cognitive dimensions

Relationships =
  typed, directed or explicitly undirected cognitive connections
  carrying relationship semantics and possible impact information

A dimension may participate in relationships with ordinary cognitive objects
or other dimensions.

## 22. Example

Suppose GRI interacts repeatedly with Identity-X.

The system may eventually contain:

Identity-X
    |
    +--- Trust Dimension
    |       value = 5
    |       weight = externally assigned
    |       state = active for current update
    |       learning_rate = defined value
    |
    +--- Concept associations
    |
    +--- Beliefs
    |
    +--- Relationship structures

The Trust value is not the relationship itself.

The evidence for Trust changes is not stored as Trust.

The historical transitions that produced Trust=5 are not stored as Trust.

Instead:

PCG stores current Trust state.

CSTR stores the governed transition history.

TCM temporarily stores original communication/experience context.

## 23. Architecture Boundary

The resulting separation is:

TCM
"What happened?"

Cognitive Interpretation
"What may this mean?"

Evidence
"What supports the proposal?"

Governance
"Is the proposed cognitive change permitted?"

Cognitive Kernel
"Execute the authorized transition."

PCG
"What persistent cognition exists now?"

CSTR
"What governed transition produced this state?"

This separation is foundational to GRI.

## 24. Open Questions

The following remain intentionally unresolved:

- exact identity ontology
- exact belief representation
- whether beliefs are graph nodes or structured propositions
- exact concept formation rules
- exact goal ontology
- dimension subject/target cardinality
- whether Trust attaches to identities, relationships, or both
- relationship impact representation
- relationship confidence/strength semantics
- object-level versus graph-level versioning
- identity resolution
- duplicate concept resolution
- contradiction representation
- belief revision semantics
- goal conflict representation
- dimension conflict resolution
- current learning-state representation
- graph traversal semantics
- storage/indexing technology

These questions should be resolved through cognitive architecture and
experimentation before implementation technology is allowed to constrain them.

## 25. Core Principle

The PCG is not a database schema.

It is the **ontology of persistent cognition**.

The implementation storage layer must adapt to this ontology.

The ontology must not be redesigned merely to fit a selected database.
