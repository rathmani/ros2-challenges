import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import time

class MultiThreadedNode(Node):
    def __init__(self):
        super().__init__('multithreaded_node')
        self.group = ReentrantCallbackGroup()

        # Timer lent : 500ms
        self.create_timer(0.5, self.slow_callback,
                         callback_group=self.group)
        # Timer rapide : 50ms
        self.create_timer(0.05, self.fast_callback,
                         callback_group=self.group)

    def slow_callback(self):
        self.get_logger().info('Callback LENT démarré...')
        time.sleep(0.4)  # simule un traitement long
        self.get_logger().info('Callback LENT terminé')

    def fast_callback(self):
        self.get_logger().info('Callback RAPIDE !')

def main(args=None):
    rclpy.init(args=args)
    node = MultiThreadedNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
