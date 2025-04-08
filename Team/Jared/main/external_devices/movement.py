'''
Copyright 2015, Austin Owens, All rights reserved.

Created on March 29, 2015

@author: Austin Owens
'''

#import microcontroller
import main.utility_package.utilities as utilities

#TCB = microcontroller.MicrocontrollerDataPackets()

advM = utilities.AdvancedMath()
e1 = advM.e1
e2 = advM.e2
e3 = advM.e3


class BrushedThruster():
    
    def __init__(self, motorID, orientation, location):
        self.motorID = motorID #ID value that we assign to thruster
        self.orientation = orientation #Direction thruster is facing: 3=Positive Z-axis, 2=Positive Y-axis, 1=Positive X-axis, -1=Negative X-axis, -2=Negative Y-axis, -3=Negative Z-axis 
        self.location = location #[Unit in x direction, Unit in y direction, Unit in z direction] Location data currently doesn't do anything.
        
        self.maxPwm = 204 #80% duty cycle
        self.pwm = 0  #Initial speed will be zero 

    def setPWM(self, pwm):
        '''
        This function gets called instead of setting self.speed directly so a 
        check can be done to make sure we don't go over a certain PWM by mistake.
        '''
        if pwm > self.maxPwm:
            self.pwm = self.maxPwm
        elif pwm < -self.maxPwm:
            self.pwm = -self.maxPwm
        else:
            self.pwm = pwm
            
    def sendThrusterPacket(self):
        print "ID:", self.motorID, " Location:", self.location, " Orientation:", self.orientation, " Thrust Direction:", int(self.pwm < 0), " PWM:", abs(self.pwm)
        #TCB.motorSet(self.motorID, self.pwm < 0, abs(self.pwm)) #if seed is less than 0, direction is reverse (1), #if seed is more than 0, direction is forward (0) 

class MovementController():
    
    def __init__(self, thrusters):
        self.thrusters = thrusters 
        
    def simpleMove(self, *motorPwms):
        for index, motorPwm in enumerate(motorPwms):
            self.thrusters[index].setPWM(motorPwm) #Assign motor PWMs to objects speed variable
            self.thrusters[index].sendThrusterPacket()
            
    def move(self, xPwmTranslate, yPwmTranslate, zPwmTranslate, xPwmRotate, yPwmRotate, zPwmRotate):
        motorPwms = []

        for index, thruster in enumerate(self.thrusters): #For each thruster object..
            #Rotates about X-axis or Z-axis or translates along Y-axis or any combination given this thruster configuration
            if thruster.orientation == [0, 1, 0] and thruster.location == [1, 0, 1]:    #If thruster is facing in positive Y direction and is translated along the positive X and positive Z directions only.
                motorPwms.append(-yPwmTranslate + xPwmRotate + -zPwmRotate)
                    
            elif thruster.orientation == [0, 1, 0] and thruster.location == [-1, 0, 1]:   #If thruster is facing in positive Y direction and is translated along the negative X and positive Z directions only.
                motorPwms.append(-yPwmTranslate + xPwmRotate + zPwmRotate)
                
            elif thruster.orientation == [0, 1, 0] and thruster.location == [-1, 0, -1]:  #If thruster is facing in positive Y direction and is translated along the negative X and negative Z directions only.
                motorPwms.append(-yPwmTranslate + -xPwmRotate + zPwmRotate)
                
            elif thruster.orientation == [0, 1, 0] and thruster.location == [1, 0, -1]:   #If thruster is facing in positive Y direction and is translated along the positive X and negative Z directions only.
                motorPwms.append(-yPwmTranslate + -xPwmRotate + -zPwmRotate)
                
            elif thruster.orientation == [0, -1, 0] and thruster.location == [1, 0, 1]:   #If thruster is facing in negative Y direction and is translated along the positive X and positive Z directions only.
                motorPwms.append(yPwmTranslate + -xPwmRotate + zPwmRotate)
                
            elif thruster.orientation == [0, -1, 0] and thruster.location == [-1, 0, 1]:  #If thruster is facing in negative Y direction and is translated along the negative X and positive Z directions only.
                motorPwms.append(yPwmTranslate + -xPwmRotate + -zPwmRotate)
                
            elif thruster.orientation == [0, -1, 0] and thruster.location == [-1, 0, -1]: #If thruster is facing in negative Y direction and is translated along the negative X and negative Z directions only.
                motorPwms.append(yPwmTranslate + xPwmRotate + -zPwmRotate)
                
            elif thruster.orientation == [0, -1, 0] and thruster.location == [1, 0, -1]:  #If thruster is facing in positive Y direction and is translated along the positive X and negative Z directions only.
                motorPwms.append(yPwmTranslate + xPwmRotate + zPwmRotate)
            
            #Rotates about Y-axis or translates along X-axis or any combination given this thruster configuration
            elif thruster.orientation == [1, 0, 0] and thruster.location[2] == 1:     #If thruster is facing in positive X direction and is translated along the positive Z direction (and can be located anywhere in the X and Y direction)
                motorPwms.append(-xPwmTranslate + -yPwmRotate)
            
            elif thruster.orientation == [1, 0, 0] and thruster.location[2] == -1:  #If thruster is facing in positive X direction and is translated along the negative Z direction (and can be located anywhere in the X and Y direction)
                motorPwms.append(-xPwmTranslate + yPwmRotate)
            
            elif thruster.orientation == [-1, 0, 0] and thruster.location[2] == 1:  #If thruster is facing in negative X direction and is translated along the positive Z direction (and can be located anywhere in the X and Y direction)
                motorPwms.append(xPwmTranslate + yPwmRotate)
            
            elif thruster.orientation == [-1, 0, 0] and thruster.location[2] == -1: #If thruster is facing in negative X direction and is translated along the negative Z direction (and can be located anywhere in the X and Y direction)
                motorPwms.append(xPwmTranslate + -yPwmRotate)
                
            #Rotates about Y-axis or translates along Z-axis or any combination given this thruster configuration
            elif thruster.orientation == [0, 0, 1] and thruster.location[0] == 1:   #If thruster is facing in positive Z direction and is translated along the positive X direction (and can be located anywhere in the Y and Z direction)
                motorPwms.append(-zPwmTranslate + yPwmRotate)  
            
            elif thruster.orientation == [0, 0, 1] and thruster.location[0] == -1:  #If thruster is facing in positive Z direction and is translated along the negative X direction (and can be located anywhere in the Y and Z direction)
                motorPwms.append(-zPwmTranslate + -yPwmRotate)
            
            elif thruster.orientation == [0, 0, -1] and thruster.location[0] == 1:  #If thruster is facing in negative Z direction and is translated along the positive X direction (and can be located anywhere in the Y and Z direction)
                motorPwms.append(zPwmTranslate + -yPwmRotate)
            
            elif thruster.orientation == [0, 0, -1] and thruster.location[0] == -1: #If thruster is facing in negative Z direction and is translated along the negative X direction (and can be located anywhere in the Y and Z direction)
                motorPwms.append(zPwmTranslate + yPwmRotate)
                
        for index, motorPwm in enumerate(motorPwms): #This for loop is so that I can send the thruster data packets all at once so the motors would seem to turn on all at the same time
            self.thrusters[index].setPWM(motorPwm)
            self.thrusters[index].sendThrusterPacket()
            
    #def advancedMove(self, xTranslate, yTranslate, zTranslate, xRotate, yRotate, zRotate): #Translation in meters with respect to NSEW, rotation in degrees with respect to NSEW
        #T = advM.matrixMultiply(advM.Trans(e1, xTranslate), advM.Trans(e2, yTranslate), advM.Trans(e3, zTranslate), advM.Rot(e1, xRotate), advM.Rot(e3, yRotate), advM.Rot(e3, zRotate))
        #print T
        
        

if __name__=="__main__":
    thruster1 = BrushedThruster(1, [0, 1, 0], [1, 0, 1])  #Up/Down thruster
    thruster2 = BrushedThruster(2, [0, 1, 0], [-1, 0, 1])  #Up/Down thruster
    thruster3 = BrushedThruster(3, [0, 1, 0], [1, 0, -1])  #Up/Down thruster
    thruster4 = BrushedThruster(4, [0, 1, 0], [-1, 0, -1])  #Up/Down thruster
    thruster5 = BrushedThruster(5, [-1, 0, 0], [0, 1, 1]) #Left/Right thruster
    thruster6 = BrushedThruster(6, [-1, 0, 0], [0, 1, -1]) #Left/Right thruster
    thruster7 = BrushedThruster(7, [0, 0, -1], [1, 1, 0]) #Fwd/Rev thruster
    thruster8 = BrushedThruster(8, [0, 0, -1], [-1, 1, 0]) #Fwd/Rev thruster

    thrusters = [thruster1, thruster2, thruster3, thruster4, thruster5, thruster6, thruster7, thruster8]
    moveController = MovementController(thrusters)
    
    #moveController.simpleMove(255, 255, 255, 255, 0, 0, 0, 0)
    moveController.move(0, 50, 0, 50, 0, 50)
    #moveController.advancedMove(0, 0, 0, 25, 0, 0)
