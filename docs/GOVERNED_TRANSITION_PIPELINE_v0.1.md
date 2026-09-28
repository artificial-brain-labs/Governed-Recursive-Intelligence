# GRI Governed Transition Pipeline v0.1

**Status:** Initial integration specification  
**Version:** 0.1  
**Depends on:** Governance v0.1, Cognitive Kernel v0.1, CSTR v0.1

## Purpose

This specification defines the first executable integration of GRI governance and state-transition execution.

The pipeline makes the architectural boundary explicit:

Proposal -> Governance -> Authorization -> Kernel -> State Transition -> CSTR

## Authority

The pipeline does not grant CRP or a foundation model direct state-writing authority.

A proposal is only an input to governance.

The governance decision is the only authorization supplied to the kernel.

The kernel remains the only component that mutates persistent cognitive state.

## Execution

1. Receive current state and proposal.
2. Evaluate local constraints.
3. Evaluate global constitutional constraints.
4. Produce GovernanceDecision.
5. Pass that decision to the Cognitive Kernel.
6. Kernel commits only when status is approved.
7. Kernel produces successor state and CSTR.
8. Pipeline attaches the complete governance decision to the CSTR.

## Required Outcomes

### Approved

Governance returns approved -> kernel may commit if kernel invariants also pass.

### Rejected

Governance returns rejected -> kernel produces null transition.

### Requires Review

Governance returns requires_review -> kernel produces null transition.

### Pending

Governance returns pending -> kernel produces null transition.

This preserves the rule:

Only approved governance can authorize commitment.

## Failure Ownership

Governance owns authorization failures.

Kernel owns execution/precondition failures.

CSTR records both.

Examples:

- no evidence -> governance rejection
- constitutional constraint failure -> governance rejection
- target missing -> kernel null transition
- unsupported operation -> kernel null transition

## Architectural Invariant

The integrated pipeline must never provide a second path from proposal to persistent state.

There is exactly one commitment route:

Proposal -> Governance -> approved -> Kernel -> successor state

## No-Guessing

The pipeline never creates missing evidence.

It passes explicit evidence references into governance and the kernel.

Unknown remains unknown.

## Future Work

This v0.1 integration does not yet implement:
- CRP adapter
- full CSTR object model
- persistent storage
- transaction locking
- distributed concurrency
- constitutional policy engine
- recursive reflection
- human review workflow

Those remain separate architectural layers.
