import paho.mqtt.client as mqtt
import json
from statemachine import StateMachine, State
from IOcontroller import IOcontroller
from MotionController import MotionController
from INA219 import Battery
from threading import Thread
import time

client = mqtt.Client()


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

class Stop(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0

    def enterState(self):
        print("Enter Stop state")
        self.manager.motion.coastBrake()

    def run(self):
        timestamp = time.time()
        if (timestamp - self.timestamp) > 0.4:
            print("run stop state")
            self.timestamp = timestamp

class ManualControl(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        self.typerun = "S"
        self.speed = 0.5

    def enterState(self):
        print("Enter Manual Control state")
        self.runManualControl()

    def setSpeed(self, speed):
        self.speed = speed

    def setManualControl(self, typerun):
        self.typerun = typerun

    def runManualControl(self):
        if self.typerun == "S":
            self.manager.motion.dynamicBrake()
        elif self.typerun == "F":
            self.manager.motion.forward(self.speed)
        elif self.typerun == "B":
            self.manager.motion.backward(self.speed)
        elif self.typerun == "L":
            self.manager.motion.turnLeft(self.speed)
        elif self.typerun == "R":
            self.manager.motion.turnRight(self.speed)

    def run(self):
        timestamp = time.time()
        if (timestamp - self.timestamp) > 0.4:
            print("run manual control state")
            self.runManualControl()
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
    state = "INIT"
    def __init__(self):
        Thread.__init__(self)
        IOcom = Thread(name='IOcom', target=self.IOthread)
        CANcom = Thread(name='CANcom', target=self.CANthread)
        testthread = Thread(name='testhread', target=self.MQTTthread)
        #MQTTpol = Thread(name="MQTTpol", target=self.MQTTpol)
        self.runstate = Run(self)
        self.breakstate = Break(self)
        self.stopstate = Stop(self)
        self.manualcontrol = ManualControl(self)
        self.nextState(self.stopstate)
        testthread.setDaemon(True)
        IOcom.setDaemon(True)
        CANcom.setDaemon(True)
        #MQTTpol.setDaemon(True)
        testthread.start()
        IOcom.start()
        CANcom.start()
        #MQTTpol.start()
        client.connect("localhost", 1883, 60)

    def testThread(self):
        while True:
            print("run testthread");
            time.sleep(1)

    def MQTTpol(self):
        while True:
            print("MQTTpol thread")
            #client.loop_forever()
            time.sleep(0.04)

    def IOthread(self):
        while True:
            ts = time.time()
            self.perimeterValue = self.ioController.readPerimeterAvg()
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
            #self.leftMotorDistance = self.motion.getDistanceLeft()
            #self.rightMotorDistance = self.motion.getDistanceRight()
            ta = time.time()
            #print("CAN thread")
            time.sleep(0.01)
            #print(ta - ts)

    def MQTTthread(self):
        while True:
            ts = time.time()
            x = {}
            x["lmCurrent"] = "%.2f" % self.leftMotorCurrent
            x["rmCurrent"] = "%.2f" % self.rightMotorCurrent
            x["lmSpeed"] = "%.2f" % self.leftMotorSpeed
            x["rmSpeed"] = "%.2f" % self.rightMotorSpeed
            x["lmDistance"] = self.leftMotorDistance
            x["rmDistance"] = self.rightMotorDistance
            x["lPressure"] = self.pressureSensorLeft
            x["rPressure"] = self.pressureSensorRight
            x["bVoltage"] = self.batteryVoltage
            x["bCurrent"] = self.batteryCurrent
            x["bPower"] = self.batteryPower
            x["perimeter"] = self.perimeterValue
            y = json.dumps(x)
            client.publish("diagnostics", y)
            ta = time.time()
            time.sleep(0.1)
            #print("MQTT thread")
            #print(ta -ts)

    def nextState(self, state):
        self.state = state
        self.state.enterState()

    def runStatemachine(self):
        self.state.run()
        #self.client.loop()


    def stop(self):
        self.motion.coastBrake()
