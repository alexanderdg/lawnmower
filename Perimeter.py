import requests
import time

class Perimeter:
    def __init__(self):
        self.ipAdres = "192.168.0.148"
        self.periCurrent = 0.0
        self.fault = 0
        self.status = "off"


    def getHTTPRequest(self, value):
        returnValue = -1
        try:
            receive = requests.get("http://" + self.ipAdres + value)
            #print(receive.text[:2])
            if receive.text[:2] == "OK":
                returnValue = 1
            else:
                returnValue = 0
        except:
            print("Probleem bij het verbinden")
        return returnValue

    def setPerimeterOff(self):
        return self.getHTTPRequest("/off")

    def setPerimeterOn(self):
        return self.getHTTPRequest("/on")

    def askForStatus(self):
        returnValue = -1
        try:
            receive = requests.get("http://" + self.ipAdres + "/status")
            try:
                self.periCurrent = float((str(receive.content).split("'")[1]).split(":")[0])
            except (ValueError, TypeError):
                print("Fout bij het lezen van de periStroom")
            self.fault = (str(receive.content).split("'")[1]).split(":")[1]
            self.status = (str(receive.content).split("'")[1]).split(":")[2]
            returnValue = 1
        except:
            print("Probleem bij het verbinden")
        return returnValue, self.periCurrent, self.fault, self.status