#!/usr/bin/env python3
"""
examples/end_to_end/teach_a_skill.py  —  Teach, publish, install, use
=====================================================================

The platform loop of Parts XV–XVII, end to end: a person teaches a skill in the studio, it
is published to the marketplace (verified first), another robot installs it, and uses
it — with credit and provenance recorded along the way.

    python3 examples/end_to_end/teach_a_skill.py
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from body import SimRobot
from platform import Skill, capability, studio
from platform.marketplace import Marketplace
from backend.services import TrustService, ProvenanceService
from learning import BroadLearning
from mind import SelfModel


@capability(arms=1, reach_m=0.5)
class WipeSurface(Skill):
    precondition = "a cloth and a surface are present"
    effect = "the surface has been wiped clean"
    def act(self, obs, robot):
        robot.move("surface", speed_mps=0.2)


def main():
    print("=" * 62)
    print("  TEACH -> PUBLISH -> INSTALL -> USE  (Parts XV–XVII, end to end)")
    print("=" * 62)

    trust = TrustService()
    provenance = ProvenanceService()
    market = Marketplace(trust=trust)
    self_model = SelfModel()
    learner = BroadLearning(self_model=self_model)

    # 1. TEACH — a person demonstrates the skill in the studio (with consent).
    contribution = studio.make_contribution(
        teacher="alice", skill="WipeSurface", modality="demonstration")
    provenance.record("teaching_contribution", **contribution)
    learner.ingest("teacher", "WipeSurface", quality=0.9)   # experience -> competence
    print("\n1. taught by:", contribution["teacher"],
          "| modality:", contribution["modality"],
          "| consent:", contribution["consent"])

    # 2. PUBLISH — the taught skill is published to the marketplace (verified).
    print("2. publish:", market.publish(WipeSurface))

    # 3. INSTALL — a different robot discovers and installs it.
    robot = SimRobot(robot_id="sim-0002")
    found = market.discover(needs="wiped")
    print("3. discovered:", [s["name"] for s in found])
    ok, msg = market.install("WipeSurface", robot)
    provenance.record_install("WipeSurface", robot.robot_id)
    print("   install:", ok, "-", msg)

    # 4. USE — the robot runs the newly acquired skill.
    world = robot.perceive({"objects": ["cloth", "surface"], "people": []})
    robot.set_world(world)
    robot.trace.clear()
    robot.run_skill("WipeSurface")
    print("4. used the skill:")
    for line in robot.trace:
        print("  ", line)

    # What the platform recorded (accountability + credit).
    print("\nprovenance records:")
    for r in provenance.all():
        print("  ", {k: r[k] for k in r if k != "at"})
    print("\nrobot's competence after teaching:", self_model.report())
    print("\nOne person taught; the whole ecosystem can now use it.\n")


if __name__ == "__main__":
    main()
