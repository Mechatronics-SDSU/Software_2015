'''
Created on Jun 4, 2015

@author: Jard
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
        menu = self.window.commandOptions["menu"]
        menu.delete(0, "end")
        #if len(board) > 0:
         #   optionList = self.log.getParameters(board)
          #  options = optionList.
        optionList = []
        if board == "Sparton":
            for name, obj in inspect.getmembers(sparton.SpartonAhrsDataPacket):
                if inspect.ismethod(obj):
                    if not (name.startswith("__")):
                        optionList.append([name, obj])
            #spartonList = self.log.getParameters("Sparton")
            #optionList = spartonList.Sparton

        if board == "TCB":
            for name, obj in inspect.getmembers(tcb.TCB1DataPackets):
                if inspect.ismethod(obj):
                    if not (name.startswith("__")):
                        optionList.append([name, obj])
                    
            #TCBList = self.log.getParameters("TCB")
            #optionList = TCBList.TCB

        if board == "SIB":
            for name, obj in inspect.getmembers(sib.SIBDataPackets):
                if inspect.ismethod(obj):
                    if not (name.startswith("__")):
                        optionList.append([name, obj])
            #MicrocontrollerList = self.log.getParameters("Microcontroller")
            #optionList = MicrocontrollerList.Microcontroller

        for option in optionList:
            menu.add_command(label=option[0], command = lambda value=option: self.update_commands(value))
        self.window.commandValue.set(optionList[0][0])
    
    def update_commands(self, new_command):
        self.window.commandValue.set(new_command[0])
        self.window.scriptOut.delete("1.0", "end")
        self.window.scriptOut.insert("insert", new_command[1].__doc__)
        self.window.scriptText.insert("insert", new_command[1].__name__+"(")
        #for i, parameter in enumerate(new_command[1].func_code.co_varnames):
        new_args = inspect.getargspec(new_command[1])
        for i, parameter in enumerate(new_args[0]):
            if parameter != "self":
                self.window.scriptText.insert("insert", new_args[0][i])
                if i < len(new_args[0])-1:
                    self.window.scriptText.insert("insert", ", ")
        self.window.scriptText.insert("insert", ")\n")
    
    def load(self):
        pass
    
    def export(self):
        pass
    
        
def serial_ports():
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def findPort(board):
    available_ports = lp.comports()
    portFound = False
    for port in available_ports:
        print port
        if board == "SPARTON":
            if port[2] == 'FTDIBUS\\VID_0403+PID_6001+FTFUT6OLA\\0000':
                portFound = True
                return serial.Serial(port[0], 9600)
            elif port[2] == 'FTDIBUS\\VID_0403+PID_6001+A900X4K5A\\0000':
                portFound = True
                return serial.Serial(port[0], 9600)
        if board == "PMUD":
            if port[2] == 'PutDeviceIDhere':
                portFound = True
                return serial.Serial(port[0], 9600)
        if board == "SIB":
            if port[2] == 'PutDeviceIDhere':
                portFound = True
                return serial.Serial(port[0], 9600)
        if board == "TCB":
            if port[2] == 'PutDeviceIDhere':
                portFound = True
                return serial.Serial(port[0], 9600)
        if portFound == True:
            break
    if portFound == False:
        return #What to put here??
        
        
if __name__ == '__main__':
    print(serial_ports())
    available_ports = lp.comports()
    boards = []
    for port in available_ports:
        print port
        #counter += 1
        if port[2] == 'FTDIBUS\\VID_0403+PID_6001+FTFUT6OLA\\0000':
            print "Sparton 6E located in " + port[0]
            boards.append("Sparton 6E")
        if port[2] == 'FTDIBUS\\VID_0403+PID_6001+A900X4K5A\\0000':
            print "Sparton 6 located in " + port[0]
            boards.append("Sparton 6")
    window = Tkinter.Tk()
    window.geometry("800x400+0+0") #"1590x870+0+0"
    window.title("COM boards")
    tab = Tkinter.Frame(window)
    tab.grid(row = 0, column = 0)
    Tkinter.Label(tab, text = "Boards", font=("TkDefaultFont", 13)).grid(row = 0, column = 0, columnspan = 2)
    box_value = Tkinter.StringVar()
    box_value.set("")
    boards.append("Sparton")
    boards.append("TCB")
    boards.append("DVL")
    if len(boards) > 0:
        i = len(boards)
        options = apply(Tkinter.OptionMenu, (tab, box_value) + tuple(boards))
    else:
        options = Tkinter.OptionMenu(tab, box_value, '')
    options.grid(row=1,column=0)
    '''box = ttk.Combobox(tab, textvariable=box_value)
    if len(boards) > 0:
        box['values'] = (boards)
    else:
        box['values'] = ('A', 'B')
    box.current(0)
    box.grid(row=1,column=0)'''
    #print sparton.SpartonAhrsDataPacket.accelerationVectorGet.__name__
    #for name, obj in inspect.getmembers(sparton.SpartonAhrsDataPacket):
     #   if inspect.ismethod(obj):
      #      print name
       #     print obj.__doc__
    print inspect.getmembers(sparton.SpartonAhrsDataPacket)[0]
    #print inspect.getdoc(SPA.SpartonAhrsDataPacket.rawAccelerationGet)
    window.mainloop()
        