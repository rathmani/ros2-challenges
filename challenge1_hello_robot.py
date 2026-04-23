import rclpy
from rclpy.node import Node

class HelloRobotNode(Node):
    def __init__(self):
        super().__init__('hello_robot')
        self.create_timer(2.0, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info('Hello ROS2!')

def main(args=None):
    rclpy.init(args=args)
    node = HelloRobotNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

