'''
Created on Oct 24, 2014

@author: Austin Owens
'''
import time
from random import random
from my_main.data_logging.data_logger import DataLog

logger = DataLog()
            
class NavigationManagementSystem():
    def __init__(self):
        self.mcGetDataPacket = []
        self.mcAlertDataPacket = None
        self.processActive = True
        self.loggerIterationCounter = 0
        
        #For MC
        self.depthPayload = [0, 0]
        self.motor1Payload = [0, 0, 0, 0]
        self.motor2Payload = [0, 0, 0, 0]
        self.motor3Payload = [0, 0, 0, 0]
        self.motor4Payload = [0, 0, 0, 0]
        self.motor5Payload = [0, 0, 0, 0]
        self.motor6Payload = [0, 0, 0, 0]
        
        #For AHRS
        self.ahrsData = [0, 0, 0]
        
        #For Controller
        self.ciData = []
        
    def start(self, pipe):
        #import microcontroller
        #import sparton_ahrs
        import controller_input
        
        #Microcontroller initializing
        #mcSendDataPackets = microcontroller.MicrocontrollerDataPackets()
        #mcResponseThread = microcontroller.MicrocontrollerResponse()
        #mcResponseThread.start()
        
        #Sparton AHRS initializing
        #spartonResponseThread = sparton_ahrs.SpartonAhrsResponse("COM3")
        #spartonResponseThread.start()
        
        #Controller initializing
        controllerResponseThread = controller_input.controllerResponse()
        controllerResponseThread.start()
        
        while True:
            #mcData, mcAlertData = self.microcontrollerData(mcSendDataPackets, mcResponseThread)
            mcData = None
            #ahrsData = self.spartonAhrsData(spartonResponseThread)
            ahrsData = None
            self.__logNavigationData__(iterationsUntilLogging = 10, position = [random()*100, random()*100, random()*100], yaw = random()*360, pitch = random()*180-90, roll = random()*180-90)        
            ciData = self.controllerData(controllerResponseThread)
            
            time.sleep(0.1) #Allows for other threads to get a chance to work
            
            #if len(spartonResponseThread.getList) > 0:
            pipe.send([mcData, ahrsData, ciData])
        
    def spartonAhrsData(self, spartonResponseThread):
        
        while len(spartonResponseThread.getList) > 0:
            self.ahrsData = spartonResponseThread.getList.pop(0)
        return self.ahrsData
        
    def microcontrollerData(self, mcSendDataPackets, mcResponseThread):
        #Send Getters
        
        while len(mcResponseThread.getList) > 0:
            
            mcGetDataPacket = mcResponseThread.getList.pop(0)
            
            if (mcGetDataPacket[1] == 0):
                depth = mcGetDataPacket[2]
                depthLeftOver = mcGetDataPacket[3]
                
                self.depthPayload[0] = ((depth << 8) | depthLeftOver)/100.0#(((((depth << 8) | depthLeftOver)*46.3)/4095)-14.7)/0.43
                self.depthPayload[1] = (((((depth << 8) | depthLeftOver)*46.3)/4095)-14.7)/0.43 #This calculation is used to see the depth of the sub in feet.
                
                #logger.logData("Depth",  "MC", 0, "Depth:", self.depthPayload[0], "Depth In Feet:", self.depthPayload[1])
                
            elif (mcGetDataPacket[1] == 1):
                desiredDirection = mcGetDataPacket[2]
                desiredSpeed = mcGetDataPacket[3]
                currentDirection = mcGetDataPacket[4]
                currentSpeed = mcGetDataPacket[5]
                self.motor1Payload[0] = desiredDirection
                self.motor1Payload[1] = desiredSpeed
                self.motor1Payload[2] = currentDirection
                self.motor1Payload[3] = currentSpeed
                
                #logger.logData("Motor 1",  "MC", 1, "Desired Direction:", self.motor1Payload[0], "Desired Speed:", self.motor1Payload[1], "Current Direction:", self.motor1Payload[2], "Current Speed:", self.motor1Payload[3])
                
            elif (mcGetDataPacket[1] == 2):
                desiredDirection = mcGetDataPacket[2]
                desiredSpeed = mcGetDataPacket[3]
                currentDirection = mcGetDataPacket[4]
                currentSpeed = mcGetDataPacket[5]
                self.motor2Payload[0] = desiredDirection
                self.motor2Payload[1] = desiredSpeed
                self.motor2Payload[2] = currentDirection
                self.motor2Payload[3] = currentSpeed
                
                #logger.logData("Motor 2", "MC", 2, "Desired Direction:", self.motor2Payload[0], "Desired Speed:", self.motor2Payload[1], "Current Direction:", self.motor2Payload[2], "Current Speed:", self.motor2Payload[3])
                
            elif (mcGetDataPacket[1] == 3):
                desiredDirection = mcGetDataPacket[2]
                desiredSpeed = mcGetDataPacket[3]
                currentDirection = mcGetDataPacket[4]
                currentSpeed = mcGetDataPacket[5]
                self.motor3Payload[0] = desiredDirection
                self.motor3Payload[1] = desiredSpeed
                self.motor3Payload[2] = currentDirection
                self.motor3Payload[3] = currentSpeed
                
                #logger.logData("Motor 3", "MC", 3, "Desired Direction:", self.motor3Payload[0], "Desired Speed:", self.motor3Payload[1], "Current Direction:", self.motor3Payload[2], "Current Speed:", self.motor3Payload[3])
                
            elif (mcGetDataPacket[1] == 4):
                desiredDirection = mcGetDataPacket[2]
                desiredSpeed = mcGetDataPacket[3]
                currentDirection = mcGetDataPacket[4]
                currentSpeed = mcGetDataPacket[5]
                self.motor4Payload[0] = desiredDirection
                self.motor4Payload[1] = desiredSpeed
                self.motor4Payload[2] = currentDirection
                self.motor4Payload[3] = currentSpeed
                
                #logger.logData("Motor 4", "MC", 4, "Desired Direction:", self.motor4Payload[0], "Desired Speed:", self.motor4Payload[1], "Current Direction:", self.motor4Payload[2], "Current Speed:", self.motor4Payload[3])
                
            elif (mcGetDataPacket[1] == 5):
                desiredDirection = mcGetDataPacket[2]
                desiredSpeed = mcGetDataPacket[3]
                currentDirection = mcGetDataPacket[4]
                currentSpeed = mcGetDataPacket[5]
                self.motor5Payload[0] = desiredDirection
                self.motor5Payload[1] = desiredSpeed
                self.motor5Payload[2] = currentDirection
                self.motor5Payload[3] = currentSpeed
                
                #logger.logData("Motor 5", "MC", 5, "Desired Direction:", self.motor5Payload[0], "Desired Speed:", self.motor5Payload[1], "Current Direction:", self.motor5Payload[2], "Current Speed:", self.motor5Payload[3])
                
            elif (mcGetDataPacket[1] == 6):
                desiredDirection = mcGetDataPacket[2]
                desiredSpeed = mcGetDataPacket[3]
                currentDirection = mcGetDataPacket[4]
                currentSpeed = mcGetDataPacket[5]
                self.motor6Payload[0] = desiredDirection
                self.motor6Payload[1] = desiredSpeed
                self.motor6Payload[2] = currentDirection
                self.motor6Payload[3] = currentSpeed
                
                #logger.logData("Motor 6", "MC", 6, "Desired Direction:", self.motor6Payload[0], "Desired Speed:", self.motor6Payload[1], "Current Direction:", self.motor6Payload[2], "Current Speed:", self.motor6Payload[3])
            
        while len(mcResponseThread.alertList) > 0:
            self.mcAlertDataPacket.append(mcResponseThread.alertList.pop(0))
            #Could do actions under here according to what data packet is and only return the important stuff to reduce overhead
        
        mcData = [[self.depthPayload[0], self.depthPayload[1]],
        [self.motor1Payload[0], self.motor1Payload[1], self.motor1Payload[2], self.motor1Payload[3]],
        [self.motor2Payload[0], self.motor2Payload[1], self.motor2Payload[2], self.motor2Payload[3]],
        [self.motor3Payload[0], self.motor3Payload[1], self.motor3Payload[2], self.motor3Payload[3]],
        [self.motor4Payload[0], self.motor4Payload[1], self.motor4Payload[2], self.motor4Payload[3]],
        [self.motor5Payload[0], self.motor5Payload[1], self.motor5Payload[2], self.motor5Payload[3]],
        [self.motor6Payload[0], self.motor6Payload[1], self.motor6Payload[2], self.motor6Payload[3]]]
           
        mcAlertData = None             
        
        return mcData, mcAlertData
        
    def __logNavigationData__(self, **kwargs): #Might not need to have this hear. Could have this in the my_main since this data will be sent there anyway
        if self.loggerIterationCounter >= 4:
            logger.logData('Position', kwargs.get('position')[0], kwargs.get('position')[1], kwargs.get('position')[2])
            logger.logData('Yaw', kwargs.get('yaw'))
            logger.logData('Pitch', kwargs.get('pitch'))
            logger.logData('Roll', kwargs.get('roll'))
            self.loggerIterationCounter = 0
        self.loggerIterationCounter += 1
        
    def controllerData(self, controllerResponseThread):
        
        while len(controllerResponseThread.getList) > 0:
            self.ciData = controllerResponseThread.getList.pop(0)
        return self.ciData
         
if __name__ == '__main__':
    import multiprocessing
    import cv2

    nms = NavigationManagementSystem()
    
    cap = cv2.VideoCapture(0)

    parent_conn, child_conn = multiprocessing.Pipe()
    process = multiprocessing.Process(target=nms.start, args=(child_conn,))
    process.start()
    
    while True:
        
            
        print parent_conn.recv()
        flag, img = cap.read()
        
        cv2.imshow('Raw Img', img)
        
        ch = cv2.waitKey(1)
        if ch == 27:
            process.terminate()
            break