# Change Record 0009 — Cognitive Dimension Model v0.1

**Date:** 2026-09-28  
**Area:** GRI cognitive architecture  
**Status:** Proposed / documented  
**Branch:** feature/crp-v0.1

## Context

The GRI Cognitive State Transition Model already defined the unified cognitive
dimension tuple:

D = (value, weight, state, constraints, relationships, learning_rate)

The model needed a precise interpretation before defining the internal PCG
ontology.

## Decision

Formalize the unified cognitive dimension as the common structure for all
dimensions, with Trust as the first concrete example.

Trust is not a separate architecture. It is an instance of the common
dimension model.

### Value

Value is the current numerical state of the dimension.

For the initial Trust model, value is an integer that may increase or decrease.

### Weight

Weight is externally assigned importance/priority for the dimension.

Weight is distinct from value and does not represent truth, confidence, or
evidence strength.

### State

State indicates whether the dimension is active or inactive for a particular
PCG update event.

Inactive does not mean deleted, false, or weakened.

### Constraints

Constraints define local governance conditions applicable to the dimension.

They remain subordinate to Global Constitutional Governance.

### Relationships

Relationships define how a dimension connects to other dimensions/cognitive
objects in the PCG.

A relationship is not merely a link. It carries direction, relationship type,
and possible impact semantics.

A source-dimension change produces an evaluated possible effect/proposal for the
target. It does not automatically mutate the target.

### Learning Rate

Learning rate controls how quickly a dimension is permitted to adapt its value.

It does not decide whether an update is authorized.

Authorization remains the responsibility of evidence, proposal, and governance.

## Architectural Consequence

The PCG ontology should represent dimensions as persistent cognitive objects
and relationships as typed, potentially directed edges carrying cognitive-impact
semantics.

This keeps cognitive theory independent from a particular graph database or
storage technology.

## Explicit Boundary

Dimension update:

Experience
-> Evidence
-> Dimension Proposal
-> Local Governance
-> Global Governance
-> Governed Dimension Update
-> CSTR
-> PCG

Cross-dimension influence:

Dimension Change
-> Relationship Evaluation
-> Possible Target Proposal
-> Governance
-> Possible Target Update

Relationship influence is therefore not automatic state mutation.

## Open Research

Exact mathematical forms for Trust value bounds, weight, learning rate,
relationship impact, activation, and cross-dimension conflict remain open.
They must be experimentally validated rather than prematurely fixed.
