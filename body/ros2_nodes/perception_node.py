"""
body/ros2_nodes/perception_node.py  —  ROS 2 perception node (stub)
===================================================================

A stub illustrating how the body's sensing is exposed as a ROS 2 node.
On a real robot this would subscribe to camera and depth topics, run perception, and
publish a scene graph that the mind consumes. Left as a stub because it requires a
ROS 2 installation (rclpy) and real sensors.
"""
# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import Image
#
# class PerceptionNode(Node):
#     def __init__(self):
#         super().__init__("perception")
#         self.create_subscription(Image, "/camera/image_raw", self.on_image, 10)
#         # publish a scene graph on /perception/scene
#     def on_image(self, msg):
#         ...  # detect objects and people, publish the scene
#
# def main():
#     rclpy.init(); rclpy.spin(PerceptionNode()); rclpy.shutdown()

def main():
    raise SystemExit("ROS 2 node stub — requires a ROS 2 (rclpy) environment and hardware. "
                     "Run the pure-Python examples/ instead to see the system work.")
