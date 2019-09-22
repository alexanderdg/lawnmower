from CANwrapper import CANwrapper
import math
import time

DIAMETER_WHEEL = 120
ENCODER_COUNTS_PER_REVOLUTION = 3591.84

class MotionController:
    def __init__(self):
        self.canwrapper = CANwrapper()
        radiusWheel = DIAMETER_WHEEL / 2000.0
        self.perimeterWheel = 2 * math.pi * radiusWheel

    def driveDistanceLeft(self):
        self.canwrapper.driveDistance1(10000,50,1)

    def driveDistanceRight(self):
        self.canwrapper.driveDistance2(10000, 50, 1)

    def turn90Left(self):
        self.canwrapper.driveDistance1(530, 75, 0)
        self.canwrapper.driveDistance2(530, 75, 0)

    def turn90Right(self):
        self.canwrapper.driveDistance1(530, 75, 1)
        self.canwrapper.driveDistance2(530, 75, 1)

    def turnLeft(self, speedMS):
        CPMS = self.MStoCPMSconverter(speedMS)
        result = 0
        if self.canwrapper.drive1(CPMS, 0) != -1 and self.canwrapper.drive2(CPMS, 0) != -1:
            result = 1
        return result

    def turnRight(self, speedMS):
        CPMS = self.MStoCPMSconverter(speedMS)
        result = 0
        if self.canwrapper.drive1(CPMS, 1) != -1 and self.canwrapper.drive2(CPMS, 1) != -1:
            result = 1
        return result

    def forward(self, speedMS):
        CPMS = self.MStoCPMSconverter(speedMS)
        result = 0
        if self.canwrapper.drive1(CPMS, 1) != -1 and self.canwrapper.drive2(CPMS, 0) != -1:
            result = 1
        return result

    def backward(self, speedMS):
        CPMS = self.MStoCPMSconverter(speedMS)
        result = 0
        if self.canwrapper.drive1(CPMS, 0) != -1 and self.canwrapper.drive2(CPMS, 1) != -1:
            result = 1
        return result

    def getLeftSpeed(self):
        returnValue = -1
        timeout = 0
        while returnValue == -1 and timeout < 5:
            returnValue = self.canwrapper.getSpeed1()
            timeout += 1
        return self.CPMStoMSconverter(returnValue)


    def getRightSpeed(self):
        returnValue = -1
        timeout = 0
        while returnValue == -1 and timeout < 5:
            returnValue = self.canwrapper.getSpeed2()
            timeout += 1
        return self.CPMStoMSconverter(returnValue)

    def getLeftCurrent(self):
        returnValue = -1
        timeout = 0
        while returnValue == -1 and timeout < 5:
            returnValue = self.canwrapper.getCurrent1()
            timeout += 1
        if returnValue < 0.03:
            returnValue = 0
        return returnValue

    def getRightCurrent(self):
        returnValue = -1
        timeout = 0
        while returnValue == -1 and timeout < 5:
            returnValue = self.canwrapper.getCurrent2()
            timeout += 1
        if returnValue < 0.03:
            returnValue = 0
        return returnValue

    def getLeftCurrentWatchdog(self):
        return self.canwrapper.getAWatchdog1()

    def getRightCurrentWatchdog(self):
        return self.canwrapper.getAWatchdog2()

    def reverse(self, speedMS):
        CPMS = self.MStoCPMSconverter(speedMS)
        result = 0
        if self.canwrapper.drive1(CPMS, 0) != -1 and self.canwrapper.drive2(CPMS, 1) != -1:
            result = 1
        return result

    def dynamicBrake(self):
        self.canwrapper.dBrake1()
        self.canwrapper.dBrake2()

    def coastBrake(self):
        self.canwrapper.cBrake1()
        self.canwrapper.cBrake2()

    def MStoCPMSconverter(self, speedS):
        RPS = speedS / self.perimeterWheel
        CountEncoder = RPS * (ENCODER_COUNTS_PER_REVOLUTION/4)
        return int(CountEncoder/10)

    def CPMStoMSconverter(self, countMS):
        countS = countMS * 10
        RPS = countS / (ENCODER_COUNTS_PER_REVOLUTION/4)
        speedS = RPS * self.perimeterWheel
        return speedS

    def getDistanceLeft(self):
        return self.canwrapper.getDistance1()

    def getDistanceRight(self):
        return self.canwrapper.getDistance2()

    def selfTest(self):
        diagnostics = 9
        oldDistanceLeft = self.getDistanceLeft()
        oldDistanceRight = self.getDistanceRight()
        self.turnLeft(0.3)
        time.sleep(0.5)
        currentLeft = self.getLeftCurrent()
        currentRight = self.getRightCurrent()
        newDistanceLeft = self.getDistanceLeft()
        newDistanceRight = self.getDistanceRight()
        self.coastBrake()
        if currentLeft < 0.05:
            diagnostics = 1
            print("Linker motor is niet aangesloten")
        elif currentRight < 0.05:
            diagnostics = 2
            print("Rechter motor is niet aangesloten")
        elif newDistanceLeft - oldDistanceLeft < 10:
            diagnostics = 3
            print("Encoder van de linker motor werkt niet")
        elif newDistanceRight - oldDistanceRight < 10:
            diagnostics = 4
            print("Encoder van de rechter motor werkt niet")
        else:
            diagnostics = 0
            print("Selftest van de motoren was in orde")
        return diagnostics


    def printDiagnostics(self):
        value = self.getRightCurrent()
        value2 = self.getRightSpeed()
        value3 = self.getRightCurrentWatchdog()
        value4 = self.canwrapper.getDistance2()
        value5 = self.getLeftCurrent()
        value6 = self.getLeftSpeed()
        value7 = self.getLeftCurrentWatchdog()
        value8 = self.canwrapper.getDistance1()
        print("Printed current 1: %.2f 2: %.2f" % (value5, value))
        print("Printed speed 1: %.2f 2: %.2f" % (value6, value2))
        print("Printed watchdog 1: ", value7, " 2: ", value3)
        #print("Printed distance 1: ", value8, " 2: ", value4)