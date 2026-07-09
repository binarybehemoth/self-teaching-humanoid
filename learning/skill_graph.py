"""
learning/skill_graph.py  —  The Skill Graph
===========================================

The organised map of a robot's skills and their prerequisites. Learning is
structured through this graph: a skill can be acquired once its prerequisites are, and
a failure can be diagnosed into a missing or weak prerequisite.
"""
from __future__ import annotations


class SkillGraph:
    def __init__(self):
        self._deps: dict[str, list[str]] = {}   # skill -> prerequisite skills

    def add(self, skill: str, prerequisites: list[str] | None = None) -> None:
        self._deps[skill] = list(prerequisites or [])

    def prerequisites(self, skill: str) -> list[str]:
        return self._deps.get(skill, [])

    def can_learn(self, skill: str, known: set[str]) -> tuple[bool, list[str]]:
        """A skill is learnable once its prerequisites are known."""
        missing = [p for p in self.prerequisites(skill) if p not in known]
        return (len(missing) == 0, missing)

    def frontier(self, known: set[str]) -> list[str]:
        """Skills whose prerequisites are all met but which are not yet known —
        the frontier a self-set curriculum aims at."""
        out = []
        for skill in self._deps:
            if skill not in known:
                ok, _ = self.can_learn(skill, known)
                if ok:
                    out.append(skill)
        return out
