import sys
import glob
import serial
from serial.tools import list_ports as lp
import Tkinter, ttk


class UpdateBoard:
    def __init__(self, window):
        self.window = window
        
    
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
    
    window.mainloop()
        