#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.002
MAX_EXPECTED_AMPS = 10

class Battery:
    def __init__(self):
        self.ina = INA219(shunt_ohms=SHUNT_OHMS, address=0x45, max_expected_amps=MAX_EXPECTED_AMPS)
        self.ina.configure()

    def readCurrent(self):
        current = "-1"
        try:
            current = "{:.2f}".format(self.ina.current() / 1000.0)
        except DeviceRangeError as e:
            print(e)
        return current

    def readVoltage(self):
        voltage = "-1"
        try:
            voltage = "{:.2f}".format(self.ina.voltage())
        except Exception as e:
            print(e)
        return voltage

    def readPower(self):
        power = "-1"
        try:
            power = "{:.2f}".format(self.ina.power() / 1000.0)
        except Exception as e:
            print(e)
        return power

    def selfTest(self):
        diagnostics = 9
        if self.readPower() != -1:
            diagnostics = 0
            print("INA219 is in orde")
        return diagnostics