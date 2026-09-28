# Change Record 0005 — Governance v0.1

**Date:** 2026-09-28
**Area:** GRI governance architecture
**Status:** Proposed / documented
**Branch:** feature/crp-v0.1

## Context

The Cognitive Kernel v0.1 established that persistent cognitive state can only be changed through an authorized transition.

The architecture therefore requires an explicit authorization mechanism rather than an opaque approval flag.

## Decision

Introduce Governance v0.1 as a distinct, non-mutating architecture layer.

Governance evaluates:
1. local constraints for the affected target/dimension
2. global constitutional constraints

The effective authorization is:

A_t = LocalGovernance(P_t) ∩ GlobalGovernance(P_t)

## Decision Model

Governance produces:
- approved
- rejected
- pending
- requires_review

Only approved permits kernel execution.

Individual constraint results remain traceable.

## Boundary

Governance authorizes.

The Cognitive Kernel executes.

Governance MUST NOT directly modify persistent cognitive state.

## No-Guessing

Governance cannot manufacture evidence or promote hypotheses into facts.

Insufficient evidence may cause rejection or review, but missing information remains missing.

## Consequence

The GRI transition pipeline now has an explicit authorization boundary:

Proposal
-> Local Governance
-> Global Constitutional Governance
-> Governance Decision
-> Cognitive Kernel
