"""
learning/broad_learning.py  —  Broad Learning
=============================================

Acquiring competence from many sources at once (Parts V–VII): human demonstration, other
robots, the robot's own experience, and imagination. This module illustrates the
INTERFACE by which experience of every kind is turned into skill improvements; a real
pipeline trains large models on large data.
"""
from __future__ import annotations


class BroadLearning:
    """Ingests experience from any source into competence updates."""

    SOURCES = ("human_video", "teacher", "fleet", "experience", "imagination")

    def __init__(self, self_model=None):
        self.self_model = self_model
        self._ingested: list[dict] = []

    def ingest(self, source: str, skill: str, quality: float = 1.0) -> None:
        assert source in self.SOURCES, f"unknown source: {source}"
        self._ingested.append({"source": source, "skill": skill, "quality": quality})
        # In this scaffold, ingesting quality experience nudges competence upward.
        if self.self_model is not None and quality >= 0.5:
            self.self_model.record_outcome(skill, success=True)

    def summary(self) -> dict:
        by_source: dict[str, int] = {}
        for e in self._ingested:
            by_source[e["source"]] = by_source.get(e["source"], 0) + 1
        return by_source
