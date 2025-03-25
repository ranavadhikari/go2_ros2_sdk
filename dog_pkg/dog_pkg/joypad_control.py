import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class JoypadControl(Node):
    def __init__(self):
        super().__init__('joypad_control')

        # Subscribe to joystick input topic
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10
        )

        # Publisher for robot velocity commands
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Define button names based on common controllers (Modify if needed)
        self.button_names = {
            0: "A", 1: "B", 2: "X", 3: "Y",
            4: "LB", 5: "RB", 6: "Back", 7: "Start",
            8: "Power", 9: "Left Stick", 10: "Right Stick"
        }

        self.get_logger().info("Joystick control node started")

    def joy_callback(self, msg: Joy):
        twist = Twist()

        # Debugging joystick values
        self.get_logger().info(f"Axes: {msg.axes}")
        
        # Print button status
        button_status = {self.button_names[i]: ("Pressed" if state == 1 else "Released") for i, state in enumerate(msg.buttons) if i in self.button_names}
        self.get_logger().info(f"Buttons: {button_status}")

        # Assign axes for movement
        linear_axis = msg.axes[1]   # Forward/backward (Left stick vertical)
        turn_axis = msg.axes[0]     # Turning (Left stick horizontal)
        rotate_axis = msg.axes[3]   # Rotate in place (Right stick horizontal)

        # Set movement speed
        twist.linear.x = linear_axis * 0.5  # Adjust speed if needed
        twist.angular.z = turn_axis * 1.0 + rotate_axis * 1.5  # Rotation scaling

        # Publish movement only if there's joystick input
        if linear_axis != 0 or turn_axis != 0 or rotate_axis != 0:
            self.cmd_vel_pub.publish(twist)

        # Button actions
        if msg.buttons[0] == 1:  # A button
            self.get_logger().info("A button pressed - Executing Action 1 (Stand Up)")

        if msg.buttons[1] == 1:  # B button
            self.get_logger().info("B button pressed - Executing Action 2 (Sit Down)")

        if msg.buttons[2] == 1:  # X button
            self.get_logger().info("X button pressed - Executing Action 3 (Custom Action)")

        if msg.buttons[3] == 1:  # Y button
            self.get_logger().info("Y button pressed - Executing Action 4 (Another Action)")

        if msg.buttons[4] == 1:  # LB button
            self.get_logger().info("LB button pressed - Activating Left Grip")

        if msg.buttons[5] == 1:  # RB button
            self.get_logger().info("RB button pressed - Activating Right Grip")

        if msg.buttons[6] == 1:  # Back button
            self.get_logger().info("Back button pressed - Reset Position")

        if msg.buttons[7] == 1:  # Start button
            self.get_logger().info("Start button pressed - Initiating Mode Change")

        # Add more buttons as needed...

def main(args=None):
    rclpy.init(args=args)
    node = JoypadControl()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
