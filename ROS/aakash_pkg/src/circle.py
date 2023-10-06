#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def draw_circle():
    rospy.init_node('draw_circle', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    # Set linear speed (in turtle's units)
    vel_msg.linear.x = 2.0

    # Set the time to complete the circle (in seconds)
    circle_time = 10.0

    # Set the rate at which we publish the velocity (in Hz)
    rate = rospy.Rate(10)  # 10 Hz

    start_time = rospy.Time.now().to_sec()
    while not rospy.is_shutdown():
        current_time = rospy.Time.now().to_sec()
        elapsed_time = current_time - start_time

        if elapsed_time >= circle_time:
            break

        # Calculate the angle the turtle has rotated around the center
        angle = 2.0 * 3.141592653589793 * (elapsed_time / circle_time)

        # Set the angular speed (rotate at a constant rate)
        vel_msg.angular.z = 2.0

        # Move the turtle by publishing the velocity message
        velocity_publisher.publish(vel_msg)

        # Sleep for a short duration
        rate.sleep()

    # Stop the turtle after completing the circle
    vel_msg.linear.x = 0.0
    vel_msg.angular.z = 0.0
    velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    try:
        draw_circle()
    except rospy.ROSInterruptException:
        pass
