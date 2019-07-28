import smbus

SLAVE_ADDRESS = 0x08

class IOcontroller:
    def __init__(self):
        self.bus = smbus.SMBus(1)

    def readDistanceSensor1(self):
        block = self.readData(2)
        distance = block[0] + (block[1] << 8)
        return distance

    def readDistanceSensor2(self):
        block = self.readData(3)
        distance = block[0] + (block[1] << 8)
        return distance

    def readDistanceSensor3(self):
        block = self.readData(4)
        distance = block[0] + (block[1] << 8)
        return distance

    def readDistanceSensor4(self):
        block = self.readData(5)
        distance = block[0] + (block[1] << 8)
        return distance

    def readPerimeterLeft(self):
        block = self.readData(8)
        distance = block[0] + (block[1] << 8)
        return distance

    def readPerimeterRight(self):
        block = self.readData(9)
        distance = block[0] + (block[1] << 8)
        return distance

    def readPresureSensorLeft(self):
        block = self.readData(6)
        distance = block[0] + (block[1] << 8)
        return distance

    def readPresureSensorRight(self):
        block = self.readData(7)
        distance = block[0] + (block[1] << 8)
        return distance

    def readData(self, CMD):
        try:
            # block = bus.write_byte(SLAVE_ADDRESS, 1023)
            block = self.bus.read_i2c_block_data((SLAVE_ADDRESS), CMD, 2)
            return block
        except:
            print("Fout tijdens het zenden van i2c commando")