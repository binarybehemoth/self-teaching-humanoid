"""
backend/services/provenance.py  —  Data & Provenance Service
============================================================

Keeps the records, lineage, and consent that make the system auditable.
Because every important event leaves a structured record, the system's behaviour can
be reconstructed and accounted for — the precondition for assigning responsibility.
"""
from __future__ import annotations
import time


class ProvenanceService:
    def __init__(self):
        self._records: list[dict] = []

    def record_install(self, skill: str, robot_id: str) -> None:
        self._records.append({"event": "install", "skill": skill,
                              "robot": robot_id, "at": time.time()})

    def record(self, event: str, **fields) -> None:
        self._records.append({"event": event, **fields, "at": time.time()})

    def robots_with(self, skill: str) -> list[str]:
        """Trace which robots installed a skill — used for recall."""
        return [r["robot"] for r in self._records
                if r.get("event") == "install" and r.get("skill") == skill]

    def all(self) -> list[dict]:
        return list(self._records)
