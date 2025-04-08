import numpy as np
import cv2
import time

if __name__ == '__main__':
    
    #im = cv2.imread('Banana.jpg',1)
    #other = cv2.imread('Banana.jpg',1)

    #im = cv2.imread('Lightning.jpg',1)
    #other = cv2.imread('Lightning.jpg',1)
    
    #im = cv2.imread('t4.jpg',1)
    #other = cv2.imread('t4.jpg',1)
    
    #im = cv2.imread('space.jpg',1)
    #other = cv2.imread('space.jpg',1)
    
    cap = cv2.VideoCapture("corn.mp4") 
    time.sleep(1)
    low_yellow = np.array([20, 100, 100])
    high_yellow = np.array([50, 255, 255])
    
    #low_yellow = np.array([160, 20, 20])
    #high_yellow = np.array([200, 150, 150])
                           
    
    #ret,thresh = cv2.threshold(im,127,255,0)
    #contours,hierarchy = cv2.findContours(thresh, 1, 2)
    while True:
        flag, im = cap.read()
        other = im
        
        im = cv2.blur(im, (10,10))
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        img = cv2.inRange(hsv, low_yellow, high_yellow)
        mask = cv2.inRange(hsv, low_yellow, high_yellow)
        
        height, width = img.shape
        blank_image = np.zeros((height,width,3), np.uint8)
        
        ret,thresh = cv2.threshold(img,127,255,0)
        flag, contours, h = cv2.findContours(thresh,1,2)
        
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
            print len(approx)
            if len(approx) ==4:#23,22,21 & 15 @ .01///// 45 & 64 & 86, 171, 181 @ .001
                print "Ok"
                cv2.drawContours(other,[cnt],0,(0,255,0),3)
                cv2.drawContours(blank_image,[cnt],0,(255,255,255),3)
            '''elif len(approx)==5:
                print "pentagon"
                cv2.drawContours(img,[cnt],0,255,-1)
            elif len(approx)==3:
                print "triangle"
                cv2.drawContours(img,[cnt],0,(0,255,0),-1)
            elif len(approx)==4:
                print "square"
                cv2.drawContours(img,[cnt],0,(0,0,255),-1)
            elif len(approx) == 9:
                print "half-circle"
                cv2.drawContours(img,[cnt],0,(255,255,0),-1)
            elif len(approx) > 15:
                print "circle"
                cv2.drawContours(img,[cnt],0,(0,255,255),-1)'''
        cv2.imshow('img',img)
        cv2.imshow('other',other)
        cv2.imshow('Filter', mask)
        #blank_image[:,0:0.5*width] = (255,0,0)  
        ch = cv2.waitKey(5)
        if ch == 27:
                break
    print img.shape
    cv2.destroyAllWindows()