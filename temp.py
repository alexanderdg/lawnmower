import time
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("currentLeft")

def on_message(client, userdata, msg):
  p = msg.payload.decode()
  print(p)


client = mqtt.Client()
client.connect("robot.local",1883,60)

client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()