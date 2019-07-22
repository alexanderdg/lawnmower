from MotionController import MotionController
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
    motion = MotionController()
    print('Starting main program')
    try:
        #j1 = CANwatcher()
        #j1.start()

        motion.turnLeft(0.5)
        #print("return of drive function {}", result)
        while True:
            motion.printDiagnostics()
            time.sleep(0.1)

    except ServiceExit:
        #j1.shutdown_flag.set()
        #j1.join()
        pass
    motion.dynamicBrake()
    print('Exiting main program')


if __name__ == '__main__':
    main()