import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from action_tutorials_interfaces.action import Fibonacci
import time

class NavigationActionServer(Node):
    def __init__(self):
        super().__init__('navigation_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'navigate_to_pose',
            self.execute_callback
        )
        self.get_logger().info('Action Server Navigation pret!')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Deplacement vers la cible...')
        distance = float(goal_handle.request.order)
        steps = 10
        for i in range(steps):
            remaining = distance * (steps - i) / steps
            feedback = Fibonacci.Feedback()
            feedback.partial_sequence = [int(remaining)]
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f'Distance restante: {remaining:.2f}m')
            time.sleep(0.5)
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = [0]
        return result

def main(args=None):
    rclpy.init(args=args)
    node = NavigationActionServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
