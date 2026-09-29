# Change Record 0025 — Governance Decision & Authorization Model v0.1

**Date:** 2026-09-28
**Branch:** feature/crp-v0.1
**Status:** Proposed / documented

## 1. Decision

Introduce the Governance Decision & Authorization Model (GDA) v0.1 as a refinement of Governance v0.1.

It formalizes the decision object, constraint evaluation lifecycle, authorization freshness, and the separation between Governance authorization and Kernel execution.

## 2. Core Boundary

Proposal -> Governance Evaluation -> Authorization Decision -> Cognitive Kernel

Governance approval is not a statement that the underlying external-world proposition is true.

## 3. Authorization Decision

AuthorizationDecision = (
decision_id,
proposal_id,
state_reference,
local_evaluations,
global_evaluations,
status,
conditions,
reason,
governance_version,
timestamp,
provenance
)

The exact serialization remains open.

## 4. Two-Level Governance

The existing architecture is retained:

Local Governance + Global Constitutional Governance

Local approval cannot override global rejection.

## 5. Constraint Evaluation

Applicable constraints produce explicit results:

pass / fail / review / not_applicable

Applicability must not silently become pass when unresolved.

## 6. Authorization States

Supported states remain:

approved
rejected
pending
requires_review

Only approved authorizes Kernel execution.

## 7. Authorization Freshness

Authorization is bound to the relevant proposal, predecessor state, governance version, and evaluation context.

Material changes may require re-evaluation.

## 8. Governance vs Kernel

Governance determines whether a transition is authorized.

The Kernel determines whether that authorized transition can be executed against the actual predecessor state.

Governance Authorization != Kernel Execution Success

## 9. Rejection Semantics

A rejected proposal does not establish that the underlying proposition is false. It means the proposed persistent cognitive transition was not authorized under applicable governance rules.

## 10. Persistent Boundary

No alternate persistence route is introduced.

Proposal -> Governance -> Cognitive Kernel -> PCG

CSTR records authorization context and the committed or null transition.

## 11. Recursive and Goal Governance

Recursive proposals use the same governance path. Goal evolution remains constitutionally bounded. No goal or recursive process may authorize itself.

## 12. No-Guessing Impact

GDA reinforces:

approval != truth
rejection != falsity
missing evidence != falsity
proposal != authorization
review != authorization
local approval cannot override global rejection
stale authorization cannot silently authorize a changed state

## 13. Consequences

GDA makes authorization a first-class traceable object, clarifies local/global governance, addresses stale authorization, and keeps Governance and Kernel responsibilities separate.

Future work remains for machine-readable policy, state binding, conditional authorization, human review, cryptographic authorization, and distributed governance.

## 14. Repository Principle

This is architectural documentation only. No claim is made that the complete GDA engine is implemented.

Future implementation must preserve:

Proposal -> Governance -> Authorization -> Kernel -> Persistent Cognition.
