"""
backend/services/trust.py  —  The Trust-and-Safety Service
=========================================================

Verifies, sandboxes, and (when needed) recalls skills — the ecosystem-scale safety
layer (Parts XV–XVII). Every skill is verified before it can be installed anywhere, and a
harmful skill can be traced through provenance and withdrawn from every robot that
installed it.

This illustrates the interface with simple, transparent checks. Real verification runs
a skill through extensive testing and sandboxed execution.
"""
from __future__ import annotations


class TrustService:
    def __init__(self):
        self._recalled: set[str] = set()

    def verify(self, skill_cls, contract: dict) -> bool:
        """A skill must pass verification before it becomes installable."""
        # Basic, transparent gates (a real service tests far more thoroughly):
        if not contract.get("effect"):
            return False                        # must declare what it achieves
        if not contract.get("precondition"):
            return False                        # must declare when it may run
        if contract["name"] in self._recalled:
            return False                        # recalled skills stay out
        # A skill may not require disabling safety, etc. (checked here in a real system).
        return True

    def recall(self, skill_name: str) -> dict:
        """Withdraw a skill across the ecosystem (traced via provenance)."""
        self._recalled.add(skill_name)
        return {"recalled": skill_name}

    def is_recalled(self, skill_name: str) -> bool:
        return skill_name in self._recalled
