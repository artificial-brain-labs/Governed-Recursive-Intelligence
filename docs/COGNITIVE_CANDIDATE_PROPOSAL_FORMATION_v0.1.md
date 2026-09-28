# GRI Cognitive Candidate & Proposal Formation Model v0.1

**Status:** Foundational architecture specification
**Version:** 0.1
**Depends on:** Cognitive Interpretation Layer v0.1, Evidence Classification & Evaluation Model v0.1, Interaction Cognitive Graph v0.1, Persistent Cognitive Graph Ontology v0.1, CCA v0.1, Governance v0.1, Cognitive Kernel v0.1, CSTR v0.1

## 1. Purpose

The Cognitive Candidate & Proposal Formation Model (CCPFM) defines how GRI transforms evaluated evidence and interaction cognition into explicit candidate cognitive consequences and, when justified, a structured cognitive proposal.

Its central boundary is:

Candidate != Proposal != Commitment

A candidate is something GRI may need to consider.

A proposal is a structured request for a possible persistent cognitive transition.

A commitment occurs only after Governance authorization and Cognitive Kernel execution.

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
-> Candidate Formation
-> Proposal Formation
-> Consolidation Readiness
-> Governance
-> Cognitive Kernel
-> PCG / CSTR

Candidate and proposal formation may be revisited when new evidence, clarification, retrieved cognition, or frontier output enters the interaction.

## 3. Core Principle

> GRI must separate the recognition that a cognitive change may be warranted from the decision to request that change.

Therefore:

Evidence -> Candidate -> Proposal -> Governance -> Commitment

and never:

Evidence -> PCG

## 4. Candidate Model

A candidate is a temporary interaction-scoped representation of a possible cognitive consequence.

Conceptually:

Candidate = (
candidate_id,
interaction_id,
instance_id,
candidate_type,
target_reference,
content,
operation,
evidence_references,
interpretation_references,
context_references,
alternatives,
conflicts,
status,
provenance
)

The exact serialization remains open.

## 5. Candidate Types

Initial candidate types may include:

- belief candidate;
- concept candidate;
- relationship candidate;
- goal-effect candidate;
- goal candidate;
- cognitive-dimension update candidate;
- learning-state candidate;
- identity candidate;
- reconciliation candidate.

The candidate ontology remains extensible.

A candidate type does not imply that persistence will occur.

## 6. Candidate Formation

Candidate formation may use:

- interpreted communication;
- evaluated evidence;
- relevant PCG structures;
- active goals;
- active cognitive dimensions;
- established relationships;
- requirement context;
- observed changes;
- repeated interaction patterns;
- prior candidate history.

The formation process must preserve provenance for each basis.

## 7. Candidate Target

A candidate may target:

- an existing persistent object;
- an existing relationship;
- an existing dimension instance;
- a candidate object;
- a candidate relationship;
- a new object type permitted by the ontology.

An unresolved reference must remain unresolved.

Candidate target != persistent identity.

## 8. Candidate Operations

The initial operation vocabulary is:

- create;
- modify;
- reinforce;
- weaken;
- remove;
- no_change.

The operation describes a possible cognitive consequence.

It is not authorization.

For example:

Candidate:
Trust Dimension X
Operation:
increase

does not mean:

Trust has increased.

It means an increase is being considered.

## 9. Candidate Evidence Requirements

Every candidate that could affect persistent cognition must identify the evidence supporting it.

A candidate may also identify:

- contradictory evidence;
- unresolved evidence;
- evidence limitations;
- evidence gaps.

No candidate should silently treat an unsupported inference as established evidence.

## 10. Candidate vs Interpretation

Interpretation answers:

> What might the received information mean?

Candidate formation answers:

> Given the interpreted information and evaluated evidence, what persistent cognitive consequence might need to be considered?

Therefore:

Interpretation != Candidate

Example:

Interpretation:
The communication describes repeated cancellation behavior.

Candidate:
Possible modification of an existing relationship/dimension concerning reliability.

The candidate remains subject to evidence evaluation, reconciliation, governance, and authorization.

## 11. Candidate vs Evidence

Evidence supports or contradicts a claim.

A candidate proposes a possible cognitive consequence based on evaluated information.

Therefore:

Evidence != Candidate

Evidence may support multiple competing candidates.

For example:

E1 -> supports Candidate A
E1 -> also supports Candidate B

when the evidence is compatible with more than one cognitive interpretation.

## 12. Candidate Conflict

Multiple candidates may exist for the same interaction.

Examples:

Candidate A:
John = Identity-X

Candidate B:
John = Identity-Y

or:

Candidate A:
Trust increases

Candidate B:
Trust unchanged

The system must preserve the alternatives until sufficient evidence, clarification, reconciliation, or governed decision-making resolves the conflict.

Candidate conflict must not be silently resolved by arbitrary selection.

## 13. Candidate Status

Temporary candidate states may include:

- identified;
- active;
- unresolved;
- ambiguous;
- supported;
- weakly_supported;
- contradicted;
- redundant;
- superseded;
- proposed;
- rejected;
- discarded;
- consolidated;
- no_change.

These states describe candidate processing.

They do not represent persistent truth.

## 14. Reconciliation With Existing PCG

Candidate formation must compare proposed consequences against relevant persistent cognition.

Conceptually:

Candidate
+
Relevant PCG
-> Reconciliation Evaluation

Possible outcomes:

- genuinely new;
- modification of existing cognition;
- reinforcement of existing cognition;
- weakening of existing cognition;
- redundant;
- contradictory to existing cognition;
- unresolved;
- target not found;
- target resolution required.

PCG retrieval failure must not be interpreted as absence of the target.

## 15. New vs Reinforcement

GRI must distinguish:

New cognition

from:

Reinforcement of existing cognition.

If PCG already contains an established belief and new evidence supports it, the candidate may represent reinforcement rather than creation.

The exact reinforcement mathematics remains open.

## 16. Modification vs Replacement

A candidate modifying an existing cognitive object should preserve object identity where the ontology defines the object as persistent.

Conceptually:

Object-X version 4
-> Candidate modification
-> governed transition
-> Object-X version 5

This is different from silently deleting Object-X and creating a new unrelated object.

## 17. Relationship Candidates

Relationship candidates are first-class candidate structures.

Example:

Identity-A
-> candidate relationship
-> Identity-B

The candidate may specify:

- source;
- target;
- relationship type;
- direction;
- semantics;
- evidence;
- proposed operation.

A candidate relationship does not become a persistent relationship until the governed transition path completes.

## 18. Cognitive Dimension Candidates

A candidate may propose a change to a cognitive dimension.

Example:

Trust(X).value:
4 -> 5

The candidate describes the proposed consequence.

It does not itself change the value.

The candidate should preserve:

- dimension identity;
- previous known state;
- proposed operation;
- evidence;
- relationship context;
- learning-rate context where relevant;
- local constraints;
- provenance.

Learning rate controls adaptation speed; it does not authorize the change.

## 19. Belief Candidates

A belief candidate should identify:

- proposition;
- target;
- supporting evidence;
- contradictory evidence;
- relevant interpretation;
- temporal scope;
- provenance;
- proposed operation.

A belief candidate is not yet a belief.

The conceptual sequence remains:

Evidence
-> Candidate Belief
-> Proposal
-> Governance
-> Kernel
-> Persistent Belief

## 20. Goal Candidates

A goal candidate may represent:

- creation;
- modification;
- suspension;
- removal;
- evolution;
- observed goal effect.

Goal candidates require particular governance sensitivity because goals influence future salience and cognition.

A proposed goal does not become authoritative merely because it is generated.

Goal evolution remains constitutionally bounded.

## 21. Identity Candidates

Identity candidates require special protection.

A name, pronoun, or reference may generate an identity candidate, but:

Reference != Identity

Identity candidates should preserve:

- source reference;
- candidate entity description;
- supporting evidence;
- alternative matches;
- ambiguity;
- provenance.

Identity persistence requires the normal governed cognitive transition path.

## 22. Candidate Confidence and Support

CCPFM v0.1 does not mandate a universal numerical candidate confidence score.

Candidate support should instead preserve structured information about:

- supporting evidence;
- contradictory evidence;
- unresolved evidence;
- source limitations;
- interpretation alternatives;
- reconciliation state.

If numerical confidence is introduced later, it must not automatically become:

- truth probability;
- belief strength;
- Trust value;
- governance authorization.

## 23. Proposal Formation

A proposal is formed only when a candidate has sufficient structural basis to request a potential persistent transition.

Conceptually:

Candidate
-> Candidate Evaluation
-> Proposal Formation

A proposal should contain at least:

- proposal_id;
- target type;
- target reference;
- operation;
- evidence references;
- rationale;
- relevant predecessor state reference;
- provenance;
- unresolved conditions where applicable.

The exact proposal schema remains open.

## 24. Proposal Preconditions

Before proposal formation, GRI should evaluate:

1. Is the target sufficiently identified?
2. Is the proposed operation defined?
3. Is there explicit evidence support?
4. Are contradictions represented?
5. Is relevant persistent cognition available where required?
6. Is the candidate redundant?
7. Is the candidate materially unresolved?
8. Are required temporal/context conditions represented?
9. Are required local constraints identifiable?
10. Is the candidate sufficiently structured for governance evaluation?

Failure of these conditions does not imply falsehood.

It may result in:

- candidate retained;
- further evidence requested;
- clarification required;
- additional retrieval;
- no-change;
- candidate discarded.

## 25. Proposal != Governance

Proposal formation does not authorize the proposed change.

The boundary remains:

Proposal
-> Governance
-> Authorization

Governance evaluates whether the proposal is permitted under local and global constraints.

CCPFM must not bypass Governance.

## 26. Proposal != Kernel Execution

A proposal is not a state mutation.

The Cognitive Kernel executes only an authorized proposal.

Therefore:

Proposal -> Kernel

is prohibited unless the required Governance authorization is present.

## 27. Proposal and CSTR

When a proposal reaches the persistent transition boundary, its identity and supporting context must be traceable in CSTR.

CSTR should preserve:

- proposal reference;
- evidence references;
- interpretation reference;
- governance decision;
- predecessor state;
- successor state or null outcome.

A rejected proposal may still produce a CSTR when evaluated by the persistent transition path.

## 28. Null Proposal / No-Change

Not every candidate produces a proposal.

Valid outcomes include:

Candidate -> No Proposal

Reasons may include:

- insufficient evidence;
- unresolved ambiguity;
- redundancy;
- contradiction;
- low relevance;
- no persistent consequence;
- target unresolved;
- governance-sensitive information requiring additional processing.

A no-proposal result must not be interpreted as evidence that the underlying proposition is false.

## 29. Candidate Re-evaluation

Candidates must be re-evaluated when materially new information arrives.

Canonical loop:

New Information
-> Interpretation
-> Evidence Evaluation
-> Candidate Re-evaluation
-> Proposal Update / New Candidate / No Change

Frontier output follows the same path.

Prior candidates should remain traceable in temporary processing history where their evolution matters.

## 30. Candidate Consolidation Readiness

A candidate/proposal is ready for CCA handoff when:

1. required interpretation is complete enough for the current decision;
2. relevant evidence has been explicitly identified;
3. contradictions and alternatives are represented;
4. target resolution is sufficient for the proposed operation;
5. relevant PCG context has been reconciled;
6. the candidate is either explicitly retained as no-change or structurally ready for proposal evaluation;
7. any resulting proposal is structurally complete;
8. unresolved conditions are explicit.

CCA remains the consolidation boundary.

## 31. Relationship to CCA

The canonical handoff is:

ICG
-> Candidate Extraction
-> Evidence Evaluation
-> Candidate Formation
-> Proposal Formation or Explicit Null
-> Consolidation Readiness
-> CCA
-> Governance
-> Kernel

CCA does not invent missing candidates and does not authorize them.

## 32. No-Guessing Invariants

CCPFM v0.1 establishes:

1. Candidate != Interpretation.
2. Candidate != Evidence.
3. Candidate != Proposal.
4. Proposal != Commitment.
5. Evidence does not automatically create a candidate.
6. Candidate does not automatically become a proposal.
7. Proposal does not authorize itself.
8. A reference is not automatically an identity.
9. An unresolved target remains unresolved.
10. Contradictory candidates remain explicit.
11. Candidate support is not truth.
12. Candidate confidence is not automatically belief confidence or Trust.
13. Candidate formation does not mutate PCG.
14. Proposal formation does not mutate PCG.
15. Frontier output must re-enter GRI before creating or modifying candidates.
16. Retrieval failure is not target absence.
17. No-change is a valid outcome.
18. Governance remains the authorization boundary.
19. Kernel remains the persistent mutation boundary.

## 33. Architectural Invariants

1. Candidate formation is temporary interaction cognition.
2. Candidate provenance is preserved.
3. Evidence references are explicit.
4. Relevant PCG is reconciled before persistent proposal formation where required.
5. Multiple candidates may coexist.
6. Candidate conflicts remain explicit.
7. Proposal structure is explicit.
8. Proposal authorization remains outside CCPFМ.
9. Persistent state mutation remains outside CCPFМ.
10. CSTR remains the historical transition record.
11. Null outcomes remain valid.
12. Frontier output re-enters candidate evaluation.

## 34. Canonical Flow

Received Information
-> Interpretation
-> Evidence Classification
-> Evidence Evaluation
-> Relevant PCG
-> Candidate Formation
-> Candidate Reconciliation
-> Proposal Formation or Explicit No-Change
-> Consolidation Readiness
-> CCA
-> Governance
-> Cognitive Kernel
-> PCG / CSTR

## 35. Open Questions

CCPFM v0.1 intentionally leaves open:

- formal candidate ontology;
- proposal schema;
- candidate scoring/support semantics;
- belief proposal thresholds;
- reinforcement equations;
- identity resolution;
- relationship candidate reconciliation;
- conflict resolution;
- multi-target proposals;
- candidate dependencies;
- candidate prioritization;
- goal proposal constraints;
- dimension-specific proposal rules;
- proposal merging;
- concurrent proposals;
- rollback/compensation;
- recursive proposal generation;
- cryptographic provenance;
- candidate retention;
- serialization.

## 36. Core Principle

> GRI may recognize that a cognitive change deserves consideration without treating that recognition as a decision to change.

The complete boundary is:

Evidence
-> Candidate
-> Proposal
-> Governance
-> Cognitive Kernel
-> Persistent Cognition

Only the final governed kernel transition changes what GRI persistently knows or represents.
