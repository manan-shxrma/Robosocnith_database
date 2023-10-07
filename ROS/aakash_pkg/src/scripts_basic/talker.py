#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def talker():
    pub_object= rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        greeting_str = "hello World" 
        rospy.loginfo(greeting_str)
        pub_object.publish(greeting_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
