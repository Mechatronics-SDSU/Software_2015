from cv2 import *
import Depth
from random import random

cam = VideoCapture(0)
a, b = cam.read()
depth = Depth.Depth(b, [random() * 32])

while True:
    a, b = cam.read()
    #b = imread("trex.png")
    depth.update(b, [random() * 32])
    imshow("win", depth.im)
    ch = waitKey(1)
    if ch == 27:
        break
    
cam.release()
destroyAllWindows()
