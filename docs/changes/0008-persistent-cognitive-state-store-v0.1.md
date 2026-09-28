# Change Record 0008 — Persistent Cognitive State Store v0.1

**Date:** 2026-09-28
**Area:** GRI persistence architecture
**Status:** Proposed / documented
**Branch:** feature/crp-v0.1

## Context

GRI now has an executable path from CRP through Governance and the Cognitive Kernel to a successor cognitive state and CSTR.

The current kernel state exists only in memory. GRI therefore requires a persistence boundary.

Earlier architecture decisions establish:
- TCM stores transient communication.
- PCG stores enduring cognitive consequences.
- CSTR stores transition history.
- CCA is the gateway through which cognitive consequences enter persistent cognition.

## Decision

Introduce a Persistent Cognitive State Store abstraction.

The store is downstream of the Cognitive Kernel and cannot authorize or create transitions.

A committed transition must be persisted with:
- predecessor state reference
- successor state
- CSTR
- transition identity
- state version continuity

## Storage Strategy

Use a file-backed append-only journal as the v0.1 reference implementation.

This is not a decision that GRI will use files in production.

The abstraction deliberately leaves database, graph, distributed, and event-sourcing decisions open.

## State Versioning

The store uses expected predecessor state_version protection.

A stale transition must fail instead of overwriting newer cognition.

## Atomicity

The storage layer uses a transaction envelope to keep successor-state persistence and CSTR persistence as one recoverable logical commit.

The envelope is a storage implementation artifact and does not redefine CSTR or PCG.

## Consequence

GRI now has a durable persistence boundary while keeping cognition, governance, execution, history, and storage architecturally separate.

The next research work can evaluate PCG's actual internal ontology and graph semantics without being forced by the storage technology.
