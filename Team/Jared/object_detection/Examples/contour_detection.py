import cv2
import numpy as np

im = cv2.imread('Lightning.jpg',1)
other = cv2.imread('Lightning.jpg',1)

low_yellow = np.array([20, 50, 50])
high_yellow = np.array([40, 255, 255])
                       
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
img = cv2.inRange(hsv, low_yellow, high_yellow)

ret,thresh = cv2.threshold(img,127,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]
epsilon = 0.01*cv2.arcLength(cnt, True)
print cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)
cv2.drawContours(other, approx, -1, (255,0,0), 3)
M = cv2.moments(cnt)
print M
print len(approx)

while True:
    cv2.imshow('mask', img)
    cv2.imshow('Output', other)
    ch = cv2.waitKey(5)
    if ch == 27:
        break
cv2.destroyAllWindows()
print cv2.contourArea(cnt)