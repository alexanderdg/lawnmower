import requests
import time
from Perimeter import Perimeter

peri = Perimeter()

print(peri.setPerimerOn())
time.sleep(2)
value, periCurrent, fault, status = peri.askForStatus()
print("Peri current is " + periCurrent)
print(peri.setPerimeterOff())