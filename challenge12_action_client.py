import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from action_tutorials_interfaces.action import Fibonacci

class NavClient(Node):
    def __init__(self):
        super().__init__('nav_client')
        self._client = ActionClient(self, Fibonacci, 'navigate_to_pose')

    def go_to(self, x, y):
        goal = Fibonacci.Goal()
        goal.order = int(x + y)

        self._client.wait_for_server()
        self.get_logger().info(f'Envoi goal non-bloquant: order={goal.order}')

        # Version NON-BLOQUANTE avec callback
        future = self._client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn('Goal rejeté!')
            return
        self.get_logger().info('Goal accepté!')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback):
        self.get_logger().info(f'Feedback: {feedback.feedback.partial_sequence}')

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Résultat: {result.sequence}')

def main(args=None):
    rclpy.init(args=args)
    node = NavClient()
    node.go_to(3, 7)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
