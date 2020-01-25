import smbus
import time

SLAVE_ADDRESS = 0x08

class IOcontroller:
    avgPressureLeft = 0
    avgPressureRight = 0
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.avgPressureLeft = self.readPresureSensorLeft()
        self.avgPressureRight = self.readPresureSensorRight()

    def readDistanceSensor1(self):
        block = self.readDataWithRetry(2, 2)
        distance = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
        return distance

    def readDistanceSensor2(self):
        block = self.readDataWithRetry(3, 2)
        distance = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
        return distance

    def readDistanceSensor3(self):
        block = self.readDataWithRetry(4, 2)
        distance = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
        return distance

    def readDistanceSensor4(self):
        block = self.readDataWithRetry(5, 2)
        distance = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
        return distance

    def readPerimeterAvg(self):
        block = self.readDataWithRetry(8, 2)
        value = -1
        if block != None:
            value = block[0] + (block[1] << 8)
        return value

    def readPerimeterMagn(self):
        block = self.readDataWithRetry(8, 3)
        value = -1
        if block != None:
            value = block[0] + (block[1] << 8)
            if block[2] != 1:
                value = value * -1
        return value

    def readPresureSensorRight(self):
        block = self.readDataWithRetry(6, 2)
        returnValue = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
            self.avgPressureRight = 0.99 * self.avgPressureRight + 0.01 * distance
            returnValue = int(distance - self.avgPressureRight)
        return returnValue

    def readPresureSensorLeft(self):
        block = self.readDataWithRetry(7, 2)
        returnValue = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
            self.avgPressureLeft = 0.99 * self.avgPressureLeft + 0.01 * distance
            returnValue = int(distance - self.avgPressureLeft)
        return returnValue

    def selfTest(self):
        diagnostics = 9
        if self.readPresureSensorLeft() > 0 and self.readPresureSensorRight() > 0:
            diagnostics = 0
            print("IO controller is in orde")
        return diagnostics

    def readData(self, CMD, bytes):
        try:
            # block = bus.write_byte(SLAVE_ADDRESS, 1023)
            block = self.bus.read_i2c_block_data((SLAVE_ADDRESS), CMD, bytes)
            return block
        except Exception as e:
            time.sleep(0.000001)
            #print("Fout tijdens het zenden van i2c commando: " + str(CMD))
            #print(e)

    def readDataWithRetry(self, CMD, bytes):
        block = None
        timeout = 0
        while (block == None or (block[0] == 255) and block[1] == 255) and timeout < 5:
            block = self.readData(CMD, bytes)
            timeout += 1
        return block

    def setLed(self, red, green, blue):
        ledvalues = [red, green, blue]
        try:
            # block = bus.write_byte(SLAVE_ADDRESS, 1023)
            block = self.bus.write_i2c_block_data((SLAVE_ADDRESS), 1, ledvalues)
            return block
        except Exception as e:
            time.sleep(0.000001)
            #print("Fout tijdens het zenden van i2c commando: " + str(1))
            #print(e)