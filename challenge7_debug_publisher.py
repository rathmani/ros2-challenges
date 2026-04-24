import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class StatusPub(Node):
    def __init__(self):
        super().__init__('status')
        self.pub = self.create_publisher(
            String, '/robot/status', 10)  # BUG 1 corrigé
        self.timer = self.create_timer(1, self.cb)

    def cb(self):
        msg = String()          # BUG 2 corrigé
        msg.data = 'OK'
        self.pub.publish(msg)   # BUG 3 corrigé
        self.get_logger().info('Publié: OK')

def main(args=None):
    rclpy.init(args=args)
    node = StatusPub()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
