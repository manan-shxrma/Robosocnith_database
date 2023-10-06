#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


def callback(data):
    global x,y,theta
    x=data.x
    y=data.y
    theta=data.theta

def rotate_right(cmd_vel,vel_pub,rate):
    while abs(theta)>1.8:
        cmd_vel.linear.x=0.0
        cmd_vel.angular.z=1.57
        vel_pub.publish(cmd_vel)
        rate.sleep()

def move_straight(cmd_vel,vel_pub,rate):
    while y>5.8:
        cmd_vel.linear.x=0.5
        cmd_vel.angular.z=0.0
        vel_pub.publish(cmd_vel)
        rate.sleep()


def move_turtle():
    global x,y,theta
    rospy.init_node('turtle_controller', anonymous=True)
    vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=5)
    rospy.Subscriber('/turtle1/pose',Pose,callback)
    rate = rospy.Rate(10)
    
    cmd_vel=Twist()
    cmd_vel.linear.x=2.0
    cmd_vel.angular.z=1.0

    while not rospy.is_shutdown():
        print(f"Current Position - X: {x:.6f}, Y: {y:.6f}, Theta: {theta:.6f}")
        rospy.loginfo("Published Twist: Linear=%.2f, Angular=%.2f,",cmd_vel.linear.x,cmd_vel.angular.z)
        if theta<3.1:
            vel_pub.publish(cmd_vel)
            rate.sleep()
        else:
            while abs(theta)>1.8:
                cmd_vel.linear.x=0.0
                cmd_vel.angular.z=1.57
                vel_pub.publish(cmd_vel)
                rate.sleep()
            rate.sleep()
            move_straight(cmd_vel,vel_pub,rate)
            break

if __name__ == '__main__':
    try:
        x,y,theta =0,0,0
        move_turtle()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass