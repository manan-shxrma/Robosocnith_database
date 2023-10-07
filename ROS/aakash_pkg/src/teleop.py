#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

# Define a class for teleoperation
class Teleop:
    # Initialize the class
    def __init__(self):
        # Create a node with a name
        rospy.init_node('teleop', anonymous=True)
        # Create a publisher to publish Twist messages to /cmd_vel topic
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        # Create a Twist message object
        self.twist = Twist()
        # Set the rate of publishing messages
        self.rate = rospy.Rate(10)

    # Define a method to get keyboard input
    def get_key(self):
        # Import the module for keyboard input
        import sys, select, termios, tty
        # Save the terminal settings
        settings = termios.tcgetattr(sys.stdin)
        # Set the terminal to raw mode
        tty.setraw(sys.stdin.fileno())
        # Select the input stream
        select.select([sys.stdin], [], [], 0)
        # Read one character from the input stream
        key = sys.stdin.read(1)
        # Restore the terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        # Return the key pressed
        return key

    # Define a method to update the twist message based on the key pressed
    def update_twist(self, key):
        # Define the linear and angular speed increments
        linear_increment = 0.1
        angular_increment = 0.1
        # Define a dictionary to map keys to twist values
        key_map = {
            'w': (linear_increment, 0),
            'a': (0, angular_increment),
            's': (-linear_increment, 0),
            'd': (0, -angular_increment),
            'x': (0, 0),
            ' ': (0, 0)
        }
        # Check if the key is in the dictionary
        if key in key_map:
            # Get the linear and angular speed changes from the dictionary
            linear_change, angular_change = key_map[key]
            # Update the linear and angular speed of the twist message
            self.twist.linear.x += linear_change
            self.twist.angular.z += angular_change

    # Define a method to run the teleoperation loop
    def run(self):
        # Print some instructions for the user
        print("Control your TurtleBot3!")
        print("---------------------------")
        print("Moving around:")
        print("   w")
        print("a  s  d")
        print("   x")
        
        print("w/x : increase/decrease linear velocity")
        print("a/d : increase/decrease angular velocity")
        
        print("space key, x : force stop")
        
        print("CTRL-C to quit")
        
        # Loop until rospy is shutdown
        while not rospy.is_shutdown():
            # Get the key pressed by the user
            key = self.get_key()
            # Update the twist message based on the key pressed
            self.update_twist(key)
            # Publish the twist message to /cmd_vel topic
            self.pub.publish(self.twist)
            # Sleep for the rate duration
            self.rate.sleep()

# Create an object of Teleop class and run it
if __name__ == '__main__':
    teleop = Teleop()
    teleop.run()
