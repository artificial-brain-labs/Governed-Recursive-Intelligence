# Change Record 0006 — Governed Transition Pipeline v0.1

**Date:** 2026-09-28  
**Area:** GRI governance/kernel integration  
**Status:** Proposed / documented  
**Branch:** feature/crp-v0.1

## Context

Governance v0.1 and Cognitive Kernel v0.1 were implemented as separate layers.

The architecture now requires an explicit integration boundary showing that authorization flows from Governance to the Kernel and that no alternative commitment path exists.

## Decision

Introduce an end-to-end governed transition pipeline.

The pipeline:
1. receives a proposal
2. evaluates local and global governance
3. produces a GovernanceDecision
4. passes that decision to the Cognitive Kernel
5. allows commitment only for approved decisions
6. records the complete governance decision in CSTR

## Boundary

Governance authorizes.

Kernel executes.

CSTR records.

CRP and foundation models cannot bypass this pipeline.

## Consequence

GRI now has an executable path from proposal through governance to persistent state transition and historical recording.

The next major integration point is a CRP-to-pipeline adapter, provided it preserves the same authority boundaries.
