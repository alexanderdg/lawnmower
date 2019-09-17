from MotionController import MotionController
import time


if __name__ == '__main__':
    motion = MotionController()
    while True:
      print(motion.getRightCurrent())
      time.sleep(1)