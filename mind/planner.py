"""
mind/planner.py  —  The Deliberative Planner
============================================

The slow, reasoning half of the dual-system mind (Parts VIII–X). Given a task, it
decomposes it into a sequence of steps and selects a skill for each, drawing on the
skill graph (Parts XI–XIV) and on memory of similar tasks. The fast, reactive half — the
vision-language-action policy — then carries out each step in the moment (see
mind/policy.py).

This is a deliberately simple, transparent planner: it maps known goals to known skill
sequences. A real planner would reason far more richly, but the shape is the same —
decompose, select skills, hand each to the reactive system — and, importantly, every
action the plan ultimately produces is still gated by the safety monitor.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Step:
    skill: str
    target: str | None = None


class Planner:
    def __init__(self, memory=None, self_model=None):
        self.memory = memory
        self.self_model = self_model
        # A tiny library of goal -> plan mappings for the sim. Real planning is richer.
        self._recipes = {
            "clear the table": self._plan_clear_table,
            "water the plants": self._plan_water_plants,
        }

    def plan(self, goal: str, obs) -> list[Step]:
        goal = goal.lower().strip()
        recipe = self._recipes.get(goal)
        if recipe is None:
            return []
        steps = recipe(obs)
        # Honesty about limits (Parts VIII–X): note our confidence in this plan.
        if self.self_model is not None:
            self.self_model.note_attempt(goal)
        return steps

    def _plan_clear_table(self, obs) -> list[Step]:
        # For each removable object on the table, grasp it and place it away.
        removable = [o for o in obs.objects if o not in ("table", "plant")]
        steps: list[Step] = []
        for obj in removable:
            steps.append(Step("grasp", obj))
            steps.append(Step("place", obj))
        return steps

    def _plan_water_plants(self, obs) -> list[Step]:
        return [Step("water_plants", "plant")]
