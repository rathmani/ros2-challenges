import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import tf_transformations
import math

class TF2Broadcaster(Node):
    def __init__(self):
        super().__init__('tf2_broadcaster')
        self.broadcaster = TransformBroadcaster(self)
        self.angle = 0.0
        self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'robot'

        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0

        q = tf_transformations.quaternion_from_euler(0, 0, self.angle)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        self.broadcaster.sendTransform(t)
        self.angle += 0.5 * 0.1  # 0.5 rad/s

def main(args=None):
    rclpy.init(args=args)
    node = TF2Broadcaster()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
