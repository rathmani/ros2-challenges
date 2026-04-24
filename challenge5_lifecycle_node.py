import rclpy
from rclpy.lifecycle import Node, State, TransitionCallbackReturn
from std_msgs.msg import String

class LifecyclePublisher(Node):
    def __init__(self):
        super().__init__('lifecycle_publisher')
        self.publisher_ = None
        self.timer_ = None

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        self.publisher_ = self.create_publisher(String, '/message', 10)
        self.timer_ = self.create_timer(1.0, self.timer_callback)
        self.get_logger().info('Node activé — publisher démarré!')
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        self.destroy_timer(self.timer_)
        self.destroy_publisher(self.publisher_)
        self.publisher_ = None
        self.timer_ = None
        self.get_logger().info('Node désactivé — publisher arrêté!')
        return TransitionCallbackReturn.SUCCESS

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello depuis Lifecycle Node!'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publié: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = LifecyclePublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
