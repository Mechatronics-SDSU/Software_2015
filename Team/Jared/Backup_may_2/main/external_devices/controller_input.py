'''
Copyright 2014, Austin Owens, All rights reserved.

Created on Dec 25, 2014

@author: Jared
'''
import pygame
from pygame.locals import *
import os, sys
import threading
import time

class controllerResponse(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.runThread = True
        self.requestTime = 0.01 #How often I request data packets from device
        
        self.getList = []
        
    def run(self):
        
        while self.runThread:
            try:
                pygame.init()
                pygame.event.get()                  
                joystick_count = pygame.joystick.get_count()
                # assume first joystick
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
                # Get the name from the OS for the controller/joystick
                name = joystick.get_name()
                # Usually axis run in pairs, up/down for one, and left/right for the other
                num_axes = joystick.get_numaxes()    
                num_buttons = joystick.get_numbuttons()
                num_hats = joystick.get_numhats()
                axes = []
                buttons = []
                hats = []
                
                for i in range(num_axes):
                    axis = joystick.get_axis( i )
                    axes.append(axis)
                    
                for i in range(num_buttons):
                    button = joystick.get_button( i )
                    buttons.append(button)
                    
                for i in range(num_hats):
                    hat = joystick.get_hat( i )
                    hats.append(hat)
                
                time.sleep(self.requestTime)
                
                self.getList.append([name, axes, buttons, hats])
            except:
                connection = [False, False, False, False]
                self.getList.append(connection)
        
    def killThread(self):
        '''
        Ends thread process. 
        
        **Parameters**: \n
        * **No Input Parameters.**
        
        **Returns**: \n
        * **No Return.**\n
        '''
        self.runThread = False
