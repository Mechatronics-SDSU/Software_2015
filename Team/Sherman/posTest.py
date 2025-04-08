from cv2 import *
import Position
from random import random

cam = VideoCapture(0)
a, b = cam.read()
pos = Position.Position(b, [random() * 90])

while True:
    i = random()
    if pos.roundVal(random()) == 1:
        pos.update(b, [random() * 90])
    else:
        pos.update(b, [random() * -90])
    imshow("win", b)
    a, b = cam.read()
    ch = waitKey(1)
    if ch == 27:
        break

cam.release()
destroyAllWindows()

'''
cam = VideoCapture(0)
a, b = cam.read()
pos = Position.Position(b, [23.323423])
pos.update(b)
imshow("win", pos.im)
waitKey(0)
cam.release()
'''
