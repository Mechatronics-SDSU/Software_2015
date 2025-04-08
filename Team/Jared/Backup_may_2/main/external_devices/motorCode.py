'''
Copyright 2015, Austin Owens, All rights reserved.

Created on March 29, 2015

@author: Austin Owens
'''

#import microcontroller

#TCB = microcontroller.MicrocontrollerDataPackets()

class BrushedThruster():
    
    def __init__(self, motorID, location, orientation):
        self.motorID = motorID #ID value that we assign to thruster
        self.location = location #[Unit in x direction, Unit in y direction, Unit in z direction] Location data currently doesn't do anything.
        self.orientation = orientation #Direction thruster is facing: 3=Positive Z-axis, 2=Positive Y-axis, 1=Positive X-axis, -1=Negative X-axis, -2=Negative Y-axis, -3=Negative Z-axis 
        
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

    def moveTranslate(self, xPwm, yPwm, zPwm):
        '''
        This function translates the sub along an axis. Assumes thrusters are symmetric.
        '''
        motorPwms = []
        
        for index, thruster in enumerate(self.thrusters): #For each thruster object..
            if thruster.orientation == 1:    #If thruster is oriented in the x axis...
                motorPwms.append(-xPwm)      #Apply reverse thrust to go in the x direction
            elif thruster.orientation == -1: #If thruster is oriented in the negative x axis...
                motorPwms.append(xPwm)       #Apply forward thrust to go in the x direction
            elif thruster.orientation == 2:  #If thruster is oriented in the y axis...
                motorPwms.append(-yPwm)      #Apply reverse thrust to go in the y direction
            elif thruster.orientation == -2: #If thruster is oriented in the negative y axis...
                motorPwms.append(yPwm)       #Apply forward thrust to go in the y direction
            elif thruster.orientation == 3:  #If thruster is oriented in the z axis...
                motorPwms.append(-zPwm)      #Apply reverse thrust to go in the z direction
            elif thruster.orientation == -3: #If thruster is oriented in the negative x axis...
                motorPwms.append(zPwm)       #Apply forward thrust to go in the z direction
                
        for index, motorPwm in enumerate(motorPwms):
            self.thrusters[index].setPWM(motorPwm) #Assign motor PWMs to objects speed variable
            self.thrusters[index].sendThrusterPacket()
            
    def moveAngular(self, xPwm, yPwm, zPwm):
        '''
        This function rotates the sub about an axis.
        '''
        motorPwms = []
        
        for index, thruster in enumerate(self.thrusters): #For each thruster object..
            #Rotates about X-axis
            if thruster.orientation == 2 and thruster.location[2] == 1:
                motorPwms.append(xPwm)  
            elif thruster.orientation == 2 and thruster.location[2] == -1:
                motorPwms.append(-xPwm)
            elif thruster.orientation == -2 and thruster.location[2] == 1:
                motorPwms.append(-xPwm)
            elif thruster.orientation == -2 and thruster.location[2] == -1:
                motorPwms.append(xPwm)
            
            #Rotates about Y-axis
            elif thruster.orientation == 1 and thruster.location[2] == 1:
                motorPwms.append(-yPwm)  
            elif thruster.orientation == 1 and thruster.location[2] == -1:
                motorPwms.append(yPwm)
            elif thruster.orientation == -1 and thruster.location[2] == 1:
                motorPwms.append(yPwm)
            elif thruster.orientation == -1 and thruster.location[2] == -1:
                motorPwms.append(-yPwm)
                
            #Rotates about Y-axis
            elif thruster.orientation == 3 and thruster.location[0] == 1:
                motorPwms.append(yPwm)  
            elif thruster.orientation == 3 and thruster.location[0] == -1:
                motorPwms.append(-yPwm)
            elif thruster.orientation == -3 and thruster.location[0] == 1:
                motorPwms.append(-yPwm)
            elif thruster.orientation == -3 and thruster.location[0] == -1:
                motorPwms.append(yPwm)
                
            #Rotates about Z-axis
            elif thruster.orientation == 2 and thruster.location[0] == 1:
                motorPwms.append(-zPwm)  
            elif thruster.orientation == 2 and thruster.location[0] == -1:
                motorPwms.append(zPwm)
            elif thruster.orientation == -2 and thruster.location[0] == 1:
                motorPwms.append(zPwm)
            elif thruster.orientation == -2 and thruster.location[0] == -1:
                motorPwms.append(-zPwm)
                
        for index, motorPwm in enumerate(motorPwms):
            self.thrusters[index].setPWM(motorPwm) #Assign motor PWMs to objects speed variable
            self.thrusters[index].sendThrusterPacket()
            
    def advancedMove(self, xPwmTranslate, yPwmTranslate, zPwmTranslate, xPwmAngular, yPwmAngular, zPwmAngular): #Put in as many PWMs as you do thrusters
        pass
            
    def simpleMove(self, *motorPwms):
        for index, motorPwm in enumerate(motorPwms):
            self.thrusters[index].setPWM(motorPwm) #Assign motor PWMs to objects speed variable
            self.thrusters[index].sendThrusterPacket()


if __name__=="__main__":
    thruster1 = BrushedThruster(1, [1, -1, 1], 2)  #Up/Down thruster
    thruster2 = BrushedThruster(2, [-1, -1, 1], 2)  #Up/Down thruster
    thruster3 = BrushedThruster(3, [1, -1, -1], 2)  #Up/Down thruster
    thruster4 = BrushedThruster(4, [-1, -1, -1], 2)  #Up/Down thruster
    thruster5 = BrushedThruster(5, [0, 0, 1], -1) #Left/Right thruster
    thruster6 = BrushedThruster(6, [0, 0, -1], -1) #Left/Right thruster
    thruster7 = BrushedThruster(7, [1, 0, 0], -3) #Fwd/Rev thruster
    thruster8 = BrushedThruster(8, [-1, 0, 0], -3) #Fwd/Rev thruster

    thrusters = [thruster1, thruster2, thruster3, thruster4, thruster5, thruster6, thruster7, thruster8]
    moveController = MovementController(thrusters)
    
    moveController.moveTranslate(255, 0, 0)
    #moveController.moveAngular(255, 255, 0)
    #moveController.advancedMove(0, 0, 0, 0, 0, 0)
    #moveController.simpleMove(255, 255, 255, 255, 0, 0, 0, 0)
