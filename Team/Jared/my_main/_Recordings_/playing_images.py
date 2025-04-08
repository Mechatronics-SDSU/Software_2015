'''
Created on Oct 2, 2014

@author: Austin
'''

import cv2
import fnmatch, os
import time

cap1 = cv2.VideoCapture(0) #Find imaging devices

count = 0
flag = 0



def readImageFromFile():
    if count < len(fnmatch.filter(os.listdir('Front/'), '*.png')):
        rawImg = cv2.imread('Front/Image{}.png'.format(count)) #Read in image from file in a .png format
        cv2.imshow('rawImg', rawImg) #Show img
    
    else:
        return 1
    
    return 0
    

if __name__ == "__main__":
    while True:
        time.sleep(0.2)
        
        flag = readImageFromFile() #Uncomment this line to read images from that file
        
        count+=1
        
        ch = cv2.waitKey(1) #Listen for keyboard cmds
        
        if ch == 27 or flag == 1: #If the esc button is pushed or done reading pictures
            break #break out of while loop
    
    cv2.destroyAllWindows() #Destroy all windows