import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import datetime

class LoggerNode(Node):
    def __init__(self):
        super().__init__('logger_node')
        self.sub = self.create_subscription(
            String, '/cmd_text', self.callback, 10)
        self.log_file = open('robot_commands.log', 'a')
        self.get_logger().info('Logger Node démarré!')

    def callback(self, msg):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f'[{timestamp}] {msg.data}\n'
        self.log_file.write(line)
        self.log_file.flush()
        self.get_logger().info(f'Enregistré: {msg.data}')

    def destroy_node(self):
        self.log_file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = LoggerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
