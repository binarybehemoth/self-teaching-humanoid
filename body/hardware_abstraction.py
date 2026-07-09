"""
body/hardware_abstraction.py  —  The Hardware-Abstraction Layer
==============================================================

The clean interface between the software above and the hardware below.
The mind and skills speak to *this* interface; a manufacturer supporting a new robot
implements it for their machine, so that every existing skill runs
on the new body unchanged.

`SimRobot` is one implementation (in software). A real robot's implementation would
map these same methods onto ROS 2 topics, actions, and services driving physical
actuators and sensors. The interface is identical, which is the whole point: the code
that drives the sim drives the real machine.
"""
from __future__ import annotations
from typing import Protocol, runtime_checkable
from safety import WorldView


@runtime_checkable
class RobotBody(Protocol):
    """The interface every body — simulated or physical — must implement."""
    robot_id: str
    arms: int
    reach_m: float
    sensors: tuple

    def perceive(self, scene) -> WorldView: ...
    def move(self, target: str, speed_mps: float = 0.25, **params) -> bool: ...
    def grasp(self, target: str, force_n: float = 10.0, **params) -> bool: ...
    def release(self, target: str = None, **params) -> bool: ...
    def install_skill(self, name: str, skill_cls: type) -> None: ...
    def run_skill(self, name: str, target=None, **params) -> None: ...


# A real robot would provide, e.g.:
#
#   class Ros2Robot:
#       def __init__(self, node):
#           self._node = node          # rclpy node
#           # publishers/action-clients for joint commands, subscribers for sensors
#       def move(self, target, speed_mps=0.25, **p):
#           # translate into a ROS 2 action goal to the motion controller,
#           # AFTER the safety monitor has approved it (same seam as the sim)
#           ...
#
# See body/ros2_nodes/ for the node stubs.
