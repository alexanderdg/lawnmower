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

    def getLeftSpeed(self):
        return self.CPMStoMSconverter(self.canwrapper.getSpeed1())

    def getRightSpeed(self):
        return self.CPMStoMSconverter(self.canwrapper.getSpeed1())

    def getLeftCurrent(self):
        return self.canwrapper.getCurrent1()

    def getRightCurrent(self):
        return self.canwrapper.getCurrent2()

    def getLeftCurrentWatchdog(self):
        return self.canwrapper.getAWatchdog1()

    def getRightCurrentWatchdog(self):
        return self.canwrapper.getAWatchdog2()

    def reverse(self, speedMS):
        CPMS = self.MStoCPMSconverter(speedMS)
        result = 0
        if self.canwrapper.drive1(CPMS, 0) != -1:
            result = 1
        return result

    def dynamicBrake(self):
        self.canwrapper.dBrake1()
        self.canwrapper.dBrake2()

    def MStoCPMSconverter(self, speedS):
        RPS = speedS / self.perimeterWheel
        CountEncoder = RPS * (ENCODER_COUNTS_PER_REVOLUTION/4)
        return int(CountEncoder/10)

    def CPMStoMSconverter(self, countMS):
        countS = countMS * 10
        RPS = countS / (ENCODER_COUNTS_PER_REVOLUTION/4)
        speedS = RPS * self.perimeterWheel
        return speedS

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
        print("Printed distance 1: ", value8, " 2: ", value4)