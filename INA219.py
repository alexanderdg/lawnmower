#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.002
MAX_EXPECTED_AMPS = 10


def read():
    ina = INA219(shunt_ohms=SHUNT_OHMS, address=0x45, max_expected_amps=MAX_EXPECTED_AMPS)
    ina.configure()

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resister
        print(e)


if __name__ == "__main__":
    read()
