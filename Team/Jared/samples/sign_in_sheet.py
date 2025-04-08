import Tkinter
import tkMessageBox
import ttk
import ctypes
from Tkconstants import *
import database
from Tkinter import IntVar, Frame
import sys

top = Tkinter.Tk()
top.title("Sign in")
screenRes = ctypes.windll.user32.GetSystemMetrics(0)-10, ctypes.windll.user32.GetSystemMetrics(1)-30
guiWidth, guiHeight, guiXPosition, guiYPosition = screenRes[0]/2, screenRes[1], screenRes[0]/4, 0
top.geometry(str(guiWidth)+"x"+str(guiHeight)+"+"+str(guiXPosition)+"+"+str(guiYPosition))

class Application():
    def __init__(self):

        self.robo_names, self.mech_names = database.rollList()
        self.notebook = ttk.Notebook(top)
        self.notebook.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        self.robo_tab = Tkinter.Frame(self.notebook, width=1000, height=200)
        self.robo_tab.place()
        self.notebook.add(self.robo_tab, text="Robosub")
        self.robo = None
        self.mech = None
        
        self.mech_tab = Tkinter.Frame(self.notebook, width=1000, height=200)
        self.mech_tab.place()
        self.notebook.add(self.mech_tab, text="Mechatronics 101")
        
        self.field = None
        self.E1 = Tkinter.Entry
        self.E2 = Tkinter.Entry
        self.E3 = Tkinter.Entry
        
    def __retrieveInput__(self):
        print self.E1.get()
        print self.E2.get()
        tab_name = self.notebook.tab(self.notebook.select(), "text")
        database.insertNewMember(tab_name, self.E1.get(), self.E2.get(), self.E3.get())
        self.field.destroy()
        self.__guiUpdate__()
        
    def __popUp__(self):
        wt = self.notebook.tab(self.notebook.select(), "text")
        if wt == "Robosub":
            print "Robosub"
        self.field = Tkinter.Tk()
        self.field.title("Sign up")
        L1 = Tkinter.Label(self.field, text="Name")
        L1.grid(row = 1)
        self.E1 = Tkinter.Entry(self.field, bd =5)
        self.E1.grid(row = 1, column = 2)
            
        L2 = Tkinter.Label(self.field, text="Red ID")
        L2.grid(row = 2)
        self.E2 = Tkinter.Entry(self.field, bd =5)
        self.E2.grid(row = 2, column = 2)
        
        L3 = Tkinter.Label(self.field, text="Major")
        L3.grid(row = 3)
        self.E3 = Tkinter.Entry(self.field, bd =5)
        self.E3.grid(row = 3, column = 2)
        self.robo.getList()
        
        B = Tkinter.Button(self.field, text ="Enter", command = self.__retrieveInput__)
        B.grid(row = 4, column = 2)
        
    def guiSetup(self):#creates the gui
        self.robo = Checkbar(self.robo_tab, self.robo_names)
        self.robo.place(x = 20, y = 30)
        self.mech = Checkbar(self.mech_tab, self.mech_names)
        self.mech.place(x = 20, y = 30)
        B = Tkinter.Button(top, text ="Sign Up", command = self.__popUp__)
        B.place(x=325, y=25, anchor=N)
        B = Tkinter.Button(top, text ="Close", command = self.__list__)
        B.pack(side = BOTTOM)
        
    def __guiUpdate__(self):
        self.robo_names, self.mech_names = database.rollList()
        robo = Checkbar(self.robo_tab, self.robo_names)
        robo.place(x = 20, y = 30)
        mech = Checkbar(self.mech_tab, self.mech_names)
        mech.place(x = 20, y = 30)
        
    def __list__(self):
        tab_name = self.notebook.tab(self.notebook.select(), "text")
        if tab_name == "Robosub":
            names = self.robo.getList()
        elif tab_name == "Mechatronics 101":
            names = self.mech.getList()
        database.rollCallFinished(names, tab_name)
        sys.exit(0)
        
    def run(self):
        top.mainloop()

class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=Tkinter.W):
        Frame.__init__(self, parent)
        self.vars = []
        i = 0
        for pick in picks:
            var = IntVar()
            chk = Tkinter.Checkbutton(self, text=pick, variable=var)
            if i < 20:
                chk.grid(column = 0)
            elif i < 40:
                chk.grid(column = 1)
            elif i < 60:
                chk.grid(column = 2)
            i += 1
            self.vars.append((var, pick))
    def state(self):
        return map((lambda var: var.get()), self.vars)
    def getList(self):
        names = []
        for var, name in self.vars:
            if var.get() == 1:
                names.append(name)
                return names

if __name__ == '__main__':
    sign_in = Application()
    sign_in.guiSetup()
    sign_in.run()