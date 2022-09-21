import sys

from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node
import string
import random

from std_msgs.msg import String #extra

class Calculator(Node):

    def __init__(self):
        a = 1

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str


    def reverse_string(self,input):
        return input[::-1]

    def count_string(self,input):
        return len(input)

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        calc = Calculator()
        minimal_client = MinimalClientAsync()
        input = int(msg.data)
        minimal_client.get_logger().info('Input data %d' %(input))
        random_string = calc.get_random_string(input)
        minimal_client.get_logger().info('random string %s' %(random_string))
        reverse_string = calc.reverse_string(random_string)
        minimal_client.get_logger().info('Reverse string %s' %(reverse_string))
        counted_string = calc.count_string(reverse_string)
        minimal_client.get_logger().info('Counted string %d' %(counted_string))
        response = minimal_client.send_request(counted_string)

        minimal_client.destroy_node()
  
class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a):
        self.req.a = a
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()