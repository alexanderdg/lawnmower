import can
import time
from threading import Thread

bustype = 'socketcan'
channel = 'can0'
COAST_BRAKE = 0
DYNAMIC_BRAKE = 1
SET_CONTROLLED_SPEED = 2
GET_HALL_SENSOR = 3
GET_CURRENT = 4
ERR_MOSFETDRIVER = 5
SET_CURRENT_TRESHHOLD = 6
ANALOG_WATCHDOG = 7
SET_CONTROLLED_DISTANCE = 8
GET_HALL_COUNT = 9
RESET_HALL_COUNT = 10
RUN_DIAGNOSTICS = 11


class CANdriver(Thread):
    ACK_DRIVE_1 = 0
    ACK_DRIVE_2 = 0
    ACK_CBRAKE_1 = 0
    ACK_CBRAKE_2 = 0
    ACK_DBRAKE_1 = 0
    ACK_DBRAKE_2 = 0
    ACK_SETCS1 = 0
    ACK_SETCS2 = 0
    CURRENT1 = 0.0
    CURRENT2 = 0.0
    SPEED1 = 0
    SPEED2 = 0
    ERRDRIVER1 = 0
    ERRDRIVER2 = 0
    WATCHDOG1 = 0
    WATCHDOG2 = 0
    status_setDistance1 = 0
    status_setDistance2 = 0
    driveDistance1 = 0
    driveDistance2 = 0
    statusDriveDistance1 = 0
    statusDriveDistance2 = 0

    def __init__(self):
        Thread.__init__(self)
        self.bus = can.interface.Bus(channel=channel, bustype=bustype)
        self.ACK_SETCS1 = 0

    def run(self):
        self.readCanBus()


    def readCanBus(self):
        for message in self.bus:
            try:
                if message.arbitration_id == 0:
                    if message.data[1] == COAST_BRAKE:
                        ack = message.data[2]
                        if message.data[0] == 1:
                            self.ACK_CBRAKE_1 = ack
                        elif message.data[0] == 2:
                            self.ACK_CBRAKE_2 = ack

                    elif message.data[1] == DYNAMIC_BRAKE:
                        ack = message.data[2]
                        if message.data[0] == 1:
                            self.ACK_DBRAKE_1 = ack
                        elif message.data[0] == 2:
                            self.ACK_DBRAKE_2 = ack

                    elif message.data[1] == SET_CONTROLLED_SPEED:
                        ack = message.data[2]
                        if message.data[0] == 1:
                            self.ACK_SETCS1 = ack
                        elif message.data[0] == 2:
                            self.ACK_SETCS2 = ack

                    elif message.data[1] == GET_CURRENT:
                        msbcurrent = message.data[2]
                        lsbcurrent = message.data[3]
                        dcurrent = (msbcurrent << 8) + lsbcurrent
                        if message.data[0] == 1:
                            self.CURRENT1 = dcurrent / 10000.0
                        elif message.data[0] == 2:
                            self.CURRENT2 = dcurrent / 10000.0

                    elif message.data[1] == GET_HALL_SENSOR:
                        speed = message.data[2]
                        if message.data[0] == 1:
                            self.SPEED1 = speed
                        elif message.data[0] == 2:
                            self.SPEED2 = speed

                    elif message.data[1] == ERR_MOSFETDRIVER:
                        error = message.data[2]
                        if message.data[0] == 1:
                            self.ERRDRIVER1 = error
                        elif message.data[0] == 2:
                            self.ERRDRIVER2 = error

                    elif message.data[1] == ANALOG_WATCHDOG:
                        watchdog = message.data[2]
                        if message.data[0] == 1:
                            self.WATCHDOG1 = watchdog
                        elif message.data[0] == 2:
                            self.WATCHDOG2 = watchdog

                    elif message.data[1] == SET_CONTROLLED_DISTANCE:
                        result = message.data[2]
                        if result == 2:
                            msbdistance = message.data[3]
                            lsbdistance = message.data[4]
                            distance = (msbdistance << 8) + lsbdistance
                            if message.data[0] == 1:
                                self.status_setDistance1 = distance
                            elif message.data[0] == 2:
                                self.status_setDistance2 = distance
                        elif result == 1 or result == 2:
                            if message.data[0] == 1:
                                self.status_setDistance1 = 0
                            elif message.data[0] == 2:
                                self.status_setDistance2 = 0

                    elif message.data[1] == GET_HALL_COUNT:
                        part = message.data[2]
                        if part == 0:
                            part1 = message.data[3]
                            part2 = message.data[4]
                            part3 = message.data[5]
                            part4 = message.data[6]
                            distance = part1 + (part2 << 8) + (part3 << 16) + (part4 << 24)
                            if message.data[0] == 1:
                                self.driveDistance1 = distance
                            elif message.data[0] == 2:
                                self.driveDistance2 = distance
                        elif part == 1:
                            if message.data[0] == 1:
                                self.statusDriveDistance1 = 1
                            elif message.data[0] == 2:
                                self.statusDriveDistance2 = 1
                time.sleep(0.0001)
            except Exception as e:
                print("Fout gebeurd tijdens het ontvangen van de CAN data")
                print(e)




    def drive(self, motorcontroller, speed, direction):
        msg = can.Message(arbitration_id=motorcontroller, data=[SET_CONTROLLED_SPEED, speed, direction, 0, 0, 0, 0, 0],
                          extended_id=False)
        self.bus.send(msg)
        if motorcontroller == 1:
            self.ACK_DRIVE_1 = 0
        elif motorcontroller == 2:
            self.ACK_DRIVE_2 = 0

    def driveDistance(self, motorcontroller, distance, speed, direction):
        distancelsb = distance & 0xFF
        distancemsb = (distance >> 8) & 0xFF
        msg = can.Message(arbitration_id=motorcontroller, data=[SET_CONTROLLED_DISTANCE, distancemsb, distancelsb, speed, direction, 0, 0, 0],
                          extended_id=False)
        self.bus.send(msg)
        if motorcontroller == 1:
            self.statusDriveDistance1 = 0
        elif motorcontroller == 2:
            self.statusDriveDistance2 = 0


    def dynamicBrake(self, motorcontroller):
        msg = can.Message(arbitration_id=motorcontroller, data=[DYNAMIC_BRAKE], extended_id=False)
        self.bus.send(msg)
        if motorcontroller == 1:
            self.ACK_DBRAKE_1 = 0
        elif motorcontroller == 2:
            self.ACK_DBRAKE_2 = 0

    def coastBrake(self, motorcontroller):
        msg = can.Message(arbitration_id=motorcontroller, data=[COAST_BRAKE], extended_id=False)
        self.bus.send(msg)
        if motorcontroller == 1:
            self.ACK_CBRAKE_1 = 0
        elif motorcontroller == 2:
            self.ACK_CBRAKE_2 = 0

    def readCurrent(self, motorcontroller):
        msg = can.Message(arbitration_id=motorcontroller, data=[GET_CURRENT], extended_id=False)
        self.bus.send(msg)
        if motorcontroller == 1:
            self.CURRENT1 = -1
        elif motorcontroller == 2:
            self.CURRENT2 = -1

    def readSpeed(self, motorcontroller):
        msg = can.Message(arbitration_id=motorcontroller, data=[GET_HALL_SENSOR], extended_id=False)
        self.bus.send(msg)
        if motorcontroller == 1:
            self.SPEED1 = -1
        elif motorcontroller == 2:
            self.SPEED2 = -1

    def readDistance(self, motorcontroller):
        msg = can.Message(arbitration_id=motorcontroller, data=[GET_HALL_COUNT], extended_id=False)
        self.bus.send(msg)
        if motorcontroller == 1:
            self.driveDistance1 = -1
        elif motorcontroller == 2:
            self.driveDistance2 = -1

    def getDISTANCE1(self):
        return self.driveDistance1

    def getDISTANCE2(self):
        return self.driveDistance2

    def getDBRAKE1(self):
        return self.ACK_DBRAKE_1

    def getDBRAKE2(self):
        return self.ACK_DBRAKE_2

    def getCBRAKE1(self):
        return self.ACK_CBRAKE_1

    def getCBRAKE2(self):
        return self.ACK_CBRAKE_2

    def getACKCS1(self):
        return self.ACK_SETCS1

    def getACKCS2(self):
        return self.ACK_SETCS2

    def getCURRENT1(self):
        return self.CURRENT1

    def getCURRENT2(self):
        return self.CURRENT2

    def getSPEED1(self):
        return self.SPEED1

    def getSPEED2(self):
        return self.SPEED2

    def getWATCHDOG1(self):
        return self.WATCHDOG1

    def getWATCHDOG2(self):
        return self.WATCHDOG2

    def getStatusDistance1(self):
        return self.statusDriveDistance1

    def getStatusDistance2(self):
        return self.statusDriveDistance2