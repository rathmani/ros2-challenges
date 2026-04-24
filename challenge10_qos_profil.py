import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import Float64, String

class QoSNode(Node):
    def __init__(self):
        super().__init__('qos_node')

        # QoS pour LiDAR haute fréquence : BEST_EFFORT + KEEP_LAST(1)
        lidar_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # QoS pour commandes critiques : RELIABLE + KEEP_LAST(10)
        command_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Subscriber LiDAR
        self.lidar_sub = self.create_subscription(
            Float64, '/lidar/scan', self.lidar_callback, lidar_qos)

        # Publisher commandes critiques
        self.cmd_pub = self.create_publisher(
            String, '/robot/commands', command_qos)

        self.create_timer(1.0, self.publish_command)
        self.get_logger().info('QoS Node démarré!')

    def lidar_callback(self, msg):
        self.get_logger().info(f'LiDAR reçu: {msg.data:.2f}m')

    def publish_command(self):
        msg = String()
        msg.data = 'AVANCER'
        self.cmd_pub.publish(msg)
        self.get_logger().info(f'Commande publiée: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = QoSNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
