#! /usr/bin/env python

import rospy
import actionlib
import time
from pkg_ros_iot_bridge.msg import msgRosIotAction
from pkg_ros_iot_bridge.msg import msgRosIotGoal

class Para_grn():
    """docstring for Para_grn"""
    def __init__(self):
        rospy.init_node('actionClient', anonymous=True)
        self.CLIENT_BRIDGE = actionlib.SimpleActionClient('/action_ros_iot', msgRosIotAction)
        # self.CLIENT_BRIDGE.wait_for_server()
        rospy.loginfo("This Action server is up, we can send results!")

    def send_para(self, Id, datas):

        goal_bridge = msgRosIotGoal(data=str(datas), sheetName=Id)
        self.CLIENT_BRIDGE.send_goal(goal_bridge)
        rospy.loginfo("Sent result to action bridge")

if __name__ == '__main__':

    try:

        Param = Para_grn()

        while not rospy.is_shutdown():

            Param.send_para("Thid is data send by client", "This is sheetName send by client")
            time.sleep(3)
        
    except rospy.ROSInterruptException:
        print 'Something went wrong:'