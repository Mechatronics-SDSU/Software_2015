import numpy as np
import cv2
import time
        
if __name__ == '__main__':
    
    #im = cv2.imread('Banana.jpg',1)
    #other = cv2.imread('Banana.jpg',1)

    im = cv2.imread('Lightning.jpg',1)
    other = cv2.imread('Lightning.jpg',1)
    
    #im = cv2.imread('t1.jpg',1)
    #other = cv2.imread('t1.jpg',1)
    
    #im = cv2.imread('board2.png',1)
    #other = cv2.imread('board2.png',1)
    
    #im = cv2.imread('space.jpg',1)
    #other = cv2.imread('space.jpg',1)
    
    #im = cv2.imread('boardcut.jpg',1)
    #other = cv2.imread('boardcut.jpg',1)
    
    #cap = cv2.VideoCapture(0) 
    #time.sleep(1)
    low_yellow = np.array([10, 50, 50])
    high_yellow = np.array([40, 255, 255])
    
    #low_yellow = np.array([160, 20, 20])
    #high_yellow = np.array([200, 150, 150])
    
    #low_yellow = np.array([100, 20, 20])
    #high_yellow = np.array([130, 255, 255])    
                           
    
    #ret,thresh = cv2.threshold(im,127,255,0)
    #contours,hierarchy = cv2.findContours(thresh, 1, 2)
    hier = []
    while True:
        #flag, im = cap.read()
        #other = im
        #im = cv2.blur(im, (2,2))
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        img = cv2.inRange(hsv, low_yellow, high_yellow)
        mask = cv2.inRange(hsv, low_yellow, high_yellow)
        #img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        
        #height, width = img.shape
        #blank_image = np.zeros((height,width,3), np.uint8)
        
        ret,thresh = cv2.threshold(img,127,255,0)
        flag, contours, h = cv2.findContours(thresh,1,2)
        
        hier = []
        squares_cont = []
        for n, cnt in enumerate(contours):
            approx = cv2.approxPolyDP(cnt,0.005*cv2.arcLength(cnt,True),True)#0.17 only gets the squares with nothing
            #print len(approx)
            if len(approx) >1:#23,22,21 & 15 @ .01///// 45 & 64 & 86, 171, 181 @ .001
                print "Woo"
                print len(approx)
                cv2.drawContours(other,[cnt],0,(0,255,0),-1)
                #cv2.drawContours(blank_image,[cnt],0,(255,255,255),-1)
            elif len(approx)==5:
                print "pentagon"
                #cv2.drawContours(img,[cnt],0,255,-1)
            #elif len(approx)==3:
                #print "triangle"
                #cv2.drawContours(img,[cnt],0,(0,255,0),-1)
            elif len(approx)==4:
                #hier.append(n)
                print "square"
                squares_cont.append([n,cnt])
                hier.append(h[0][n][1])
                if h[0][n][1] == hier[0]:
                    pass
                    cv2.drawContours(other,[cnt],0,(0,0,255),3)
                else:
                    pass
                    cv2.drawContours(other,[cnt],0,(255,0,0),3)
                    print h[0][n][3]
            #elif len(approx) > 15:
             #   print "circle"
                cv2.drawContours(img,[cnt],0,(0,255,255),-1)
        try:
            outer_square = max(hier)
            for i, cnt in squares_cont:
                if h[0][i][1] < outer_square:
                    cv2.drawContours(other,[cnt],0,(255,255,0),3)
                else:
                    cv2.drawContours(other,[cnt],0,(255,0,0),4)
        except:
            print "No squares"
        cv2.imshow('img',img)
        cv2.imshow('other',other)
        cv2.imshow('mask',mask)
        #cv2.imshow('black', blank_image)
        #blank_image[:,0:0.5*width] = (255,0,0)  
        ch = cv2.waitKey(0)
        if ch == 27:
                break
    cv2.imwrite('Board_detect.png', other)
    print n
    print len(contours)
    print len(h[0])
    print h[0]
    print h[0][n]
    print hier
    print h[0][n][0]
    cv2.destroyAllWindows()