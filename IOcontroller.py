import smbus
import time

SLAVE_ADDRESS = 0x08

class IOcontroller:
    def __init__(self):
        self.bus = smbus.SMBus(1)

    def readDistanceSensor1(self):
        block = self.readDataWithRetry(2)
        distance = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
        return distance

    def readDistanceSensor2(self):
        block = self.readDataWithRetry(3)
        distance = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
        return distance

    def readDistanceSensor3(self):
        block = self.readDataWithRetry(4)
        distance = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
        return distance

    def readDistanceSensor4(self):
        block = self.readDataWithRetry(5)
        distance = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
        return distance

    def readPerimeterLeft(self):
        block = self.readDataWithRetry(8)
        distance = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
        return distance

    def readPerimeterRight(self):
        block = self.readDataWithRetry(9)
        distance = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
        return distance

    def readPresureSensorLeft(self):
        block = self.readDataWithRetry(6)
        distance = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
        return distance

    def readPresureSensorRight(self):
        block = self.readDataWithRetry(7)
        distance = -1
        if block != None:
            distance = block[0] + (block[1] << 8)
        return distance

    def readData(self, CMD):
        try:
            # block = bus.write_byte(SLAVE_ADDRESS, 1023)
            block = self.bus.read_i2c_block_data((SLAVE_ADDRESS), CMD, 2)
            return block
        except Exception as e:
            time.sleep(0.000001)
            #print("Fout tijdens het zenden van i2c commando: " + str(CMD))
            #print(e)

    def readDataWithRetry(self, CMD):
        block = None
        timeout = 0
        while block == None and timeout < 5:
            block = self.readData(CMD)
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