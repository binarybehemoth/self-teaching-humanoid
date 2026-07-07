"""
platform/marketplace.py  —  The Skill Marketplace
=================================================

Where skills are published, discovered, and installed (Parts XV–XVII). Every skill passes
the trust layer's verification before anyone can install it, and installation is
subject to capability negotiation via the standard layer.

This in-memory implementation is a faithful illustration of the interface; the real
marketplace is a back-end service (see backend/services/marketplace.py).
"""
from __future__ import annotations
from . import standard


class Marketplace:
    def __init__(self, trust=None):
        self._listings: dict[str, dict] = {}   # name -> {contract, cls, verified}
        self._trust = trust

    def publish(self, skill_cls) -> dict:
        """Publish a skill. It is verified before it becomes installable."""
        skill = skill_cls()
        contract = skill.contract()
        verified = True if self._trust is None else self._trust.verify(skill_cls, contract)
        self._listings[contract["name"]] = {
            "contract": contract, "cls": skill_cls, "verified": verified,
        }
        return {"published": contract["name"], "verified": verified}

    def discover(self, needs: str = "") -> list[dict]:
        """Browse listings, optionally filtered by a need in the effect text."""
        out = []
        for name, entry in self._listings.items():
            if needs.lower() in entry["contract"]["effect"].lower():
                out.append({"name": name, **entry["contract"], "verified": entry["verified"]})
        return out

    def install(self, name: str, robot) -> tuple[bool, str]:
        """Install a skill onto a robot — verified, then compatibility-checked."""
        entry = self._listings.get(name)
        if not entry:
            return False, "no such skill"
        if not entry["verified"]:
            return False, "skill is not verified — cannot install"
        ok, why = standard.can_run(entry["contract"], standard.capability_descriptor(robot))
        if not ok:
            return False, why
        robot.install_skill(name, entry["cls"])
        return True, "installed"
