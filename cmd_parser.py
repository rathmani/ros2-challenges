import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class CmdParser(Node):
    def __init__(self):
        super().__init__('cmd_parser')
        self.sub = self.create_subscription(
            String, '/cmd_text', self.callback, 10)
        self.pub = self.create_publisher(
            Twist, '/robot_response', 10)
        self.history = []
        self.get_logger().info('CMD Parser démarré!')

    def callback(self, msg):
        cmd = msg.data.strip().lower()
        twist = Twist()
        parts = cmd.split()

        if len(parts) == 2 and parts[0] == 'avance':
            twist.linear.x = float(parts[1])
        elif len(parts) == 2 and parts[0] == 'recule':
            twist.linear.x = -float(parts[1])
        elif len(parts) == 2 and parts[0] == 'tourne_gauche':
            twist.angular.z = float(parts[1])
        elif len(parts) == 2 and parts[0] == 'tourne_droite':
            twist.angular.z = -float(parts[1])
        elif cmd == 'stop':
            pass  # tout à zéro

        self.history.append(cmd)
        if len(self.history) > 10:
            self.history.pop(0)

        self.pub.publish(twist)
        self.get_logger().info(f'Commande: {cmd} → linear={twist.linear.x}, angular={twist.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    node = CmdParser()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
