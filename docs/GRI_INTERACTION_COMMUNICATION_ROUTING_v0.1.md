# GRI Interaction Communication & Routing Layer v0.1

**Status:** Foundational architecture specification  
**Version:** 0.1  
**Scope:** External communication, protocol normalization, frontier-model delegation, GRI routing

## 1. Purpose

GRI may be connected to third-party frontier models. It therefore requires an explicit boundary between external communication, GRI cognition, and delegated foundation-model processing.

This layer defines that boundary.

For v0.1, the provisional name is **GRI Interaction Communication & Routing Layer (ICRL)**.

The ICRL is responsible for:

- converting incoming communication into a structured GRI communication envelope
- identifying the interaction
- separating protocol/transport handling from cognition
- deciding what information should be processed by GRI
- deciding what information should be delegated to a frontier model
- supporting hybrid processing
- receiving frontier-model output back into GRI
- preventing frontier-model output from directly becoming persistent cognition

JSON is treated as the initial serialization format, not as the cognitive architecture itself.

## 2. Existing Evidence

The individual mechanisms used by this architecture are established.

Semantic LLM routers already route requests among different models using heuristics, embeddings, classifiers, and other signals. Research also describes routers that dynamically select among heterogeneous LLMs or alternate between an LLM and a stronger agent. citeturn0search0turn0academia24turn1search24

Model Context Protocol (MCP) provides a standardized way for applications to expose tools, resources, and prompts to models and separates context provision from model interaction. It does not define GRI-style persistent cognition or a constitutional decision about which parts of an interaction belong to the system's own cognitive process. citeturn0search2turn0search3

Therefore the GRI proposal should not claim that model routing itself is new.

The potentially distinctive architectural combination is:

External Communication
-> GRI-owned communication normalization
-> GRI cognitive routing
-> selective frontier-model delegation
-> frontier output re-entry
-> evidence/interpretation validation
-> persistent cognitive processing

The exact GRI routing policy remains a research contribution to be experimentally validated rather than claimed as novel solely from architecture.

## 3. Communication Envelope

Every external interaction first enters a normalized GRI communication envelope.

Conceptually:

Communication Envelope =
(
interaction_id,
timestamp,
source,
channel,
payload,
message_type,
conversation_reference,
provenance,
security_metadata
)

The envelope is an interface representation.

It is not itself cognition.

The raw communication remains associated with TCM.

## 4. Protocol vs Cognitive Representation

GRI must maintain a distinction between:

- **communication protocol** — how external information is represented and exchanged
- **cognitive representation** — how information is represented for cognition

The existing CRP is a cognitive representation protocol.

The ICRL may use a separate communication envelope/protocol.

Therefore:

Communication Protocol != CRP

JSON is only the initial serialization mechanism.

## 5. First Event of a New Interaction

The canonical first-stage lifecycle is:

External Environment
-> Communication Reception
-> Communication Envelope
-> Interaction Identification
-> Cognitive Instance Creation
-> Curiosity Activation
-> Cognitive Routing

Protocol normalization occurs before cognitive interpretation.

The act of converting communication to JSON does not mean GRI has understood the content.

## 6. Interaction Identification

GRI must determine whether incoming communication is:

1. a continuation of an existing interaction/conversation
2. a new interaction
3. new information within an existing conversation
4. an interaction that references existing persistent cognition
5. an interaction whose relationship to prior cognition is unresolved

This classification is itself not allowed to silently create persistent facts.

If classification is uncertain, the uncertainty remains explicit.

## 7. Cognitive Routing Decision

After protocol normalization and interaction-instance creation, GRI decides how the communication should be processed.

The routing outcome may be:

- **GRI-native** — process primarily through GRI cognitive machinery
- **Frontier-delegated** — send selected information to a third-party frontier model
- **Hybrid** — retain selected information in GRI while delegating selected portions to a frontier model
- **Clarification-required** — request missing information before continuing
- **Blocked** — governance/security/protocol constraints prevent delegation or processing

Routing is a GRI control decision.

A frontier model must not be allowed to decide that it should receive unrestricted GRI state.

## 8. Selective Delegation

The routing mechanism determines which portion of communication may be delegated.

Conceptually:

Interaction
-> Segment / Classify Information
-> Routing Decision
-> GRI Processing Set
-> Frontier Delegation Set
-> Hybrid Execution

The delegation decision may consider:

- task type
- required reasoning capability
- available GRI cognition
- evidence requirements
- privacy/security constraints
- data sensitivity
- goal relevance
- latency/cost
- model capability
- whether the task requires external knowledge
- whether GRI already has sufficient persistent cognition

The exact routing policy is open.

## 9. GRI State Access Boundary

A frontier model does not receive the entire PCG by default.

When external reasoning requires persistent cognition, GRI retrieves the minimum relevant evidence/context from PCG and supplies only the authorized context.

Conceptually:

PCG
-> Relevance Retrieval
-> Evidence / Context Selection
-> Governance / Access Check
-> Frontier Context

This creates a least-context principle:

> A frontier model receives only the cognitive context required for the delegated task.

## 10. When GRI Reads Persistent Cognition

The interaction instance accesses persistent cognition when:

- evidence is required for a decision
- prior knowledge is relevant to interpreting the current interaction
- the system must determine whether information is already known
- a relationship or dimension must be evaluated
- new information may need to be reconciled with existing cognition
- the system needs to preserve or update persistent information
- a goal requires historical context

PCG retrieval is therefore demand-driven rather than automatically loading the entire persistent graph.

## 11. Curiosity and Routing

Curiosity is the first cognitive dimension activated for a new interaction.

Curiosity evaluates whether the interaction contains:

- something already known
- something partially known
- something unknown
- something ambiguous
- something potentially valuable to investigate

This supports:

Known -> use existing cognition

Partially Known -> retrieve relevant cognition + investigate missing portion

Unknown -> investigate / seek information

Ambiguous -> clarify or investigate

Curiosity does not establish the external-world truth of the unknown item.

## 12. Frontier Model as External Cognitive Processor

A frontier model is treated as an external reasoning/interaction processor.

It may:

- interpret language
- generate candidate reasoning
- summarize
- transform content
- answer questions
- propose hypotheses
- perform specialized reasoning

Its output is not automatically trusted as persistent cognition.

The output returns through the ICRL:

Frontier Model
-> Frontier Response Envelope
-> GRI Validation
-> Interpretation / Evidence Classification
-> ICG
-> Candidate / Proposal
-> CCA

## 13. Frontier Response Re-entry

Every frontier response becomes external input to GRI's cognitive architecture.

Conceptually:

Frontier Output
-> Structural Validation
-> Provenance Attachment
-> Evidence / Interpretation Classification
-> ICG Integration
-> Cognitive Evaluation

The provenance must identify:

- originating interaction
- frontier provider
- model identity where available
- request/delegation reference
- timestamp
- delegated input reference
- response reference

The response may be useful evidence about what the model produced, but model output is not automatically evidence that an external-world proposition is true.

## 14. Frontier Output Is a Proposal Source, Not a State Writer

The boundary is:

Frontier Model
-> Candidate / Interpretation / Proposal
-> GRI Governance
-> Cognitive Kernel
-> PCG

Never:

Frontier Model
-> PCG

This preserves the GRI invariant:

> Foundation models may propose cognition; GRI owns cognition.

## 15. Multiple Frontier Calls

An interaction may require multiple frontier-model calls.

The cognitive instance remains the owner of the interaction lifecycle.

Conceptually:

Interaction Instance
-> Route
-> Frontier Call 1
-> Re-enter GRI
-> Evaluate
-> Frontier Call 2 if required
-> Re-enter GRI
-> ...
-> Consolidation Ready

A frontier model therefore participates in a controlled cognitive loop rather than owning the conversation state.

## 16. Output Routing

GRI also controls what happens to the result after frontier processing.

Possible outcomes:

- return directly to the external user
- use internally as evidence/interpretation input
- request another frontier call
- request clarification from the external environment
- produce a cognitive proposal
- produce no persistent cognitive change
- route to another permitted processor

The external answer and persistent cognition are separate outputs.

A response can be returned to the user without becoming persistent belief.

## 17. Interaction Instance Ownership

The interaction instance owns the orchestration context for one interaction.

It contains references to:

- interaction_id
- communication envelope
- ICG
- active dimensions
- retrieved PCG references
- routing decisions
- frontier delegation records
- returned frontier outputs
- candidates
- proposals
- consolidation state

It does not own persistent cognition.

## 18. Exact Handoff to CCA

The interaction instance hands control to CCA when the current interaction has reached **consolidation readiness**.

Consolidation readiness occurs when:

1. required interaction processing for the current decision is complete;
2. required frontier-model calls, if any, have completed or been intentionally terminated;
3. relevant persistent cognition has been retrieved where needed;
4. relevant evidence has been explicitly identified;
5. candidate cognitive consequences have been evaluated;
6. any resulting proposals are structurally complete; and
7. GRI can state either:
   - a candidate/proposal requiring consolidation evaluation, or
   - that no persistent cognitive consequence is currently justified.

This means CCA is not triggered merely because a message arrived.

The interaction may loop through GRI and frontier models several times before consolidation readiness.

The canonical handoff is:

Interaction Instance
-> ICG
-> Routing / Frontier Loop
-> Evidence Evaluation
-> Proposal or Explicit Null
-> **CCA**

## 19. Null Handoff

CCA must also receive explicit null outcomes when processing has concluded but no persistent change is justified.

Examples:

- information already known
- insufficient evidence
- ambiguity remains
- low salience
- frontier output not sufficiently grounded
- no meaningful cognitive consequence
- governance cannot authorize the proposed change

A null result preserves:

PCG_(t+1) = PCG_t

where applicable.

## 20. Communication Output

After cognitive processing, GRI may construct an external response.

The response path is:

PCG / ICG / reasoning result
-> Response Formation
-> Communication Envelope
-> External Environment

The response is an outward communication event.

It does not automatically become a persistent belief.

## 21. Security and Governance Boundary

The ICRL must eventually support policies for:

- data minimization
- frontier-provider authorization
- sensitive-data exclusion
- context access
- provider/model selection
- delegation limits
- output validation
- auditability
- provenance
- user/tenant boundaries
- constitutional restrictions

These are architecture requirements, but their detailed policy definitions remain open.

## 22. Architectural Invariants

1. Every external interaction is normalized before cognitive processing.
2. Communication serialization is not cognition.
3. New interactions create a cognitive instance.
4. Curiosity activates first.
5. PCG is accessed on cognitive need, not automatically in full.
6. Frontier models receive only authorized relevant context.
7. Frontier outputs re-enter GRI as external model outputs.
8. Frontier outputs cannot directly mutate PCG.
9. GRI controls delegation and response routing.
10. Multiple frontier calls may occur within one interaction instance.
11. CCA receives control only at consolidation readiness.
12. Null consolidation is valid.
13. Persistent cognition remains governed and traceable.
14. The communication protocol and CRP remain separate concerns.
15. Unknown remains unknown.

## 23. Open Questions

- final name and specification of the communication protocol
- exact JSON envelope
- segmentation method
- deterministic versus learned routing
- whether routing itself is a cognitive dimension/process
- privacy classification
- frontier-provider capability registry
- context minimization algorithm
- routing confidence representation
- frontier response trust/evidence model
- output validation model
- delegation cost/latency policy
- multi-model parallelism
- interruption/cancellation
- recursive routing
- routing audit record
- relationship between routing history and CSTR

## 24. Architectural Summary

The new boundary is:

External Environment
-> GRI Communication Envelope
-> Interaction Instance
-> Curiosity
-> Cognitive Routing
-> {GRI Processing | Frontier Model | Hybrid}
-> Frontier Output Re-entry
-> ICG
-> Evidence / Proposal
-> CCA
-> Governance
-> Kernel
-> PCG + CSTR

The central principle is:

> GRI decides what cognition it owns, what reasoning it delegates, what information crosses the delegation boundary, and what returned information is allowed to influence persistent cognition.
