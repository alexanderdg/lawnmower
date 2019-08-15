import paho.mqtt.client as mqtt
from MotionController import MotionController
from IOcontroller import IOcontroller
from INA219 import Battery
import time
import signal
import threading

bustype = 'socketcan'
channel = 'can0'
client = mqtt.Client()
io = IOcontroller()
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
        client.subscribe("ledRed")
        client.subscribe("ledGreen")
        client.subscribe("ledBlue")
        client.subscribe("runBool")

def on_message(client, userdata, msg):
        global runBool
        p = msg.payload.decode()
        if(msg.topic == "ledRed"):
            io.setLed(int(p), 0, 0)
        elif(msg.topic == "runBool"):
            if(p == "True"):
                runBool = 1
            elif(p == "False"):
                runBool = 0

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
    #os.system("mpg123 /share/Sourcecode/lawnmower/WAV\ files/StartingMoving.mp3")
    motion = MotionController()
    battery = Battery()
    print('Starting main program')
    try:
        j1 = MQTTloop()
        j1.start()

        #motion.turn90Right()
        #time.sleep(200)
        #print("return of drive function {}", result)
        while True:
            LeftCurrent = motion.getLeftCurrent()
            RightCurrent = motion.getRightCurrent()
            LeftSpeed = motion.getLeftSpeed()
            RightSpeed = motion.getRightSpeed()
            PressureSensorLeft = io.readPresureSensorLeft()
            PressureSensorRight = io.readPresureSensorRight()
            client.publish("currentLeft", "%.2f" % LeftCurrent)
            client.publish("currentRight", "%.2f" % RightCurrent)
            client.publish("speedLeft", "%.2f" % LeftSpeed)
            client.publish("speedRight", "%.2f" % RightSpeed)
            client.publish("distanceLeft", motion.getDistanceLeft())
            client.publish("distanceRight", motion.getDistanceRight())
            client.publish("pressureLeft", PressureSensorLeft)
            client.publish("pressureRight", PressureSensorRight)
            client.publish("batteryVoltage", battery.readVoltage())
            client.publish("batteryCurrent", battery.readCurrent())
            client.publish("batteryPower", battery.readPower())
            if(runBool == 1):
                if LeftCurrent > 1.0 or RightCurrent > 1.0 or PressureSensorRight > 60 or PressureSensorLeft > 60:
                    motion.dynamicBrake()
                    time.sleep(3)
                    motion.reverse(0.5)
                    time.sleep(1)
                    motion.turn90Right()
                    time.sleep(3)
                    motion.forward(0.5)

                else:
                    motion.forward(0.5)
            else:
                motion.coastBrake()

            time.sleep(0.1)

    except ServiceExit:
        j1.shutdown_flag.set()
        j1.join()
        pass

    motion.dynamicBrake()
    print('Exiting main program')


if __name__ == '__main__':
    main()