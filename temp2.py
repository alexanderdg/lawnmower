#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time

# Create client instance and connect to localhost
client = mqtt.Client()
client.connect("localhost",1883,60)

# Publish message to topic/iopi and set pin 1 on bus 1 to on
client.publish("topic/iopi", "1,1");
time.sleep(2)

# Publish message to topic/iopi and set pin 1 on bus 1 to off
client.publish("topic/iopi", "1,0");
time.sleep(2)
# Publish message to topic/iopi and set pin 1 on bus 2 to on
client.publish("topic/iopi", "17,1");
time.sleep(2)
# Publish message to topic/iopi and set pin 1 on bus 2 to off
client.publish("topic/iopi", "17,0");
client.disconnect();