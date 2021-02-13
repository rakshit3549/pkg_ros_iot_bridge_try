#! /usr/bin/env python

'''This Client Node sends goals to appropriate server to do task '''

import rospy
import actionlib
import time
from pkg_ros_iot_bridge.msg import msgRosIotAction
from pkg_ros_iot_bridge.msg import msgRosIotGoal
# from pkg_ros_iot_bridge.msg import msgMqttSub

class main():
    """docstring for main"""
    def __init__(self):
    
        self.CLIENT_BRIDGE = actionlib.SimpleActionClient('/action_ros_iot', msgRosIotAction)
        self.CLIENT_BRIDGE.wait_for_server()
        rospy.loginfo("This Action server is up, we can send results!")

    def function(self):

        datas = {'package_details': {'package_colour': {'packagen31': 'green', 'packagen12': 'red',
                                                         'packagen11': 'yellow', 'packagen10': 'green',
                                                         'packagen22': 'yellow', 'packagen30': 'yellow',
                                                         'packagen20': 'green', 'packagen32': 'red',
                                                         'packagen00': 'red', 'packagen01': 'yellow',
                                                         'packagen02': 'green', 'packagen21': 'red'}}}
        datas = str(datas) 
        goal_bridge = msgRosIotGoal(data = datas)
        self.CLIENT_BRIDGE.send_goal(goal_bridge)
        rospy.loginfo("Sent result to action bridge")

if __name__ == '__main__':

    try:
        # 1. Initialize ROS Node
        rospy.init_node('action_client')

        print(str(time.strftime("%d%y")))

        datas = {'package_details': {'package_colour': {'packagen31': [3, 1, 'green'], 'packagen12': [1, 2, 'red'],
                                                        'packagen11': [1, 1, 'yellow'], 'packagen10': [1, 0, 'green'],
                                                        'packagen22': [2, 2, 'yellow'], 'packagen30': [3, 0, 'yellow'],
                                                        'packagen20': [2, 0, 'green'], 'packagen32': [3, 2, 'red'],
                                                        'packagen00': [0, 0, 'red'], 'packagen01': [0, 1, 'yellow'],
                                                        'packagen02': [0, 2, 'green'], 'packagen21': [2, 1, 'red']}}}

        data = datas["package_details"]["package_colour"]
        print(sorted(data.values()))

        obj_client = main()

        while not rospy.is_shutdown() :
            obj_client.function()
            time.sleep(5)

        rospy.spin()

    except rospy.ROSInterruptException:
        print 'Something went wrong:'
