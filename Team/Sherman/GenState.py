from cv2 import *

class GeneralState:
    
    def __init__(self, image):
        self.tempCoords = (0, 12)
        self.temp = None
        self.timeCoords = (320,10)
        self.motorCoords= []
        self.textOffset = 10
        self.batteryCoords =  [(440, 450), (540, 480)]
        self.battEnd = (540, 480)
        self.batteries = []
        self.motors = []
        self.battMax = 50       #distance in pixels 
        self.colorOne = (0,255,255)
        self.colorTwo = (0, 0, 255)
        self.median = (490, 450)
        self.medianEnd = (490, 480)
        self.alerts = []
        self.time = time.localtime()
        self.im = image

    def update(self, *data):
        #assign data as needed
        displayBattery()
        displayTime()
        displayMotors()
        displayTemp()
        
    def displayBattery(self):
        rectangle(self.im, self.batteryCoords[0], self.battEnd, (128, 128, 128), -1)
        #for j in range(0, 2):
            #rectangle(self.im, self.batteryCoords[j], self.getBattery(j), self.colorOne, -1)
            #rectangle(self.im, self.batteryCoords[1], self.getBattery(1), self.colorTwo, -1)
                    
        for i in range(0, 2):
            putText(self.im, str(self.batteries[0]), self.getBattery(i), FONT_HERSHEY_SIMPLEX, .5, self.colorOne)

        line(self.im, self.median, self.medianEnd, (0, 0, 0))
        
    def getBattery(self, which):
        if which == 0:
            val1, val2 = self.batteryCoords[which][0] + (self.batteries[which] * self.battMax), self.medianEnd[1]
        else:
            val1, val2 = self.battEnd[0] - (self.batteries[which] * self.battMax), self.battEnd[1]-30
        return (val1, val2)

    def displayTime(self):
        theTime = str(self.time.tm_mon)+"/"+str(self.time.tm_mday)+"/"+str(self.time.tm_year)+":"+str(self.time.tm_hour)+"/"+str(self.time.tm_min)+"/"+str(self.time.tm_sec)
        putText(self.im, theTime, self.timeCoords, FONT_HERSHEY_SIMPLEX, .5, self.colorOne)

    def displayMotors(self):
        for i in range(0, len(self.motors)):
            text = str("M" + str(i) + ":" + str(self.motors[i]))
            putText(self.im, text, (self.motorCoords[0], self.motorCoords[1] + (self.textOffset*i)), FONT_HERSHEY_SIMPLEX, .5, self.colorOne)
            
    def displayAlerts(self):
        offset = 36/len(self.alerts)
        if offset < 12:
            offset = 12
        color = (255,255,255)
        
        for i in range(0, len(self.alerts)):    
            if i == 0:
                color = (255,255,0)
            elif i == 1:
                color = (255,0,255)
            elif i == 2:
                color = (0, 255,255)
            putText(self.im, str(self.mapAlerts(self.alerts[i])), (self.im.shape[1] - 50, self.im.shape[0]), FONT_HERSHEY_SIMPLEX, .5, color)
        
    def mapAlerts(self, alert):
        if alert == 0:
            return "text"
        elif alert == 1:
            return "otherText"
        
    def displayTemp(self):
        for i in range(0, 2):
            putText(self.im, "Temp:" + str(self.temp[i]), self.tempCoords[i], FONT_HERSHEY_SIMPLEX, .5, self.colorOne)
            
