from CANwrapper import CANwrapper
import time
import signal

bustype = 'socketcan'
channel = 'can0'

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
        result = canwrapper.drive1(100, 1)
        #print("return of drive function {}", result)
        while True:
            value = canwrapper.getCurrent2()
            value2 = canwrapper.getSpeed2()
            value3 = canwrapper.getAWatchdog2()
            value4 = canwrapper.getDistance2()
            value5 = canwrapper.getCurrent1()
            value6 = canwrapper.getSpeed1()
            value7 = canwrapper.getAWatchdog1()
            value8 = canwrapper.getDistance1()
            print("Printed current 1: %.2f 2: %.2f" % (value5, value))
            print("Printed speed 1: ", value6, " 2: ", value2)
            print("Printed watchdog 1: ", value7, " 2: ", value3)
            print("Printed distance 1: ", value8, " 2: ", value4)
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
