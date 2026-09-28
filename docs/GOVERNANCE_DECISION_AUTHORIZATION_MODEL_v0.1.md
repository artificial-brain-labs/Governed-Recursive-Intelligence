# GRI Governance Decision & Authorization Model v0.1

**Status:** Foundational architecture specification
**Version:** 0.1
**Depends on:** Governance v0.1, GRI Constitution v1.0, Cognitive Candidate & Proposal Formation Model v0.1, Cognitive Dimension Model v0.1, CSTR v0.1, Cognitive Kernel v0.1

## 1. Purpose

The Governance Decision & Authorization Model (GDA) formalizes how GRI evaluates a structured cognitive proposal against applicable local constraints and global constitutional constraints.

It defines the authorization boundary:

Proposal -> Governance Evaluation -> Authorization Decision -> Cognitive Kernel

It does not interpret experience, establish external truth, generate evidence, or mutate persistent cognition.

## 2. Core Principle

Governance determines whether a proposed cognitive transition is authorized; it does not determine whether the underlying external-world proposition is true.

Governance Approval != Truth
Governance Evaluation != Cognitive Execution

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

## 4. Governance Context

Evaluation receives bounded context containing the proposal, affected target, predecessor state reference, evidence references, applicable dimension/object constraints, constitutional rules, relevant goal context, governance version, and authorization context.

Governance does not require unrestricted PCG access.

## 5. Two-Level Governance

### Local Governance

Evaluates target- or dimension-specific constraints such as update limits, permitted operations, learning-rate limits, lifecycle rules, relationship constraints, evidence requirements, and review conditions.

### Global Constitutional Governance

Evaluates system-wide constraints including constitutional principles, safety constraints, ethical constraints, system-wide invariants, master governance restrictions, goal-evolution restrictions, and recursive-modification restrictions.

Local approval cannot override global rejection.

## 6. Constraint Evaluation

Each applicable constraint produces an explicit evaluation:

ConstraintEvaluation = (
constraint_id,
layer,
applicability,
status,
reason,
rule_version
)

Status values:
- pass
- fail
- review
- not_applicable

Applicability must not silently become pass when unresolved.

## 7. Authorization States

GDA supports:
- approved
- rejected
- pending
- requires_review

Only approved authorizes Cognitive Kernel execution.

## 8. Decision Rules

1. Any mandatory global constraint failure -> rejected.
2. Any mandatory local constraint failure -> rejected.
3. Any unresolved mandatory governance condition -> requires_review or pending according to applicable workflow.
4. Any mandatory review condition -> requires_review.
5. If all applicable mandatory constraints pass and no review condition remains -> approved.

The exact precedence between pending and requires_review remains open where no workflow is defined.

## 9. Conditional Authorization

Future governance rules may permit approval with explicit conditions. A conditional decision must identify the condition, enforcement layer, required completion state, and expiration where applicable.

Conditions must not be treated as satisfied merely because a proposal was approved.

## 10. Evidence and Targets

Governance may require evidence references but does not create evidence.

Governance may evaluate whether targets are sufficiently defined. Unresolved identity or target ambiguity must not silently become authorization.

## 11. State Preconditions

Authorization is bound to the predecessor state against which the proposal was evaluated.

Authorization for state version t is not automatically valid for a materially changed state version t+1.

If the predecessor state changes before execution, re-evaluation may be required.

## 12. Governance vs Kernel

Governance answers:

Is this transition authorized?

The Kernel answers:

Can this authorized transition be executed against the actual predecessor state?

Therefore:

Governance Authorization != Kernel Execution Success

Kernel execution failure must not be converted into a different governance authorization.

## 13. Re-evaluation

A proposal may require governance re-evaluation when evidence, proposal contents, target resolution, relevant PCG, predecessor state, or applicable governance rules change materially.

Previous authorization remains historical; it does not automatically authorize the revised proposal.

## 14. Recursive, Goal, Dimension, and Relationship Governance

Recursive proposals follow the same path:

Reflection -> Candidate -> Proposal -> Governance -> Kernel

Goal creation, modification, suspension, removal, and evolution remain constitutionally bounded.

Dimension updates pass through local dimension governance and global governance. Learning rate controls adaptation speed, not authorization.

Relationship changes require evaluation of source, target, type, direction, semantics, evidence, and applicable constraints.

## 15. Governance Decision Provenance

The decision must preserve which proposal was evaluated, predecessor state, local and global constraints, evidence references inspected, decision, reason, and governance version.

This information becomes part of CSTR at the persistent transition boundary.

## 16. Rejection Semantics

A rejected proposal does not establish that its underlying proposition is false.

It establishes only that the proposed persistent cognitive transition was not authorized under the applicable governance rules.

A rejected proposal may still be recorded in CSTR.

## 17. Null Transition

When a proposal is not authorized:

S_(t+1) = S_t

This is a valid null transition and its governance reason remains traceable.

## 18. No-Guessing Invariants

1. Governance approval is not truth.
2. Governance rejection is not proof of falsity.
3. Governance does not create evidence.
4. Missing evidence is not evidence of falsity.
5. Unresolved identity is not authorization.
6. Candidate is not authorization.
7. Proposal is not authorization.
8. Review is not authorization.
9. Local approval cannot override global rejection.
10. Recursive cognition cannot bypass governance.
11. Governance does not directly mutate PCG.
12. Stale authorization cannot automatically authorize a changed state.
13. Kernel execution remains separate from authorization.
14. Governance cannot silently invent missing conditions.

## 19. Architectural Invariants

1. Every persistent cognitive proposal passes through Governance.
2. Governance has local and global constitutional layers.
3. Every authorization decision is explicit.
4. Individual constraint evaluations remain traceable.
5. Only approved decisions may authorize Kernel execution.
6. Governance does not execute state changes.
7. Governance does not establish external-world truth.
8. Governance decisions are versioned and provenanced.
9. Material proposal/state/rule changes can invalidate prior authorization.
10. CSTR records authorization context at the transition boundary.

## 20. Canonical Flow

Proposal
-> Authorization Context
-> Local Constraint Evaluation
-> Global Constitutional Evaluation
-> Authorization Decision
-> Approved -> Cognitive Kernel
-> Rejected / Pending / Review -> Null or deferred transition
-> CSTR

## 21. Open Questions

- complete constitutional policy language
- machine-readable constraint ontology
- constraint dependency resolution
- conditional authorization
- human approval workflows
- authorization expiry
- state-version binding
- policy versioning
- distributed governance
- cryptographic authorization
- emergency governance
- goal conflict resolution
- risk models
- evidence thresholds
- governance learning
- constitutional self-modification
- audit storage
- authorization delegation

## 22. Core Principle

Governance is the constitutional decision boundary between a proposed cognitive change and permission to execute that change.

The final boundary remains:

Proposal -> Governance Authorization -> Cognitive Kernel -> Persistent Cognitive State
