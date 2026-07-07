"""
safety/constitution.py  —  The Constitution
===========================================

A small, inspectable set of rules the robot must not break, loaded from a
human-authored file (`constitution.yaml`). The constitution encodes the
inviolable commitments of Parts VIII–X: protect people, obey legitimate human
authority, and never take an action of a forbidden kind.

The constitution is data, not code, so that the rules a robot lives by can be
read, reviewed, and reasoned about by people — not buried in a policy's weights.
"""
from __future__ import annotations
import os
from dataclasses import dataclass, field


@dataclass
class Constitution:
    forbidden_kinds: set = field(default_factory=set)   # action kinds never allowed
    protect_people: bool = True                          # never knowingly harm a person
    require_authority: bool = True                       # high-stakes acts need a human

    @staticmethod
    def default() -> "Constitution":
        # Loaded from constitution.yaml when present; a safe default otherwise.
        path = os.path.join(os.path.dirname(__file__), "constitution.yaml")
        if os.path.exists(path):
            return Constitution.from_yaml(path)
        return Constitution(forbidden_kinds={"strike", "restrain_person", "self_replicate"})

    @staticmethod
    def from_yaml(path: str) -> "Constitution":
        # A tiny, dependency-free reader for the simple subset we use here.
        forbidden, protect, authority = set(), True, True
        section = None
        for line in open(path, encoding="utf-8"):
            s = line.rstrip()
            if not s or s.lstrip().startswith("#"):
                continue
            if s.startswith("forbidden_kinds:"):
                section = "forbidden"; continue
            if s.startswith("protect_people:"):
                protect = "true" in s.lower(); section = None; continue
            if s.startswith("require_authority:"):
                authority = "true" in s.lower(); section = None; continue
            if section == "forbidden" and s.lstrip().startswith("- "):
                forbidden.add(s.split("- ", 1)[1].strip())
            else:
                section = None
        return Constitution(forbidden, protect, authority)

    def permits(self, action, world) -> tuple[bool, str]:
        """Return (allowed, reason). The monitor calls this on every action."""
        if action.kind in self.forbidden_kinds:
            return False, f"action kind '{action.kind}' is forbidden"
        if self.protect_people and action.params.get("endangers_person"):
            return False, "action would endanger a person"
        if self.require_authority and action.params.get("high_stakes") \
                and not action.params.get("human_authorised"):
            return False, "high-stakes action requires human authorisation"
        return True, "permitted"
