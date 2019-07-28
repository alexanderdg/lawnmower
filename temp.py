from IOcontroller import IOcontroller

io = IOcontroller()
while 1:
	temp = io.readDistanceSensor1()
	print(temp)
