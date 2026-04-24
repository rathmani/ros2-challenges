import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class TemperatureSubscriber(Node):
    def __init__(self):
        super().__init__('temperature_subscriber')
        self.subscription = self.create_subscription(
            Float64, '/temperature', self.callback, 10)
        self.get_logger().info('Subscriber température démarré!')

    def callback(self, msg):
        temp = msg.data
        if temp > 30.0:
            self.get_logger().warn(f'Température trop haute: {temp:.2f}°C > 30°C!')
        elif temp < 10.0:
            self.get_logger().warn(f'Température trop basse: {temp:.2f}°C < 10°C!')
        else:
            self.get_logger().info(f'Température normale: {temp:.2f}°C')

def main(args=None):
    rclpy.init(args=args)
    node = TemperatureSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
