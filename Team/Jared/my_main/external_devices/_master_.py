'''
Created on Oct 24, 2014

@author: Austin Owens
'''
import multiprocessing
import _navigation_management_system_
import cv2

nms = _navigation_management_system_.NavigationManagementSystem()

cap = cv2.VideoCapture(0)

nmsPosition = [0, 0, 0] #X, Y, Z
nmsYaw = 0
nmsPitch = 0
nmsRoll = 0

if __name__ == "__main__":
            
    parent_conn, child_conn = multiprocessing.Pipe()
    process = multiprocessing.Process(target=nms.start, args=(child_conn,))
    process.start()
    
    while True:
        print parent_conn.recv()
        flag, img = cap.read()
        
        cv2.imshow('Raw Img', img)
        
        ch = cv2.waitKey(1)
        if ch == 27:
            child_conn.close()
            parent_conn.close()
            process.terminate()
            break
    
    
    