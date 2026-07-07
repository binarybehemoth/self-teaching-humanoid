"""
platform/standard.py  —  The Standard Operating Layer
=====================================================

The common language that lets skills and robots of different makes work together
(Parts XV–XVII). A robot advertises a capability descriptor; the standard layer negotiates
whether a given skill can run on a given body, declining transfers across
unbridgeable gaps rather than shipping a skill that will fail.
"""
from __future__ import annotations


def can_run(skill_contract: dict, robot_caps: dict) -> tuple[bool, str]:
    """Capability negotiation: does this robot satisfy this skill's requirements?"""
    req = skill_contract.get("requires", {})
    if robot_caps.get("arms", 0) < req.get("arms", 0):
        return False, "morphology gap: skill needs more arms than the robot has"
    if robot_caps.get("reach_m", 0.0) < req.get("reach_m", 0.0):
        return False, "reach gap: robot cannot reach far enough for this skill"
    need = set(req.get("sensors", []))
    have = set(robot_caps.get("sensors", []))
    if not need.issubset(have):
        return False, f"sensor gap: robot lacks {sorted(need - have)}"
    return True, "compatible"


def capability_descriptor(robot) -> dict:
    """The standard descriptor a robot presents to the ecosystem."""
    return {
        "embodiment": robot.embodiment,
        "arms": robot.arms,
        "reach_m": robot.reach_m,
        "sensors": list(robot.sensors),
        "safety": {"monitor": True, "override": True, "constitution": True},
    }
