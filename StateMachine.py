import paho.mqtt.client as mqtt
import json
from statemachine import StateMachine, State
from IOcontroller import IOcontroller
from MotionController import MotionController
from INA219 import Battery
from Perimeter import Perimeter
from threading import Thread
import time
import os

client = mqtt.Client()


class Run(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        #print("init start state")

    def enterState(self):
        print("Enter Run state")
        self.manager.status = "Lawnmower is mowing the lawn"
        self.manager.ioController.setLed(0, 100, 0)



    def run(self):
        timestamp = time.time()
        if (timestamp - self.timestamp) > 0.4:
            print("run run state")
            self.manager.motion.forward(0.5)
            self.timestamp = timestamp
        if (self.manager.motion.getRightCurrent() > 1.2
            or self.manager.pressureSensorRight > 5
            or self.manager.perimeterValue > 500):
            self.manager.nextState(self.manager.TryLeftState)
        if (self.manager.motion.getLeftCurrent() > 1.2
            or self.manager.pressureSensorLeft > 5):
            self.manager.nextState(self.manager.TryRightState)
        elif abs(self.manager.perimeterValue) > 120:
            self.manager.nextState(self.manager.runslow)

class RunSlow(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        #print("init start state")

    def enterState(self):
        print("Enter Run Slow state")
        self.manager.status = "Ride slow by the obstacle"
        self.manager.ioController.setLed(100, 50, 0)

    def run(self):
        timestamp = time.time()
        if (timestamp - self.timestamp) > 0.4:
            print("run run slow state")
            self.manager.motion.forward(0.3)
            self.timestamp = timestamp

        if self.manager.motion.getLeftCurrent() > 1.2 or self.manager.motion.getRightCurrent() > 1.2 or self.manager.pressureSensorRight > 5 or self.manager.pressureSensorLeft > 5 or self.manager.perimeterValue > 300 or abs(self.manager.perimeterValue) > 500:
            self.manager.nextState(self.manager.TryLeftState)
        elif abs(self.manager.perimeterValue) < 120:
            self.manager.nextState(self.manager.runstate)

class TryLeft(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        self.original_timestamp = 0

    def enterState(self):
        print("Enter TryLeft state")
        self.manager.status = "Try to avoid right obstacle by turning left"
        self.manager.ioController.setLed(100, 0 ,0)
        self.original_timestamp = time.time()

    def run(self):
        timestamp = time.time()
        if (self.manager.pressureSensorLeft > 5
            or self.manager.pressureSensorRight > 5
            or self.manager.motion.getLeftCurrent() > 1.2
            or self.manager.motion.getRightCurrent() > 1.2
            or self.manager.perimeterValue > 500) and ((timestamp - self.original_timestamp) > 0.5):
            self.manager.nextState(self.manager.TryInsteadRightState)
        if (timestamp - self.timestamp) > 0.4:
            print("run TryLeft state")
            self.timestamp = timestamp
            if timestamp - self.original_timestamp < 3:
                self.manager.motion.dynamicBrake()
            elif timestamp - self.original_timestamp < 4:
                self.manager.motion.reverse(0.5)
            elif timestamp - self.original_timestamp < 4.5:
                self.manager.motion.coastBrake()
            elif timestamp - self.original_timestamp < 5:
                self.manager.motion.turn90Left()
            elif timestamp - self.original_timestamp > 8:
                self.manager.nextState(self.manager.runstate)


class TryRight(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        self.original_timestamp = 0

    def enterState(self):
        print("run TryRight state")
        self.manager.status = "Try to avoid left obstacle by turning right"
        self.manager.ioController.setLed(100, 0, 0)
        self.original_timestamp = time.time()

    def run(self):
        timestamp = time.time()
        if (self.manager.pressureSensorLeft > 5
            or self.manager.pressureSensorRight > 5
            or self.manager.motion.getLeftCurrent() > 1.2
            or self.manager.motion.getRightCurrent() > 1.2
            or self.manager.perimeterValue > 500)and ((timestamp - self.original_timestamp) > 0.5):
            self.manager.nextState(self.manager.TryInsteadLeftState)
        if (timestamp - self.timestamp) > 0.4:
            print("run TryRight state")
            self.timestamp = timestamp
            if timestamp - self.original_timestamp < 3:
                self.manager.motion.dynamicBrake()
            elif timestamp - self.original_timestamp < 4:
                self.manager.motion.reverse(0.5)
            elif timestamp - self.original_timestamp < 4.5:
                self.manager.motion.coastBrake()
            elif timestamp - self.original_timestamp < 5:
                self.manager.motion.turn90Right()
            elif timestamp - self.original_timestamp > 8:
                self.manager.nextState(self.manager.runstate)


class TryInsteadLeft(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        self.original_timestamp = 0

    def enterState(self):
        print("run TryInsteadLeft state")
        self.manager.status = "Try to instead avoid obstacle by left"
        self.manager.ioController.setLed(255, 0, 0)
        self.original_timestamp = time.time()

    def run(self):
        timestamp = time.time()
        if (self.manager.pressureSensorLeft > 5
            or self.manager.pressureSensorRight > 5
            or self.manager.motion.getLeftCurrent() > 1.2
            or self.manager.motion.getRightCurrent() > 1.2
            or self.manager.perimeterValue > 500)and ((timestamp - self.original_timestamp) > 0.5):
            self.manager.nextState(self.manager.TryBackwardState)
        if (timestamp - self.timestamp) > 0.4:
            print("run TryInsteadLeft state")
            self.timestamp = timestamp
            if timestamp - self.original_timestamp < 3:
                self.manager.motion.dynamicBrake()
            elif timestamp - self.original_timestamp < 4:
                self.manager.motion.reverse(0.5)
            elif timestamp - self.original_timestamp < 4.5:
                self.manager.motion.coastBrake()
            elif timestamp - self.original_timestamp < 5:
                self.manager.motion.turn90Left()
            elif timestamp - self.original_timestamp > 8:
                self.manager.nextState(self.manager.runstate)

class TryInsteadRight(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        self.original_timestamp = 0

    def enterState(self):
        print("run TryInsteadRight state")
        self.manager.status = "Try to instead avoid obstacle by right"
        self.manager.ioController.setLed(255,0,0)
        self.original_timestamp = time.time()

    def run(self):
        timestamp = time.time()
        if (self.manager.pressureSensorLeft > 5
            or self.manager.pressureSensorRight > 5
            or self.manager.motion.getLeftCurrent() > 1.2
            or self.manager.motion.getRightCurrent() > 1.2
            or self.manager.perimeterValue > 500)and ((timestamp - self.original_timestamp) > 0.5):
            self.manager.nextState(self.manager.TryBackwardState)
        if (timestamp - self.timestamp) > 0.4:
            print("run TryInsteadRight state")
            self.timestamp = timestamp
            if timestamp - self.original_timestamp < 3:
                self.manager.motion.dynamicBrake()
            elif timestamp - self.original_timestamp < 4:
                self.manager.motion.reverse(0.5)
            elif timestamp - self.original_timestamp < 4.5:
                self.manager.motion.coastBrake()
            elif timestamp - self.original_timestamp < 5:
                self.manager.motion.turn90Right()
            elif timestamp - self.original_timestamp > 8:
                self.manager.nextState(self.manager.runstate)

class TryBackward(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        self.original_timestamp = 0

    def enterState(self):
        print("run TryBackward State")
        self.manager.status = "Try to avoid obstacle by riding backwards"
        self.manager.ioController.setLed(255, 0, 0)
        self.original_timestamp = time.time()

    def run(self):
        timestamp = time.time()
        if (self.manager.pressureSensorLeft > 5
            or self.manager.pressureSensorRight > 5
            or self.manager.motion.getLeftCurrent() > 1.2
            or self.manager.motion.getRightCurrent() > 1.2
            or self.manager.perimeterValue > 500) and ((timestamp - self.original_timestamp) > 0.5):
            self.manager.nextState(self.manager.stuck)
        if (timestamp - self.timestamp) > 0.4:
            print("run TryInsteadRight state")
            self.timestamp = timestamp
            if timestamp - self.original_timestamp < 3:
                self.manager.motion.dynamicBrake()
            elif timestamp - self.original_timestamp < 8:
                self.manager.motion.backward(0.5)
            elif timestamp - self.original_timestamp >= 8:
                self.manager.nextState(self.manager.runstate)


class TryLastTimeRight(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        self.original_timestamp = 0
        #print("init start state")

    def enterState(self):
        print("Enter Break Right state")
        self.manager.status = "Avoid obstacle by turning right"
        self.manager.ioController.setLed(100, 0, 0)
        self.original_timestamp = time.time()

    def run(self):
        timestamp = time.time()
        if (timestamp - self.original_timestamp > 1) and (self.manager.motion.getLeftCurrent() > 1.2 or self.manager.motion.getRightCurrent() > 1.2 or self.manager.pressureSensorRight > 5 or self.manager.pressureSensorLeft > 5):
            self.manager.motion.dynamicBrake()
            self.manager.nextState(self.manager.stuck)
        if (timestamp - self.timestamp) > 0.4:
            if timestamp - self.original_timestamp < 3:
                self.manager.motion.dynamicBrake()
            elif timestamp - self.original_timestamp < 4:
                self.manager.motion.reverse(0.5)
            elif timestamp - self.original_timestamp < 4.5:
                self.manager.motion.coastBrake()
            elif timestamp - self.original_timestamp < 5:
                self.manager.motion.turn90Right()
            elif timestamp - self.original_timestamp > 8:
                self.manager.nextState(self.manager.runstate)
            print("run break right state")
            self.timestamp = timestamp

class TryLastTimeLeft(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        self.original_timestamp = 0
        #print("init start state")

    def enterState(self):
        print("Enter Break Left state")
        self.manager.status = "Avoid obstacle by turning left"
        self.manager.ioController.setLed(100, 0, 0)
        self.original_timestamp = time.time()

    def run(self):
        timestamp = time.time()
        if (timestamp - self.original_timestamp > 1) and (self.manager.motion.getLeftCurrent() > 1.2 or self.manager.motion.getRightCurrent() > 1.2 or self.manager.pressureSensorRight > 5 or self.manager.pressureSensorLeft > 5):
            self.manager.motion.dynamicBrake()
            self.manager.nextState(self.manager.stuck)
        if (timestamp - self.timestamp) > 0.4:
            if timestamp - self.original_timestamp < 1:
                self.manager.motion.dynamicBrake()
            elif timestamp - self.original_timestamp < 2.5:
                self.manager.motion.coastBrake()
            elif timestamp - self.original_timestamp < 3:
                self.manager.motion.turn90Left()
            elif timestamp - self.original_timestamp > 6:
                self.manager.nextState(self.manager.runstate)
            print("run break left state")
            self.timestamp = timestamp

class Stop(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0

    def enterState(self):
        print("Enter Stop state")
        self.manager.status = "Lawnmower routine is stopped"
        self.manager.ioController.setLed(0, 0, 100)
        self.manager.motion.coastBrake()

    def run(self):
        timestamp = time.time()
        if (timestamp - self.timestamp) > 0.4:
            print("run stop state")
            self.timestamp = timestamp

class Stuck(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0

    def enterState(self):
        print("Enter Stuck state")
        self.manager.status = "Lawnmower is blocked"
        self.manager.ioController.setLed(0, 0, 0)
        os.system("mpg123 /share/Sourcecode/lawnmower/WAV\ files/stuck.mp3")
        self.manager.motion.coastBrake()

    def run(self):
        timestamp = time.time()
        if (timestamp - self.timestamp) > 10:
            print("run stuck state")
            os.system("mpg123 /share/Sourcecode/lawnmower/WAV\ files/stuck.mp3")
            self.timestamp = timestamp

class ManualControl(object):
    def __init__(self, manager):
        self.manager = manager
        self.timestamp = 0
        self.typerun = "S"
        self.speed = 0.5

    def enterState(self):
        print("Enter Manual Control state")
        self.manager.status = "Manual control is activated"
        self.manager.ioController.setLed(0, 0, 0)
        self.runManualControl()

    def setSpeed(self, speed):
        self.speed = speed

    def getSpeed(self):
        return self.speed

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
    periCurrent = ""
    periFault = ""
    periStatus = ""
    motion = MotionController()
    ioController = IOcontroller()
    battery = Battery()
    peri = Perimeter()
    status = ""
    state = "INIT"
    def __init__(self):
        Thread.__init__(self)
        IOcom = Thread(name='IOcom', target=self.IOthread)
        CANcom = Thread(name='CANcom', target=self.CANthread)
        testthread = Thread(name='testhread', target=self.MQTTthread)
        periThread = Thread(name='periThread', target=self.periThread)
        #MQTTpol = Thread(name="MQTTpol", target=self.MQTTpol)
        self.runstate = Run(self)
        self.TryLeftState = TryLeft(self)
        self.TryRightState = TryRight(self)
        self.TryInsteadLeftState = TryInsteadLeft(self)
        self.TryInsteadRightState = TryInsteadRight(self)
        self.TryLastTimeRightState = TryLastTimeRight(self)
        self.TryLastTimeLeftState = TryLastTimeLeft(self)
        self.TryBackwardState = TryBackward(self)
        self.stuck = Stuck(self)
        self.stopstate = Stop(self)
        self.manualcontrol = ManualControl(self)
        self.runslow = RunSlow(self)
        self.nextState(self.stopstate)
        self.status = "wait to be started"
        testthread.setDaemon(True)
        IOcom.setDaemon(True)
        CANcom.setDaemon(True)
        periThread.setDaemon(True)
        #MQTTpol.setDaemon(True)
        testthread.start()
        IOcom.start()
        CANcom.start()
        periThread.start()
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
            #self.leftMotorDistance = self.motion.getDistanceLeft()
            #self.rightMotorDistance = self.motion.getDistanceRight()
            ta = time.time()
            #print("CAN thread")
            time.sleep(0.02)
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
            x["distance1"] = self.distance1
            x["distance2"] = self.distance2
            x["distance3"] = self.distance3
            x["distance4"] = self.distance4
            x["status"] = self.status
            x["periCurrent"] = self.periCurrent
            x["periStatus"] = self.periStatus
            x["periFault"] = self.periFault
            y = json.dumps(x)
            client.publish("diagnostics", y)
            ta = time.time()
            time.sleep(0.1)
            #print("MQTT thread")
            #print(ta -ts)

    def periThread(self):
        while True:
                value, self.periCurrent, self.periFault, self.periStatus = self.peri.askForStatus()
                if value != 1:
                    if self.state == self.runstate:
                        os.system("mpg123 /share/Sourcecode/lawnmower/WAV\ files/ConnectionPerimeterLost.mp3")
                        self.nextState(self.stopstate)
                elif float(self.periCurrent) < 0.00:
                    if self.state == self.runstate:
                        os.system("mpg123 /share/Sourcecode/lawnmower/WAV\ files/PerimeterWireBroken.mp3")
                        self.nextState(self.stopstate)
                time.sleep(5)

    def nextState(self, state):
        self.state = state
        self.state.enterState()

    def runStatemachine(self):
        self.state.run()
        #self.client.loop()


    def stop(self):
        self.motion.coastBrake()
