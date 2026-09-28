"""Reference file-backed persistence for GRI cognitive state and CSTR."""
from __future__ import annotations

import json
import os
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from typing import Any

from kernel import CognitiveState


class StateStoreError(RuntimeError):
    pass


class StaleStateError(StateStoreError):
    pass


class StateStore:
    def initialize(self, state: CognitiveState) -> None:
        raise NotImplementedError

    def read_current_state(self) -> CognitiveState:
        raise NotImplementedError

    def read_state_version(self) -> int:
        raise NotImplementedError

    def read_transition(self, transition_id: str) -> dict[str, Any]:
        raise NotImplementedError

    def list_transitions(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    def record_transition(self, cstr: dict[str, Any]) -> None:
        """Persist transition history without changing current state."""
        raise NotImplementedError

    def commit_transition(
        self,
        *,
        expected_state_version: int,
        successor: CognitiveState,
        cstr: dict[str, Any],
    ) -> None:
        raise NotImplementedError


def _state_dict(state: CognitiveState) -> dict[str, Any]:
    return asdict(state)


def _state_from_dict(data: dict[str, Any]) -> CognitiveState:
    return CognitiveState(**data)


class JsonJournalStateStore(StateStore):
    """Small reference implementation; not intended as production storage."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.journal = self.root / "journal.jsonl"
        self.manifest = self.root / "manifest.json"

    def _write_atomic(self, path: Path, data: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(data, encoding="utf-8")
        os.replace(tmp, path)

    def _read_entries(self) -> list[dict[str, Any]]:
        if not self.journal.exists():
            return []
        entries = []
        for line in self.journal.read_text(encoding="utf-8").splitlines():
            if line.strip():
                entries.append(json.loads(line))
        return entries

    def initialize(self, state: CognitiveState) -> None:
        if self.manifest.exists() or self.journal.exists():
            raise StateStoreError("store is already initialized")
        self._write_atomic(
            self.journal,
            json.dumps(
                {"type": "initial_state", "state": _state_dict(state)},
                separators=(",", ":"),
            ) + "\n",
        )
        self._write_atomic(
            self.manifest,
            json.dumps(
                {"state_id": state.state_id, "state_version": state.state_version},
                separators=(",", ":"),
            ),
        )

    def read_current_state(self) -> CognitiveState:
        entries = self._read_entries()
        if not entries:
            raise StateStoreError("store is not initialized")
        state = entries[0]["state"]
        for entry in entries[1:]:
            if entry["type"] == "commit":
                state = entry["successor_state"]
        return _state_from_dict(state)

    def read_state_version(self) -> int:
        return self.read_current_state().state_version

    def read_transition(self, transition_id: str) -> dict[str, Any]:
        for entry in self._read_entries():
            if entry.get("type") in {"commit", "transition"} and entry["cstr"].get("transition_id") == transition_id:
                return deepcopy(entry["cstr"])
        raise KeyError(transition_id)

    def list_transitions(self) -> list[dict[str, Any]]:
        return [
            deepcopy(entry["cstr"])
            for entry in self._read_entries()
            if entry.get("type") in {"commit", "transition"}
        ]

    def record_transition(self, cstr: dict[str, Any]) -> None:
        if "transition_id" not in cstr or "outcome" not in cstr:
            raise StateStoreError("CSTR requires transition_id and outcome")
        entry = {
            "type": "transition",
            "transition_id": cstr["transition_id"],
            "cstr": deepcopy(cstr),
        }
        with self.journal.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, separators=(",", ":")) + "\\n")

    def commit_transition(
        self,
        *,
        expected_state_version: int,
        successor: CognitiveState,
        cstr: dict[str, Any],
    ) -> None:
        current = self.read_current_state()
        if current.state_version != expected_state_version:
            raise StaleStateError(
                f"expected state version {expected_state_version}, "
                f"found {current.state_version}"
            )
        if cstr.get("outcome") != "committed":
            raise StateStoreError("commit_transition requires a committed CSTR")
        if str(cstr["state_before"]["state_version"]) != str(expected_state_version):
            raise StateStoreError("CSTR predecessor version does not match expected version")
        if str(cstr["state_after"]["state_version"]) != str(successor.state_version):
            raise StateStoreError("CSTR successor version does not match successor state")

        entry = {
            "type": "commit",
            "transition_id": cstr["transition_id"],
            "successor_state": _state_dict(deepcopy(successor)),
            "cstr": deepcopy(cstr),
        }

        with self.journal.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, separators=(",", ":")) + "\n")

        self._write_atomic(
            self.manifest,
            json.dumps(
                {"state_id": successor.state_id, "state_version": successor.state_version},
                separators=(",", ":"),
            ),
        )
