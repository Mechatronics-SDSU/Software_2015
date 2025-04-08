'''
Copyright 2014, Austin Owens, All rights reserved.

Created on Oct 24, 2014

@author: Austin Owens
'''
import data_packet_generator
import threading
import serial
import time

#MC = serial.Serial("COM7", 9600) #My Computer


class MicrocontrollerDataPackets(data_packet_generator.DataPacket):
    def depthGet(self):
        '''
        Sends get request for the current depth.
        
        **Parameters**: \n
        * **No Input Parameters.**
         
        **Returns**: \n
        * **No Return.**\n
        '''

        self.clearPacket()
        self.setByteCount(6)
        self.setFrameID(0)
        self.calcCRC32Out()
        self.pack()
        self.send(MC)
        
        return 0
    
    def motorGet(self, motorNum):
        '''
        Sends get request for motor status (speed and direction of the motors).
        
        **Parameters**: \n
        * **motorNum** - Which motors to move.
         
        **Returns**: \n
        * **No Return.**\n
        '''
        
        self.clearPacket()
        self.setByteCount(6)
        self.setFrameID(motorNum)
        self.calcCRC32Out()
        self.pack()
        self.send(MC)
    
    def motorSet(self, movementMotors, direction, PWM):
        '''
        Sends set command to power a single thruster.
        
        **Parameters**: \n
        * **movementMotors** - Which motors to move.
        * **direction** - Direction of motor movement (forward/reverse).
        * **PWM** - Power intensity of the motors.
         
        **Returns**: \n
        * **No Return.**\n
        '''

        self.clearPacket()
        self.setByteCount(8)
        self.setFrameID(movementMotors + 224) #224 is the offset
        self.setPayload(direction, PWM) #0: Both fwd; 1: Both rev; 2: One fwd one rev; 3: One rev one fwd
        self.calcCRC32Out()
        self.pack()
        self.send(MC)

    def resetSet(self):
        '''
        Sends reset signal to the F0 board.
        
        **Parameters**: \n
        * **No Input Parameters.**
         
        **Returns**: \n
        * **No Return.**\n
        '''
        
        self.clearPacket()
        self.setByteCount(6)
        self.setFrameID(240)
        self.calcCRC32Out()
        self.pack()
        self.send(MC)
        
class MicrocontrollerResponse(data_packet_generator.DataPacket, threading.Thread):
    def __init__(self):
        '''
        Initializes the thread (starts thread process).
        
        **Parameters**: \n
        * **No Input Parameters.**
        
        **Returns**: \n
        * **No Return.**\n
        '''
        threading.Thread.__init__(self)
        
        self.runThread = True
        
        self.mcSendDataPackets = MicrocontrollerDataPackets()
        
        self.lowerFrameIdForAlerts = 119
        self.upperFrameIdForAlerts = 124
        
        self.alertList = []
        self.getList = []
    
    def run(self):
            
        while self.runThread:

            dataPacket = self.unpack() #Reads in data packets
            if dataPacket != None and dataPacket != [0]:
                if ((dataPacket[1] >= self.lowerFrameIdForAlerts) and (dataPacket[1] <= self.upperFrameIdForAlerts)):
                    self.alertList.append(dataPacket)
                else:
                    self.getList.append(dataPacket)
                    
    def unpack(self):
        '''
        Extracts the raw data from the transmission (collects all bytes into array).
        
        **Parameters**: \n
        * **No Input Parameters.**
         
        **Returns**: \n
        * **self.dataPacketIn** - The raw data transmission.\n
        '''
        try:
            if MC.inWaiting() != 0:
                self.dataPacketIn = []
                self.dataPacketIn.append(ord(MC.read()))
                if self.dataPacketIn[0] >= 6 and self.dataPacketIn[0] <= 16: #If the byte count is between 6 and 16 (this is the min and max range of bytes in a data packet that we have...this could change in the future)
                    for x in range(1, self.dataPacketIn[0]):
                        self.dataPacketIn.append(ord(MC.read()))
                    self.dataPacketIn = self.calcCRC32In(self.dataPacketIn)
                    return self.dataPacketIn
        except Exception as msg:
            print "Can't receive data from F4:", msg
            
    def killThread(self):
        '''
        Ends thread process. 
        
        **Parameters**: \n
        * **No Input Parameters.**
        
        **Returns**: \n
        * **No Return.**\n
        '''
        self.runThread = False
        
if __name__ == '__main__':
    
    MicrocontrollerDataPackets().depthGet()
    time.sleep(1)
    dataPacket = MicrocontrollerResponse().unpack()
    print dataPacket