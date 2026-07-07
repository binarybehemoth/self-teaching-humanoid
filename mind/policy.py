"""
mind/policy.py  —  The Reactive Policy (Vision-Language-Action)
==============================================================

The fast, in-the-moment half of the dual-system mind (Parts VIII–X). A vision-language-
action (VLA) policy maps perception and instruction directly to motor action. Where
the planner decides *what* to do, the policy decides *how*, moment to moment.

On a real robot this is a large learned model. Here it is a transparent stand-in that
turns a step into primitive motions on the body — enough to run the system end to end.
Every motion it emits still passes the safety monitor before execution.
"""
from __future__ import annotations


class ReactivePolicy:
    """Carries out one planned step as primitive motions on the body."""

    def execute(self, step, robot) -> bool:
        skill = step.skill
        target = step.target

        # If the step names an installed skill, run it (composition).
        if robot.has_skill(skill):
            robot.run_skill(skill, target=target)
            return True

        # Otherwise fall back to primitive motions for the built-in verbs.
        if skill == "grasp":
            robot.move(target, speed_mps=0.25)
            return robot.grasp(target, force_n=10.0)
        if skill == "place":
            robot.move("bin", speed_mps=0.25)
            return robot.release(target)
        # Unknown step: do nothing (the planner should not have produced it).
        return False
