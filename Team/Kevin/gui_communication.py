'''
Created on Mar 1, 2015

@author: kevin
'''
'''
Created on Feb 27, 2015

@author: Austin
'''
import Tkinter
import tkMessageBox
from idlelib.tabbedpages import TabSet

class DvlControl:
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)

    def commInterface(self):
        pass
        
class TcbControl:
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)
  
    def commInterface(self):
        self.top.geometry("500x600+550+100")
        self.top.title("TCB Communication")
        
        #Creates a command section
        motorControlFrame = Tkinter.Frame(self.top)
        motorControlFrame.grid(row = 0, column = 0)
        
        #Creates a Motor Control label
        Tkinter.Label(motorControlFrame, text = "Motor Control", font=("TkDefaultFont", 13)).grid(row = 0, column = 0, columnspan = 2)
        
        #Motor Control buttons
        B1= Tkinter.Button(motorControlFrame, width = 10, text = "Motor 1", background = "Red")
        B1.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "s")
        B1.config(background = "Green")# to cahnges the params
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 2", background = "Red").grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 3", background = "Red").grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 4", background = "Red").grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 5", background = "Red").grid(row = 5, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 6", background = "Red").grid(row = 6, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 7", background = "Red").grid(row = 7, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 8", background = "Red").grid(row = 8, column = 0, padx = 5, pady = 5, sticky = "s")
        
        #Motor Control sliders
        motor1Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor1Scale.grid(row = 1, column = 1)
        motor2Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor2Scale.grid(row = 2, column = 1)
        motor3Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor3Scale.grid(row = 3, column = 1)
        motor4Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor4Scale.grid(row = 4, column = 1)
        motor5Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor5Scale.grid(row = 5, column = 1)
        motor6Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor6Scale.grid(row = 6, column = 1)
        motor7Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor7Scale.grid(row = 7, column = 1)
        motor8Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor8Scale.grid(row = 8, column = 1)
        
        #Creates Motor Control description labels
        Tkinter.Label(motorControlFrame, text = "Motor State").grid(row = 9, column = 0)
        Tkinter.Label(motorControlFrame, text = "Motor PWM").grid(row = 9, column = 1)
        
class Hydra_Board():
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)
       
class Sparton_AHRS():
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)

class PNI_AHRS():
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)
    
class Weapons_Control_Board():
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)
    def commInterface(self):
        self.top.geometry("500x600+550+100")
        self.top.title("Weapons Control Board")
        motorControlFrame = Tkinter.Frame(self.top)
        motorControlFrame.grid(row = 0, column = 0)
        Tkinter.Label(motorControlFrame, text = "Weapons Control", font=("TkDefaultFont", 13)).grid(row = 0, column = 0, columnspan = 1)
        Tkinter.Button(motorControlFrame, width = 20, text = "torpedo 1", background = "Red").grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 20, text = "torpedo 2", background = "Red" ).grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "s")
class Power_Monitoring_Board():
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)
        

        
        
    '''
    notes 
    TCB, add a kill switch
    TCB, add a way to send bytes 
    send a byte to all things for testing 
    show text feed back ex: fired
    pmud/ soft kill
    pmud/ alart frame with label to tell, check boxs
    '''
    