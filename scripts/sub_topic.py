#! /usr/bin/env python

'''This Client Node sends goals to appropriate server to do task '''

import rospy
import json
from pkg_ros_iot_bridge.msg import msgMqttSub

def func_callback_topic_my_topic(my_msg):
	data = json.loads(my_msg.message)
	for i in data:
		print data[i]


if __name__ == '__main__':

    try:
    	# 1. Initialize ROS Node
        rospy.init_node('node_action_client_turtle')

        # 4. Initialize Subscriber
        rospy.Subscriber("/ros_iot_bridge/mqtt/sub", msgMqttSub, func_callback_topic_my_topic)

        rospy.spin()

    except rospy.ROSInterruptException:
        print 'Something went wrong:'