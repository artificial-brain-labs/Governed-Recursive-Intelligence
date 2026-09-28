# Change Record 0022 — Cognitive Interpretation Layer v0.1

**Date:** 2026-09-28  
**Branch:** feature/crp-v0.1  
**Status:** Proposed / documented  
**Related architecture:** GRI Cognitive Instance, ICG, CRIDM, PCRRM, ICSM, CCA, Frontier Output Re-entry

## 1. Decision

Introduce the **Cognitive Interpretation Layer (CIL) v0.1** as the explicit GRI processing layer responsible for transforming received communication/experience into structured candidate meanings while preserving the distinction between observation, interpretation, evidence, requirement, and persistent cognition.

## 2. Why This Change Is Required

The architecture already defines:

- how an interaction is received;
- how a Cognitive Instance is created;
- how Curiosity activates;
- how requirements are identified;
- how relevant persistent cognition is retrieved;
- how internal sufficiency is evaluated;
- how routing and frontier delegation operate.

A missing architectural boundary remained between raw communication and requirement identification.

Without an explicit interpretation layer, semantic parsing could silently become:

`Communication -> Assumed Meaning -> Requirement / Cognition`

This conflicts with the GRI no-guessing principle.

CIL makes the semantic transformation explicit and traceable.

## 3. Architectural Decision

The canonical sequence is now:

`Communication
-> Cognitive Instance
-> Curiosity
-> Cognitive Interpretation
-> Requirement Identification
-> Requirement Decomposition
-> PCG Relevance Retrieval
-> Internal Cognition Sufficiency
-> Gap Identification
-> Routing`

Interpretation is temporary interaction cognition and does not directly mutate PCG.

## 4. Core Boundaries

The following distinctions are now explicit:

### Observation != Interpretation

What was received is not automatically what it means.

### Interpretation != Evidence

An interpretation of communication does not establish an external-world fact.

### Interpretation != Requirement

An interpretation can contribute to requirement identification, but a requirement describes what processing is needed.

### Interpretation != Belief

Interpretation cannot directly create persistent belief.

### Reference != Identity

A name, pronoun, or object reference does not automatically resolve to a persistent identity.

### Candidate Relationship != Persistent Relationship

An interpreted relationship remains temporary until evidence, proposal, governance, and kernel execution establish persistence.

### Frontier Output != Truth

Frontier output is new information and must re-enter GRI interpretation and evaluation.

## 5. New Interpretation Model

CIL defines the conceptual representation:

`Interpretation =
(
interpretation_id,
interaction_id,
instance_id,
source_references,
interpretation_type,
content,
basis,
context_references,
alternatives,
uncertainty_state,
status,
provenance
)`

The exact serialization remains open.

## 6. Important New Architectural Property

Not every interaction contains a requirement.

GRI must support:

`Interpretation -> No Current Requirement`

without treating that as a failure.

This allows informational, corrective, relational, conversational, and other interactions to be processed without inventing a task.

## 7. Frontier Integration

Frontier models may assist interpretation only after the established routing process authorizes delegation.

Every returned frontier response remains new information:

`Frontier Model
-> Frontier Response
-> New Information Re-entry
-> Cognitive Interpretation
-> Requirement / Evidence Evaluation`

The model that produced an interpretation does not receive authority to define persistent cognition.

## 8. No-Guessing Impact

CIL reinforces the repository-wide principle that missing information must remain missing.

In particular:

- missing context is not invented;
- ambiguous references remain ambiguous;
- alternative interpretations may coexist;
- temporal precision is not invented;
- hidden intent is not assumed;
- semantic interpretation is not factual commitment;
- interpretation does not mutate PCG.

## 9. Relationship to Existing Architecture

CIL supplies structured interpretation context to:

- CRIDM for requirement identification;
- ICG for temporary interpretation nodes and relationships;
- PCRRM for possible retrieval seeds;
- ICSM for requirement-relative sufficiency evaluation;
- routing for downstream capability decisions;
- CCA only after candidate/proposal processing is complete.

CIL does not replace any of these components.

## 10. Persistent Cognition Boundary

The existing persistent transition boundary remains unchanged:

`Evidence -> Proposal -> Governance -> Cognitive Kernel -> PCG`

CIL introduces no alternate path.

## 11. Consequences

Positive consequences:

- semantic interpretation becomes an explicit architectural concern;
- no-guessing boundaries become easier to enforce;
- ambiguous meaning can be represented without premature commitment;
- requirement extraction becomes traceable;
- frontier-assisted interpretation can be safely re-entered;
- interpretation provenance becomes available for later reasoning.

Tradeoffs:

- the cognitive pipeline gains another explicit processing stage;
- interpretation and requirement representations must be kept distinct;
- future implementation will need a formal interpretation ontology;
- ambiguity management becomes an explicit computational concern.

## 12. Open Questions

The following remain intentionally unresolved:

- exact interpretation ontology;
- parser implementation;
- semantic representation;
- pragmatic interpretation;
- reference resolution;
- temporal normalization;
- uncertainty semantics;
- conflict resolution;
- multilingual processing;
- frontier-assisted interpretation;
- provenance serialization;
- interpretation/evidence classification;
- interpretation/requirement mapping;
- computational budgets.

## 13. Repository Principle

This change is architectural documentation only.

No claim is made that a production CIL implementation exists yet.

Future implementation must be derived from this specification and must preserve the stated invariants.
