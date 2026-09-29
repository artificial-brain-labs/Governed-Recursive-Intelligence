# Change 0030 — Durable Pipeline Public Export v0.1

**Status:** Implemented  
**Date:** 2026-09-29  
**Branch:** `feature/crp-v0.1`

## 1. Purpose

Change 0030 aligns the public `pipeline` package interface with the durable execution contract implemented in `pipeline/pipeline.py`.

## 2. Change

The package initializer now exports both supported pipeline entrypoints:

- `execute_governed_transition`
- `execute_and_persist_transition`

This allows callers and tests to import the durable pipeline through the package boundary:

```python
from pipeline import execute_and_persist_transition
```

## 3. Architectural Impact

No cognitive, governance, state-transition, or persistence semantics are changed.

The change only exposes an already-implemented execution path through the package's public API.

## 4. Verification Target

The repository test suite should be executed after synchronizing the Codespace checkout with this commit.

The expected immediate result is that `tests/test_pipeline.py` can complete collection instead of failing on the package import.

## 5. Invariant

The public package API must expose every supported canonical execution entrypoint documented and implemented by the pipeline layer.

## 6. Conclusion

Change 0030 is an implementation/interface alignment fix only. It does not modify GRI cognitive theory or execution semantics.
