from CANdriver import CANdriver
import time
import threading
import signal
import can

bustype = 'socketcan'
channel = 'can0'


class CANwatcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.candriver = CANdriver()
        self.shutdown_flag = threading.Event()

    def run(self):
        print('Thread #%s started' % self.ident)
        self.candriver.drive(1,100,0)
        self.candriver.drive(2,100,0)
        #CANdriver.drive(1,100,0)
        #CANdriver.drive(2, 100, 0)
        time.sleep(1)
        self.candriver.coastBrake(1)
        self.candriver.coastBrake(2)
        self.candriver.readCurrent(1)
        while not self.shutdown_flag.is_set():
            self.candriver.readCanBus()
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

    print('Starting main program')
    try:
        j1 = CANwatcher()
        j1.start()
        while True:
            time.sleep(1)

    except ServiceExit:
        j1.shutdown_flag.set()
        j1.join()

    print('Exiting main program')


if __name__ == '__main__':
    main()
