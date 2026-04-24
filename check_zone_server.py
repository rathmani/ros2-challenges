import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from action_tutorials_interfaces.action import Fibonacci
from tf2_ros import Buffer, TransformListener
import math

class CheckZoneServer(Node):
    def __init__(self):
        super().__init__('check_zone_server')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self._action_server = ActionServer(
            self, Fibonacci, '/check_zone', self.execute_callback)
        self.get_logger().info('Check Zone Server prêt!')

    def execute_callback(self, goal_handle):
        robot_id = goal_handle.request.order
        max_radius = 3.0
        steps = 5

        for i in range(steps):
            try:
                tf = self.tf_buffer.lookup_transform(
                    'world', f'robot{robot_id}', rclpy.time.Time())
                x = tf.transform.translation.x
                y = tf.transform.translation.y
                distance = math.sqrt(x**2 + y**2)

                feedback = Fibonacci.Feedback()
                feedback.partial_sequence = [int(distance * 100)]
                goal_handle.publish_feedback(feedback)
                self.get_logger().info(
                    f'Robot{robot_id} distance: {distance:.2f}m / max: {max_radius}m')

                if distance > max_radius:
                    self.get_logger().warn(f'Robot{robot_id} hors zone!')

            except Exception as e:
                self.get_logger().warn(f'TF non disponible: {e}')

            import time
            time.sleep(1.0)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = [robot_id]
        return result

def main(args=None):
    rclpy.init(args=args)
    node = CheckZoneServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
