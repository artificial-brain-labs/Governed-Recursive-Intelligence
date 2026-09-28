# GRI Cognitive Routing Decision Model v0.1

**Status:** Foundational architecture specification  
**Version:** 0.1  
**Depends on:** Cognitive Instance Lifecycle v0.1, ICRL v0.1, ICG v0.1, PCG Ontology v0.1, Cognitive Dimension Model v0.1

## 1. Purpose

The Cognitive Routing Decision determines how GRI should process information after the Cognitive Instance has activated Curiosity and evaluated relevant internal cognition.

The routing decision answers:

> Should GRI process this requirement internally, retrieve more internal cognition, ask for clarification, delegate selected work to a frontier model, use a hybrid path, or stop processing?

Routing is an orchestration decision. It is not a truth judgment and does not authorize persistent cognitive change.

## 2. Core Principle

The canonical sequence is:

`Interaction
-> Curiosity
-> Relevant PCG Retrieval
-> Internal Cognition Sufficiency Evaluation
-> Missing Requirement Identification
-> Routing Decision`

The fundamental invariant is:

> **Internal Cognition Before External Delegation.**

A frontier model is not the default fallback whenever GRI cannot immediately answer something.

## 3. Routing Input

The routing decision receives a structured routing context from the Cognitive Instance.

Conceptually:

`RoutingContext =
(
interaction_id,
instance_id,
current_information,
current_goal,
active_dimensions,
relevant_pcg_references,
known_state,
uncertainty,
evidence_state,
missing_requirements,
security_context,
available_capabilities,
processing_history
)`

The exact serialization remains open.

Routing must not require unrestricted access to the complete PCG.

## 4. Routing Questions

The router evaluates the following questions in sequence.

### Question 1 — What is the interaction asking GRI to accomplish?

Determine the current task or cognitive objective.

If the objective is unresolved and the missing information materially affects processing, clarification may be required.

### Question 2 — What relevant cognition already exists?

Retrieve relevant PCG structures where necessary.

Possible findings:

- sufficient existing cognition
- partially sufficient cognition
- relevant but stale/insufficient cognition
- no relevant cognition found
- retrieval failure
- unresolved identity/context

These states must remain distinct.

### Question 3 — Can GRI complete the requirement internally?

If existing cognition plus GRI-native processing is sufficient:

`Route -> GRI-native`

No frontier delegation is required.

### Question 4 — What exactly is missing?

If internal processing is insufficient, identify the missing requirement.

Examples:

- external/current information
- specialized reasoning
- language transformation
- complex generation
- additional interpretation
- clarification
- missing internal context
- another permitted processor

### Question 5 — Can the missing requirement be resolved without a frontier model?

Possible internal actions include:

- additional PCG retrieval
- ICG expansion
- relationship evaluation
- activation of another cognitive dimension
- additional evidence evaluation
- clarification
- another GRI-native processing step

If yes, routing remains inside GRI.

### Question 6 — Is frontier delegation justified?

Frontier delegation is justified only when the missing requirement genuinely benefits from an available external capability or information source and delegation is permitted by security/governance constraints.

## 5. Canonical Routing Outcomes

The router may produce one of five primary outcomes.

### 5.1 GRI-Native

GRI has sufficient cognition or native processing capability.

`Routing -> GRI Processing`

### 5.2 Frontier-Delegated

A bounded requirement is delegated to an authorized frontier model.

`Routing -> Context Selection -> Governance/Access Check -> Frontier`

### 5.3 Hybrid

GRI retains part of the processing while a selected portion is delegated.

`GRI Processing + Frontier Processing`

The two processing paths remain under the same Cognitive Instance.

### 5.4 Clarification-Required

The interaction cannot be processed safely or correctly without missing information from the external environment.

`GRI -> Clarification -> New Information Re-entry`

Clarification is not equivalent to frontier delegation.

### 5.5 Blocked

Processing or delegation is prohibited by governance, security, protocol, authorization, or other applicable constraints.

A blocked route does not create persistent cognition.

## 6. Internal Retrieval Before Delegation

The router must distinguish:

`PCG Not Found`

from:

`PCG Retrieval Failed`

from:

`PCG Contains Insufficient Knowledge`

from:

`PCG Contains Relevant Knowledge But Additional Capability Is Required`

These states have different routing consequences.

In particular:

`PCG Not Found != Frontier Required`

Additional internal retrieval may be appropriate.

## 7. Frontier Delegation Scope

When frontier delegation is selected, the router must identify the smallest useful delegation unit.

Conceptually:

`Interaction
-> Relevant Segment / Task
-> Missing Requirement
-> Delegation Scope
-> Authorized Context
-> Frontier Request`

The router should not delegate the complete interaction merely because one part requires external processing.

This supports selective delegation.

## 8. Context Minimization

Before a frontier request leaves GRI:

`PCG
-> Relevant Context Retrieval
-> Context Minimization
-> Security / Governance Check
-> Frontier Context`

The frontier model receives only the context authorized and required for the delegated task.

Unrelated PCG structures remain inside GRI.

## 9. Frontier Capability Selection

The router may select among authorized frontier models according to a capability registry.

Potential capability descriptors include:

- reasoning capability
- language capability
- modality
- external-knowledge capability
- specialized domain capability
- context capacity
- latency characteristics
- cost characteristics
- provider authorization
- privacy/security constraints

The architecture does not mandate a particular model-selection algorithm.

A model must never receive access merely because it has greater general capability.

## 10. Frontier Output Re-entry

Every frontier response is treated as **new information entering GRI**.

It follows the same cognitive processing principle:

`Frontier Output
-> New Information
-> Curiosity / Context Evaluation
-> Relevant PCG Retrieval
-> Internal Cognition Sufficiency Evaluation
-> Interpretation / Evidence Classification
-> ICG
-> Routing if Required
-> Candidate / Proposal / Explicit Null`

Therefore a frontier response may trigger another routing decision.

For example:

`Frontier Call 1
-> New Information
-> GRI Evaluation
-> Frontier Call 2
-> New Information
-> GRI Evaluation
-> ...`

The loop remains owned by the Cognitive Instance.

## 11. Frontier Output Truth Boundary

The router must never treat frontier output as automatically true.

The following are distinct:

- model produced a statement
- GRI has an interpretation of the statement
- the statement has supporting evidence
- GRI has accepted a governed belief

Therefore:

`Frontier Output != External-World Fact`

and:

`Frontier Output != Persistent Belief`

The response can become part of evidence processing only through the normal GRI evaluation path.

## 12. Routing and Cognitive Dimensions

Routing may activate or be influenced by cognitive dimensions.

For example:

- Curiosity identifies an unknown.
- Relevance determines whether investigation matters.
- Goal relationships determine whether the information affects an active goal.
- Trust may affect how a relationship-related interaction is evaluated.
- Other dimensions may identify task-specific cognitive requirements.

However, a dimension's activation or value must not directly bypass routing governance.

The relationship pattern remains:

`Dimension Change
-> Relationship Evaluation
-> Candidate Effect
-> Governance
-> Possible Update`

## 13. Routing Is Not Governance

Routing answers:

> Where should processing occur?

Governance answers:

> Is a proposed cognitive change permitted?

Therefore:

`Routing != Governance`

A route to a frontier model does not authorize a cognitive update.

A GRI-native route does not authorize a cognitive update.

Both paths eventually remain subject to evidence, proposal, governance, and the Cognitive Kernel when persistent cognition is involved.

## 14. Routing Is Not Evidence

A routing decision is not evidence about the external world.

For example:

`Route -> Frontier`

does not mean:

`External Proposition -> True`

Likewise:

`Route -> GRI-native`

does not mean:

`Internal Cognition -> Correct`

Routing determines processing strategy only.

## 15. Routing State

Each routing decision should preserve sufficient temporary history to answer:

- why routing was required
- what internal cognition was evaluated
- what requirement was identified as missing
- which route was selected
- what context crossed the boundary
- which provider/model was selected where applicable
- what result returned
- whether another routing cycle followed

The authoritative persistent transition history remains CSTR when persistent cognition is evaluated or changed.

Routing history itself must not silently become persistent cognition.

## 16. Canonical Decision Flow

`Incoming Information
-> Curiosity
-> Relevant PCG Retrieval
-> Internal Cognition Sufficiency
      |
      +-- Sufficient -----------------> GRI-Native
      |
      +-- Insufficient
              |
              v
       Identify Missing Requirement
              |
       +------+---------+-------------+
       |                |             |
       v                v             v
 Additional         Clarification   External/
 Internal Work      Required        Specialized
       |                |           Capability
       |                |             |
       v                v             v
 GRI-Native       Clarification   Delegation Check
                                      |
                              +-------+-------+
                              |               |
                              v               v
                           Allowed         Not Allowed
                              |               |
                              v               v
                         Frontier/Hybrid    Blocked
                              |
                              v
                       Frontier Response
                              |
                              v
                       NEW INFORMATION
                              |
                              +----> Same GRI Process
`

## 17. No-Guessing Invariants

1. Missing PCG information does not automatically justify frontier delegation.
2. Retrieval failure is not evidence of absence.
3. Unknown remains unknown.
4. Routing is not truth.
5. Routing is not evidence.
6. Frontier output is not automatically truth.
7. Frontier output is not automatically belief.
8. Frontier output re-enters the same GRI cognitive process.
9. Delegation does not authorize persistent cognition.
10. A route cannot bypass Governance or the Cognitive Kernel.
11. Context supplied to a frontier model must be authorized and relevant.
12. A frontier model cannot request unrestricted PCG access.
13. Clarification is distinct from frontier delegation.
14. GRI-native processing is not automatically correct.
15. Null processing is a valid outcome.

## 18. Architectural Invariants

1. GRI evaluates relevant internal cognition before frontier delegation.
2. GRI identifies the missing requirement before delegating.
3. GRI decides what portion of the interaction crosses the delegation boundary.
4. GRI decides which authorized frontier capability may be used.
5. Frontier responses re-enter GRI as new information.
6. The same Cognitive Instance owns re-entrant routing.
7. Multiple frontier calls may occur when justified.
8. Frontier output cannot directly mutate PCG.
9. Persistent cognitive change remains governed and traceable.
10. Routing history remains distinct from persistent cognition.

## 19. Open Questions

- exact internal cognition sufficiency function
- routing decision representation
- deterministic versus learned routing
- capability registry schema
- model capability discovery
- routing confidence representation
- delegation granularity
- context minimization algorithm
- routing cost/latency optimization
- multi-model parallel routing
- routing conflict resolution
- maximum recursive delegation depth
- timeout and cancellation
- routing audit serialization
- whether routing itself becomes a cognitive dimension
- interaction between routing history and learning

## 20. Core Principle

> **GRI thinks first, determines what is missing, and only then decides whether external intelligence is required.**

And when external intelligence is used:

> **The frontier model provides information or reasoning to GRI; GRI remains responsible for evaluating what that information means and whether it should influence persistent cognition.**
