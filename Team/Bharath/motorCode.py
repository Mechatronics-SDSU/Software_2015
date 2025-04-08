#!/usr/bin/python
from abc import ABCMeta, abstractmethod

'''
    Thruster is parent class of Brushless thruster. We have made this class as abstract
    because, in future we might need to create many more sub thruster classes
'''
class Thruster():

    __metaclass__ = ABCMeta
    pass
        
'''
    BrushlessThruster is a type of motor we are using. This class inherits properties from 
    parent Thruster class.
'''
class BrushlessThruster(Thruster):

    def __init__(self,motorID,location,direction):
        self.direction = direction
        self.location = location
        self.motorID = motorID
        self.speed = 0  #intial speed will be zero
    
    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self,speed):

        if speed > 80:
            self.__speed = 80
        elif speed < -80:
            self.__speed = -80
        else:
            self.__speed = speed


'''
    Movement is abstract class. All subclasses of Movement has to implement move method
'''
class Movement():

    __metaclass__ = ABCMeta

    @abstractmethod
    def move(self):
        pass

'''
    MovementOne is subclass of Movement. This class name has to be changed to some thing else.
    We are not using any of stabilizaionDirectionArray and stabilization module. As Austin is
    re writing stabilization module.
'''
class MovementOne(Movement):

    def __init__(self):

        pass

    
    def move(self,heave,sway,surge,clockwise = False):

        
        up,down,left,right,forward,backward = 0,0,0,0,0,0
                
        if sway > 0:
            left,right = 0,sway
        else:
            left,right = sway,0

        if clockwise:
            print "inside clockwise and anticlockwise",left,right
            return up,down,up,down,left,right,forward,backward
        
        if heave > 0:
            up,down = 0,heave
        else:
            up,down = heave,0

        if surge > 0:
            forward,backward = surge, 0
        else:
            forward,backward = 0,surge


        return up,down,up,down,left,right,forward,backward

'''
    RobotController is context class, which has instance of both MovementOne and BrushlessThruster.
    Using instance of this two classes. It controls movement of robosub.
'''

class RobotController():

    def __init__(self):
        self.movementController = MovementOne()
        self.thrusterMotor = self.motorInitialise()

    
    def motorInitialise(self):
        thursterList = []
        location = None
        for i in xrange(0,8):
            if i == 0:
                location = (-1,-1,1)
            if i == 1:
                location = (1,-1,1)
            if i == 2:
                location = (1,-1,-1)
            if i == 3:
                location = (-1,-1,-1)
            if i == 4:
                location = (1,0,0)
            if i == 5:
                location = (-1,0,0)
            if i == 6:
                location = (0,0,-1)
            if i == 7:
                location = (0,0,1)
            '''if i in (0,1,2,3):
                direction  = "Up,Down"
            elif i in (4,5):
                direction = "Left,Right"
            else:
                direction = "Forward,Backward"'''
            thursterList.append(BrushlessThruster(i+1,location,0))

        return thursterList
        #print self.thrusterMotor
    def printThrusterValues(self):
        for thruster in self.thrusterMotor:
            print thruster.speed,thruster.motorID,thruster.direction,thruster.location
        
    def setThrusterMotorPwm(self,args):
        index = 0
        #print len(self.thrusterMotor)
        for i in args:
            self.thrusterMotor[index].speed = i
            #print self.thrusterMotor[index].speed,self.thrusterMotor[index].motorID,self.thrusterMotor[index].direction
            index += 1

    #def move(self,heave,sway,surge,clockwise = False):
    def move(self,*arg):
        
        if len(arg) == 8:
            self.setThrusterMotors(arg[0],arg[1],arg[2],arg[3],arg[4],arg[5],arg[6],arg[7])
        elif len(arg) == 4:
            self.setThrusterMotorPwm(self.movementController.move(arg[0],arg[1],arg[2],arg[3]))
        else:
            self.setThrusterMotorPwm(self.movementController.move(arg[0],arg[1],arg[2]))
        
    def setThrusterMotors(self,motorOne,motorTwo,motorThree,motorFour,motorFive,motorSix,motorSeven,motorEight):
        
        self.thrusterMotor[0].speed = motorOne
        self.thrusterMotor[1].speed = motorTwo
        self.thrusterMotor[2].speed = motorThree
        self.thrusterMotor[3].speed = motorFour
        self.thrusterMotor[4].speed = motorFive
        self.thrusterMotor[5].speed = motorSix
        self.thrusterMotor[6].speed = motorSeven
        self.thrusterMotor[7].speed = motorEight


if __name__=="__main__":

    one = RobotController()
    one.move(-3,2,5)       
    one.printThrusterValues() 
    one.move(100,-300,40)
    one.printThrusterValues()
    one.move(0,30,0,True)
    one.printThrusterValues()
    one.move(30,0,0,0,0,0,0,0)
    one.printThrusterValues()
