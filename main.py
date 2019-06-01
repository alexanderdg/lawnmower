from CANdriver import CANdriver
from CANwrapper import CANwrapper
import time
import threading
import signal
import can

bustype = 'socketcan'
channel = 'can0'


class CANwatcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #self.canwrapper = CANwrapper()
        self.shutdown_flag = threading.Event()

    def run(self):
        print('Thread #%s started' % self.ident)
        #result = self.canwrapper.drive1(100, 1)
        #print("return of drive function {}", result)
        while not self.shutdown_flag.is_set():
            time.sleep(1)
            # ... Clean shutdown code here ...
        print('Thread #%s stopped' % self.ident)


class ServiceExit(Exception):
    pass


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit


def main():
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    canwrapper = CANwrapper()
    print('Starting main program')
    try:
        #j1 = CANwatcher()
        #j1.start()

        result = canwrapper.drive2(100, 1)
        print("return of drive function {}", result)
        while True:
            value = canwrapper.getCurrent2()
            value2 = canwrapper.getSpeed2()
            value3 = canwrapper.getAWatchdog2()
            value4 = canwrapper.getDistance2()
            print("Printed current : %.4f", value)
            print("Printed speed : %4d", value2)
            print("Printed watchdog : %1d", value3)
            print("Printed distance : %1d", value4)
            time.sleep(0.1)

    except ServiceExit:
        #j1.shutdown_flag.set()
        #j1.join()
        pass
    canwrapper.dBrake1()
    canwrapper.dBrake2()
    print('Exiting main program')


if __name__ == '__main__':
    main()
