## 15. Cognitive Dimensions

Each cognitive dimension is represented conceptually as:

D = (value, weight, state, constraints, relationships, learning_rate)

A cognitive dimension is a persistent, governed cognitive object. Trust is a
concrete instance of this unified model rather than a separate subsystem.

The fields mean:

- **value** = current dimension state; for Trust v0.1 this is an integer that may increase or decrease.
- **weight** = externally assigned importance or priority of the dimension.
- **state** = whether the dimension is active or inactive for a particular PCG update event.
- **constraints** = local governance conditions applicable to the dimension.
- **relationships** = typed, potentially directed connections to other cognitive dimensions or PCG objects, including possible impact semantics.
- **learning_rate** = how quickly the dimension is permitted to adapt its value through governed learning.

Relationships represent possible influence, not automatic mutation. A change in
one dimension may produce a proposed effect on a related dimension, which must
still pass governance before commitment.

The learning rate controls adaptation speed, not authorization. Evidence,
proposal, governance, and the cognitive transition mechanism determine whether a
dimension actually changes.

The exact numerical ranges, update equations, activation rules, and
cross-dimension impact equations remain open for experimental definition.

A dimension update therefore changes part of S_t, rather than creating a
separate ad-hoc learning mechanism.

For the detailed dimension ontology, see:
docs/COGNITIVE_DIMENSION_MODEL_v0.1.md.
