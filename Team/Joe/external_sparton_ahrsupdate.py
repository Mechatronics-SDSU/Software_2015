'''
.. module:: external_sparton_ahrs
   :synopsis: Sparton Altitude Heading Reference System (AHRS) device communication.
   
:Author: Austin Owens <sdsumechatronics@gmail.com>
:Date: Created on May 28, 2014
:Description: This module contains the commands for all the functions that can be called with the legacy protocol for the Sparton AHRS

'''

import serial
import struct
import time

class SpartonAhrsDataPacket():
    '''
    This class contains setters and getters commands for the Sparton AHRS in Legacy format. It only handles the sending values.
    '''
    def __init__(self, comPort):
        '''
        Initializes the Sparton AHRS and array of location values.
        
        **Parameters**: \n
        * **comPort** - Serial port number that the Sparton AHRS is connected to.
        
        **Return**: \n
        * **No Return.**\n
        '''
        self.SPARTON_AHRS = serial.Serial(comPort, 115200)

        # This gives the number of bytes that are in the list when the message is sent
        self.locationArray = [[0x01, 9], [0x02, 5], [0x09, 5], [0x83, 5], [0x0F, 5], [0x8B, 5], [0x8C, 5], [0x8D, 5], [0x8E, 5], [0x04, 11], [0x56, 4], [0x08, 5], [0x05, 9], [0x06, 7], [0x07, 11], [0x11, 5], [0x57, 4], [0x4A, 4]]
        
        
    def positionStreamModeSet(self, stream_period):
        '''
        Sets the Sparton AHRS to continuousely stream the position variable.
        The best stream time is 20 milli-seconds per transmission so that all the data will 
        be able to be output form the device. For this reason 20ms is the default value.
                    
        Send: ASCII string NorthTek protocol with the positionrate as the variable, 20 
              as the time interval, and the 'set' command to set the variable positionrate
              to 20.
                    
        Response: N/A
		
        **Parameters**: \n
        * **No Input Parameters.**
         
        **Returns**: \n
        * **stream_period** - Period which the AHRS will stream the data specified in milli-seconds.
        '''
        
        self.SPARTON_AHRS.write("positionrate " + str(stream_period) + " set\0") # I don't know if "\0" is needed here

    def positionStreamModeStop(self):
        
        '''
	Stops the Sparton AHRS to continuousely stream the position variable.
		
	Send: ASCII string NorthTek protocol with the positionrate as the variable, 0 
	      as the time interval, and the 'set' command to set the variable positionrate
	      to 0.
		
	Response: N/A
		
        **Parameters**: \n
        * **No Input Parameters.**
         
        **Returns**: \n
        * **No Return.**\n
        '''
        

        self.SPARTON_AHRS.write("positionrate 0 set\0") # I don't know if "\0" is needed here
        
    def positionGet(self):
        '''
	Get the position variable.  This variable is a composite of 14 floats to include:
	pitch, roll, yawt, magErr, temperature, magp X/Y/Z, accelp X/Y/Z, gyrop X/Y/Z in the 
	order listed.		
		
	Send: RFS Protocol 
		
	Response: 1 instance of RFS response with 14 variables
		
        **Parameters**: \n
        * **No Input Parameters.**
         
        **Returns**: \n
        * **No Return.**\n
        '''
        

        self.SPARTON_AHRS.write(bytearray([0x01, 0x0B, 0x40, 0x10, 0x81, 0x00, 0x00, 0x00, 0x00, 0x08, 0x02, 0x1E, 0x3C, 0x44, 0x03]))

    def unpack(self):
        
        dataPacketIn = []
        print "Bytes in the buffer:", self.SPARTON_AHRS.inWaiting()
        if self.SPARTON_AHRS.inWaiting() != 0:      
            for x in range(self.SPARTON_AHRS.inWaiting()):
                dataPacketIn.append(ord(self.SPARTON_AHRS.read()))
            
            self.SPARTON_AHRS.flushInput()
                
            return dataPacketIn            
    
    def extractSensorData(self, spartonAhrsDataPacket):
        '''
        Reads in the raw transmission and extracts all bytes of the packet
        
        **Parameters**: \n
        * **spartonAhrsDataPacket** - The raw data packet transmission. It includes all meta-data and protocol-specific junk.
         
        **Returns**: \n
        * **sensorValues** - The meaningful data (the payload).\n
        '''
        
        sensorValues = []
        if (spartonAhrsDataPacket[1] == 0x01):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append(spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)
            sensorValues.append(spartonAhrsDataPacket[4] << 8 | spartonAhrsDataPacket[5] << 0)
            sensorValues.append(spartonAhrsDataPacket[6] << 8 | spartonAhrsDataPacket[7] << 0) 
        
        elif (spartonAhrsDataPacket[1] == 0x02):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append((spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)*360.0/4096)
            
        elif (spartonAhrsDataPacket[1] == 0x09):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append((spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)*360.0/4096)
            
        elif (spartonAhrsDataPacket[1] == 0x83):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append((spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)*10.0)
            
        elif (spartonAhrsDataPacket[1] == 0x0F):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append((spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)*10.0)
            
        elif (spartonAhrsDataPacket[1] == 0x8B):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append((spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)*100.0)
            
        elif (spartonAhrsDataPacket[1] == 0x8C):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append(spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)
            
        elif (spartonAhrsDataPacket[1] == 0x8D):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append(spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)
            
        elif (spartonAhrsDataPacket[1] == 0x8E):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append((spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)*10.0)
            
        elif (spartonAhrsDataPacket[1] == 0x04):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append(spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)
            sensorValues.append(spartonAhrsDataPacket[4] << 8 | spartonAhrsDataPacket[5] << 0)
            sensorValues.append(spartonAhrsDataPacket[6] << 8 | spartonAhrsDataPacket[7] << 0)
            sensorValues.append(spartonAhrsDataPacket[8] << 8 | spartonAhrsDataPacket[9] << 0)
            
        elif (spartonAhrsDataPacket[1] == 0x56):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append(spartonAhrsDataPacket[2])
            
        elif (spartonAhrsDataPacket[1] == 0x08):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append(spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)
            
        elif (spartonAhrsDataPacket[1] == 0x05):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append(spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)
            sensorValues.append(spartonAhrsDataPacket[4] << 8 | spartonAhrsDataPacket[5] << 0)
            sensorValues.append(spartonAhrsDataPacket[6] << 8 | spartonAhrsDataPacket[7] << 0)
            
        elif (spartonAhrsDataPacket[1] == 0x06):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append(((spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0) & 0b0000111111111111 )*90.0/4096)
            sensorValues.append(((spartonAhrsDataPacket[4] << 8 | spartonAhrsDataPacket[5] << 0) & 0b0000111111111111 )*180.0/4096)
            
        elif (spartonAhrsDataPacket[1] == 0x07):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append(spartonAhrsDataPacket[2] << 8 | spartonAhrsDataPacket[3] << 0)
            sensorValues.append(spartonAhrsDataPacket[4] << 8 | spartonAhrsDataPacket[5] << 0)
            sensorValues.append(spartonAhrsDataPacket[6] << 8 | spartonAhrsDataPacket[7] << 0)
            sensorValues.append(spartonAhrsDataPacket[8] << 8 | spartonAhrsDataPacket[9] << 0)
            
        elif (spartonAhrsDataPacket[1] == 0x11):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append((spartonAhrsDataPacket[2]*256 + spartonAhrsDataPacket[3])/10.0)
            
        elif (spartonAhrsDataPacket[1] == 0x57):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append(spartonAhrsDataPacket[2])
            
        elif (spartonAhrsDataPacket[1] == 0x4A):
            sensorValues.append(spartonAhrsDataPacket[1])
            sensorValues.append(spartonAhrsDataPacket[2])
            
        
        return sensorValues
    
    def netHeading(self, headingValue):
        '''
        Initializes the heading such the the initial heading upon start is defined to be "0".
        
        **Parameters**: \n
        * **headingValue** - The current heading value from AHRS. 
         
        **Returns**: \n
        * **self.netValue** - The difference between the current heading and the initial heading (heading at start).\n
        '''
        
        global netValueIteration
        
        if netValueIteration == 0: 
            self.initialValue = headingValue
              
        self.netValue = headingValue - self.initialValue
        
        #This if statement will give you net value. Will go from 0 to 360, if gone over 360, will loop back to 0
        if self.netValue < 0:
            self.netValue = self.netValue + 360
            
        #This if statement will go from 0 to 180, if gone over 180, will loop to -179  
        if self.netValue >= 180:
            self.netValue = self.netValue - 360

        netValueIteration += 1
        
        return self.netValue

if __name__ == "__main__":
    ahrs = SpartonAhrsDataPacket("COM6")
    while True:
        ahrs.positionGet()
        time.sleep(2)
        dataPacket = ahrs.unpack()
        if dataPacket != None:
            print "Whole Data Packet:", dataPacket
            #print struct.unpack('f', struct.pack('I' , dataPacket[0] << 24 | dataPacket[1] << 16 | dataPacket[2] << 8 | dataPacket[3] << 0))[0]
    
    
