'''
Created on Dec 20, 2014

@author: Austin
'''

import sparton_ahrs
import time

ahrs = sparton_ahrs.SpartonAhrsDataPacket("COM3")


while True:
    ahrs.trueHeadingGet()
    ahrs.pitchAndRollGet()
    
    time.sleep(0.01)
    
    headingDataPacket = ahrs.unpack()
    pitchRollDataPacket = ahrs.unpack()
    
    if headingDataPacket != None or pitchRollDataPacket != None:
        headingData = ahrs.extractSensorData(headingDataPacket)
        pitchRollData = ahrs.extractSensorData(pitchRollDataPacket)
        
        print headingData[1], pitchRollData[1], pitchRollData[2]