"""
learning/effective_learning.py  —  Effective Learning
=====================================================

The self-improving learner: it organises its skills (skill graph),
practises in imagination, sets its own curriculum toward the frontier, and learns from
failure by editing the skill graph. This module illustrates the loop; the reasoning is
kept simple and transparent.
"""
from __future__ import annotations
from .skill_graph import SkillGraph


class EffectiveLearning:
    def __init__(self, skill_graph: SkillGraph, self_model=None):
        self.graph = skill_graph
        self.self_model = self_model

    def next_curriculum(self, known: set[str]) -> list[str]:
        """Propose the next skills to learn — the frontier."""
        return self.graph.frontier(known)

    def learn_from_failure(self, skill: str, known: set[str]) -> str:
        """Diagnose a failure into a missing prerequisite and target it."""
        ok, missing = self.graph.can_learn(skill, known)
        if missing:
            return f"failure on '{skill}' traced to missing prerequisite(s): {missing}"
        return f"'{skill}' has its prerequisites; failure lies within the skill itself"
