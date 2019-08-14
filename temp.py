from IOcontroller import IOcontroller
import time

io = IOcontroller()
io.setLed(0,2,0)
while 1:
	temp1 = io.readPresureSensorLeft()
	temp2 = io.readPresureSensorRight()
	#temp3 = io.readDistanceSensor3()
	#temp4 = io.readDistanceSensor4()
	print(temp1)
	print(temp2)
	#print(temp3)
	#print(temp4)
	print(" ----------------")
	time.sleep(0.2)