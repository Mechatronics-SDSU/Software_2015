from cv2 import *
import math

class Position:

    def __init__(self, im, ahrs):
        self.pos = []
        self.radius = 72.0
        self.r2 = 60.5
        self.center = (320, 384)
        self.update(im, ahrs)

    #store data, update image
    def update(self, image, ahrs):
        self.im = image
        self.data = ahrs
        for i in range(0,181):
            line(self.im, self.getNext(self.radius, i), self.getNext(self.radius, i), (255,0,255))
            for num in range(0, len(self.data)):
                line(self.im, self.getNext(self.radius, self.data[num] + 90), self.getNext(self.r2, self.data[num] + 95), (0, 255,255))
                line(self.im, self.getNext(self.radius, self.data[num] + 90), self.getNext(self.r2, self.data[num] + 85), (0, 255, 255))

    def getX(self, rad, theta):
        return (rad * math.cos(math.radians(theta))) + self.center[0]

    def getY(self, rad, theta):
        return self.center[1] - (rad * math.sin(math.radians(theta)))

    def roundVal(self, val):
        if val - int(val) > .5:
            return int(math.ceil(val))
        else:
            return int(math.floor(val))

    def getNext(self, rad, i):
        return (self.roundVal(self.getX(rad, i)), self.roundVal(self.getY(rad, i)))
