import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from example_interfaces.srv import Trigger

class HistoryService(Node):
    def __init__(self):
        super().__init__('history_service')
        self.history = []
        self.sub = self.create_subscription(
            String, '/cmd_text', self.cmd_callback, 10)
        self.srv = self.create_service(
            Trigger, '/get_history', self.history_callback)
        self.get_logger().info('History Service démarré!')

    def cmd_callback(self, msg):
        self.history.append(msg.data.strip())
        if len(self.history) > 10:
            self.history.pop(0)

    def history_callback(self, request, response):
        response.success = True
        response.message = '\n'.join(self.history[-10:])
        return response

def main(args=None):
    rclpy.init(args=args)
    node = HistoryService()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
