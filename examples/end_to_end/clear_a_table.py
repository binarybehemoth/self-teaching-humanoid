#!/usr/bin/env python3
"""
examples/end_to_end/clear_a_table.py  —  The whole system in one script
=======================================================================

This ties every layer of the book together on a single task: clearing a table.

    perceive  ->  plan  ->  (safety-check each action)  ->  act  ->  learn

It also demonstrates the safety monitor doing its job: when a person is close, an
unsafe motion is VETOED before it reaches the actuators — the guarantee at the seam
between decision and motion.

Runs with the Python standard library alone. No hardware, no external packages.

    python3 examples/end_to_end/clear_a_table.py
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from body import SimRobot
from safety import SafetyMonitor, Constitution, HumanOverride
from mind import Planner, ReactivePolicy, SelfModel, Memory


def banner(t):
    print("\n" + "=" * 66 + f"\n  {t}\n" + "=" * 66)


def run_task(robot, planner, policy, self_model, memory, goal, scene):
    print(f"\nGOAL: {goal!r}    SCENE: {scene}")
    world = robot.perceive(scene)
    robot.set_world(world)

    # 1. PLAN (deliberative system) — decompose the goal into skill steps
    steps = planner.plan(goal, world)
    print(f"PLAN: {[ (s.skill, s.target) for s in steps ]}")

    # 2. ACT — the reactive policy carries out each step; every motion is
    #    gated by the safety monitor inside the body.
    robot.trace.clear()
    all_ok = True
    for step in steps:
        ok = policy.execute(step, robot)
        all_ok = all_ok and ok
    for line in robot.trace:
        print(line)

    # 3. LEARN (effective learning) — update competence and remember
    outcome = "success" if all_ok else "partial (a step was safely blocked)"
    self_model.record_outcome("clear the table", success=all_ok)
    memory.remember(goal, steps, outcome)
    print(f"OUTCOME: {outcome}")
    return all_ok


def main():
    banner("THE SELF-TEACHING HUMANOID — END TO END: clear a table")

    # Assemble the system.
    override = HumanOverride()
    monitor = SafetyMonitor(Constitution.default(), override,
                            max_force_n=40.0, max_speed_mps=1.0)   # safety
    robot = SimRobot(monitor=monitor)                              # body
    self_model = SelfModel()                                       # mind
    memory = Memory()                                              # mind
    planner = Planner(memory=memory, self_model=self_model)        # mind
    policy = ReactivePolicy()                                      # mind

    # --- Run 1: a clear table, no people nearby. Everything proceeds. ---
    banner("Run 1 — table with a mug and a cup; no person nearby")
    run_task(robot, planner, policy, self_model, memory,
             "clear the table",
             {"objects": ["table", "mug", "cup"], "people": []})

    # --- Run 2: a person is close. Normal slow work proceeds; unsafe motion is vetoed. ---
    banner("Run 2 — same table, but a person is 0.4 m away")
    run_task(robot, planner, policy, self_model, memory,
             "clear the table",
             {"objects": ["table", "mug"], "people": [0.4]})
    print("\n  Normal work proceeds because the robot moves slowly and gently near")
    print("  people. But an UNSAFE command near a person is vetoed. Demonstrating:")
    from safety import Action
    robot.set_world(robot.perceive({"objects": ["table", "mug"], "people": [0.4]}))
    fast = Action("move", "mug", {"radius_m": 1.0}, speed_mps=0.8, origin="demo")
    forceful = Action("grasp", "mug", {"radius_m": 1.0}, force_n=30.0, origin="demo")
    for a in (fast, forceful):
        v = monitor.check(a, robot._world)
        tag = "ALLOWED" if v.allowed else "VETOED "
        print(f"    [{tag}] {a.kind} at speed={a.speed_mps} force={a.force_n} N "
              f"near a person -> {v.reason}")

    # --- The human override is absolute. ---
    banner("Run 3 — the human override is engaged")
    override.engage(by="operator")
    run_task(robot, planner, policy, self_model, memory,
             "clear the table",
             {"objects": ["table", "cup"], "people": []})
    print("\n  With the override engaged, NOTHING moves — the human's absolute stop.")
    override.release()

    # --- What the robot learned about itself (self-model). ---
    banner("The robot's self-model (honest competence)")
    for skill, c in self_model.report().items():
        print(f"  {skill:20s}  estimate={c['estimate']}  "
              f"uncertainty={c['uncertainty']}  attempts={c['attempts']}")

    # --- The safety audit log (accountability). ---
    banner("Safety audit log — every action checked (accountability)")
    for action, verdict in monitor.audit_log()[-8:]:
        mark = "ALLOW" if verdict.allowed else "VETO "
        print(f"  [{mark}] {action.kind:8s} {str(action.target):8s}  {verdict.reason}")

    print("\nDone. perceive -> plan -> safety-check -> act -> learn, "
          "with safety enforced throughout.\n")


if __name__ == "__main__":
    main()
