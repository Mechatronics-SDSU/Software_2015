from cv2 import *

class Depth:
    '''#class variables 
    im = None
    sensorReadings = []    #Array of sensor readings. packaging them as an array allows for easy iteration in the function below
    poolDepth = 32         #Max depth of pool
    depthTop = None        #Location of the depth scale (top-most point) as determined by the size of the image
    depthBottom = None     #Location of the depth scale (bottom-most point) as determined by the size of the image
    scaleRange = None      #Height of the scale
    cursors = []           #Array of depth : scale-location mapped values
    scalePos = None        #X-line of the scale
    color = (255,255,255)  #Chosen color of the scale
    interval = None        #Width of space between markers
    text = None            #Optional text variable for displaying value of depth
    '''
    
    def __init__(self, image, data):     
        self.im = image
        self.cursors = []
        self.sensorReadings = []
        self.depthTop = int(self.im.shape[0] * .1)
        self.poolDepth = 32
        self.depthBottom = (int) (self.im.shape[0] - self.depthTop)
        self.scaleRange = (int) (self.depthBottom - self.depthTop)
        self.scalePos = (int) (self.im.shape[1] * .8)
        self.interval = (int) (self.scaleRange / 10)
        self.depthBottom = (int) (self.depthTop + (self.interval * 10))
        self.text = FONT_HERSHEY_SIMPLEX
        self.color = (255,0,255)
        self.update(self.im, data)
        

    #updates the depth object with a new image, and new sensor data
    def update(self, image, data):
        self.im = image            #initialize the new image
        self.sensorReadings = data #initiailze the new data
        self.convertDepth()        #map depth to the scale
        self.drawLines()           #create the representation of the scale on the image
        self.cursors = []          #"        "

    def convertDepth(self):
        for x in range(0, len(self.sensorReadings)):
            self.cursors.append((int)((self.sensorReadings[x] / self.poolDepth) * self.scaleRange))
            #if self.sensorReadings[x] > self.poolDepth:    shouldn't occur
            #    self.cursors[x] = self.poolDepth
            self.cursors[x] += self.depthTop
        
    def drawLines(self):
        line(self.im, (self.scalePos, self.depthTop), (self.scalePos, self.depthBottom), self.color, 1, 1)
        
        for x in range(0, 11):
            line(self.im, (self.scalePos - 10, self.depthTop + (self.interval * x)), (self.scalePos, self.depthTop + (self.interval * x)), self.color, 1, 1)

        for x in range(0, len(self.cursors)):
            line(self.im, (self.scalePos, self.cursors[x]), (self.scalePos + 5, self.cursors[x] + 5), self.color, 1, 1)
            line(self.im, (self.scalePos, self.cursors[x]), (self.scalePos + 5, self.cursors[x] - 5), self.color, 1, 1)   
            putText(self.im, str(self.sensorReadings[x]), (self.scalePos + 5, self.cursors[x]), self.text, .5, self.color, 1, 1)
