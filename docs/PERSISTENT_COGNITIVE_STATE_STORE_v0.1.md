# GRI Persistent Cognitive State Store v0.1

**Status:** Initial persistence specification  
**Version:** 0.1  
**Depends on:** Cognitive State Transition Model v0.1, CSTR v0.1, Cognitive Kernel v0.1

## 1. Purpose

The Persistent Cognitive State Store provides durable storage for GRI's persistent cognitive state and transition history.

It is a storage abstraction, not a new cognitive layer.

The logical distinction remains:

- **PCG:** what persistent cognition exists now
- **CSTR:** what governed transitions produced or preserved that cognition
- **TCM:** transient communication and experience context

Therefore:

TCM != PCG != CSTR

## 2. Architectural Boundary

The Cognitive Kernel remains the only component that determines a state transition.

The store does not decide whether a proposal is valid, governed, or cognitively justified.

The store persists the result of an already-authorized kernel transition.

Pipeline:

Governance
-> Cognitive Kernel
-> State Transition
-> Persistence Store
-> PCG + CSTR

The store must never provide an alternate route around Governance or the Kernel.

## 3. Persistent State

A persistent state is identified by:

- state_id
- state_version
- predecessor state reference

The state contains the current logical components:

- PCG
- cognitive dimensions
- goals
- relationships
- learning state
- transition-history references

The store may serialize these structures differently, but their architectural meaning remains unchanged.

## 4. State Version Continuity

For a committed transition:

S_t -> S_(t+1)

The store must verify that the transition was based on the current expected predecessor version.

Conceptually:

expected_version == stored_current_version

If not, the write must fail rather than silently overwrite newer cognition.

This establishes optimistic state-version protection for the reference implementation.

## 5. CSTR Persistence

Every evaluated transition that enters the persistent execution boundary must have a durable CSTR.

This includes:

- committed transitions
- null transitions
- governance rejection
- required review
- kernel precondition failure

A null transition is still part of cognitive history.

## 6. Atomic Commit Boundary

A committed transition must persist as one logical operation:

1. predecessor validation
2. successor state creation
3. CSTR creation
4. durable commit

The reference implementation uses a transaction envelope to make the storage operation recoverable without making CSTR itself contain the full state.

The transaction envelope is a storage artifact, not part of GRI cognitive theory.

## 7. Recovery

On restart, the store must be able to determine:

- current state
- current state version
- transition history
- last committed transition

Recovery must not invent missing cognition.

If a transaction is incomplete or corrupted, the store must fail safely rather than reconstructing unsupported cognitive content.

## 8. Storage Abstraction

The logical interface should support:

- initialize
- read_current_state
- read_state_version
- read_transition
- list_transitions
- commit_transition

The implementation must remain independent of a particular database.

## 9. Reference Implementation

v0.1 uses a file-backed append-only journal as the reference implementation.

This is intentionally a prototype storage mechanism.

It demonstrates:

- durability
- state-version continuity
- transition history
- recovery
- separation between logical state and CSTR

It does not claim that files are the final production storage architecture.

## 10. No Direct State Writes

Callers cannot persist arbitrary cognitive mutations through the store.

The commit operation requires:

- expected predecessor version
- successor state
- CSTR
- committed transition identity

This keeps the store downstream of the Kernel.

## 11. No-Guessing

Persistence never fills missing fields with inferred cognition.

It must preserve:

Observed != Interpreted != Inferred != Believed

and:

Unknown remains Unknown.

## 12. CSTR and PCG Relationship

CSTR references state versions.

PCG/state storage contains the resulting persistent cognition.

CSTR does not become the PCG.

PCG does not replace CSTR.

Historical transition data may later be used by recursive cognition, but history is evidence about system behavior and must not automatically become external-world belief.

## 13. TCM Boundary

TCM is not stored as persistent cognitive state by this component.

Transient communication storage may exist elsewhere.

The Persistent Cognitive State Store only persists information that has crossed the governed cognitive-transition boundary.

## 14. Future Research

This specification deliberately leaves open:

- database technology
- distributed storage
- sharding
- cryptographic integrity
- event sourcing vs snapshots
- graph database representation
- vector/semantic indexes
- concurrency beyond version checks
- compaction
- archival
- encryption
- access control
- replication

These are implementation concerns, not yet GRI cognitive theory.

## 15. Core Invariants

1. Persistent state changes only originate from the Cognitive Kernel.
2. Every committed transition references a predecessor state.
3. State versions cannot silently regress.
4. CSTR remains distinct from PCG.
5. Null transitions remain durable history.
6. TCM is not persistent cognitive state.
7. Recovery never invents cognition.
8. Storage cannot bypass Governance or the Kernel.
9. A stale predecessor cannot overwrite newer cognition.
10. Persistence preserves provenance and transition identity.
