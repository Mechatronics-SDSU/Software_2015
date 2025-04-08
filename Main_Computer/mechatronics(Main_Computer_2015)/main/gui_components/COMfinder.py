'''
Copyright 2015, Austin Owens, All rights reserved.

.. module:: COMfinder
   :synopsis: Detects which daughter cards are connected and sets up Comms Tab accordingly.
   
:Author: Felipe Jared Guerrero <felipejaredgm@gmail.com>
:Date: Created on April 10, 2015
:Description: Sets up the board drop-down, method listbox, and consoles based on the connected board.
'''
import sys
import glob
import serial
import previous_state_logging_system
from serial.tools import list_ports as lp
import Tkinter, ttk
import inspect
import imp
import main.external_devices.sparton_ahrs as sparton
import main.external_devices.microcontroller_sib as sib
import main.external_devices.microcontroller_tcb as tcb
import main.external_devices.microcontroller_pmud as pmud
import main.external_devices.movement as movement

def runScript(window):
    '''
        Executes the Python code written in the Comms Tab.
        
        **Parameters**: \n
        * **window** - Main Tkinter window.
        
        **Returns**: \n
        * **No Return.**\n
        '''
    script = window.scriptText.get("1.0", "end")
    commScript = imp.new_module('commScript')
    exec(script, commScript.__dict__)
    
class UpdateBoard:
    '''
    This class detects connected boards and updates commands available on the Comms Tab.
    '''
    def __init__(self, window):
        '''
        Initializes log file and sets window as instance attribute.
        
        **Parameters**: \n
        * **window** - Main Tkinter window..
        
        **Returns**: \n
        * **No Return.**\n
        '''
        self.log = previous_state_logging_system.Log('_Saved_Settings_/_Device_ID_/_Board_Command_List_.txt')
        self.window = window  
                                  
    def update(self):
        '''
        Upadtes the methods in the listbox to match the selected board.
        
        **Parameters**: \n
        * **No Input Parameters** 
        
        **Returns**: \n
        * **No Return.**\n
        '''
        board = self.window.boardValue.get()
        self.window.commandListBox.delete(0, "end")

        optionList = []
        if board == "Sparton" or board == "Sparton6E":
            for name, obj in inspect.getmembers(sparton.SpartonAhrsDataPacket):
                if inspect.ismethod(obj):
                    if not (name.startswith("__")):
                        optionList.append([name, obj])

        if board == "TCB1" or board == "TCB2":
            for name, obj in inspect.getmembers(tcb.TCBDataPackets):
                if inspect.ismethod(obj):
                    if not (name.startswith("__")):
                        optionList.append([name, obj])

        if board == "SIB":
            for name, obj in inspect.getmembers(sib.SIBDataPackets):
                if inspect.ismethod(obj):
                    if not (name.startswith("__")):
                        optionList.append([name, obj])
                        
        if board == "PMUD":
            for name, obj in inspect.getmembers(pmud.PMUDDataPackets):
                if inspect.ismethod(obj):
                    if not (name.startswith("__")):
                        optionList.append([name, obj])
                        
        if board == "MOVEMENT":
            for name, obj in inspect.getmembers(movement.MovementController):
                if inspect.ismethod(obj):
                    if not (name.startswith("__")):
                        optionList.append([name, obj])
                        
        
        self.window.optionList = optionList
        for option in optionList:
            self.window.commandListBox.insert("end", option[0])
        
    def add_command(self):
        '''
        Adds selected method from listbox to Comms Tab code console.
        
        **Parameters**: \n
        * **No Input Parameters** 
        
        **Returns**: \n
        * **No Return.**\n
        '''
        w = self.window.commandListBox
        value = w.get(w.curselection()[0])
        for name, command in self.window.optionList:
            if value == name:
                self.window.scriptText.insert("insert", self.window.boardValue.get()+".")
                self.window.scriptText.insert("insert", command.__name__+"(")
                new_args = inspect.getargspec(command)
                for i, parameter in enumerate(new_args[0]):
                    if parameter != "self":
                        self.window.scriptText.insert("insert", new_args[0][i])
                        if i < len(new_args[0])-1:
                            self.window.scriptText.insert("insert", ", ")
        self.window.scriptText.insert("insert", ")\n")
        
    def onselect(self, event):
        '''
        Puts method documentation on Comms output console when method is selected.
        
        **Parameters**: \n
        * **event** - Event when selected command changes.
        
        **Returns**: \n
        * **No Return.**\n
        '''
        w = self.window.commandListBox
        value = w.get(w.curselection()[0])
        for name, command in self.window.optionList:
            if value == name:
                self.window.scriptOut.delete("1.0", "end")
                self.window.scriptOut.insert("insert", command.__doc__)
        
if __name__ == '__main__':
    pass
        