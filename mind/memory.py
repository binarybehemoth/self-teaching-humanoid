"""
mind/memory.py  —  Memory
=========================

What the robot retains and recalls across tasks. A minimal episodic store:
the planner and self-model draw on it to act with context rather than from scratch.
"""
from __future__ import annotations
import time


class Memory:
    def __init__(self):
        self._episodes: list[dict] = []

    def remember(self, goal: str, steps, outcome: str) -> None:
        self._episodes.append({
            "goal": goal,
            "n_steps": len(steps),
            "outcome": outcome,
            "at": time.time(),
        })

    def recall(self, goal: str) -> list[dict]:
        return [e for e in self._episodes if e["goal"] == goal]

    def all(self) -> list[dict]:
        return list(self._episodes)
