#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def move_turtle():

    rospy.init_node('turtle_controller',anonymous =True)

    turtle_cmd_pub =rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10)

    rate = rospy.Rate(10)

    cmd_vel=Twist()
    cmd_vel.linear.x = 1.0
    cmd_vel.angular.z = 1.0

    for _ in range(35):
        rospy.loginfo("Published Twist: Linear=%.2f, Angular=%.2f,",cmd_vel.linear.x,cmd_vel.angular.z)
        turtle_cmd_pub.publish(cmd_vel)
        rate.sleep()

    cmd_vel.linear.x=0.0
    cmd_vel.angular.z=1.0

    for _ in range(15):
        rospy.loginfo("Published Twist: Linear=%.2f, Angular=%.2f,",cmd_vel.linear.x,cmd_vel.angular.z)
        turtle_cmd_pub.publish(cmd_vel)
        rate.sleep()

    cmd_vel.linear.x=1.0
    cmd_vel.angular.z=0.0

    for _ in range(15):
        rospy.loginfo("Published Twist: Linear=%.2f, Angular=%.2f,",cmd_vel.linear.x,cmd_vel.angular.z)
        turtle_cmd_pub.publish(cmd_vel)
        rate.sleep()

if __name__ == '__main__':
    try:
        move_turtle()
    except rospy.ROSInterruptException:
        pass
