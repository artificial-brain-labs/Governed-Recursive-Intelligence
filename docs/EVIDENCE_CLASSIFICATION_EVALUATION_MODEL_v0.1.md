# GRI Evidence Classification & Evaluation Model v0.1

**Status:** Foundational architecture specification  
**Version:** 0.1  
**Depends on:** Cognitive Interpretation Layer v0.1, Cognitive Requirement Identification & Decomposition Model v0.1, Interaction Cognitive Graph v0.1, Persistent Cognition Relevance Retrieval Model v0.1, Internal Cognition Sufficiency Model v0.1, Cognitive State Transition Model v0.1

## 1. Purpose

The Evidence Classification & Evaluation Model (ECEM) defines how GRI determines what received information can legitimately support during cognitive processing.

It establishes the boundary between:
- what was observed or communicated;
- what was interpreted;
- what the available information is evidence for;
- what remains unsupported;
- what evidence may justify a cognitive proposal.

It does not create persistent belief by itself.

Therefore:

Evidence != Truth != Belief != Proposal != Commitment

## 2. Architectural Position

The canonical sequence is:

Communication
-> Cognitive Instance
-> Curiosity
-> Cognitive Interpretation
-> Requirement Identification
-> Evidence Classification & Evaluation
-> PCG Relevance Retrieval
-> Internal Cognition Sufficiency
-> Gap Identification
-> Routing
-> Candidate / Proposal
-> Governance
-> Cognitive Kernel
-> PCG

Evidence evaluation may also operate iteratively after retrieval, native reasoning, clarification, tool use, or frontier re-entry.

## 3. Core Principle

> GRI must classify what information is evidence for before allowing that information to support persistent cognitive change.

The critical distinction is:

Evidence About X != Evidence That X Is True

For example, “The user said John cancelled the meeting” is evidence that the user communicated that proposition. It is not automatically sufficient evidence that John cancelled the meeting in the external world.

## 4. Evidence Model

An evidence item is represented conceptually as:

Evidence = (
evidence_id,
interaction_id,
instance_id,
source_reference,
claim_scope,
evidence_type,
supports,
contradicts,
basis,
strength_context,
limitations,
status,
provenance
)

The exact serialization remains open.

strength_context is deliberately not defined as truth probability or belief confidence in v0.1.

## 5. Evidence Source

Evidence must identify where it came from.

Possible sources include:
- direct communication;
- observed interaction;
- authorized persistent cognition;
- tool result;
- external document;
- sensor/environmental input;
- system event;
- frontier-model output;
- another explicitly authorized source.

Source provenance is essential because identical content can have different evidentiary meaning depending on its source.

## 6. Evidence About Communication

A communication itself can provide evidence about what was communicated.

Example:

Input: “John cancelled the meeting.”

Evidence may support:

Speaker communicated proposition P.

This is a valid evidence claim about the interaction.

It must not automatically be transformed into:

External Event P occurred.

## 7. Evidence About the External World

Evidence may support an external-world proposition when the source and evidence semantics justify that relationship.

Examples may include:
- an explicitly identified tool result;
- an authorized external record;
- a directly observed system event;
- an environmental observation;
- a document that is itself the relevant authoritative record.

The architecture does not assume that every source type has the same evidentiary authority.

## 8. Evidence Claim Scope

Every evidence item should identify what it supports.

Possible scopes include:
- communication claim;
- linguistic structure;
- interpretation claim;
- identity/reference claim;
- event claim;
- temporal claim;
- relational claim;
- state claim;
- provenance claim;
- system/process claim.

An evidence item should not silently support a broader claim than its source justifies.

Evidence: user said X does not automatically support Evidence: X occurred.

## 9. Evidence Type

Potential evidence types include:
- direct observation;
- explicit statement;
- structured record;
- tool result;
- retrieved cognition;
- repeated observation;
- corroborated observation;
- derived evidence;
- model-generated information;
- contextual evidence.

These are descriptive categories, not a universal ranking.

## 10. Supports and Contradicts

Evidence may:
- support a proposition;
- contradict a proposition;
- be neutral;
- leave the relationship unresolved.

Conceptually:

Evidence -> Claim Relationship -> supports / contradicts / neutral / unresolved

Contradictory evidence must remain explicit.

GRI must not resolve conflict merely by selecting the most recent, most frequent, or most convenient evidence unless a separately governed conflict-resolution rule exists.

## 11. Evidence vs Interpretation

Interpretation describes meaning assigned to received information.

Evidence describes what that information can support.

Example:

Observation:
The communication contains “John cancelled the meeting again.”

Interpretation:
The communication presents a recurring meeting-cancellation event involving a reference called John.

Evidence:
The communication supports the claim that the speaker communicated that proposition.

The external event remains a separate proposition requiring appropriate evidence evaluation.

Therefore:

Observation -> Interpretation -> Evidence Classification

not:

Observation -> Interpretation -> Fact

## 12. Evidence vs Inference

An inference is a reasoning result derived from available information. It is not automatically an observation.

Example:

Observed: John cancelled the meeting twice.

Inference: John may have a recurring cancellation pattern.

The inference can become a candidate proposition for evaluation. It must not be silently rewritten as an observed fact.

Therefore:

Inference != Observation

## 13. Evidence Sufficiency

Evidence evaluation must distinguish:
- evidence exists;
- evidence is relevant;
- evidence supports the proposition;
- evidence is sufficient for the requested processing;
- evidence is sufficient for persistent cognitive commitment.

These are different questions.

Evidence Presence != Evidence Relevance != Evidence Sufficiency != Truth

The required threshold depends on the cognitive operation.

## 14. Requirement-Relative Evidence

Evidence must be evaluated relative to the current requirement.

The same evidence can be sufficient for one requirement and insufficient for another.

Example:

Requirement A: “What did the user report?”

The user's statement may be directly sufficient.

Requirement B: “Did the reported event actually occur?”

The same statement may be insufficient by itself.

Therefore evidence sufficiency is requirement-relative.

## 15. Evidence Context

Evidence evaluation may consider:
- current requirement;
- claim being evaluated;
- source provenance;
- temporal context;
- identity/context resolution;
- relevant persistent cognition;
- corroborating evidence;
- contradictory evidence;
- source limitations;
- authorization/access context;
- processing history.

The evaluator must not use unavailable context as though it existed.

## 16. Evidence Status

An evidence item may have temporary states such as:
- identified;
- classified;
- relevant;
- supportive;
- contradictory;
- insufficient;
- unresolved;
- conflicting;
- superseded;
- inaccessible;
- invalid-source;
- re-evaluation-required.

These describe evidence processing. They do not themselves establish truth.

## 17. Evidence Aggregation

Multiple evidence items may jointly support a proposition.

Evidence Set = E1 + E2 + ... + En -> Evaluation

Aggregation must preserve individual provenance and limitations.

The architecture does not assume that more evidence automatically means stronger evidence.

Repeated copies of the same underlying source are not necessarily independent corroboration.

## 18. Corroboration

Corroboration may increase the evidentiary basis for a proposition when sources are meaningfully independent or otherwise legitimately corroborating.

But:

Repeated Source != Independent Corroboration

The exact corroboration model remains an open research problem.

## 19. Contradictory Evidence

When evidence supports competing propositions, GRI must preserve the conflict.

For example:

E1 -> supports(P)
E2 -> contradicts(P)

The system may then:
- retrieve additional evidence;
- seek clarification;
- perform further native reasoning;
- request authorized external information;
- route to frontier capability;
- preserve the proposition as unresolved.

It must not silently convert conflict into certainty.

## 20. Temporal Validity

Evidence may have a temporal scope:
- historical;
- current;
- future-dated;
- time-bounded;
- recurring.

Historical Evidence != Automatically Current Evidence

Freshness is requirement-dependent and must be evaluated explicitly.

## 21. Identity and Evidence

Evidence may refer to an entity without establishing which persistent identity it corresponds to.

Example:

“John cancelled the meeting.”

The statement may provide evidence that the speaker used the reference “John.” If multiple John candidates exist, the identity relationship remains unresolved.

Therefore:

Evidence About Reference != Evidence of Persistent Identity

## 22. Evidence from Persistent Cognition

Retrieved PCG content can participate as evidence for current reasoning, but its provenance and historical status must remain available.

A retrieved belief, concept, or relationship is not automatically infallible merely because it is persistent.

PCG Retrieval != Truth Verification

## 23. Frontier-Model Output as Evidence

Frontier-model output is new information.

It can provide evidence about:
- what the model generated;
- a transformation it performed;
- a reasoning path it proposed;
- information it returned from an authorized capability.

It does not automatically provide evidence that an external-world proposition is true.

Canonical path:

Frontier Output
-> New Information Re-entry
-> Cognitive Interpretation
-> Evidence Classification
-> Evidence Evaluation

The model's confidence or fluency must not be treated as truth authorization.

## 24. Evidence and Requirement

Evidence evaluation may determine whether an identified requirement has adequate support.

Example:

Requirement: Determine whether event X occurred.
Evidence State: insufficient.

This does not mean:

Event X did not occur.

It means GRI does not currently have sufficient evidence to establish the requested proposition under the current evaluation.

## 25. Evidence and Internal Cognition Sufficiency

ECEM supplies evidence state to ICSM.

Requirement + Relevant Cognition + Evidence Evaluation -> ICSM

ICSM can then distinguish:
- sufficient evidence;
- incomplete evidence;
- conflicting evidence;
- unresolved evidence;
- no identified evidence;
- retrieval failure.

Evidence evaluation does not itself decide whether frontier delegation is required.

## 26. Evidence and Routing

Routing may use evidence gaps as one input.

Evidence Insufficient
-> Identify Missing Requirement
-> Determine Internal Recovery Options
-> Routing

Evidence insufficiency does not automatically imply frontier delegation.

## 27. Evidence and Cognitive Proposal

A cognitive proposal may reference one or more evidence items.

Evidence
-> Candidate Proposition
-> Cognitive Proposal
-> Governance
-> Kernel

A proposal must preserve which evidence supports it and what limitations remain.

The existence of evidence does not guarantee that the proposal will be approved.

## 28. Evidence and Persistent Cognition

Evidence is not itself persistent cognition.

The prohibited shortcut is:

Evidence -> PCG

The governed path remains:

Evidence -> Proposal -> Governance -> Cognitive Kernel -> PCG

This applies to beliefs, relationships, concepts, goals, dimensions, and other persistent structures.

## 29. Null Cognitive Consequence

Evidence evaluation may conclude that no persistent cognitive change is justified.

Examples:
- evidence insufficient;
- evidence redundant;
- conflicting evidence unresolved;
- proposition already adequately represented;
- interpretation remains ambiguous;
- experience is not cognitively relevant.

Then:

PCG_(t+1) = PCG_t

The evaluation may still be recorded in temporary processing history and, when it reaches the persistent transition boundary, by CSTR.

## 30. Evidence Provenance

Every evidence item should preserve enough provenance to answer:
- where it came from;
- when it was received;
- what source produced it;
- what communication or observation generated it;
- what interpretation led to its classification;
- what claim it supports or contradicts;
- what context was used;
- whether it was independently corroborated;
- whether it was later superseded or contradicted.

## 31. Evidence Re-evaluation

Evidence must be re-evaluated when materially new information enters GRI.

New Information
-> Interpretation
-> Evidence Classification
-> Evidence Re-evaluation
-> Requirement / Sufficiency Re-evaluation
-> Routing or Proposal

Frontier output follows the same path.

Prior evidence must not be silently rewritten; its status may change through explicit re-evaluation.

## 32. Evidence Failure vs Absence

GRI must distinguish:
- No Evidence Identified;
- Evidence Retrieval Failed;
- Evidence Exists but Is Inaccessible;
- Evidence Exists but Is Insufficient;
- Evidence Is Conflicting.

Therefore:

Retrieval Failure != Evidence Absence

and:

Evidence Absence != Proposition False

## 33. No-Guessing Invariants

ECEM v0.1 establishes:

1. Evidence is not automatically truth.
2. Interpretation is not automatically evidence of an external-world proposition.
3. Inference is not observation.
4. Evidence about communication is not automatically evidence that the communicated event occurred.
5. Evidence scope must remain explicit.
6. Source provenance must be preserved.
7. Missing evidence is not evidence of falsity.
8. Retrieval failure is not evidence absence.
9. Conflicting evidence remains conflicting.
10. Repeated copies of one source are not automatically independent corroboration.
11. Historical evidence is not automatically current evidence.
12. Frontier output is not automatically external-world evidence.
13. Evidence does not directly mutate PCG.
14. Evidence does not authorize action.
15. Evidence sufficiency is requirement-relative.
16. Evidence existence does not guarantee proposal approval.
17. No cognitive commitment occurs without the established governed transition path.

## 34. Architectural Invariants

1. Evidence classification is an explicit GRI processing concern.
2. Evidence must identify its source and claim scope.
3. Interpretation and evidence remain distinct representations.
4. Evidence evaluation may operate iteratively.
5. Evidence state feeds requirement and sufficiency evaluation.
6. Evidence gaps do not automatically trigger frontier delegation.
7. Contradictory evidence remains explicit.
8. Evidence provenance is preserved.
9. Persistent cognition remains downstream of proposal, governance, and kernel execution.
10. CSTR remains the authoritative historical record for persistent transition evaluation.
11. Frontier output must re-enter evidence evaluation before influencing persistent cognition.
12. No alternate path exists from evidence directly to PCG.

## 35. Canonical Evidence Flow

Received Information
-> Observation / Communication Record
-> Cognitive Interpretation
-> Evidence Classification
-> Claim-Scope Evaluation
-> Evidence Relevance
-> Evidence Sufficiency / Conflict Evaluation
-> Requirement & Sufficiency Context
-> Internal Recovery / Routing
-> Candidate / Proposal
-> Governance
-> Cognitive Kernel
-> PCG / CSTR

A valid interaction may terminate earlier with:

Evidence Evaluation -> No Sufficient Basis -> Null Cognitive Consequence

## 36. Open Questions

ECEM v0.1 intentionally leaves open:
- formal evidence ontology;
- source authority model;
- evidence independence;
- corroboration rules;
- numerical evidence-strength semantics;
- Bayesian/probabilistic vs symbolic/hybrid evaluation;
- temporal decay;
- conflict resolution;
- source reliability representation;
- claim ontology;
- evidence composition;
- evidence threshold by cognitive operation;
- external verification policy;
- tool-result trust model;
- frontier output evidence semantics;
- evidence serialization;
- evidence retention;
- privacy and access control;
- cryptographic provenance;
- adversarial evidence handling.

## 37. Core Principle

> GRI must know not only what information it received, but what that information is legitimately evidence for—and it must preserve the limits of that evidence before allowing cognitive commitment.

The persistent boundary remains:

Evidence -> Proposal -> Governance -> Cognitive Kernel -> Persistent Cognition

with no direct evidence-to-PCG path.
