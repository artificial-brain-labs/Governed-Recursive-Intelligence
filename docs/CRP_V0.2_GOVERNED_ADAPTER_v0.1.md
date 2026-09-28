# CRP v0.2 → Governed Transition Adapter v0.1

**Status:** Initial integration specification
**Version:** 0.1
**Depends on:** CRP v0.2, Governance v0.1, Cognitive Kernel v0.1, Governed Transition Pipeline v0.1

## Purpose

The adapter is the controlled boundary between CRP v0.2 and the executable GRI transition pipeline.

It ensures that structured representation can enter cognition execution without acquiring authority that belongs to Governance or the Cognitive Kernel.

## Authority Boundary

The adapter performs:
1. CRP structural validation
2. CRP semantic validation
3. predecessor state-context validation
4. extraction of evidence references
5. extraction of the proposal
6. invocation of actual Governance
7. invocation of the Cognitive Kernel

The adapter does not authorize proposals, mutate persistent state directly, trust CRP governance as authorization, infer missing evidence, or create beliefs/facts.

## Critical Rule: CRP Governance Is Not Authorization

CRP v0.2 contains governance metadata, but that metadata is not authoritative for execution.

The adapter ignores the CRP governance status when deciding whether a transition may commit.

Instead:

CRP Proposal -> Actual Governance -> GovernanceDecision -> Kernel

This prevents a serialized CRP candidate from self-authorizing persistent cognitive change.

## State Context

Before execution, CRP state_context must match the supplied CognitiveState in both state_id and state_version.

A mismatch is rejected before Governance or Kernel execution.

## Evidence

Evidence IDs are extracted from CRP evidence objects.

The adapter does not manufacture evidence.

Semantic validation must establish that proposal evidence references valid CRP evidence objects.

## Proposal

The CRP proposal is passed as a proposal candidate.

A missing proposal remains a valid non-commitment case.

The adapter does not convert interpretation or inference into a proposal.

## Execution Sequence

CRP Event
-> Structural Validation
-> Semantic Validation
-> State Context Validation
-> Evidence/Proposal Extraction
-> Local Governance
-> Global Governance
-> Governance Decision
-> Cognitive Kernel
-> Successor State
-> CSTR

## Failure Semantics

Invalid CRP: rejected before execution.

State-context mismatch: rejected before execution.

Governance rejection/review: explicit null transition and CSTR.

Kernel precondition failure: explicit null transition and CSTR.

## No-Guessing

The adapter never promotes:
- inference -> fact
- interpretation -> observation
- CRP governance metadata -> authorization
- unknown -> known
- proposal -> commitment

## Result

Foundation Model
-> CRP Candidate
-> CRP Validation
-> CRP Adapter
-> Governance
-> Cognitive Kernel
-> CSTR
-> Persistent Cognitive State

CRP remains a representation protocol.
Governance remains the authorization layer.
The Cognitive Kernel remains the state-transition authority.
