# CRP v0.1 Semantic Validation

CRP uses two validation layers.

## Structural validation

JSON Schema Draft 2020-12 validates the representation structure: required
fields, types, enumerations, array constraints, unknown-property rejection,
and basic formats.

## Semantic integrity validation

The deterministic validator checks relationships across the complete Cognitive
Event that isolated field validation cannot establish.

### Rules

1. **Provenance integrity**  
   `provenance.source_interaction` MUST equal `interaction_id`.

2. **Unknown means unknown**  
   An observation marked `unknown` MUST NOT contain facts.

3. **Inference grounding**  
   Every inference basis MUST reference an observed fact in the same event.
   Linguistic observations such as the presence of the word "again" must be
   represented explicitly as facts if they are used as evidence.

4. **Governance boundary**  
   A cognitively rejected event MUST NOT contain cognitive updates that could
   be treated as authorized changes.

5. **No truth oracle**  
   Semantic validation does not determine whether an external-world claim is
   true. It validates representation integrity and evidence relationships only.

## Architectural boundary

The validation sequence is:

Foundation Model
→ CRP Candidate
→ Structural Validation
→ Semantic Validation
→ Governance Validation
→ Cognitive Kernel
→ Persistent Cognitive Graph

A CRP candidate that fails validation MUST NOT be written directly to the
Persistent Cognitive Graph.

JSON Schema is therefore the first gate, not the complete cognitive safety
mechanism.
