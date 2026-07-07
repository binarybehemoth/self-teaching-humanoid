"""
platform/skills.py  —  The Skill Interface
==========================================

A skill encapsulates an expert: it exposes what it does and what it needs, and hides
the policy that does it. This is the interface a developer writes to when building on
the platform (Chapter 40; extended in Chapter 51).

A skill declares:
  - a precondition (what must be true to run it),
  - an effect (what it achieves),
  - the capabilities it requires of a body (via @capability),
  - the skills it depends on (via @depends),
and implements `act(observation, robot)`.

Everything the rest of the system needs is in that contract: the marketplace uses it
to list and match the skill, the standard layer uses it to negotiate compatibility,
the composition machinery uses it to let others build on it, and the safety monitor
governs every action it produces — automatically, on every robot.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Requirement:
    """What a skill needs of a body — its embodiment requirements."""
    arms: int = 1
    reach_m: float = 0.5
    sensors: tuple = ("camera",)


def capability(arms: int = 1, reach_m: float = 0.5, sensors: tuple = ("camera",)):
    """Declare the body a skill needs. Used by the standard layer to negotiate fit."""
    def deco(cls):
        cls.requirement = Requirement(arms=arms, reach_m=reach_m, sensors=sensors)
        return cls
    return deco


def depends(*skill_specs: str):
    """Declare the skills this skill builds on, e.g. depends('grasp>=5.1', 'pour>=3.0')."""
    def deco(cls):
        cls.dependencies = list(skill_specs)
        return cls
    return deco


class Skill:
    """
    Base class for every skill. Subclasses set `precondition` and `effect` and
    implement `act`. Composition is done by calling `self.use(other_skill, ...)`,
    and object lookup by `self.find(kind, observation)`.
    """
    requirement: Requirement = Requirement()
    dependencies: list = []
    precondition: str = ""
    effect: str = ""

    # --- authored by the skill developer ---
    def act(self, obs, robot) -> None:
        raise NotImplementedError("a skill must implement act(obs, robot)")

    # --- helpers the platform provides ---
    def find(self, kind: str, obs) -> Optional[str]:
        """Locate an object of a kind in the current observation."""
        for o in obs.objects:
            if o == kind or o.startswith(kind):
                return o
        return None

    def use(self, skill_name: str, target=None, **params) -> None:
        """Compose: invoke another (already-installed) skill by name."""
        self._robot.run_skill(skill_name, target=target, **params)

    # --- bookkeeping used by the runtime ---
    def _bind(self, robot):
        self._robot = robot
        return self

    @property
    def name(self) -> str:
        return type(self).__name__

    def contract(self) -> dict:
        """The full, inspectable contract — what the marketplace and standard layer read."""
        return {
            "name": self.name,
            "precondition": self.precondition,
            "effect": self.effect,
            "requires": {
                "arms": self.requirement.arms,
                "reach_m": self.requirement.reach_m,
                "sensors": list(self.requirement.sensors),
            },
            "dependencies": list(self.dependencies),
        }
