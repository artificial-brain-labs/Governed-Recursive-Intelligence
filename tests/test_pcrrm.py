import copy

from kernel import CognitiveState
from retrieval import PCRRM, RetrievalContext, RetrievalSeed, RetrievalStatus


def state():
    return CognitiveState(
        state_id="STATE-RET-1",
        state_version=7,
        pcg={
            "ID-X": {"object_id": "ID-X", "object_type": "identity", "name": "Identity-X"},
            "ID-Y": {"object_id": "ID-Y", "object_type": "identity", "name": "Identity-Y"},
            "CONCEPT-1": {"object_id": "CONCEPT-1", "object_type": "concept", "label": "collaboration"},
        },
        dimensions={"trust-1": {"object_id": "trust-1", "dimension": "trust", "value": 5}},
        goals={"goal-1": {"object_id": "goal-1", "object_type": "goal", "label": "reliable collaboration"}},
        relationships={
            "rel-1": {
                "relationship_id": "rel-1",
                "source_id": "ID-X",
                "target_id": "ID-Y",
                "type": "works-with",
            }
        },
        learning={},
        history=[],
    )


def context():
    return RetrievalContext(
        interaction_id="INT-RET-1",
        instance_id="CI-RET-1",
        requirement={"task": "remember", "subject": "ID-X"},
    )


def test_direct_seed_retrieves_without_mutating_state():
    original = copy.deepcopy(state().__dict__)
    s = state()

    result = PCRRM().retrieve(
        s,
        context(),
        seeds=(RetrievalSeed("SEED-1", "identity", "ID-X"),),
    )

    assert result.retrieval_status == RetrievalStatus.COMPLETE
    assert "ID-X" in result.selected_objects
    assert s.__dict__ == original


def test_relationship_expansion_is_bounded_and_uses_established_relationship():
    result = PCRRM(max_expansion_depth=1).retrieve(
        state(),
        context(),
        seeds=(RetrievalSeed("SEED-1", "identity", "ID-X"),),
    )

    assert "rel-1" in result.selected_relationships
    assert "ID-Y" in result.selected_objects
    assert result.expansion_history[-1]["layer"] == 2


def test_missing_seed_does_not_invent_identity():
    result = PCRRM().retrieve(
        state(),
        context(),
        seeds=(RetrievalSeed("SEED-1", "identity", "UNKNOWN"),),
    )

    assert result.retrieval_status == RetrievalStatus.NO_RELEVANT_COGNITION_FOUND
    assert result.unresolved_candidates[0]["reason"] == "target_not_found"
    assert result.selected_objects == {}


def test_no_seed_is_not_retrieval_failure():
    result = PCRRM().retrieve(state(), context())

    assert result.retrieval_status == RetrievalStatus.NO_RELEVANT_COGNITION_FOUND
    assert result.retrieval_status != RetrievalStatus.RETRIEVAL_FAILURE


def test_retrieval_is_not_sufficiency_or_truth_evaluation():
    result = PCRRM().retrieve(
        state(),
        context(),
        seeds=(RetrievalSeed("SEED-1", "identity", "ID-X"),),
    )

    assert "sufficiency" not in result.provenance
    assert "truth" not in result.provenance


def test_restricted_reference_remains_restricted():
    ctx = RetrievalContext(
        interaction_id="INT-RET-1",
        instance_id="CI-RET-1",
        requirement={"task": "remember", "subject": "ID-X"},
        security_context={"restricted_object_ids": ["ID-X"]},
    )
    result = PCRRM().retrieve(
        state(),
        ctx,
        seeds=(RetrievalSeed("SEED-1", "identity", "ID-X"),),
    )

    assert result.retrieval_status == RetrievalStatus.ACCESS_RESTRICTED
    assert result.selected_objects == {}


def test_similarity_is_not_used_as_a_retrieval_rule():
    result = PCRRM().retrieve(
        state(),
        context(),
        seeds=(RetrievalSeed("SEED-1", "identity", "ID-X"),),
    )

    assert result.selected_objects["ID-X"]["target_id"] == "ID-X"
    assert "ID-Y" in result.selected_objects  # via explicit relationship, not name similarity
