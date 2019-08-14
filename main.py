import os

from MotionController import MotionController
from IOcontroller import IOcontroller
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
    #os.system("mpg123 /share/Sourcecode/lawnmower/WAV\ files/StartingMoving.mp3")
    motion = MotionController()
    io = IOcontroller()
    print('Starting main program')
    try:
        #j1 = CANwatcher()
        #j1.start()

        motion.turnRight(0.5)
        #motion.turn90Right()
        #time.sleep(200)
        print("Functie is afgelopen!!!!!!!!!!!!!")
        #print("return of drive function {}", result)
        while True:
            motion.printDiagnostics()
            if motion.getLeftCurrent() > 1.0 or motion.getRightCurrent() > 1.0 or io.readPresureSensorRight() > 100 or io.readPresureSensorLeft() > 100:
                motion.dynamicBrake()
                time.sleep(3)
            else:
                motion.turnRight(0.5)

            time.sleep(0.1)

    except ServiceExit:
        #j1.shutdown_flag.set()
        #j1.join()
        pass
    motion.dynamicBrake()
    print('Exiting main program')


if __name__ == '__main__':
    main()