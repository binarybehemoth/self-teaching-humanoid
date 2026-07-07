"""
safety/override.py  —  The Human Override
=========================================

The human's absolute authority over the machine. When engaged, all motion halts
and stays halted until a human releases it. The override is designed to be always
reachable — in the front-end dashboard, physically on the robot — because the whole
safety architecture rests on a person always being able to stop the machine.
"""
from __future__ import annotations


class HumanOverride:
    def __init__(self):
        self._engaged = False

    @property
    def engaged(self) -> bool:
        return self._engaged

    def engage(self, by: str = "operator") -> None:
        """Stop everything. Called by the always-reachable stop control."""
        self._engaged = True
        self._by = by

    def release(self, by: str = "operator") -> None:
        """Allow motion again — a deliberate human act."""
        self._engaged = False
