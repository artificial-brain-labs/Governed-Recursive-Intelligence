# GRI Cognitive Instance Lifecycle v0.1

**Status:** Foundational architecture specification  
**Version:** 0.1  
**Depends on:** ICRL v0.1, ICG v0.1, CCA v0.1, PCG Ontology v0.1, CSTR v0.1, Governed Transition Pipeline v0.1

## 1. Purpose

The **Cognitive Instance (CI)** is the temporary orchestration unit through which GRI processes one interaction from communication reception through cognitive evaluation and, when appropriate, consolidation handoff.

The Cognitive Instance is not persistent cognition and is not itself a cognitive dimension.

It coordinates:

- normalized communication
- interaction identification
- Curiosity activation
- relevant persistent-cognition retrieval
- interaction-scoped cognitive processing
- cognitive routing
- selective frontier-model delegation
- frontier-output re-entry
- evidence and candidate evaluation
- proposal formation
- explicit null determination
- consolidation readiness
- handoff to CCA
- interaction closure

The central architectural model is:

`External Communication
-> ICRL
-> Cognitive Instance
-> ICG
-> Routing / Frontier Loop
-> Evidence / Proposal or Explicit Null
-> CCA
-> Governance
-> Cognitive Kernel
-> PCG + CSTR`

The Cognitive Instance owns the **process**, not the persistent cognitive state.

---

## 2. Core Definition

A Cognitive Instance is a bounded, interaction-scoped processing context created for a specific interaction.

Conceptually:

`CI_i = (instance_id, interaction_id, communication, ICG_i, active_dimensions, retrieval_context, routing_history, frontier_history, candidates, proposals, processing_state)`

The instance exists to answer:

> What does GRI need to do with this interaction before deciding whether any persistent cognition should change?

It does not answer:

> What persistent cognition exists now?

That remains the responsibility of PCG.

---

## 3. Interaction ID vs Cognitive Instance ID

These identifiers are intentionally distinct.

### Interaction ID

`interaction_id` identifies the external interaction or conversation context.

It may represent:

- a single incoming interaction
- a multi-turn conversation
- a continuation of an established conversation

Its semantics belong to the communication layer.

### Cognitive Instance ID

`instance_id` identifies the GRI cognitive-processing lifecycle associated with a processing occurrence.

The instance owns the temporary orchestration state for that lifecycle.

Therefore:

`interaction_id != instance_id`

One interaction may produce more than one cognitive-processing instance when architecture or lifecycle boundaries require a new processing context.

The exact policy for instance reuse across multi-turn conversations remains open.

---

## 4. Relationship to Major GRI Components

The Cognitive Instance sits between communication/routing and consolidation.

### ICRL

ICRL normalizes communication and establishes the interaction context.

### TCM

TCM retains temporary raw communication/experience.

TCM answers:

> What happened?

The Cognitive Instance may reference TCM content but does not redefine TCM as persistent cognition.

### ICG

The Cognitive Instance owns or coordinates the interaction-scoped ICG.

ICG answers:

> What cognitive structures are currently participating in this interaction?

### PCG

PCG provides persistent cognition when relevant.

The Cognitive Instance retrieves only the relevant persistent structures required for current processing.

It never directly mutates PCG.

### CSTR

CSTR records governed persistent-state transition history.

The Cognitive Instance may contribute transition context, but it does not create authoritative persistent transitions independently of the governed pipeline.

### CCA

CCA receives the interaction when consolidation readiness has been reached.

CCA determines how candidate consequences proceed toward governed consolidation.

---

## 5. Creation

The canonical creation sequence is:

`External Environment
-> Communication Reception
-> Communication Envelope
-> Interaction Identification
-> Cognitive Instance Creation`

The instance is created only after communication has been normalized into the GRI communication envelope.

Protocol conversion is not cognitive interpretation.

JSON serialization therefore occurs before the Cognitive Instance begins cognitive processing.

---

## 6. Initial Cognitive State

Immediately after creation, the instance establishes:

- instance identity
- interaction identity
- communication reference
- interaction context
- ICG
- processing state
- initial uncertainty
- initial routing context

The first cognitive dimension activated for a new interaction is **Curiosity**.

Canonical sequence:

`New Interaction
-> Cognitive Instance
-> Curiosity Activation
-> Context Evaluation`

Curiosity has the highest initial weight among cognitive dimensions according to the current architectural decision.

This weight indicates priority/importance in the cognitive architecture.

It does not mean Curiosity is the strongest source of truth or that it can override governance.

---

## 7. Curiosity as Initial Cognitive Trigger

Curiosity evaluates whether the interaction is:

- already known
- partially known
- unknown
- ambiguous
- potentially important to investigate

Conceptually:

`Interaction
-> Curiosity
-> Compare Against Relevant Cognition
-> Known / Partially Known / Unknown / Ambiguous`

The consequences are:

### Known

Use relevant existing cognition where sufficient.

### Partially Known

Retrieve relevant cognition and investigate the missing portion.

### Unknown

Investigate, seek information, or delegate reasoning where appropriate.

### Ambiguous

Seek clarification or perform additional investigation.

The invariant is:

`Unknown -> Curiosity -> Investigation`

not:

`Unknown -> Curiosity -> Assumed Fact`

Curiosity therefore controls exploration, not truth.

---

## 8. Curiosity Activation of Other Dimensions

Curiosity may activate other cognitive dimensions through relationships.

Conceptually:

`Curiosity
-> Related Dimension Relationship
-> Candidate Dimension Activation
-> Dimension Evaluation`

Examples may include:

- Curiosity -> Relevance
- Curiosity -> Concept Formation
- Curiosity -> Trust
- Curiosity -> Goal Relevance

These are architectural examples, not fixed relationship definitions.

The relationship model must eventually specify:

- source dimension
- target dimension
- relationship type
- direction
- activation semantics
- possible influence
- local constraints

Activation does not automatically change a dimension's persistent value.

---

## 9. Persistent Cognition Access

The Cognitive Instance accesses PCG when persistent cognition is needed for the current decision.

Typical triggers include:

1. determining whether information is already known;
2. retrieving evidence relevant to interpretation;
3. resolving relevant prior context;
4. evaluating an existing relationship;
5. evaluating a cognitive dimension;
6. reconciling new information with existing cognition;
7. determining whether a candidate is genuinely new;
8. preserving information that may have persistent relevance;
9. evaluating goal relevance;
10. supplying authorized context to a frontier model.

The complete PCG is not automatically loaded.

Conceptually:

`Cognitive Need
-> Relevance Retrieval
-> Evidence / Context Selection
-> Governance / Access Check
-> Instance Context`

---

## 10. Interaction Cognitive Graph

Each Cognitive Instance receives a distinct interaction-scoped cognitive workspace:

`CI_i -> ICG_i`

The ICG may contain:

- persistent reference nodes
- candidate nodes
- evidence nodes
- interpretation nodes
- context nodes
- activated dimensions
- temporary relationships
- candidate impact paths
- reasoning dependencies

The ICG is not a copy of PCG.

It contains only the structures relevant to current processing.

Graph expansion does not imply persistence.

---

## 11. Internal Cognition Before Frontier Delegation

Before the Cognitive Instance delegates any information or subtask to a frontier model, GRI must first evaluate relevant internal persistent cognition.

The canonical decision sequence is:

Interaction -> Curiosity -> Relevant PCG Retrieval -> Internal Cognition Sufficiency Evaluation -> Routing Decision

The internal check asks:

1. What relevant cognition already exists?
2. Is that cognition sufficient for the current goal or task?
3. What information, reasoning capability, or transformation is actually missing?
4. Can GRI resolve the missing requirement through its own cognitive machinery?
5. If not, is frontier delegation justified?
6. If delegation is justified, what minimum authorized information should cross the boundary?

Therefore:

Internal Cognition Sufficient -> GRI-native processing

Internal Cognition Insufficient -> Determine Missing Requirement -> Consider Frontier Delegation

Importantly:

Not Found in PCG != Automatically Send to Frontier

Absence of a retrieved item may represent unknown information, retrieval failure, unresolved identity, insufficient indexing, or a genuinely external-knowledge requirement. These states must remain distinguishable.

Frontier delegation is therefore a second-stage capability decision, not the default response to missing information.

### Internal Cognition Check Before Delegation

The Cognitive Instance must not send an interaction to a frontier model merely because a frontier model is available or because the information is not immediately present in the first retrieved PCG context.

The internal evaluation should determine whether:

- existing beliefs or concepts are sufficient;
- existing relationships or dimensions provide the required context;
- additional PCG retrieval may resolve the requirement;
- the task can be completed through GRI-native reasoning;
- current knowledge may be stale or insufficient for the requested task;
- external knowledge or specialized reasoning is genuinely required;
- clarification is preferable to delegation.

Only after this evaluation should the routing decision select:

- GRI-native;
- frontier-delegated;
- hybrid;
- clarification-required; or
- blocked.

### Delegation Boundary

When frontier delegation is selected:

GRI Internal Cognition Check -> Missing Requirement -> Delegation Decision -> Context Minimization -> Governance / Access Check -> Frontier Model

The frontier model receives only the authorized context required for the delegated task.

This establishes the architectural invariant:

> Internal Cognition Before External Delegation: GRI must evaluate relevant internal cognition before delegating to a frontier model and must delegate only when additional external capability or information is justified by the current interaction.

## 12. Cognitive Routing

After initial Curiosity evaluation, the Cognitive Instance determines how processing should proceed.

Possible routing outcomes are:

- GRI-native
- Frontier-delegated
- Hybrid
- Clarification-required
- Blocked

The routing decision may consider:

- cognitive requirements
- available persistent cognition
- evidence requirements
- uncertainty
- task type
- external knowledge requirements
- frontier-model capability
- privacy/security constraints
- data sensitivity
- goal relevance
- latency/cost
- governance constraints

The exact routing policy remains a research/implementation question.

The important architectural rule is:

> Routing is controlled by GRI; a frontier model does not decide what GRI state it receives.

---

## 13. Frontier Delegation

When delegation is permitted, the Cognitive Instance creates a bounded delegation request.

Conceptually:

`CI
-> Delegation Decision
-> Authorized Context Selection
-> Frontier Request
-> Frontier Model`

The request must carry sufficient provenance to reconstruct:

- interaction
- instance
- delegation request
- authorized context
- originating task
- provider/model where available

The frontier model does not receive unrestricted PCG.

Only the minimum authorized context required for the delegated task should cross the boundary.

---

## 14. Frontier Output Re-entry

A frontier response is treated as **new information entering GRI**, not as an authoritative result.

It must re-enter the same GRI cognitive process used for other incoming information.

The canonical path is:

`Frontier Model
-> Frontier Response Envelope
-> New Information Re-entry
-> Curiosity / Context Evaluation
-> Relevant PCG Retrieval
-> Internal Cognition Sufficiency Evaluation
-> Interpretation / Evidence Classification
-> ICG Integration
-> Routing if Required
-> Candidate / Proposal / Explicit Null`

Frontier output is never automatically persistent cognition.

The fact that GRI requested the response does not increase its truth status.

`Frontier Output -> New Information -> Same GRI Process`

not:

`Frontier Output -> Direct Persistent Cognition`

A model response may be:

- an interpretation
- a transformation
- a candidate hypothesis
- a reasoning result
- an answer
- a proposal source
- evidence about what the model produced

It is not automatically evidence that an external-world proposition is true.

---

## 15. Re-entrant Processing Loop

A Cognitive Instance may execute multiple processing cycles.

Conceptually:

`CI
-> Route
-> GRI Processing and/or Frontier Call
-> Re-entry
-> Evaluate
-> Route Again if Required
-> Re-entry
-> ...
-> Consolidation Readiness`

This permits iterative reasoning without transferring ownership of the interaction to the frontier model.

The instance remains the orchestration owner throughout the loop.

A frontier model may therefore contribute reasoning repeatedly while GRI retains:

- cognitive state ownership
- context access control
- evidence classification
- proposal authority
- governance boundary
- consolidation authority

---

## 16. Candidate and Proposal Formation

The Cognitive Instance may construct temporary candidates.

A candidate is not persistent cognition.

The conceptual path is:

`Experience
-> Interpretation
-> Evidence
-> Candidate Consequence
-> Proposal
-> Governance
-> Kernel
-> Persistent State`

A proposal may request:

- create
- modify
- reinforce
- weaken
- remove

The exact target may be a:

- belief
- concept
- relationship
- goal
- dimension
- learning state

The Cognitive Instance cannot bypass Governance or the Cognitive Kernel.

---

## 17. Explicit Null Outcome

The Cognitive Instance must be capable of concluding:

> No persistent cognitive consequence is currently justified.

This is a valid processing result.

Examples include:

- information already known
- insufficient evidence
- unresolved ambiguity
- low salience
- redundant information
- frontier output insufficiently grounded
- no meaningful cognitive consequence
- governance-related inability to proceed

A null outcome means, where applicable:

`PCG_(t+1) = PCG_t`

The null result must remain distinguishable from:

- processing failure
- missing data
- abandoned processing
- system crash
- governance rejection
- unresolved proposal

Where a governed evaluation has occurred, the relevant history belongs in CSTR.

---

## 18. Processing State Machine

The conceptual lifecycle is:

`created
-> envelope_ready
-> interaction_identified
-> curiosity_active
-> context_evaluation
-> processing
-> routing
-> delegated_processing [optional]
-> reentry_validation [optional]
-> evidence_evaluation
-> proposal_ready OR null_ready
-> consolidation_ready
-> handed_to_cca
-> closed`

Alternative controlled paths include:

`context_evaluation -> clarification_required`

`routing -> blocked`

`processing -> terminated`

`delegated_processing -> delegation_failed`

These states describe processing status.

They do not represent truth, confidence, or persistent cognitive strength.

The exact runtime state machine and recovery semantics remain implementation work.

---

## 19. What Processing Complete Means

Processing is complete for the current interaction decision when GRI can establish all of the following:

1. the communication relevant to the current decision has been processed;
2. required interaction context has been established or explicitly marked unresolved;
3. required PCG retrieval has occurred where necessary;
4. required Curiosity-driven investigation has completed or been intentionally terminated;
5. required frontier calls have completed, failed in a handled way, or been intentionally terminated;
6. returned frontier outputs have re-entered GRI;
7. relevant evidence has been explicitly identified;
8. candidate cognitive consequences have been evaluated;
9. any resulting proposals are structurally complete; and
10. GRI can state either:
   - a candidate/proposal requires consolidation evaluation, or
   - no persistent cognitive consequence is currently justified.

Processing complete does not mean that a persistent change has been approved.

It means the interaction has reached a valid consolidation decision boundary.

---

## 20. Exact Handoff to CCA

The Cognitive Instance hands control to CCA only at **Consolidation Readiness**.

Canonical handoff:

`Interaction Instance
-> ICG
-> Routing / Frontier Loop
-> Evidence Evaluation
-> Proposal or Explicit Null
-> CCA`

CCA then performs the consolidation-stage process leading to:

`CCA
-> Governance
-> Cognitive Kernel
-> Persistent State / CSTR`

The Cognitive Instance must not treat CCA handoff as equivalent to approval.

CCA remains a consolidation boundary.

Governance remains the authorization boundary.

Kernel remains the persistent-state execution boundary.

---

## 21. Instance Ownership and Boundaries

The Cognitive Instance owns:

- interaction processing context
- ICG lifecycle
- routing decisions
- delegation history
- frontier response re-entry
- temporary candidate/proposal context
- processing state
- consolidation-readiness determination

The Cognitive Instance does not own:

- persistent PCG state
- constitutional authority
- final governance authorization
- authoritative persistent-state mutation
- the complete historical transition record

Therefore:

`Cognitive Instance != PCG`

`Cognitive Instance != Governance`

`Cognitive Instance != Cognitive Kernel`

`Cognitive Instance != CSTR`

---

## 22. Failure and Recovery Principles

Failure must not silently become cognition.

If a frontier call fails:

- do not treat the missing response as evidence;
- preserve the failure state;
- retry only under explicit routing policy;
- seek clarification where required;
- or terminate with an explicit non-consolidation outcome.

If PCG retrieval fails:

- do not assume the requested information is absent;
- represent retrieval failure explicitly;
- avoid converting uncertainty into a new fact.

If identity resolution is ambiguous:

- retain the ambiguity;
- request clarification or defer consolidation;
- do not silently create a persistent identity.

If processing is interrupted:

- the instance may be recoverable from its temporary state where supported;
- persistent cognition must remain governed and traceable;
- incomplete processing must not be interpreted as a completed null outcome.

---

## 23. No-Guessing Invariants

The Cognitive Instance inherits the GRI no-guessing principles:

1. Communication serialization != understanding.
2. Observation != interpretation.
3. Interpretation != evidence.
4. Evidence != belief.
5. Candidate != persistent object.
6. Proposal != commitment.
7. Curiosity != knowledge.
8. Salience != truth.
9. Reference != identity.
10. Frontier output != external-world truth.
11. Relationship influence != target mutation.
12. Unknown remains unknown.
13. Missing information is not silently inferred.
14. Processing failure != null cognitive outcome.
15. Null outcome != evidence of absence.

---

## 24. Architectural Invariants

1. Every new interaction creates a bounded cognitive-processing context.
2. Curiosity is the first cognitive dimension activated for a new interaction.
3. Curiosity has the highest initial dimension weight under the current architecture.
4. Curiosity may activate related dimensions through governed relationships.
5. PCG access is demand-driven.
6. Relevant internal cognition is evaluated before frontier delegation.
7. Initial absence from PCG does not automatically trigger frontier delegation.
8. Frontier delegation occurs only when additional capability or information is justified.
9. The complete PCG is not automatically exposed to frontier models.
7. Frontier delegation is controlled by GRI.
8. Frontier outputs always re-enter GRI before influencing persistent cognition.
9. Multiple frontier calls may occur within one instance.
10. The instance never directly writes PCG.
11. Persistent change occurs only through the governed transition path.
12. Explicit null processing is valid.
13. CCA receives control only at consolidation readiness.
14. Communication protocol and CRP remain separate.
15. TCM, ICG, PCG, and CSTR retain distinct responsibilities.
16. Unknown information remains unknown.
17. Every frontier response is reintroduced as new information and processed through the same GRI cognitive process.
18. Frontier output cannot bypass Curiosity, internal cognition evaluation, evidence evaluation, Governance, or the Cognitive Kernel.

---

## 25. Open Questions

The following are intentionally not fixed in v0.1:

- exact definition of an interaction boundary
- exact policy for creating a new instance within a multi-turn conversation
- instance persistence/recovery mechanism
- instance timeout and retention
- exact Curiosity activation function
- Curiosity-to-dimension relationship ontology
- routing algorithm
- routing confidence representation
- communication segmentation
- frontier provider/model capability registry
- context minimization algorithm
- frontier response evaluation
- parallel frontier calls
- cancellation semantics
- recursive delegation limits
- interaction-level concurrency
- candidate deduplication
- conflict resolution
- exact proposal readiness rules
- CCA handoff serialization
- instance audit representation

These should be resolved through architecture and experimentation rather than prematurely embedded in implementation technology.

---

## 26. Canonical Lifecycle

The complete v0.1 lifecycle is:

`External Environment
-> Communication Reception
-> GRI Communication Envelope
-> Interaction Identification
-> Cognitive Instance Creation
-> Curiosity Activation
-> Relevant PCG Retrieval
-> ICG Construction
-> Cognitive Routing
-> {GRI-native | Frontier | Hybrid | Clarification | Blocked}
-> Frontier Output Re-entry where applicable
-> Evidence Evaluation
-> Candidate Evaluation
-> Proposal OR Explicit Null
-> Consolidation Readiness
-> CCA
-> Governance
-> Cognitive Kernel
-> PCG + CSTR
-> External Response
-> Instance Closure`

The core principle is:

> The Cognitive Instance owns the interaction lifecycle, but never owns persistent cognition.

