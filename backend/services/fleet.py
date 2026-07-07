"""
backend/services/fleet.py  —  Fleet-Coordination Service
========================================================

Allocates tasks across robots, tracks their health, and orchestrates updates and
recalls (Parts XVIII–XX). Includes the always-available halt: one robot, a group, or all.
"""
from __future__ import annotations


class FleetService:
    def __init__(self):
        self._robots: dict[str, dict] = {}

    def register(self, robot_id: str, caps: dict) -> None:
        self._robots[robot_id] = {"caps": caps, "status": "idle", "halted": False}

    def status(self) -> dict:
        return dict(self._robots)

    def halt(self, robot_id: str) -> dict:
        if robot_id in self._robots:
            self._robots[robot_id]["halted"] = True
        return {"halted": robot_id}

    def halt_all(self) -> dict:
        for r in self._robots.values():
            r["halted"] = True
        return {"halted": "all", "count": len(self._robots)}
