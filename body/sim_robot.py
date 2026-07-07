"""
body/sim_robot.py  —  A Simulated Robot
=======================================

A pure-Python simulated humanoid, so the whole system can be run and understood on
one computer without any hardware or external packages (Chapter 50).

The same interface is implemented by the ROS 2 hardware-abstraction layer for a real
machine (see body/hardware_abstraction.py), so the code that drives this simulated
robot drives a physical one unchanged — the point of the abstraction.

CRUCIALLY: every action this robot is asked to take passes the safety monitor before
it is executed. The robot cannot move in a way the monitor vetoes — the guarantee is
enforced here, at the seam between decision and motion.
"""
from __future__ import annotations
from safety import SafetyMonitor, Action, WorldView


class SimRobot:
    def __init__(self, robot_id: str = "sim-0001", arms: int = 2,
                 reach_m: float = 0.7, sensors=("camera", "touch"),
                 monitor: SafetyMonitor | None = None):
        self.robot_id = robot_id
        self.embodiment = f"{arms}-arm humanoid (sim)"
        self.arms = arms
        self.reach_m = reach_m
        self.sensors = tuple(sensors)
        self.monitor = monitor or SafetyMonitor()
        self._skills: dict[str, type] = {}     # name -> Skill subclass
        self._holding: str | None = None
        self.trace: list[str] = []             # a human-readable log of what happened

    # --- the world the robot perceives (a toy scene for the sim) ---
    def perceive(self, scene) -> WorldView:
        self._scene = scene
        return WorldView(people_distances_m=scene.get("people", []),
                         objects=scene.get("objects", []))

    # --- skills ---
    def install_skill(self, name: str, skill_cls: type) -> None:
        self._skills[name] = skill_cls

    def has_skill(self, name: str) -> bool:
        return any(name == n or n.startswith(name) for n in self._skills)

    def run_skill(self, name: str, target=None, **params) -> None:
        cls = self._resolve(name)
        if cls is None:
            self.trace.append(f"  ! skill '{name}' not installed")
            return
        skill = cls()._bind(self)
        self.trace.append(f"  -> running skill: {skill.name}"
                          + (f" (target={target})" if target else ""))
        skill.act(self._world, self)

    def _resolve(self, name: str):
        if name in self._skills:
            return self._skills[name]
        for n, cls in self._skills.items():        # allow 'grasp' to match 'grasp>=5.1'
            if n.startswith(name):
                return cls
        return None

    # --- primitive motions — each one goes through the safety monitor ---
    def move(self, target: str, speed_mps: float = 0.25, **params) -> bool:
        return self._do(Action("move", target, params, speed_mps=speed_mps, origin="skill"),
                        f"move to {target}")

    def grasp(self, target: str, force_n: float = 10.0, **params) -> bool:
        ok = self._do(Action("grasp", target, params, force_n=force_n, origin="skill"),
                      f"grasp {target}")
        if ok:
            self._holding = target
        return ok

    def release(self, target: str = None, **params) -> bool:
        ok = self._do(Action("release", target or self._holding, params, origin="skill"),
                      f"release {target or self._holding}")
        if ok:
            self._holding = None
        return ok

    def _do(self, action: Action, description: str) -> bool:
        """Execute a motion IFF the safety monitor allows it. The enforced seam."""
        verdict = self.monitor.check(action, self._world)
        if not verdict.allowed:
            self.trace.append(f"     [SAFETY] VETOED {description}: {verdict.reason}")
            return False
        self.trace.append(f"     [ok] {description}")
        return True

    # bind the current world for the duration of a task
    def set_world(self, world: WorldView) -> None:
        self._world = world
