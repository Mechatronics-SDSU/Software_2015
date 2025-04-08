'''
Copyright 2015, Austin Owens, All rights reserved.

Created on Feb 27, 2015

@author: Kevin
'''
import Tkinter
import tkMessageBox
from idlelib.tabbedpages import TabSet
from Tkinter import *
import ttk


class DvlControl:
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)

    def commInterface(self):
        self.top.geometry("500x600+550+100")
        self.top.title("DVL")
        DVLFrame = Tkinter.Frame(self.top)
        DVLFrame.grid(row = 0, column = 0)
        
        Tkinter.Label(DVLFrame, text = "Get things", font=("TkDefaultFont", 13)).grid(row = 0, column = 0, columnspan = 2)
        
        self.box_value = StringVar()
        self.box = ttk.Combobox(DVLFrame, textvariable=self.box_value)
        self.box['values'] = ('yaw', 'pitch', 'roll','temperature','x,y,z','elevation')
        self.box.current(0)
        self.box.grid(row=1,column=0)
        Tkinter.Button(DVLFrame, width = 10, text = "on/off", background = "Red").grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(DVLFrame, width = 10, text = "send byte", background = "Red").grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "s")
        
        
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
        B1.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "s")
        #B1.config(background = "Green")# to cahnges the params
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 2", background = "Red").grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 3", background = "Red").grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 4", background = "Red").grid(row = 5, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 5", background = "Red").grid(row = 6, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 6", background = "Red").grid(row = 7, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 7", background = "Red").grid(row = 8, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "Motor 8", background = "Red").grid(row = 9, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "on/off", background = "Red").grid(row = 10, column = 0 , padx = 5, pady = 5, sticky = "s")#not done
        Tkinter.Button(motorControlFrame, width = 10, text = "send byte", background = "Red").grid(row = 10, column = 1, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(motorControlFrame, width = 10, text = "set all to zero", background = "Red").grid(row = 10, column = 2 , padx = 5, pady = 5, sticky = "s")
        
            
        #Motor Control sliders
        motor1Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor1Scale.grid(row = 2, column = 1)
        motor2Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor2Scale.grid(row = 3, column = 1)
        motor3Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor3Scale.grid(row = 4, column = 1)
        motor4Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor4Scale.grid(row = 5, column = 1)
        motor5Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor5Scale.grid(row = 6, column = 1)
        motor6Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor6Scale.grid(row = 7, column = 1)
        motor7Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor7Scale.grid(row = 8, column = 1)
        motor8Scale = Tkinter.Scale(motorControlFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")
        motor8Scale.grid(row = 9, column = 1)
        
        #Creates Motor Control description labels
        Tkinter.Label(motorControlFrame, text = "Motor State").grid(row = 1, column = 0)
        Tkinter.Label(motorControlFrame, text = "Motor PWM").grid(row = 1, column = 1)
        Tkinter.Label(motorControlFrame, text = "Pick motor state").grid(row = 11, column = 0)
        
        #makeing the drop down
        
        self.box_value = StringVar()
        self.box = ttk.Combobox(motorControlFrame, textvariable=self.box_value)
        self.box['values'] = ('right', 'left', 'I am lazy')
        self.box.current(0)
        self.box.grid( row=12, column=0)
        
        def Zero():#this is in testing
            motor1Scale.config(to=0)
            motor2Scale.config(to=0)
            motor3Scale.config(to=0)
            motor4Scale.config(to=0)
            motor5Scale.config(to=0)
            motor6Scale.config(to=0)
            motor7Scale.config(to=0)
            motor8Scale.config(to=0)

        
class Hydra_Board():#needs alot of work
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)
    def commInterface(self):
        self.top.geometry("500x600+550+100")
        self.top.title("Hydra Board")
        HydraFrame = Tkinter.Frame(self.top)
        HydraFrame.grid(row = 0, column = 0)
        
        #Tkinter.Label(HydraFrame, text = "Hydra Board", font=("TkDefaultFont", 13)).grid(row = 0, column = 0, columnspan = 2)
        
        Tkinter.Button(HydraFrame, width = 10, text = "send byte", background = "Red").grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(HydraFrame, width = 10, text = "on/off", background = "Red").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "s")
        
       
class Sparton_AHRS():
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)
    def commInterface(self):
        self.top.geometry("500x600+550+100")
        self.top.title("Sparton AHRS")
        SpartonFrame = Tkinter.Frame(self.top)
        SpartonFrame.grid(row = 0, column = 0)
        
        #Tkinter.Label(SpartonFrame, text = "Sparton AHRS", font=("TkDefaultFont", 13)).grid(row = 0, column = 0, columnspan = 2)
        
        Tkinter.Button(SpartonFrame, width = 10, text = "send byte", background = "Red").grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(SpartonFrame, width = 10, text = "on/off", background = "Red").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "s")
        
        Tkinter.Label(SpartonFrame, text = "pick an AHRS", font=("TkDefaultFont", 13)).grid(row = 2, column = 0, columnspan = 1)
        self.box_value = StringVar()
        self.box = ttk.Combobox(SpartonFrame, textvariable=self.box_value)
        self.box['values'] = ('AHRS 1', 'AHRS 2')
        self.box.current(0)
        self.box.grid(row=3,column=0)
        
        Tkinter.Label(SpartonFrame, text = "Get things", font=("TkDefaultFont", 13)).grid(row = 4, column = 0, columnspan = 1)
        self.box_value = StringVar()
        self.box = ttk.Combobox(SpartonFrame, textvariable=self.box_value)
        self.box['values'] = ('yaw', 'pitch','roll','other things')
        self.box.current(0)
        self.box.grid(row=5,column=0)
        
class PNI_AHRS():
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)
    def commInterface(self):
        self.top.geometry("500x600+550+100")
        self.top.title("PNI AHRS")
        PNIFrame = Tkinter.Frame(self.top)
        PNIFrame.grid(row = 0, column = 0)
        
        #Tkinter.Label(PNIFrame, text = "PNI AHRS", font=("TkDefaultFont", 13)).grid(row = 0, column = 0, columnspan = 2)
        
        Tkinter.Button(PNIFrame, width = 10, text = "send byte", background = "Red").grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(PNIFrame, width = 10, text = "on/off", background = "Red").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "s")
        
        Tkinter.Label(PNIFrame, text = "pick an AHRS", font=("TkDefaultFont", 13)).grid(row = 2, column = 0, columnspan = 1)
        self.box_value = StringVar()
        self.box = ttk.Combobox(PNIFrame, textvariable=self.box_value)
        self.box['values'] = ('AHRS 1', 'AHRS 2')
        self.box.current(0)
        self.box.grid(row=3,column=0)
        
        Tkinter.Label(PNIFrame, text = "Get things", font=("TkDefaultFont", 13)).grid(row = 4, column = 0, columnspan = 1)
        self.box_value = StringVar()
        self.box = ttk.Combobox(PNIFrame, textvariable=self.box_value)
        self.box['values'] = ('yaw', 'pitch','roll','other things')
        self.box.current(0)
        self.box.grid(row=5,column=0)
        
    
class Weapons_Control_Board():
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)
    def commInterface(self):
        self.top.geometry("500x600+550+100")
        self.top.title("Weapons Control Board")
        weaponsControlFrame = Tkinter.Frame(self.top)
        weaponsControlFrame.grid(row = 0, column = 0)
        
        #Tkinter.Label(weaponsControlFrame, text = "Weapons Control Board", font=("TkDefaultFont", 13)).grid(row = 0, column = 0, columnspan = 2)
        
        Tkinter.Button(weaponsControlFrame, width = 20, text = "torpedo 1", background = "Red").grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(weaponsControlFrame, width = 20, text = "torpedo 2", background = "Red" ).grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(weaponsControlFrame, width = 10, text = "send byte", background = "Red").grid(row = 6, column = 0, padx = 5, pady = 5, sticky = "s")
        Tkinter.Button(weaponsControlFrame, width = 10, text = "on/off", background = "Red").grid(row = 8, column = 0, padx = 5, pady = 5, sticky = "s")

class Power_Monitoring_Board():#rework
    def __init__(self, window):
        self.window = window
        self.top = Tkinter.Toplevel(self.window)
    def commInterface(self):
        self.top.geometry("500x600+550+100")
        self.top.title("Power Monitoring Board")
        PMUDFrame = Tkinter.Frame(self.top)
        PMUDFrame.grid(row = 0, column = 0)
        Tkinter.Button(PMUDFrame, width = 20, text = "torpedo 2", background = "Red" ).grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "s")
        
        self.box_value = StringVar()
        self.box = ttk.Combobox(PMUDFrame, textvariable=self.box_value)
        self.box['values'] = ('X', 'Y', 'Z')
        self.box.current(0)
        self.box.grid(row=1,column=0)
    
        
    
        

        
        
    '''
    notes 
    TCB, add a kill switch
    TCB, add a way to send bytes 
    send a byte to all things for testing 
    pmud/ soft kill
    pmud/ alart frame with label to tell, check boxs
    '''
    