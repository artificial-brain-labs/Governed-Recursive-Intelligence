# GRI Cognitive Requirement Identification & Decomposition Model v0.1

**Status:** Foundational architecture specification  
**Version:** 0.1  
**Depends on:** GRI Interaction Communication & Routing Layer v0.1, Cognitive Instance Lifecycle v0.1, Interaction Cognitive Graph v0.1, Persistent Cognition Relevance Retrieval Model v0.1, Internal Cognition Sufficiency Model v0.1

## 1. Purpose

The **Cognitive Requirement Identification & Decomposition Model (CRIDM)** defines how GRI converts an incoming interaction into a structured, temporary description of what the current Cognitive Instance needs to accomplish.

It answers:

> What does this interaction require GRI to determine, do, explain, transform, investigate, or clarify?

It does not answer:

> What is true?

It does not retrieve PCG.

It does not decide whether GRI is sufficient.

It does not decide whether a frontier model is required.

Therefore:

`Requirement != Interpretation != Cognition != Truth`

## 2. Architectural Position

The canonical sequence is:

`Communication
-> Cognitive Instance
-> Curiosity
-> Requirement Identification
-> Requirement Decomposition
-> PCG Relevance Retrieval
-> Internal Cognition Sufficiency
-> Gap Identification
-> Routing`

CRIDM therefore provides the requirement context consumed by PCRRM.

Without an explicit requirement, relevance and sufficiency become poorly defined because the same persistent cognition can be relevant to one task and irrelevant to another.

## 3. Core Principle

> **GRI must identify what the interaction requires before deciding what cognition is relevant or what processing capability is needed.**

The system must not silently complete an ambiguous requirement merely to make downstream processing easier.

Therefore:

`Ambiguous Requirement -> Explicit Ambiguity`

not:

`Ambiguous Requirement -> Assumed Requirement`

## 4. Requirement Is Not User Intent

A user interaction may contain several layers:

- literal communication;
- explicit request;
- implied task context;
- possible underlying intent;
- constraints;
- desired output;
- unresolved ambiguity.

CRIDM must distinguish what is explicitly established from what is only inferred.

For example:

> "Can you check John's meeting?"

may establish that a meeting-related check is requested, while leaving unresolved:

- which John;
- which meeting;
- what should be checked;
- whether the user means a past, current, or future meeting.

The missing elements remain unresolved.

## 5. Requirement Model

A requirement is represented conceptually as:

`Requirement =
(
requirement_id,
interaction_id,
instance_id,
task_type,
objective,
targets,
constraints,
temporal_scope,
evidence_requirements,
output_requirements,
capability_requirements,
ambiguities,
uncertainties,
provenance
)`

The exact serialization remains open.

The requirement is temporary interaction state unless a later governed process explicitly creates persistent cognition from it.

## 6. Requirement Components

### 6.1 Task Type

Task type describes what kind of operation the interaction requests.

Examples:

- retrieve;
- explain;
- compare;
- transform;
- calculate;
- create;
- investigate;
- decide;
- evaluate;
- remember/reconcile;
- clarify;
- act.

Task type is descriptive.

It does not determine the route by itself.

### 6.2 Objective

Objective describes the requested outcome.

Examples:

- identify relevant information;
- explain a concept;
- determine whether existing cognition is sufficient;
- transform provided content;
- produce a requested artifact.

Objective must preserve uncertainty where the interaction does not establish a unique objective.

### 6.3 Targets

Targets identify what the requirement concerns.

Potential targets include:

- established identities;
- candidate references;
- concepts;
- relationships;
- goals;
- cognitive dimensions;
- propositions;
- external objects;
- interaction content.

A target mention does not automatically establish a persistent identity.

### 6.4 Constraints

Constraints describe requirements that limit acceptable processing or output.

Examples:

- time period;
- geographic scope;
- format;
- language;
- privacy boundary;
- evidence requirement;
- authorization requirement;
- maximum scope;
- user-provided exclusions.

Explicit constraints must be preserved.

Missing constraints should not be invented.

### 6.5 Temporal Scope

Temporal scope describes when the requirement applies.

Possible forms include:

- historical;
- current;
- future;
- relative;
- unspecified.

Temporal scope is important because the same persistent cognition may be appropriate for a historical task but insufficient for a current-state task.

Unspecified temporal scope remains unspecified unless clarified or established by context.

### 6.6 Evidence Requirements

The interaction may explicitly require:

- explanation from existing cognition;
- supporting evidence;
- external verification;
- current information;
- source attribution;
- comparison of evidence.

CRIDM records the requirement.

It does not determine whether the evidence exists.

### 6.7 Output Requirements

Output requirements describe what form the result should take.

Examples:

- answer;
- explanation;
- list;
- structured data;
- code;
- document;
- action;
- clarification request.

Output requirements are distinct from cognitive sufficiency.

### 6.8 Capability Requirements

Some requirements inherently need capabilities such as:

- calculation;
- specialized reasoning;
- image processing;
- language transformation;
- external information access;
- tool use;
- artifact generation.

CRIDM records an explicitly identifiable capability requirement.

It does not decide whether GRI itself or another processor should provide that capability.

## 7. Explicit vs Derived Requirement Elements

Every requirement element should carry a provenance class.

At minimum:

- **explicit** — directly established by the interaction;
- **context-derived** — supported by established interaction context;
- **inferred** — interpretation produced by the cognitive process;
- **unresolved** — insufficient information to establish the element.

An inferred requirement element must not be silently represented as explicit.

For example:

`Explicit: "tomorrow"`

may establish temporal scope.

But:

`Inferred: "tomorrow morning"`

is not allowed unless the interaction or established context actually supports it.

## 8. Requirement Confidence Is Not Truth

CRIDM may need to represent whether an interpretation of the requirement is stable enough for processing.

This must not be confused with truth about the external world.

A requirement interpretation may be:

- established;
- supported by context;
- uncertain;
- ambiguous;
- unresolved.

No numerical confidence score is mandated in v0.1.

If numerical confidence is later introduced, its semantics must be explicitly defined and must not be treated as belief strength, Trust, or truth probability without architectural justification.

## 9. Requirement Decomposition

A complex interaction may contain multiple requirements.

For example:

> "Find the information about X, compare it with Y, and tell me what changed."

This can decompose into:

`R1 -> retrieve X`

`R2 -> retrieve Y`

`R3 -> compare X and Y`

`R4 -> identify changes`

The decomposition must preserve dependency relationships.

Conceptually:

`Requirement Graph =
(requirements, dependencies, shared_context, unresolved_elements)`

A later requirement may depend on the result of an earlier requirement.

## 10. Requirement Dependencies

Dependencies may include:

- prerequisite;
- evidence dependency;
- target dependency;
- context dependency;
- result dependency;
- clarification dependency.

For example:

`Retrieve X -> Retrieve Y -> Compare -> Change Analysis`

The dependency structure remains temporary.

It does not become a persistent cognitive relationship.

## 11. Requirement Ambiguity

Ambiguity is a first-class state.

Examples:

### Target Ambiguity

"Talk to John."

Multiple established or candidate identities may match.

### Objective Ambiguity

"Check the meeting."

It is unclear what should be checked.

### Temporal Ambiguity

"Is this still relevant?"

The relevant time frame is unclear.

### Scope Ambiguity

"Tell me everything about the project."

The intended scope may be undefined.

### Output Ambiguity

"Prepare it."

The requested artifact or action may be unclear.

CRIDM must preserve the ambiguity and allow the routing layer to determine whether clarification is required.

## 12. Requirement Completeness

A requirement may be complete enough for one processing stage while incomplete for another.

For example:

The task "explain this concept" may be sufficiently specified for retrieval, while an additional requested comparison may require another target.

Therefore:

`Requirement Complete for Stage A != Requirement Complete for Entire Interaction`

Requirement decomposition may proceed incrementally.

## 13. Requirement Evolution

The requirement may change as new information enters the Cognitive Instance.

For example:

`Initial Requirement
-> Clarification
-> Updated Requirement
-> Retrieval
-> Sufficiency
-> Processing`

A frontier response may also reveal that the original requirement was incomplete or ambiguous.

The returned information must re-enter GRI and may produce a revised requirement.

The revision must preserve the prior requirement in temporary processing history where needed for traceability.

## 14. Frontier Output and Requirement Re-entry

A frontier response is new information.

Therefore it may change the understanding of what the interaction requires.

The canonical loop is:

`Frontier Output
-> New Information
-> Requirement Evaluation
-> Requirement Update if justified
-> PCG Retrieval
-> Sufficiency
-> Routing`

The fact that GRI requested the frontier response does not mean that the response's interpretation of the task is automatically authoritative.

## 15. Requirement vs Interpretation

The system must distinguish:

`Interaction -> Interpretation -> Requirement Representation`

from:

`Requirement -> External-World Belief`

A requirement is a representation of what processing is being requested.

It is not a claim about the external world.

For example:

Requirement:

`Determine whether Identity-X cancelled the meeting.`

This does not establish:

`Identity-X cancelled the meeting.`

The latter requires evidence and the normal cognitive evaluation path.

## 16. Requirement and Curiosity

Curiosity initiates exploration around the requirement.

Conceptually:

`Interaction
-> Curiosity
-> What is being asked?
-> What is unknown?
-> Requirement Identification
-> Retrieval`

Curiosity may identify unresolved aspects of the requirement.

It cannot invent missing task details.

## 17. Requirement and PCRRM

CRIDM supplies PCRRM with the structured requirement context.

`Requirement
-> Retrieval Seeds
-> Relevance Retrieval`

Potential retrieval seeds may come from:

- explicit targets;
- established identities;
- concepts;
- goals;
- dimensions;
- known relationships;
- evidence references.

An unresolved target remains unresolved and cannot be converted into a persistent identity solely for retrieval.

## 18. Requirement and ICSM

ICSM evaluates sufficiency relative to the requirement.

Therefore:

`Requirement + Relevant Cognition -> Sufficiency Evaluation`

The same retrieved cognition can produce different sufficiency results under different requirements.

Example:

Historical cognition may be sufficient for:

> "What happened last year?"

but insufficient for:

> "What is happening now?"

CRIDM therefore supplies temporal and evidence requirements to ICSM.

## 19. Requirement and Routing

Routing consumes requirement and sufficiency information.

Conceptually:

`Requirement
-> Relevant Cognition
-> Sufficiency
-> Missing Requirement
-> Routing`

Routing outcomes remain:

- GRI-native;
- frontier-delegated;
- hybrid;
- clarification-required;
- blocked.

CRIDM does not select among them.

## 20. Requirement and Governance

A requirement may contain authorization-sensitive actions or constraints.

However, representing a requirement does not authorize execution.

For example:

`Requirement: "Delete X"`

does not imply:

`Authorized Action: Delete X`

Authorization remains governed by the appropriate governance and execution layers.

## 21. Requirement and Persistent Cognition

Requirement identification is non-mutating.

The following path is prohibited:

`Requirement -> PCG Mutation`

Persistent cognition can only change through the existing governed path:

`Evidence -> Proposal -> Governance -> Kernel -> PCG`

An interaction requirement may eventually produce a cognitive proposal, but that is a later stage.

## 22. Requirement Representation in ICG

The current requirement can be represented in the ICG as a Context Node.

Conceptually:

`Requirement
-> ICG Context Node
-> Requirement Dependencies
-> Retrieval Seeds
-> Processing`

The ICG may also contain:

- unresolved requirement elements;
- candidate interpretations;
- evidence requirements;
- capability requirements;
- clarification candidates.

These remain temporary.

## 23. Requirement Validation

Before retrieval begins, CRIDM should validate:

1. Is there an identifiable objective?
2. Are required targets sufficiently identified?
3. Are critical constraints known?
4. Is temporal scope adequate for the requested operation?
5. Are evidence requirements explicit where required?
6. Are there unresolved ambiguities that materially affect processing?
7. Are dependencies represented?
8. Are capability requirements identifiable where relevant?

A failed validation does not automatically mean the interaction is invalid.

It may mean:

`Clarification Required`

or:

`Continue With Explicit Uncertainty`

depending on the requirement.

## 24. Requirement State

A requirement may have temporary processing states:

- received;
- parsed;
- identified;
- decomposed;
- validated;
- partially_resolved;
- ambiguous;
- clarification_required;
- ready_for_retrieval;
- processing;
- revised;
- completed;
- blocked.

These states describe processing, not truth or persistent cognition.

## 25. Multiple Requirements

A single interaction may contain multiple requirements.

The Cognitive Instance should preserve:

- requirement identity;
- dependencies;
- shared context;
- independent ambiguity;
- processing status;
- result dependencies.

One unresolved requirement should not automatically invalidate unrelated requirements.

For example:

`R1 = explain X`

may proceed even if:

`R2 = compare X with unknown Y`

requires clarification.

This supports partial progress without guessing.

## 26. Requirement Priority

Requirement priority may be influenced by:

- explicit user ordering;
- dependency structure;
- active goal relevance;
- safety/security constraints;
- processing dependencies;
- salience.

Priority is not truth.

Priority does not authorize an action.

The exact prioritization mechanism remains open.

## 27. Requirement Provenance

Each requirement and decomposed sub-requirement should preserve temporary provenance sufficient to answer:

- which interaction produced it;
- which communication segment supports it;
- which elements were explicit;
- which elements were derived from established context;
- which elements remain inferred or unresolved;
- what clarification changed it;
- what processing stage consumed it.

Requirement provenance is interaction-processing history.

It is not automatically CSTR.

## 28. No-Guessing Invariants

CRIDM v0.1 establishes:

1. Requirement identification is not truth determination.
2. Requirement is not belief.
3. Inferred requirement elements are not automatically explicit.
4. Ambiguity remains explicit.
5. Missing task information is not silently invented.
6. An unresolved target is not an established identity.
7. Requirement decomposition does not create persistent relationships.
8. Requirement completeness is stage-dependent.
9. Requirement validation does not authorize action.
10. Requirement state does not imply truth.
11. Frontier output may revise a requirement but does not automatically define it.
12. Requirement identification does not mutate PCG.
13. Clarification is distinct from assumption.
14. Multiple requirements may proceed independently where dependencies permit.

## 29. Architectural Invariants

1. A structured requirement precedes PCG relevance retrieval.
2. Retrieval relevance is evaluated against the requirement.
3. Sufficiency is evaluated against the requirement.
4. Routing uses requirement and sufficiency context.
5. Requirement identification remains non-mutating.
6. Requirement provenance distinguishes explicit, contextual, inferred, and unresolved elements.
7. Requirement ambiguity can trigger clarification.
8. New information can revise the requirement.
9. Frontier output re-enters requirement evaluation.
10. Requirement representation never bypasses Governance for action or persistent cognitive change.

## 30. Canonical End-to-End Flow

`Incoming Communication
-> Communication Envelope
-> Cognitive Instance
-> Curiosity
-> Requirement Identification
-> Requirement Decomposition
      |
      +-- Complete enough
      |      |
      |      v
      |   PCRRM
      |      |
      |      v
      |   ICSM
      |      |
      |      v
      |   Gap Identification
      |      |
      |      v
      |   Routing
      |
      +-- Ambiguous / Missing
             |
             +--> Clarification
             |       |
             |       v
             |   New Information
             |       |
             |       +--> Same GRI Process
             |
             +--> Explicit Uncertainty
`

After processing:

`Evidence -> Proposal -> Governance -> Kernel -> PCG + CSTR`

If frontier processing occurs:

`Frontier -> New Information -> Requirement Evaluation -> PCRRM -> ICSM -> Routing`

## 31. Open Questions

CRIDM v0.1 intentionally leaves open:

- exact task ontology;
- requirement parsing implementation;
- natural-language semantic parsing;
- whether frontier models may assist requirement interpretation;
- requirement ambiguity thresholds;
- requirement priority algorithm;
- dependency representation;
- multi-turn requirement merging;
- requirement versioning;
- clarification generation;
- capability ontology;
- temporal-expression normalization;
- multilingual requirement representation;
- structured requirement serialization;
- interaction between requirement salience and cognitive dimensions;
- requirement conflict resolution.

These should be resolved through architecture, experiments, and implementation evidence.

## 32. Core Principle

> **Before GRI asks “What do I know?”, it must establish “What am I being asked to determine or accomplish?”**

The requirement layer therefore becomes the semantic starting point for relevance retrieval, sufficiency evaluation, routing, and eventual governed cognition.
