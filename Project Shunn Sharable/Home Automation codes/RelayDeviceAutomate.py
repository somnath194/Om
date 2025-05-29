import paho.mqtt.client as paho
import sys
import time

sys.path.append("D:\\programs\\Project Shunn\\Features")
import commands as cd

client = paho.Client(paho.CallbackAPIVersion.VERSION2)
bedroom_controlTopic = ""
bedroom_statusTopic = ""
 
outside_controlTopic = ""
outside_statusTopic = ""

work_controlTopic = ""
work_statusTopic = ""


mqttServer = "broker.mqtt.cool"


def onMessage(client, userdata, msg):
    print(msg.topic + ": " + str(msg.payload.decode("utf-8")))

def mqtt_publish(command,topic):
    if client.connect(mqttServer,1883, 60) != 0:
        print("could not connect to MQTT Broker!")
        sys.exit(-1)
    
    client.publish(topic,command,0)
    time.sleep(1)

def mqtt_subscribe(time_in_sec):
    if client.connect(mqttServer,1883, 60) != 0:
        print("could not connect to MQTT Broker!")
        sys.exit(-1)
    
    client.loop_start()
    client.subscribe(bedroom_statusTopic)
    client.on_message = onMessage
    time.sleep(time_in_sec)
    client.loop_stop()

def RoomControl(quary):
    if quary in cd.light_on_commands:
        mqtt_publish("relay1_on",bedroom_controlTopic)
    
    elif quary in cd.light_off_commands:
        mqtt_publish("relay1_off",bedroom_controlTopic)

    elif quary in cd.bulb_on_commands:
        mqtt_publish("relay3_on",bedroom_controlTopic)
    
    elif quary in cd.bulb_off_commands:
        mqtt_publish("relay3_off",bedroom_controlTopic)
    
    elif quary in cd.fan_on_commands:
        mqtt_publish("relay4_on",bedroom_controlTopic)
    
    elif quary in cd.fan_off_commands:
        mqtt_publish("relay4_off",bedroom_controlTopic)
    
    elif quary in cd.bathroom_light_on_commands:
        mqtt_publish("relay3_on",outside_controlTopic)
    
    elif quary in cd.bathroom_light_off_commands:
        mqtt_publish("relay3_off",outside_controlTopic)
    
    elif quary in cd.stair_light_on_commands:
        mqtt_publish("relay1_on",outside_controlTopic)
    
    elif quary in cd.stair_light_off_commands:
        mqtt_publish("relay1_off",outside_controlTopic)
    
    elif quary in cd.outside_light_on_commands:
        mqtt_publish("relay2_on",outside_controlTopic)
    
    elif quary in cd.outside_light_off_commands:
        mqtt_publish("relay2_off",outside_controlTopic)
    
    elif quary in cd.outside_camera_on_commands:
        mqtt_publish("relay4_on",outside_controlTopic)

    elif quary in cd.outside_camera_off_commands:
        mqtt_publish("relay4_off",outside_controlTopic)

# # Call this function from anywhere
# if __name__ == "__main__":
#     mqtt_subscribe(20)