#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo("I heard",)
    
def listener():

   
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('chatter', String, callback)

    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass