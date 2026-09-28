# GRI Internal Cognition Sufficiency Model v0.1

**Status:** Foundational architecture specification  
**Version:** 0.1  
**Depends on:** Cognitive Routing Decision Model v0.1, Cognitive Instance Lifecycle v0.1, Interaction Cognitive Graph v0.1, PCG Ontology v0.1, Cognitive Dimension Model v0.1, CCA v0.1

## 1. Purpose

The **Internal Cognition Sufficiency Model (ICSM)** determines whether GRI's currently available internal cognition and native processing are sufficient for the requirement being processed by a Cognitive Instance.

It answers:

> Does GRI currently have enough relevant cognition and capability to proceed internally, or is something still required?

It does **not** answer:

> Is the existing cognition objectively true?

It also does not itself decide whether to delegate to a frontier model.

Therefore:

`Cognition Sufficiency != Truth`

and:

`Cognition Sufficiency Evaluation != Routing`

The evaluation is a temporary cognitive assessment used by the routing process.

## 2. Architectural Position

The canonical sequence is:

`Interaction
-> Curiosity
-> Relevant PCG Retrieval
-> Internal Cognition Sufficiency Evaluation
-> Missing Requirement Identification
-> Routing Decision`

ICSM therefore sits immediately before routing.

Its role is to characterize the state of internal cognition so that routing does not collapse different causes of insufficiency into a single “not found” condition.

## 3. Core Principle

> **GRI must determine what it already has, what it does not have, what is uncertain, and what capability is missing before deciding where processing should occur.**

This prevents:

`PCG Not Found -> Frontier`

from becoming an automatic rule.

The correct sequence is:

`Requirement -> Relevant Cognition -> Sufficiency Evaluation -> Gap Identification -> Routing`

## 4. Requirement Before Sufficiency

Sufficiency is always relative to a requirement.

The same PCG may be sufficient for one task and insufficient for another.

For example, existing cognition may be sufficient to:

- explain a previously established concept;
- continue a known relationship context;
- perform a simple transformation;

while being insufficient to:

- answer a current external-world question;
- resolve an ambiguous identity;
- perform a specialized operation;
- determine information that is genuinely absent from PCG.

Therefore:

`Sufficiency = f(requirement, relevant cognition, available native capability, evidence context)`

The exact mathematical function is intentionally not fixed in v0.1.

## 5. Sufficiency Evaluation Context

The Cognitive Instance supplies a temporary evaluation context.

Conceptually:

`SufficiencyContext =
(
interaction_id,
instance_id,
requirement,
goal_context,
active_dimensions,
relevant_pcg_references,
icg_context,
evidence_state,
uncertainty_state,
processing_history,
available_native_capabilities
)`

The evaluation must operate on relevant cognition rather than requiring unrestricted PCG access.

## 6. What ICSM Evaluates

The evaluation considers at least the following dimensions.

### 6.1 Requirement Coverage

Does the retrieved cognition address the information or cognitive requirements of the task?

Possible states:

- sufficient
- partial
- insufficient
- absent

Coverage is task-relative.

### 6.2 Evidence State

What support exists for the relevant cognition?

Possible states include:

- supported by identified evidence
- evidence exists but is incomplete
- evidence is historical or context-dependent
- evidence status unresolved
- no supporting evidence identified

Evidence state does not independently determine truth.

### 6.3 Freshness / Temporal Adequacy

Is the available cognition temporally appropriate for the requirement?

Examples:

- historical information may be sufficient for a historical question;
- the same information may be insufficient for a current-state question.

Staleness must not be treated as falsity.

### 6.4 Consistency

Does relevant PCG contain conflicting cognitive structures?

Possible conditions:

- no detected conflict
- compatible information
- unresolved conflict

ICSM must not silently select one conflicting structure merely because it is easier to use.

### 6.5 Identity / Context Resolution

Can the entities, concepts, relationships, or context required by the task be resolved sufficiently?

Possible conditions:

- resolved
- partially resolved
- ambiguous
- unresolved

An unresolved identity is not evidence that the entity does not exist.

### 6.6 Native Capability

Does GRI itself have the processing capability required by the task?

This is distinct from knowledge availability.

A task can have:

`Knowledge Available + Native Capability Insufficient`

This is a **capability gap**, not necessarily a knowledge gap.

## 7. Canonical Sufficiency States

ICSM v0.1 distinguishes the following evaluation states.

### 7.1 Sufficient

Relevant cognition and native capability are adequate for the current requirement.

This means:

> GRI can proceed using its current internal resources.

It does not mean:

> The cognition is guaranteed to be true.

### 7.2 Partially Sufficient

Some requirements can be satisfied internally, while one or more requirements remain unresolved.

The known portion may continue to be used while the unresolved portion is explicitly retained.

### 7.3 Insufficient

Relevant cognition exists but does not adequately satisfy the requirement.

Examples:

- important knowledge is incomplete;
- evidence is inadequate for the requested conclusion;
- relevant context is missing;
- current information is stale for the task.

### 7.4 Unknown

No relevant cognition has been established for the requirement.

Unknown means:

> GRI does not currently have established relevant cognition.

It does **not** mean:

> The proposition is false.

It also does not automatically mean:

> Use a frontier model.

### 7.5 Ambiguous

The relevant cognition or requirement cannot be resolved uniquely.

Examples:

- multiple possible identities;
- conflicting interpretations;
- unclear task objective;
- unresolved relationship reference.

Ambiguity may require clarification, additional internal processing, or external investigation.

### 7.6 Retrieval Failure

The system could not reliably retrieve the relevant PCG information.

This is operational failure, not knowledge absence.

Therefore:

`Retrieval Failure != Unknown`

### 7.7 Conflict

Relevant persistent cognition contains materially conflicting structures that cannot currently be reconciled.

Conflict is preserved as conflict.

ICSM must not manufacture resolution by choosing the most recent, strongest, or easiest-to-use structure unless a separate governed conflict-resolution rule explicitly permits that action.

## 8. Knowledge Gap vs Capability Gap

A central ICSM distinction is:

### Knowledge Gap

GRI lacks required information.

Examples:

- required current information is not present;
- a required concept has not been established;
- a required relationship is unresolved.

### Capability Gap

GRI has relevant information but lacks the native capability required to complete the task.

Examples:

- specialized computation;
- unsupported modality processing;
- advanced language transformation;
- a capability not implemented in the GRI-native layer.

### Combined Gap

Both may exist.

The router must be able to distinguish:

`Knowledge Gap`

from:

`Capability Gap`

from:

`Knowledge + Capability Gap`

This distinction prevents unnecessary frontier delegation.

## 9. Internal Recovery Before Frontier

An insufficient result does not immediately become a frontier request.

ICSM may identify an internal recovery action such as:

- retrieve additional PCG structures;
- expand the relevant ICG;
- activate another cognitive dimension;
- evaluate additional relationships;
- inspect available evidence;
- resolve an internal reference;
- perform another GRI-native reasoning step.

The routing layer then determines whether such recovery is appropriate.

Therefore:

`Insufficient -> Internal Recovery Evaluation -> Routing`

not:

`Insufficient -> Frontier`

## 10. Evaluation Output

ICSM produces a structured, temporary evaluation result.

Conceptually:

`CognitionSufficiencyEvaluation =
(
requirement_state,
relevant_cognition,
coverage,
evidence_state,
freshness_state,
consistency_state,
identity_context_state,
native_capability_state,
knowledge_gaps,
capability_gaps,
internal_recovery_options,
unresolved_questions,
evaluation_provenance
)`

The exact serialization remains open.

The result is not itself a persistent cognitive object.

## 11. Evaluation vs Recommendation

ICSM describes the internal cognitive condition.

It may identify:

- what is known;
- what is partially known;
- what is missing;
- what conflicts;
- what cannot be retrieved;
- what native capability is unavailable.

It should not itself authorize:

- frontier delegation;
- persistent belief formation;
- PCG mutation;
- governance bypass.

The routing layer consumes the evaluation to select a processing route.

## 12. Evidence Boundary

ICSM must preserve the established GRI evidence boundaries.

The following remain distinct:

`Observation != Interpretation`

`Interpretation != Evidence`

`Evidence != Belief`

`Belief != Truth Guarantee`

The presence of a belief in PCG means that the belief was previously accepted through governed cognition. It does not make the belief infallible or automatically current.

ICSM may therefore evaluate the existence, relevance, provenance, freshness, and conflict status of cognition without converting that evaluation into a new fact.

## 13. Sufficiency Does Not Mean Certainty

A critical architectural distinction is:

> **Sufficient to proceed is not equivalent to certain to be true.**

For example, GRI may have a governed belief sufficient to answer a question within the current interaction context while still recognizing that:

- the belief has historical provenance;
- the external world may have changed;
- contradictory information may exist outside current cognition.

If the task requires current or independently verified information, freshness or evidence requirements may produce an insufficiency even when a related belief exists.

## 14. Freshness Is Requirement-Dependent

Freshness must be evaluated relative to the task.

Conceptually:

`Temporal Adequacy = f(information_time, requirement_time, task_semantics)`

No universal expiration period is defined in v0.1.

A historical fact may remain appropriate indefinitely for a historical question.

A current-state question may require information newer than anything currently stored.

Stale cognition is therefore not automatically deleted or weakened.

It may simply be inadequate for the present requirement.

## 15. Conflict Handling

If relevant PCG contains conflicting cognition:

`Conflict -> Preserve Conflict -> Evaluate Resolution Requirement`

Possible next actions include:

- additional internal evidence evaluation;
- retrieval of provenance;
- clarification;
- external information gathering;
- governed conflict-resolution processing.

ICSM does not select a winner.

This preserves the no-guessing invariant.

## 16. Interaction With Curiosity

Curiosity initiates exploration but does not determine the answer.

The relationship is:

`Curiosity
-> Identify Unknown / Unresolved Requirement
-> Sufficiency Evaluation
-> Gap Identification
-> Investigation or Processing`

Curiosity may therefore cause additional internal retrieval before external delegation.

An unknown remains unknown until evidence or established cognition changes its status.

## 17. Interaction With Routing

The routing model consumes ICSM output.

Conceptually:

`ICSM
-> Requirement State
-> Gap Identification
-> Routing Decision`

Examples:

### Case A — Sufficient

`Sufficient + Native Capability Available -> GRI-Native`

### Case B — Partial

`Partial -> Internal Recovery / Hybrid / Clarification / Frontier`

depending on the unresolved requirement.

### Case C — Unknown

`Unknown -> Investigate / Clarify / Frontier / Explicit Unknown`

Frontier is only one possible route.

### Case D — Retrieval Failure

`Retrieval Failure -> Retry / Alternate Retrieval / Degraded Processing / Block`

It must not be interpreted as absence.

### Case E — Conflict

`Conflict -> Resolve / Clarify / Investigate / Block`

The system must not silently select one side.

### Case F — Capability Gap

`Capability Gap -> Authorized Capability Selection`

The selected capability may be frontier-based or another permitted processor.

## 18. Interaction With PCG

ICSM reads persistent cognition.

It does not modify it.

The boundary is:

`PCG -> Relevant Retrieval -> ICSM Evaluation`

not:

`PCG -> ICSM -> PCG`

Any persistent change resulting from later processing must follow:

`Evidence -> Proposal -> Governance -> Kernel -> PCG`

## 19. Interaction With ICG

ICSM may use the ICG to determine what cognitive structures are currently active.

For example:

- active concepts;
- candidate interpretations;
- relevant relationships;
- evidence nodes;
- unresolved questions;
- goal relevance.

ICG content remains temporary.

A candidate in ICG does not become established cognition merely because ICSM considers it relevant.

## 20. Interaction With Frontier Re-entry

If routing delegates work to a frontier model, its output returns as new information.

The returned information must again pass through:

`Curiosity / Context Evaluation
-> Relevant PCG Retrieval
-> Internal Cognition Sufficiency Evaluation
-> Interpretation / Evidence Classification
-> ICG
-> Routing if Required`

Therefore frontier output does not bypass ICSM.

The fact that GRI requested the information does not make it sufficient evidence or established truth.

## 21. No-Guessing Invariants

ICSM v0.1 introduces or reinforces these invariants:

1. Sufficiency is requirement-relative.
2. Sufficiency is not truth.
3. Sufficiency is not certainty.
4. PCG absence is not falsity.
5. PCG absence is not automatically a frontier requirement.
6. Retrieval failure is not knowledge absence.
7. Unknown remains unknown.
8. Ambiguity remains explicit.
9. Conflict remains explicit until resolved by an appropriate process.
10. Stale cognition is not automatically false.
11. Knowledge gaps and capability gaps remain distinct.
12. Internal recovery should be considered before external delegation where applicable.
13. ICSM does not authorize frontier delegation.
14. ICSM does not mutate PCG.
15. ICSM does not create beliefs or facts.
16. Frontier output re-enters the same sufficiency evaluation process.
17. Existing belief does not guarantee external-world truth.
18. A sufficient internal answer may still require external information when the task explicitly requires current or externally verified information.

## 22. Architectural Invariants

1. Every routing evaluation has an explicit requirement context.
2. Relevant PCG is evaluated before external delegation.
3. The evaluation distinguishes knowledge availability from processing capability.
4. Retrieval failure remains operationally distinct from absence.
5. The evaluation preserves unresolved states rather than forcing binary answers.
6. ICSM remains non-mutating.
7. Routing consumes ICSM results but retains responsibility for route selection.
8. Governance remains the authorization boundary for persistent cognitive change.
9. Frontier responses return through the same cognitive pipeline.
10. The evaluation does not require unrestricted PCG access.
11. The evaluation itself does not become persistent cognition.

## 23. Canonical Model

The complete sequence is:

`Interaction
-> Curiosity
-> Relevant PCG Retrieval
-> Internal Cognition Sufficiency Evaluation
      |
      +-- Sufficient --------------------> GRI-Native Processing
      |
      +-- Partial -----------------------> Identify Gaps
      |
      +-- Insufficient ------------------> Identify Gaps
      |
      +-- Unknown -----------------------> Investigate / Clarify / Route
      |
      +-- Ambiguous ---------------------> Resolve / Clarify
      |
      +-- Retrieval Failure -------------> Recover / Retry / Degrade / Block
      |
      +-- Conflict ----------------------> Resolve / Investigate / Clarify
      |
      +-- Capability Gap ----------------> Capability Selection
                                             |
                                             v
                                      Routing Decision
                                             |
                           +-----------------+------------------+
                           |                                    |
                           v                                    v
                      GRI-Native                          Frontier / Hybrid
                           |                                    |
                           +-----------------+------------------+
                                             |
                                             v
                                      New Information
                                             |
                                             +--> Same GRI Process
`

## 24. Relationship to Cognitive Sufficiency and Learning

An ICSM result does not itself constitute learning.

Learning occurs only when a governed cognitive transition changes persistent state.

Therefore:

`Sufficiency Evaluation -> Learning`

is invalid as a direct path.

The valid path is:

`Evaluation
-> Candidate / Proposal
-> Governance
-> Kernel
-> Persistent State Transition`

A sufficient answer can therefore produce:

`No Cognitive Change`

and an insufficient answer can also produce:

`No Cognitive Change`

The existence of processing is not evidence that learning should occur.

## 25. Open Questions

ICSM v0.1 intentionally leaves the following unresolved:

- exact requirement representation;
- exact coverage algorithm;
- evidence adequacy thresholds;
- freshness computation;
- conflict severity model;
- capability ontology;
- native capability registry;
- how much PCG should be retrieved before declaring insufficiency;
- whether sufficiency should use symbolic, graph, probabilistic, or hybrid evaluation;
- whether task classes define different sufficiency criteria;
- exact interaction with salience and learning rate;
- whether historical belief strength contributes to sufficiency;
- how external verification requirements are represented;
- how multiple simultaneous gaps are prioritized;
- how sufficiency is evaluated under partial system failure;
- whether an evaluation can be recursively revisited after new information arrives.

These should be resolved through architecture and experimentation rather than prematurely encoded as arbitrary thresholds.

## 26. Core Principle

> **GRI does not ask only “Do I have this information?” It asks “Given the current requirement, what relevant cognition do I have, what is established, what is missing, what is unresolved, and what capability is actually required?”**

This makes internal cognition evaluation a distinct architectural function between persistent cognition retrieval and cognitive routing.
