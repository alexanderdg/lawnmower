import paho.mqtt.client as mqtt
from MotionController import MotionController
from IOcontroller import IOcontroller
from INA219 import Battery
from StateMachine import StateImp
import time
import signal
import threading
import os

bustype = 'socketcan'
channel = 'can0'
client = mqtt.Client()
temp = StateImp()
global runBool
runBool = 0

class MQTTloop(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.shutdown_flag = threading.Event()

	def run(self):
		print('Thread #%s started' % self.ident)
		while not self.shutdown_flag.is_set():
		    client.loop_forever()
		# ... Clean shutdown code here ...
		print('Thread #%s stopped' % self.ident)



def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
        global runBool
        p = msg.payload.decode()
        if(msg.topic == "ledRed"):
            #io.setLed(int(p), 0, 0)
            print("temp")
        elif(msg.topic == "runBool"):
            if(p == "True"):
                temp.nextState(temp.runstate)
            elif(p == "False"):
                temp.nextState(temp.stopstate)
        elif(msg.topic == "manualForward"):
            if p == "1":
                temp.manualcontrol.setManualControl("F")
            elif p == "0":
                temp.manualcontrol.setManualControl("S")
            temp.nextState(temp.manualcontrol)
        elif (msg.topic == "manualBackward"):
            if p == "1":
                temp.manualcontrol.setManualControl("B")
            elif p == "0":
                temp.manualcontrol.setManualControl("S")
            temp.nextState(temp.manualcontrol)
        elif (msg.topic == "manualLeft"):
            if p == "1":
                temp.manualcontrol.setManualControl("L")
            elif p == "0":
                temp.manualcontrol.setManualControl("S")
            temp.nextState(temp.manualcontrol)
        elif (msg.topic == "manualRight"):
            if p == "1":
                temp.manualcontrol.setManualControl("R")
            elif p == "0":
                temp.manualcontrol.setManualControl("S")
            temp.nextState(temp.manualcontrol)
        elif (msg.topic == "manualSpeed"):
            temp.manualcontrol.setSpeed(float(p))
            temp.nextState(temp.manualcontrol)


class ServiceExit(Exception):
    pass

def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

def main():
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    #client.loop_forever()
    os.system("mpg123 /share/Sourcecode/lawnmower/WAV\ files/StartingMoving.mp3")
    print('Starting main program')
    ts = 0
    try:
        j1 = MQTTloop()
        j1.start()
        client.subscribe("ledRed")
        client.subscribe("ledGreen")
        client.subscribe("ledBlue")
        client.subscribe("runBool")
        client.subscribe("manualForward")
        client.subscribe("manualBackward")
        client.subscribe("manualLeft")
        client.subscribe("manualRight")
        client.subscribe("manualSpeed")
        #motion.turn90Right()
        #time.sleep(200)
        #print("return of drive function {}", result)
        while True:
            temp.runStatemachine()
            time.sleep(0.02)

    except ServiceExit:
        temp.stop()
        pass

    #motion.dynamicBrake()
    print('Exiting main program')


if __name__ == '__main__':
    main()