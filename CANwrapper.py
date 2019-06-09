from CANdriver import CANdriver
import time
import signal

class CANwrapper:
    TIMEOUT = 50
    def __init__(self):
        self.candriver = CANdriver()
        self.candriver.deamon = True
        self.candriver.start()

    def raise_timeout(signum, frame):
        raise TimeoutError

    def cBrake1(self):
        self.candriver.coastBrake(1)
        counter = 0
        while 0 == self.candriver.getCBRAKE1() and counter < self.TIMEOUT:
            time.sleep(0.00001)
            counter += 1
        return self.candriver.getCBRAKE1()

    def cBrake2(self):
        self.candriver.coastBrake(2)
        counter = 0
        while 0 == self.candriver.getCBRAKE2() and counter < self.TIMEOUT:
            time.sleep(0.00001)
            counter += 1
        return self.candriver.getCBRAKE2()

    def dBrake1(self):
        self.candriver.dynamicBrake(1)
        counter = 0
        while 0 == self.candriver.getDBRAKE1() and counter < self.TIMEOUT:
            time.sleep(0.00001)
            counter += 1
        return self.candriver.getDBRAKE1()

    def dBrake2(self):
        self.candriver.dynamicBrake(2)
        counter = 0
        while 0 == self.candriver.getDBRAKE2() and counter < self.TIMEOUT:
            time.sleep(0.00001)
            counter += 1
        return self.candriver.getDBRAKE2()

    def drive1(self, speed, direction):
        self.candriver.drive(1, speed, direction)
        counter = 0
        while 0 == self.candriver.getACKCS1() and counter < self.TIMEOUT:
            time.sleep(0.00001)
            counter += 1
        return self.candriver.getACKCS1()

    def drive2(self, speed, direction):
        self.candriver.drive(2, speed, direction)
        counter = 0
        while 0 == self.candriver.getACKCS2() and counter < self.TIMEOUT:
            time.sleep(0.00001)
            counter += 1
        return self.candriver.getACKCS2()

    def getCurrent1(self):
        self.candriver.readCurrent(1)
        counter = 0
        while -1 == self.candriver.getCURRENT1() and counter < self.TIMEOUT:
            time.sleep(0.00001)
            counter += 1
        return self.candriver.getCURRENT1()

    def getCurrent2(self):
        self.candriver.readCurrent(2)
        counter = 0
        while -1 == self.candriver.getCURRENT2() and counter < self.TIMEOUT:
            time.sleep(0.00001)
            counter += 1
        return self.candriver.getCURRENT2()

    def getSpeed1(self):
        self.candriver.readSpeed(1)
        counter = 0
        while -1 == self.candriver.getSPEED1() and counter < self.TIMEOUT:
            time.sleep(0.00001)
            counter += 1
        return self.candriver.getSPEED1()

    def getSpeed2(self):
        self.candriver.readSpeed(2)
        counter = 0
        while -1 == self.candriver.getSPEED2() and counter < self.TIMEOUT:
            time.sleep(0.00001)
            counter += 1
        return self.candriver.getSPEED2()

    def getAWatchdog1(self):
        return self.candriver.WATCHDOG1

    def getAWatchdog2(self):
        return self.candriver.WATCHDOG2

    def getDistance1(self):
        self.candriver.readDistance(1)
        counter = 0
        while -1 == self.candriver.getDISTANCE1() and counter < self.TIMEOUT:
            time.sleep(0.00001)
            counter += 1
        return self.candriver.getDISTANCE1()

    def getDistance2(self):
        self.candriver.readDistance(2)
        counter = 0
        while -1 == self.candriver.getDISTANCE2() and counter < self.TIMEOUT:
            time.sleep(0.00001)
            counter += 1
        return self.candriver.getDISTANCE2()