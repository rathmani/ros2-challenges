import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class CalculatriceService(Node):
    def __init__(self):
        super().__init__('calculatrice_service')
        self.srv = self.create_service(
            AddTwoInts, '/calcule', self.calcule_callback)
        self.get_logger().info('Service /calcule prêt!')

    def calcule_callback(self, request, response):
        a, b = float(request.a), float(request.b)
        response.sum = int(a + b)
        self.get_logger().info(f'{a} + {b} = {response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = CalculatriceService()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
