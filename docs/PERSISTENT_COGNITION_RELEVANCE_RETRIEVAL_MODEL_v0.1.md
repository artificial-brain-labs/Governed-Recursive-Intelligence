# GRI Persistent Cognition Relevance Retrieval Model v0.1

**Status:** Foundational architecture specification  
**Version:** 0.1  
**Depends on:** PCG Ontology v0.1, Interaction Cognitive Graph v0.1, Cognitive Instance Lifecycle v0.1, Internal Cognition Sufficiency Model v0.1, Cognitive Dimension Model v0.1

## 1. Purpose

The **Persistent Cognition Relevance Retrieval Model (PCRRM)** defines how GRI identifies and retrieves the portions of the Persistent Cognitive Graph (PCG) that are relevant to the current interaction requirement.

It answers:

> Which existing persistent cognitive structures should participate in this interaction?

It does not answer:

> Is the retrieved cognition true?

It also does not determine whether the retrieved cognition is sufficient. That responsibility belongs to ICSM.

Therefore:

`Retrieval != Sufficiency != Truth`

## 2. Architectural Position

The canonical sequence is:

`Interaction
-> Curiosity
-> Requirement Identification
-> Relevance Retrieval
-> Internal Cognition Sufficiency Evaluation
-> Gap Identification
-> Routing`

PCRRM is therefore the bridge between the temporary Cognitive Instance and the persistent PCG.

Its purpose is to prevent two opposite failures:

1. retrieving too little cognition and incorrectly concluding that GRI does not know something;
2. retrieving too much cognition and exposing irrelevant persistent state to the current interaction.

## 3. Core Principle

> **GRI should retrieve cognition because it is relevant to the current cognitive requirement, not merely because it is available.**

Relevance is contextual.

The same PCG object can be highly relevant in one interaction and irrelevant in another.

## 4. Retrieval Is Not a Database Lookup

PCRRM is a cognitive architecture layer.

It does not prescribe:

- graph database technology;
- vector database technology;
- SQL;
- embedding search;
- a particular indexing algorithm;
- a particular ranking model.

Those are implementation mechanisms.

The architectural question is:

> What makes a persistent cognitive structure relevant?

Implementation technology must answer that question without changing its semantics.

## 5. Retrieval Context

Retrieval begins from a structured interaction requirement.

Conceptually:

`RetrievalContext =
(
interaction_id,
instance_id,
requirement,
goal_context,
active_dimensions,
current_entities,
current_concepts,
current_relationships,
temporal_requirements,
evidence_requirements,
processing_history,
security_context
)`

Not every field is required for every interaction.

The retrieval context itself is temporary and does not become persistent cognition merely because it is used for retrieval.

## 6. Requirement Decomposition

Before retrieval, the current requirement should be decomposed into relevant cognitive references where they are explicitly available.

Potential requirement elements include:

- explicit entity references;
- established identities;
- concepts;
- relationships;
- goals;
- active cognitive dimensions;
- known propositions;
- temporal requirements;
- evidence requirements;
- unresolved references;
- task/capability requirements.

The decomposition must preserve uncertainty.

If an entity cannot be resolved, PCRRM must not invent an identity merely to improve retrieval.

## 7. Retrieval Seed

Retrieval begins with one or more **retrieval seeds**.

A seed is an explicitly established or interaction-derived reference from which relevant PCG structures may be explored.

Possible seeds include:

- established persistent identity;
- established concept;
- explicit relationship;
- active goal;
- active cognitive dimension;
- governed belief relevant to the requirement;
- explicit provenance reference;
- interaction context with a known PCG association.

A textual mention is not automatically a persistent identity seed.

## 8. Relevance Sources

PCRRM recognizes several forms of relevance.

### 8.1 Direct Relevance

A PCG object directly represents the subject of the current requirement.

Example:

Requirement:
`What do we know about Identity-X?`

Relevant seed:

`Identity-X`

### 8.2 Relational Relevance

A PCG structure is relevant because it is connected to a directly relevant structure through an established cognitive relationship.

Example:

`Identity-X
-> works-with
-> Identity-Y`

When collaboration between X and Y is relevant, the relationship may justify retrieval of Identity-Y and associated relationship cognition.

Relational relevance must follow established PCG relationships.

It must not manufacture relationships merely because two objects appear semantically similar.

### 8.3 Goal Relevance

A structure may be relevant because it is connected to an active goal.

Example:

`Active Goal
-> Maintain reliable collaboration
-> relevant relationship / belief / dimension`

Goal relevance does not mean the retrieved structure is true or desirable.

It means the structure may affect current goal evaluation.

### 8.4 Dimension Relevance

A cognitive dimension may become relevant because the interaction activates that dimension.

Example:

`Relationship interaction
-> Curiosity
-> Trust activation
-> retrieve relevant Trust instances`

Dimension activation does not establish a new dimension value.

### 8.5 Evidence Relevance

A prior evidence or provenance reference may be relevant when evaluating an existing belief, relationship, dimension state, or contradiction.

Historical evidence should be retrieved as evidence/provenance, not silently promoted into a new observation.

### 8.6 Temporal Relevance

A structure may be relevant because its time context matches the requirement.

For example:

- historical cognition for a historical question;
- recent cognition for a recent-interaction question;
- current-state information where the requirement explicitly concerns the present.

Temporal relevance does not automatically establish freshness or truth.

ICSM evaluates temporal adequacy.

### 8.7 Contextual Relevance

A structure may be relevant because it shares an established interaction context, task context, or relationship context.

Contextual relevance must remain bounded.

A broad contextual connection is not sufficient reason to expose unrelated PCG content.

## 9. Relevance Is Not Similarity

Semantic similarity may be used as an implementation technique, but similarity alone must not define cognitive relevance.

For example:

Two concepts may be linguistically similar while having no established relationship in GRI cognition.

Therefore:

`Similarity != Cognitive Relevance`

An implementation may use similarity to discover candidates, but candidate relevance must subsequently be evaluated against the architectural relevance conditions.

This preserves the distinction between:

`Candidate Retrieval -> Relevance Evaluation -> Relevant PCG Reference`

## 10. Retrieval Layers

PCRRM uses bounded retrieval expansion.

### Layer 0 — Requirement

The current cognitive requirement.

### Layer 1 — Direct References

Retrieve directly referenced established PCG objects.

### Layer 2 — Immediate Relationships

Retrieve explicitly connected relationships and directly connected PCG objects when relevant to the requirement.

### Layer 3 — Goal / Dimension Context

Retrieve relevant active goals, dimensions, and their established relationships.

### Layer 4 — Supporting Cognition

Retrieve additional concepts, beliefs, evidence references, provenance, or relationship structures required to interpret the relevant structures.

### Layer 5 — Controlled Expansion

Expand further only when the current requirement cannot be evaluated adequately from the retrieved context.

The architecture does not require unrestricted graph traversal.

The exact expansion depth remains implementation-dependent.

## 11. Bounded Retrieval

Retrieval must be bounded by:

- current requirement;
- active goal context;
- relevant dimensions;
- established relationships;
- temporal needs;
- evidence requirements;
- security and access constraints;
- processing budget;
- recursion/expansion limits.

The objective is:

> enough relevant cognition to evaluate the requirement,

not:

> retrieve the entire PCG.

## 12. Relevance Evaluation

A candidate PCG structure should be evaluated against the current requirement.

Conceptually:

`Candidate
+
Requirement Context
+
Established Relationships
+
Goal Context
+
Temporal Context
+
Evidence Requirements
-> Relevance Evaluation`

Possible evaluation states include:

- relevant;
- potentially relevant;
- not relevant;
- unresolved relevance;
- inaccessible;
- retrieval error.

These are temporary evaluation states.

They do not modify the PCG.

## 13. Potentially Relevant

A candidate may be **potentially relevant** when available information suggests a meaningful connection but the connection is not sufficiently established.

Potential relevance must not be treated as established relevance.

For example:

`Semantic similarity -> Potential Candidate`

does not imply:

`Semantic similarity -> Cognitive Relationship`

Additional processing may determine whether the candidate should participate.

## 14. Relevance and No-Guessing

PCRRM inherits the core no-guessing principle.

It must not:

- create an identity to retrieve a better result;
- create a relationship to connect two candidates;
- convert similarity into a fact;
- convert a candidate into a persistent object;
- infer missing PCG state merely because retrieval would be easier.

Therefore:

`Missing Reference -> Unresolved Reference`

not:

`Missing Reference -> Assumed Identity`

## 15. Retrieval and Identity Resolution

Identity resolution is a separate cognitive problem.

PCRRM may retrieve:

- an established identity;
- multiple possible identity candidates;
- no established identity.

If multiple candidates are possible:

`Reference -> Multiple Candidates -> Ambiguous`

PCRRM must preserve the ambiguity.

It must not choose the most similar identity solely to complete retrieval.

## 16. Retrieval and Relationships

Relationships are first-class retrieval paths.

For example:

`Identity-A
-> works-with
-> Identity-B
`

may justify retrieval of Identity-B when the requirement concerns the established collaboration context.

However, the relationship itself must be retrieved and preserved as part of context.

A retrieved target without its relationship semantics may lose important cognitive meaning.

## 17. Retrieval and Dimensions

If an interaction activates a dimension, PCRRM may retrieve relevant dimension instances.

For example:

`Interaction
-> Trust-relevant context
-> Retrieve Trust Dimension Instances
-> Retrieve their relevant relationship context`

The retrieval of a Trust value does not mean the value should change.

PCRRM is read-oriented.

Any update remains:

`Evidence -> Proposal -> Governance -> Kernel -> PCG`

## 18. Retrieval and Goals

Goals affect what cognition is relevant.

Conceptually:

`Goal
-> Salience / Requirement Context
-> Relevant PCG Retrieval`

An active goal can increase the relevance of certain structures without changing those structures.

Goal relevance must not cause unrelated PCG content to be retrieved merely because it might be useful.

The retrieval boundary remains requirement-driven.

## 19. Retrieval and Evidence

Existing evidence may be retrieved to evaluate a belief or prior cognitive transition.

However:

`Historical Evidence != New Observation`

and:

`Retrieved Belief != Automatically Current Truth`

Evidence provenance must remain attached to the retrieved structure where required for later evaluation.

## 20. Retrieval Result

PCRRM produces a temporary retrieval result.

Conceptually:

`RelevantCognition =
(
retrieval_id,
requirement_reference,
selected_objects,
selected_relationships,
selected_dimensions,
supporting_evidence_references,
unresolved_candidates,
ambiguities,
retrieval_status,
expansion_history,
provenance
)`

The result may be inserted into the Cognitive Instance and represented through ICG persistent-reference nodes.

It does not become persistent cognition.

## 21. Retrieval Status

PCRRM should distinguish:

- complete;
- partial;
- no relevant cognition found;
- ambiguous;
- retrieval failure;
- access restricted.

These statuses must not be collapsed.

In particular:

`No Relevant Cognition Found != Retrieval Failure`

and:

`Retrieval Failure != Unknown`

The latter distinction is essential to ICSM.

## 22. Retrieval Completeness

Retrieval completeness is contextual.

A retrieval can be complete for the current requirement while not containing the entire PCG.

Therefore:

`Complete Retrieval != Complete PCG`

PCRRM should answer:

> Did the retrieval process satisfy the retrieval scope required for this evaluation?

It should not claim:

> No other relevant cognition exists anywhere in PCG

unless the architecture has actually established that fact through an appropriate exhaustive operation.

## 23. Retrieval and ICSM

PCRRM feeds ICSM.

The canonical relationship is:

`Requirement
-> PCRRM
-> Relevant Cognition
-> ICSM
-> Sufficiency State
-> Gap Identification
-> Routing`

ICSM may determine that retrieved cognition is insufficient and request additional retrieval.

Therefore retrieval can be iterative:

`Retrieval_1
-> Sufficiency Evaluation
-> Gap
-> Retrieval_2
-> Sufficiency Evaluation
-> ...`

The loop remains inside the Cognitive Instance.

## 24. Retrieval and Routing

PCRRM does not decide whether a frontier model is required.

For example:

`No Relevant Cognition Found`

may lead to:

- additional internal retrieval;
- clarification;
- explicit unknown;
- GRI-native investigation;
- frontier delegation;
- blocked processing.

The routing model owns that decision.

## 25. Retrieval and Frontier Delegation

If routing eventually selects frontier delegation, PCRRM helps determine which persistent context is relevant enough to cross the delegation boundary.

The sequence is:

`PCG
-> Relevant Retrieval
-> Context Minimization
-> Security / Governance Check
-> Frontier Context`

Not:

`PCG -> Entire PCG -> Frontier`

Relevant retrieval therefore also serves privacy and governance boundaries.

## 26. Frontier Output Re-entry

When frontier output returns, it becomes new information.

The new information starts the same process:

`Frontier Output
-> Requirement / Context Evaluation
-> Relevant PCG Retrieval
-> ICSM
-> Routing / Internal Processing
`

The retrieval result from the previous frontier request must not automatically be treated as sufficient for the returned information.

## 27. Retrieval Provenance

Each retrieval operation should preserve temporary provenance sufficient to answer:

- what requirement caused retrieval;
- which retrieval seeds were used;
- which PCG state/version was read;
- which paths or relationships justified expansion;
- what candidates were considered;
- what was selected;
- what remained unresolved;
- whether retrieval completed or failed;
- what security/access constraints applied.

Retrieval provenance is processing history.

It does not automatically become CSTR because retrieval itself is not a persistent cognitive transition.

## 28. Retrieval Does Not Mutate PCG

PCRRM is explicitly non-mutating.

The following path is prohibited:

`Retrieval -> PCG Mutation`

The valid architecture is:

`Retrieval
-> Cognitive Evaluation
-> Candidate / Proposal
-> Governance
-> Kernel
-> PCG`

This protects persistent cognition from retrieval-side effects.

## 29. Retrieval and Salience

Salience may influence which retrieved candidates receive further processing attention.

However:

`Salience != Relevance`

and:

`Salience != Truth`

A highly salient structure can still be irrelevant to the current requirement.

A relevant structure can have low salience but still be necessary.

Therefore salience is one input to processing prioritization, not the definition of relevance.

## 30. Retrieval and Curiosity

Curiosity can initiate retrieval by identifying an unknown or unresolved area.

The sequence is:

`Curiosity
-> Unknown / Question
-> Retrieval Seed
-> Relevant PCG Retrieval
-> Sufficiency Evaluation`

Curiosity cannot manufacture a retrieval seed by inventing an identity or relationship.

## 31. Retrieval Graph and ICG

Retrieved PCG structures enter the Cognitive Instance through persistent-reference nodes in the ICG.

Conceptually:

`PCG Object
-> Retrieval
-> Persistent Reference Node
-> ICG
-> Cognitive Processing`

The ICG reference should preserve:

- PCG object identity;
- state/version reference;
- relationship context where relevant;
- retrieval provenance.

The reference is not a copy that can independently mutate PCG.

## 32. Controlled Expansion

A retrieval expansion should have an explicit reason.

Possible reasons include:

- requirement dependency;
- established relationship;
- goal dependency;
- dimension dependency;
- evidence support;
- conflict investigation;
- identity resolution;
- temporal requirement.

Expansion without a reason should not be treated as cognitively justified.

This provides an architectural audit trail for why additional PCG context entered the interaction.

## 33. Retrieval Failure Recovery

If retrieval fails:

`Retrieval Failure -> Recovery Decision`

Possible actions include:

- retry;
- alternate retrieval mechanism;
- narrower retrieval;
- broader retrieval within authorization;
- use already retrieved context;
- request clarification;
- explicit degraded/unknown state;
- block processing.

Retrieval failure must never be silently converted into:

`No Cognition Exists`

## 34. Security and Access Boundary

Relevance does not override authorization.

A PCG object may be cognitively relevant but inaccessible to the current processing context.

Therefore:

`Relevant + Unauthorized -> Not Exposed`

Access restrictions remain distinct from absence.

A retrieval result should preserve the fact that access was restricted where that distinction affects subsequent reasoning.

## 35. Core No-Guessing Invariants

1. Retrieval is not truth evaluation.
2. Retrieval is not sufficiency evaluation.
3. Similarity is not cognitive relevance.
4. Candidate relevance is not established relationship.
5. Missing identity is not an assumed identity.
6. No relevant cognition found is not retrieval failure.
7. Retrieval failure is not knowledge absence.
8. Complete retrieval is not complete PCG.
9. Salience is not relevance.
10. Relevance is not truth.
11. Retrieved belief is not automatically current truth.
12. Historical evidence is not automatically a new observation.
13. Retrieval does not mutate PCG.
14. Retrieval does not authorize frontier delegation.
15. Relevant but unauthorized cognition must not cross the access boundary.
16. Frontier output re-enters the same retrieval process.
17. Unresolved relevance remains unresolved rather than being forced into a binary result.

## 36. Architectural Invariants

1. Retrieval begins from an explicit interaction requirement.
2. Retrieval uses relevant established seeds where available.
3. Relationship-aware expansion is permitted but bounded.
4. Goal and dimension context may influence retrieval.
5. Retrieval remains demand-driven.
6. Retrieval is non-mutating.
7. Retrieval results are temporary interaction context.
8. Retrieval status distinguishes absence, failure, ambiguity, and restriction.
9. PCRRM feeds ICSM but does not replace it.
10. ICSM may request additional retrieval.
11. Routing decides whether external delegation is required.
12. Frontier context is constructed from authorized relevant cognition.
13. Retrieved PCG references preserve state/version provenance.
14. The entire PCG is not assumed to be required for every interaction.

## 37. Canonical End-to-End Flow

`Incoming Interaction
-> Curiosity
-> Requirement Identification
-> Retrieval Seeds
-> PCG Relevance Retrieval
      |
      +-- Relevant cognition found
      |        |
      |        v
      |   ICG Persistent References
      |        |
      |        v
      |   Internal Cognition Sufficiency
      |
      +-- Partial / unresolved
      |        |
      |        v
      |   Controlled Retrieval Expansion
      |        |
      |        v
      |   Sufficiency Evaluation
      |
      +-- None found
      |        |
      |        v
      |   Routing / Investigation / Clarification
      |
      +-- Retrieval failure
               |
               v
          Recovery Decision
`

If additional information is obtained:

`New Information -> Same GRI Cognitive Process`

If a persistent consequence is eventually proposed:

`Evidence -> Proposal -> Governance -> Kernel -> PCG + CSTR`

## 38. Open Questions

PCRRM v0.1 intentionally leaves open:

- exact relevance scoring or symbolic evaluation;
- whether relevance should be deterministic, probabilistic, or hybrid;
- graph traversal algorithm;
- maximum expansion depth;
- retrieval budget;
- candidate ranking;
- semantic similarity implementation;
- embedding use;
- indexing architecture;
- temporal relevance computation;
- relationship traversal weighting;
- goal relevance propagation;
- dimension activation propagation;
- conflict-oriented retrieval;
- retrieval caching;
- concurrent retrieval isolation;
- retrieval consistency across PCG state versions;
- cryptographic retrieval provenance;
- privacy classification model;
- exact authorization mechanism;
- exhaustive retrieval semantics.

These should be resolved through architecture, experiments, and implementation evidence rather than arbitrary constants.

## 39. Core Principle

> **GRI should not retrieve everything it knows. It should retrieve what the current cognitive requirement gives it reason to consider—and it must preserve why that cognition was considered relevant.**

PCRRM therefore establishes the relevance boundary between persistent cognition and interaction-time cognition.
