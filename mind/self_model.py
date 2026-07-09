"""
mind/self_model.py  —  The Self-Model
=====================================

The robot's honest, uncertain estimate of its own competence. A new skill
begins with a LOW and UNCERTAIN estimate; the estimate rises only as the skill is
proven, per skill and per setting. This is what makes the robot act cautiously on
things it has not yet earned confidence in — and what lets it know the boundary of
what it can do.

Trust is never granted wholesale; it is accumulated from evidence.
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Competence:
    estimate: float = 0.2        # low until proven
    uncertainty: float = 0.8     # high until proven
    attempts: int = 0
    successes: int = 0


class SelfModel:
    def __init__(self):
        self._skills: dict[str, Competence] = {}
        self._goals: dict[str, int] = {}

    def competence(self, skill: str) -> Competence:
        return self._skills.setdefault(skill, Competence())

    def should_act_cautiously(self, skill: str) -> bool:
        """A robot acts cautiously on skills it has not yet proven."""
        c = self.competence(skill)
        return c.uncertainty > 0.3 or c.estimate < 0.7

    def record_outcome(self, skill: str, success: bool) -> None:
        """Update competence from evidence — the only way trust is earned."""
        c = self.competence(skill)
        c.attempts += 1
        if success:
            c.successes += 1
        c.estimate = c.successes / max(c.attempts, 1)
        # uncertainty shrinks with evidence (a simple, transparent rule)
        c.uncertainty = 1.0 / (1.0 + c.attempts)

    def note_attempt(self, goal: str) -> None:
        self._goals[goal] = self._goals.get(goal, 0) + 1

    def report(self) -> dict:
        return {name: {"estimate": round(c.estimate, 2),
                       "uncertainty": round(c.uncertainty, 2),
                       "attempts": c.attempts}
                for name, c in self._skills.items()}
