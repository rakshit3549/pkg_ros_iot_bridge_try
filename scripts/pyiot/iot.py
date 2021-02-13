# from multiprocessing.dummy import Pool
import time
import requests
import json
import paho.mqtt.client as mqtt

# class print_colour:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'

def on_connect(client, userdata, flags, rc):
    print("[INFO] Connected With Result Code: " + str(rc))


# -----------------  MQTT SUB -------------------
def iot_func_callback_sub(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def mqtt_subscribe_thread_start(arg_callback_func, arg_broker_url, arg_broker_port, arg_mqtt_topic, arg_mqtt_qos):
    try:
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = arg_callback_func
        mqtt_client.connect(arg_broker_url, arg_broker_port)
        mqtt_client.subscribe(arg_mqtt_topic, arg_mqtt_qos)
        time.sleep(1)
        mqtt_client.loop_start()
        return 0
    except:
        return -1


#_________________________________________________________

def sheetsUpdate(Id, Priority ,Cost ,order_dict):

    parameter = {"Team Id":205, "Unique Id":"Pandemic","id":str(Id),"Priority":str(Priority),"Cost":str(Cost)}

    for item in order_dict:
        if item == "city":
            parameter["City"] = str(order_dict[item])
        elif item == "order_time":
            parameter["Order Date and Time"] = str(order_dict[item])
        elif item == "order_id":
               parameter["Order ID"] = str(order_dict[item])
        elif item == "item":
            parameter["Item"] = str(order_dict[item])

    if Id == "IncomingOrders":
        for item in order_dict:
            if item == "lon":
                parameter["Longitude"] = str(order_dict[item])
            elif item == "lat":
                parameter["Latitude"] = str(order_dict[item])
            elif item == "qty":
                parameter["Order Quantity"] = str(order_dict[item])

    elif Id == 'OrdersShipped':
        for item in order_dict:
            if item == "qty":
                parameter["Shipped Quantity"] = str(order_dict[item])
            elif item == "updateDateTime":
                parameter["Shipped Date and Time"] = str(order_dict[item])
            elif item == "estimTime":
                parameter["Estimated Time of Delivery"] = str(order_dict[item])
        parameter["Shipped Status"] = "YES"

    elif Id == 'OrdersDispatched':
        for item in order_dict:
            if item == "qty":
                parameter["Dispatch Quantity"] = str(order_dict[item])
            elif item == "updateDateTime":
                parameter["Dispatch Date and Time"] = str(order_dict[item])
        parameter["Dispatch Status"] = "YES"


    elif Id == 'Inventory' :
        for item in order_dict:
            if item == "SKU":
                parameter["SKU"] = str(order_dict[item])
            elif item == "storageNo":
                parameter["Storage Number"] = str(order_dict[item])
            elif item == "item":
                parameter["Item"] = str(order_dict[item])
            elif item == "qty_invet":
                parameter["Quantity"] = str(order_dict[item])


    print("final!!!!!!!!!!!!!!!!!!")
    print parameter
    
    return sheetUpdate(parameter)

def sheetUpdate(parameters):

    try:
        URL = "https://script.google.com/macros/s/AKfycbxzDT9V-wHKWMmVTeVw4HEksTDW5CUCDanxoKQbHk0RUHScBaE5kvYq/exec"
        response = requests.get(URL, params=parameters)
        print(response.content)
        return 0
    except:
        return -1


