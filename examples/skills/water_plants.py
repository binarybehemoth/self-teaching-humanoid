#!/usr/bin/env python3
"""
examples/skills/water_plants.py  —  A composed skill (Chapter 51)
======================================================================

The worked example from the book: a new "water plants" skill built by composing
existing "grasp" and "pour" skills, written to the standard skill interface, published
to the marketplace (verified first), installed onto a robot, and run.

One person's short piece of work, written to a clean interface, becomes a capability
available to any compatible robot — the payoff of encapsulation.

    python3 examples/skills/water_plants.py
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from body import SimRobot
from platform import Skill, capability, depends
from platform.marketplace import Marketplace
from backend.services import TrustService


# --- two existing skills the ecosystem already offers ---
@capability(arms=1, reach_m=0.4)
class Grasp(Skill):
    precondition = "an object is within reach"
    effect = "the object is grasped"
    def act(self, obs, robot):
        obj = self.find("", obs) if False else None  # target passed by caller
        robot.grasp(robot._pending_target, force_n=8.0)


@capability(arms=1, reach_m=0.4)
class Pour(Skill):
    precondition = "a container is held over a target"
    effect = "liquid has been poured onto the target"
    def act(self, obs, robot):
        robot.move(robot._pending_target, speed_mps=0.2)


# --- the new skill, composed from the two above (exactly as in Ch 51) ---
@capability(arms=1, reach_m=0.6)          # what body this skill needs (Parts XV–XVII)
@depends("Grasp", "Pour")                 # skills it builds on (Chapter 40)
class WaterPlants(Skill):
    precondition = "a watering can and a plant are present"
    effect = "the plant has been watered"

    def act(self, obs, robot):
        can = self.find("watering_can", obs)
        robot._pending_target = can
        self.use("Grasp", target=can)             # compose existing skills
        plant = self.find("plant", obs)
        robot._pending_target = plant
        self.use("Pour", target=plant)
        # the safety monitor (Parts VIII–X) governs every motion above, automatically


def main():
    print("=" * 60)
    print("  A COMPOSED SKILL: water the plants (Chapter 51)")
    print("=" * 60)

    # The developer publishes their skills to the marketplace (verified first).
    market = Marketplace(trust=TrustService())
    for cls in (Grasp, Pour, WaterPlants):
        print("publish:", market.publish(cls))

    # A robot owner installs the composed skill (compatibility is negotiated).
    robot = SimRobot()
    ok, msg = market.install("WaterPlants", robot)
    # water_plants depends on Grasp and Pour — install those too
    market.install("Grasp", robot)
    market.install("Pour", robot)
    print("\ninstall WaterPlants:", ok, "-", msg)

    # Run it. Watch the composed skills execute, each motion safety-checked.
    print("\nrunning the skill on a scene with a watering can and a plant:")
    world = robot.perceive({"objects": ["watering_can", "plant", "table"], "people": []})
    robot.set_world(world)
    robot.trace.clear()
    robot.run_skill("WaterPlants")
    for line in robot.trace:
        print(line)

    print("\nThe developer wrote to the skill interface only. The marketplace,")
    print("the standard layer, and the safety monitor did the rest.\n")


if __name__ == "__main__":
    main()
