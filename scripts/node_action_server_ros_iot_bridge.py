#! /usr/bin/env python

'''                                                       Bridge between ROS and iot                                    '''


import rospy
import actionlib
import json
import threading
from pyiot import iot
from pkg_ros_iot_bridge.msg import msgRosIotAction
from pkg_ros_iot_bridge.msg import msgMqttSub

class SimpleServer():

    '''Bridge between Mqtt and Simple Action Client'''

    def __init__(self):



        self._param_config_iot = rospy.get_param('config_pyiot')
        self._config_mqtt_server_url = self._param_config_iot['mqtt']['server_url']
        self._config_mqtt_server_port = self._param_config_iot['mqtt']['server_port']
        self._config_mqtt_sub_topic = self._param_config_iot['mqtt']['topic_sub']
        self._config_mqtt_qos = self._param_config_iot['mqtt']['qos']
        self._config_mqtt_sub_cb_ros_topic = self._param_config_iot['mqtt']['sub_cb_ros_topic']

        self._ret = iot.mqtt_subscribe_thread_start(self.mqtt_sub_callback,
                                              self._config_mqtt_server_url,
                                              self._config_mqtt_server_port,
                                              self._config_mqtt_sub_topic,
                                              self._config_mqtt_qos)


        self.ros_pub = rospy.Publisher(self._config_mqtt_sub_cb_ros_topic,
                                       msgMqttSub, queue_size=10)



        self._sas = actionlib.SimpleActionServer('/action_ros_iot',
                                                msgRosIotAction,
                                                execute_cb=self.func_on_rx_goal,
                                                auto_start=False)

        if self._ret == 0:
            rospy.loginfo("MQTT Subscribe Thread Started")
        else:
            rospy.logerr("Failed to start MQTT Subscribe Thread")

        # Start the Action Server
        self._sas.start()
        rospy.loginfo("Started Action Bridge Server.")

    def priority_cost(self, data):

        if data["item"] == "Medicine":
            priority = "HP"
            cost = 500
        elif data["item"] == "Food":
            priority = "MP"
            cost = 350
        else:
            priority = "LP"
            cost = 150
        return priority, cost

    def mqtt_sub_callback(self, client, userdata, message):
        '''This is a callback function for MQTT Subscriptions'''
        # print(message.payload)
        # print(type(message.payload))
        payload = str(message.payload.decode("utf-8"))
        # print(payload)
        # print(type(payload))
        data = json.loads(payload)
        sheet_id = "IncomingOrders"
        # print(data)
        # print(type(data))
        self.update_sheets(sheet_id, data)
        #----------------------------------
        #add priority, cost, in payload
        #----------------------------------
        msg_mqtt_sub = msgMqttSub()
        msg_mqtt_sub.timestamp = rospy.Time.now()
        msg_mqtt_sub.topic = message.topic
        msg_mqtt_sub.message = payload
        self.ros_pub.publish(msg_mqtt_sub)

    def update_sheets(self, sheet_id, data):

        priority, cost = self.priority_cost(data)

        sheet = iot.sheetsUpdate(sheet_id, priority, cost, data)
        if sheet == 0:
            rospy.loginfo("sheet update sucessfull")
        else:
            rospy.loginfo("sheet update failed")




    def func_on_rx_goal(self, goals):

        '''This function runs when there is a new goal from client'''
        sheet_id = goals.sheetName
        goal_srt = goals.data

        print sheet_id, goal_srt
        
        # goal_srt = goal_srt.replace("'",'"')
        # print(goal_srt)

        # print(type(goal_srt))
        # # payload = str(message.payload.decode("utf-8"))

        # goals = json.loads(goal_srt)
        # print(type(goals))
        # print(goals)

        
        # t = threading.Thread(name="sheets",
        #                      target=self.update_sheets,
        #                      args=[sheet_id, goals])
        # t.start()




def main():

    '''Main'''

    # 1. Initialize ROS Node
    rospy.init_node('node_action_server_ros_Iot_bridge')

    #obj_server =
    SimpleServer()

    rospy.spin()

if __name__ == '__main__':

    try:

        main()

    except rospy.ROSInterruptException:
        print 'Something went wrong:'
