#! /usr/bin/env python

import rospy
import actionlib
from pkg_ros_iot_bridge.msg import msgRosIotAction
from pkg_ros_iot_bridge.msg import msgMqttSub

class SimpleServer():

    '''Bridge between Mqtt and Simple Action Client'''

    def __init__(self):

        self._sas = actionlib.SimpleActionServer('/action_ros_iot',
                                                msgRosIotAction,
                                                execute_cb=self.func_on_rx_goal,
                                                auto_start=False)
        self._sas.start()
        rospy.loginfo("Started Action Bridge Server.")

    def func_on_rx_goal(self, goals):

        '''This function runs when there is a new goal from client'''
        sheet_id = goals.sheetName
        goal_srt = goals.data
        print sheet_id, goal_srt

    

if __name__ == '__main__':

    try:

        rospy.init_node('server_ros_Iot_bridge',  anonymous=True)

        SimpleServer()

        rospy.spin()

    except rospy.ROSInterruptException:
        print 'Something went wrong:'