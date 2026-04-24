import rclpy
from rclpy.lifecycle import Node, State, TransitionCallbackReturn
from rclpy.executors import SingleThreadedExecutor
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import sys
import math

class RobotSimulator(Node):
    def __init__(self, robot_id=1):
        super().__init__(f'robot_simulator_{robot_id}')
        self.robot_id = robot_id
        self.broadcaster = None
        self.timer = None
        self.angle = 0.0

    def on_configure(self, state: State) -> TransitionCallbackReturn:
        self.broadcaster = TransformBroadcaster(self)
        self.get_logger().info(f'Robot {self.robot_id} configuré!')
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        self.timer = self.create_timer(0.1, self.broadcast_tf)
        self.get_logger().info(f'Robot {self.robot_id} activé!')
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        self.destroy_timer(self.timer)
        self.get_logger().info(f'Robot {self.robot_id} désactivé!')
        return TransitionCallbackReturn.SUCCESS

    def broadcast_tf(self):
        self.angle += 0.05
        x = float(self.robot_id) + math.cos(self.angle)
        y = math.sin(self.angle)
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = f'robot{self.robot_id}'
        t.transform.translation.x = x
        t.transform.translation.y = y
        t.transform.translation.z = 0.0
        t.transform.rotation.w = 1.0
        self.broadcaster.sendTransform(t)

def main(args=None):
    robot_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rclpy.init(args=args)
    node = RobotSimulator(robot_id)
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
