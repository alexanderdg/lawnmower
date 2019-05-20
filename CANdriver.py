import can

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


class CANdriver:
    def __init__(self):
        self.ACK_DRIVE_1 = 0
        self.ACK_DRIVE_2 = 0
        self.ACK_CBRAKE_1 = 0
        self.ACK_CBRAKE_2 = 0
        self.ACK_DBRAKE_1 = 0
        self.ACK_DBRAKE_2 = 0
        self.ACK_SETCS1 = 0
        self.ACK_SETCS2 = 0
        self.CURRENT1 = 0.0
        self.CURRENT2 = 0.0
        self.SPEED1 = 0
        self.SPEED2 = 0
        self.ERRDRIVER1 = 0
        self.ERRDRIVER2 = 0
        self.bus = can.interface.Bus(channel=channel, bustype=bustype)

    def readCanBus(self):
        for message in self.bus:
            print(message)
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
                        print("Printed current : %.4f", self.CURRENT1)
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




    def drive(self, motorcontroller: object, speed: object, direction: object) -> object:
        msg = can.Message(arbitration_id=motorcontroller, data=[SET_CONTROLLED_SPEED, speed, direction, 0, 0, 0, 0, 0],
                          extended_id=False)
        self.bus.send(msg)
        if motorcontroller == 1:
            self.ACK_DRIVE_1 = 0
            self.ACK_DRIVE_2 = 0

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
            self.ACK_CURRENT_1 = 0
        elif motorcontroller == 2:
            self.ACK_CURRENT_2 = 0