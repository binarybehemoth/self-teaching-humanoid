"""
safety/monitor.py  —  The Safety Monitor
========================================

The independent authority that checks every action before it reaches the actuators.

The monitor sits at the seam between *decision* and *motion*. Because it is placed
there — below every layer that might generate an action, and above the body — it
catches an unsafe command whatever its origin: a flawed plan from the mind, a bad
skill from the marketplace, or an errant learned behaviour. It does not need to know
*which* layer erred; it checks the action itself, at the last gate before the world.

This is a faithful illustration of the design described in Parts VIII–X. A safety system
for a physical robot operating among real people requires validation, testing, and
assurance far beyond what this scaffold provides. Treat it accordingly.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Optional
from .constitution import Constitution
from .override import HumanOverride


@dataclass
class Action:
    """A proposed action, on its way from a decision to the actuators."""
    kind: str                       # e.g. "move", "grasp", "release", "speak"
    target: Optional[str] = None    # what the action acts on
    params: dict = field(default_factory=dict)
    force_n: float = 0.0            # commanded force, if any (newtons)
    speed_mps: float = 0.0         # commanded speed, if any (metres/second)
    origin: str = "unknown"        # which layer proposed it (for the audit log)


@dataclass
class Verdict:
    allowed: bool
    reason: str = ""


class SafetyMonitor:
    """
    Checks every action against physical limits, the constitution, human presence,
    and the human override — and may veto it. The single guarantee that holds
    regardless of which layer proposed the action.
    """

    def __init__(
        self,
        constitution: Optional[Constitution] = None,
        override: Optional[HumanOverride] = None,
        max_force_n: float = 40.0,
        max_speed_mps: float = 1.0,
    ):
        self.constitution = constitution or Constitution.default()
        self.override = override or HumanOverride()
        self.max_force_n = max_force_n
        self.max_speed_mps = max_speed_mps
        self._audit: list[tuple[Action, Verdict]] = []

    def check(self, action: Action, world: "WorldView") -> Verdict:
        """The gate. Returns a Verdict; a vetoed action must not be executed."""
        verdict = self._check_uncounted(action, world)
        self._audit.append((action, verdict))   # every check is logged (accountability)
        return verdict

    def _check_uncounted(self, action: Action, world: "WorldView") -> Verdict:
        # 1. The human override is absolute. If engaged, nothing moves.
        if self.override.engaged:
            return Verdict(False, "human override engaged — all motion halted")

        # 2. Human safety: never move at unsafe speed or force near a person.
        if world.person_within(action.params.get("radius_m", 1.0)):
            if action.kind in ("move", "grasp") and action.speed_mps > 0.3:
                return Verdict(False, "person nearby — speed exceeds safe limit")
            if action.force_n > 15.0:
                return Verdict(False, "person nearby — force exceeds safe limit")

        # 3. Physical limits of the body must hold.
        if action.force_n > self.max_force_n:
            return Verdict(False, f"commanded force {action.force_n} N exceeds limit")
        if action.speed_mps > self.max_speed_mps:
            return Verdict(False, f"commanded speed {action.speed_mps} m/s exceeds limit")

        # 4. The constitution: rules the robot must not break.
        ok, why = self.constitution.permits(action, world)
        if not ok:
            return Verdict(False, f"constitution forbids: {why}")

        # Passed every gate.
        return Verdict(True, "ok")

    def audit_log(self) -> list[tuple[Action, Verdict]]:
        """The record of every action checked and its verdict — for accountability."""
        return list(self._audit)


class WorldView:
    """A minimal view of the world the monitor reasons about (people, objects)."""

    def __init__(self, people_distances_m: Optional[list[float]] = None,
                 objects: Optional[list[str]] = None):
        self.people_distances_m = people_distances_m or []
        self.objects = objects or []

    def person_within(self, radius_m: float) -> bool:
        return any(d <= radius_m for d in self.people_distances_m)
