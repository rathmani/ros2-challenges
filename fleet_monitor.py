import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
from std_msgs.msg import String
import json

class FleetMonitor(Node):
    def __init__(self):
        super().__init__('fleet_monitor')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.pub = self.create_publisher(String, '/fleet_status', 10)
        self.create_timer(1.0, self.monitor_callback)
        self.robot_ids = [1, 2, 3]
        self.get_logger().info('Fleet Monitor démarré!')

    def monitor_callback(self):
        status = {}
        for rid in self.robot_ids:
            try:
                tf = self.tf_buffer.lookup_transform(
                    'world', f'robot{rid}',
                    rclpy.time.Time())
                x = tf.transform.translation.x
                y = tf.transform.translation.y
                status[f'robot{rid}'] = {'x': round(x,2), 'y': round(y,2), 'online': True}
            except Exception:
                status[f'robot{rid}'] = {'online': False}

        msg = String()
        msg.data = json.dumps(status)
        self.pub.publish(msg)
        self.get_logger().info(f'Fleet: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = FleetMonitor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
