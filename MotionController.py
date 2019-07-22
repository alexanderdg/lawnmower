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
        if self.canwrapper.drive1(CPMS, 1) != -1 and self.canwrapper.drive2(CPMS, 1) != -1:
            result = 1
        return result

    def dynamicBrake(self):
        self.canwrapper.dBrake1()
        self.canwrapper.dBrake2()

    def MStoCPMSconverter(self, speedS):
        RPS = speedS / self.perimeterWheel
        CountEncoder = RPS * (3591.84/4)
        return int(CountEncoder/10)

    def printDiagnostics(self):
        value = self.canwrapper.getCurrent2()
        value2 = self.canwrapper.getSpeed2()
        value3 = self.canwrapper.getAWatchdog2()
        value4 = self.canwrapper.getDistance2()
        value5 = self.canwrapper.getCurrent1()
        value6 = self.canwrapper.getSpeed1()
        value7 = self.canwrapper.getAWatchdog1()
        value8 = self.canwrapper.getDistance1()
        #if(value7 == 1 or value8 == 1):
        #    self.dynamicBrake()
        #    time.sleep(2)
        #else:
        #    self.turnLeft(0.5)
        print("Printed current 1: %.2f 2: %.2f" % (value5, value))
        print("Printed speed 1: ", value6, " 2: ", value2)
        print("Printed watchdog 1: ", value7, " 2: ", value3)
        print("Printed distance 1: ", value8, " 2: ", value4)