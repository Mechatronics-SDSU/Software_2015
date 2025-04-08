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
    script = window.scriptText.get("1.0", "end")
    commScript = imp.new_module('commScript')
    exec(script, commScript.__dict__)
    
class UpdateBoard:
    def __init__(self, window):
        self.log = previous_state_logging_system.Log('_Saved_Settings_/_Device_ID_/_Board_Command_List_.txt')
        self.window = window  
                                  
    def update(self):
        board = self.window.boardValue.get()
        self.window.commandListBox.delete(0, "end")

        optionList = []
        if board == "Sparton":
            for name, obj in inspect.getmembers(sparton.SpartonAhrsDataPacket):
                if inspect.ismethod(obj):
                    if not (name.startswith("__")):
                        optionList.append([name, obj])

        if board == "TCB":
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
    
    def update_commands(self, new_command):
        pass
        
    def add_command(self):
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
        w = self.window.commandListBox
        value = w.get(w.curselection()[0])
        for name, command in self.window.optionList:
            if value == name:
                self.window.scriptOut.delete("1.0", "end")
                self.window.scriptOut.insert("insert", command.__doc__)
    
    def load(self):
        pass
    
    def export(self):
        pass
        
if __name__ == '__main__':
    pass
        