import paho.mqtt.client as mqtt
from statemachine import StateMachine, State
from IOcontroller import IOcontroller
from MotionController import MotionController
from INA219 import Battery
from threading import Thread
import time

class Run(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        #print("init start state")

    def enterState(self):
        print("Enter Run state")

    def run(self):
        timestamp = time.time()
        if (timestamp - self.timestamp) > 0.4:
            print("run run state")
            self.manager.motion.forward(0.5)
            self.timestamp = timestamp

        if self.manager.motion.getLeftCurrent() > 1.2 or self.manager.motion.getRightCurrent() > 1.2 or self.manager.pressureSensorRight > 100 or self.manager.pressureSensorLeft > 100 or self.manager.perimeterValue > 300:
            self.manager.nextState(self.manager.breakstate)



class Break(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        #print("init start state")

    def enterState(self):
        print("Enter Break state")
        self.manager.motion.dynamicBrake()
        time.sleep(3)
        self.manager.motion.reverse(0.5)
        time.sleep(1)
        self.manager.motion.coastBrake()
        time.sleep(0.5)
        self.manager.motion.turn90Right()
        time.sleep(3)
        self.manager.motion.forward(0.5)

    def run(self):
        self.manager.nextState(self.manager.runstate)
        timestamp = time.time()
        if (timestamp - self.timestamp) > 0.4:
            print("run break state")
            self.timestamp = timestamp





class StateImp(Thread, StateMachine):
    leftMotorCurrent = 0.0
    rightMotorCurrent = 0.0
    leftMotorSpeed  = 0.0
    rightMotorSpeed = 0.0
    leftMotorDistance = 0
    rightMotorDistance = 0
    pressureSensorLeft = 0
    pressureSensorRight = 0
    distance1 = 0
    distance2 = 0
    distance3 = 0
    distance4 = 0
    perimeterValue = 0
    batteryVoltage  = 0.0
    batteryCurrent = 0.0
    batteryPower = 0.0
    motion = MotionController()
    ioController = IOcontroller()
    battery = Battery()
    client = mqtt.Client()
    state = "INIT"
    def __init__(self):
        Thread.__init__(self)
        IOcom = Thread(name='IOcom', target=self.IOthread)
        CANcom = Thread(name='CANcom', target=self.CANthread)
        testthread = Thread(name='testhread', target=self.MQTTthread)
        self.runstate = Run(self)
        self.breakstate = Break(self)
        self.nextState(self.runstate)
        testthread.setDaemon(True)
        IOcom.setDaemon(True)
        CANcom.setDaemon(True)
        testthread.start()
        IOcom.start()
        CANcom.start()
        self.client.connect("localhost", 1883, 60)

    def testThread(self):
        while True:
            print("run testthread");
            time.sleep(1)

    def IOthread(self):
        while True:
            ts = time.time()
            self.perimeterValue = self.ioController.readPerimeterMagn()
            self.distance1 = self.ioController.readDistanceSensor1()
            self.distance2 = self.ioController.readDistanceSensor2()
            self.distance3 = self.ioController.readDistanceSensor3()
            self.distance4 = self.ioController.readDistanceSensor4()
            self.pressureSensorLeft = self.ioController.readPresureSensorLeft()
            self.pressureSensorRight = self.ioController.readPresureSensorRight()
            self.batteryVoltage = self.battery.readVoltage()
            self.batteryCurrent = self.battery.readCurrent()
            self.batteryPower = self.battery.readPower()
            time.sleep(0.05)
            ta = time.time()
            #print("IO thread")
            #print(ta - ts)

    def CANthread(self):
        while True:
            ts = time.time()
            self.leftMotorCurrent = self.motion.getLeftCurrent()
            self.rightMotorCurrent = self.motion.getRightCurrent()
            self.leftMotorSpeed = self.motion.getLeftSpeed()
            self.rightMotorSpeed = self.motion.getRightSpeed()
            self.leftMotorDistance = self.motion.getDistanceLeft()
            self.rightMotorDistance = self.motion.getDistanceRight()
            ta = time.time()
            #print("CAN thread")
            time.sleep(0.01)
            #print(ta - ts)

    def MQTTthread(self):
        while True:
            ts = time.time()
            self.client.publish("diagnostics", "%.2f:%.2f:%.2f:%.2f:%4d:%4d:%s" % (self.leftMotorCurrent, self.rightMotorCurrent, self.leftMotorSpeed, self.rightMotorSpeed, self.pressureSensorLeft, self.pressureSensorRight, self.batteryVoltage))
            #self.client.publish("currentLeft", "%.2f" % (self.leftMotorCurrent))
            #self.client.publish("currentRight", "%.2f" % self.rightMotorCurrent)
            #self.client.publish("speedLeft", "%.2f" % self.leftMotorSpeed)
            #self.client.publish("speedRight", "%.2f" % self.rightMotorSpeed)
            #self.client.publish("distanceLeft", self.leftMotorDistance)
            #self.client.publish("distanceRight", self.rightMotorDistance)
            #self.client.publish("pressureLeft", self.pressureSensorLeft)
            #self.client.publish("pressureRight", self.pressureSensorRight)
            #self.client.publish("batteryVoltage", self.batteryVoltage)
            #self.client.publish("batteryCurrent", self.batteryCurrent)
            #self.client.publish("batteryPower", self.batteryPower)
            ta = time.time()
            time.sleep(0.02)
            #print("MQTT thread")
            #print(ta -ts)

    def nextState(self, state):
        self.state = state
        self.state.enterState()

    def runStatemachine(self):
        self.state.run()


    def stop(self):
        self.motion.coastBrake()
