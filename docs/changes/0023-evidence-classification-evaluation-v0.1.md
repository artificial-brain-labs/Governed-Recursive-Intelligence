# Change Record 0023 — Evidence Classification & Evaluation Model v0.1

**Date:** 2026-09-28
**Branch:** feature/crp-v0.1
**Status:** Proposed / documented

## 1. Decision

Introduce ECEM v0.1 as the explicit GRI layer for determining what received information can legitimately support during cognitive processing.

## 2. Architectural Reason

CIL distinguishes observation from interpretation. ECEM adds the next boundary so interpretation cannot silently become an established external-world fact.

Core distinction:

Evidence About X != Evidence That X Is True

## 3. Evidence Boundary

Evidence is a temporary processing structure with source, claim scope, evidence type, support or contradiction relationship, limitations, status, and provenance.

Evidence does not directly create persistent cognition.

The governed path remains:

Evidence -> Proposal -> Governance -> Cognitive Kernel -> PCG

## 4. Requirement-Relative Evaluation

Evidence sufficiency depends on the current requirement.

Evidence sufficient to answer “What did the user report?” may be insufficient to answer “Did the reported event actually occur?”

## 5. Failure-State Distinctions

ECEM distinguishes:
- no evidence identified;
- evidence retrieval failure;
- evidence inaccessible;
- evidence insufficient;
- conflicting evidence.

Therefore:

Retrieval Failure != Evidence Absence
Evidence Absence != Proposition False

## 6. Frontier Integration

Frontier output remains new information and follows:

Frontier Output -> Re-entry -> Interpretation -> Evidence Classification -> Evidence Evaluation

Frontier output does not receive automatic truth or persistence authority.

## 7. No-Guessing Impact

ECEM establishes:
- evidence is not automatically truth;
- inference is not observation;
- missing evidence is not falsity;
- conflicting evidence remains explicit;
- evidence does not directly mutate PCG;
- evidence does not authorize action;
- evidence does not guarantee proposal approval.

## 8. Consequences

ECEM makes evidence a first-class architectural concern, enables explicit communication-vs-world evidence distinctions, preserves provenance and conflict, and gives ICSM and routing structured evidence-state information.

## 9. Open Questions

Formal evidence ontology, source authority, corroboration, evidence-strength semantics, conflict resolution, temporal validity, evidence thresholds, tool-result semantics, frontier evidence semantics, serialization, retention, and provenance integrity remain open.

## 10. Repository Principle

This is an architectural documentation decision only. No production evidence evaluator is claimed to exist.

Future implementation must preserve the separation between evidence, truth, proposal, governance, and commitment.
