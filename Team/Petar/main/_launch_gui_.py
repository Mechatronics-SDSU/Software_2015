import psutil, os, sys; psutil.Process(os.getpid()).set_nice(psutil.REALTIME_PRIORITY_CLASS) #Setting this process to real time for CPU
import multiprocessing
import Tkinter, ttk
import gui_components.event_handlers as event_handlers
import gui_components.update_gui as update_gui
import external_devices._navigation_management_system_ as _navigation_management_system_
import gui_components.mission_selector_system as mission_selector_system
import ctypes
import gui_components.previous_state_logging_system as previous_state_logging_system


DEBUG = False
screenRes = ctypes.windll.user32.GetSystemMetrics(0)-10, ctypes.windll.user32.GetSystemMetrics(1)-30
guiWidth, guiHeight, guiXPosition, guiYPosition = screenRes[0], screenRes[1], 0, 0
rawImgWidth, rawImgHeight = int(screenRes[0]/2.5), int(screenRes[1]/2)
processedImgWidth, processedImgHeight = int(screenRes[0]/3.4), int(screenRes[1]/3.45)
process = None; parent_conn = None #Variables for multiprocessing

window = Tkinter.Tk()

eventHandlers = event_handlers.EventHandlers(guiWidth, rawImgWidth)

NMS = _navigation_management_system_.NavigationManagementSystem()

GUI = None #Initializing GUI

class StartVehicle:
    def __init__(self, notebook, missionSelectorButtonList):
        self.notebook = notebook
        self.missionSelectorButtonList = missionSelectorButtonList
          
    def start(self, startButton, stopButton):
        #Disables Vehicle Tests tab
        self.notebook.tab(2, state = "disable") #2 indicates the tab index
        
        #Disable Up, Down, Add, Delete, and Load buttons
        for x in range(len(self.missionSelectorButtonList)):
            self.missionSelectorButtonList[x].config(state = "disable")
        
        #Disable start mission button
        startButton.config(state = "disable")
        
        #Enable abort mission button
        stopButton.config(state = "normal")
    
    def stop(self, startButton, stopButton):
        #Enable Vehicle Tests tab
        self.notebook.tab(2, state = "normal") #2 indicates the tab index
        
        #Enable Up, Down, Add, Delete, and Load buttons
        for x in range(len(self.missionSelectorButtonList)):
            self.missionSelectorButtonList[x].config(state = "normal")
        
        #Enable start mission button
        startButton.config(state = "normal")
        
        #Disable abort mission button
        stopButton.config(state = "disable")
     
class StartManual():
    def __init__(self, window, tab, notebook, missionSelectorButtonList):
        self.window = window
        self.notebook = notebook
        self.missionSelectorButtonList = missionSelectorButtonList
        self.tab = tab
        self.controllerScreen = window.controllerScreen
        #self.control = ci.controller()
        
    def __controllerSetup__(self):
        self.controllerScreen.place(relx = 0.25, rely = 0, relwidth = 0.5, relheight = 1)
        self.window.setToManual = 0
        #self.control.run(self.controllerScreen, self.window)
        
    def start(self, manualButton, stopButton):
        #Disables Vehicle Tests tab
        self.notebook.tab(2, state = "disable") #2 indicates the tab index
        
        #Disable Up, Down, Add, Delete, and Load buttons
        for x in range(len(self.missionSelectorButtonList)):
            self.missionSelectorButtonList[x].config(state = "disable")
            
        #Enable controller select buttons
        stopButton.config(state = "normal")
        
        #Disable manual control button
        manualButton.config(state = "disable")
        
        #Setup controller screen
        self.__controllerSetup__()
        
    def stop(self, manualButton, stopButton):
        #Enable Vehicle Tests tab
        self.notebook.tab(2, state = "normal") #2 indicates the tab index
        
        #Enable Up, Down, Add, Delete, and Load buttons
        for x in range(len(self.missionSelectorButtonList)):
            self.missionSelectorButtonList[x].config(state = "normal")
        
        #Enable manual control button
        manualButton.config(state = "normal")
        
        #Disable abort mission button
        stopButton.config(state = "disable")
        
        #Stop the controller
        self.window.setToManual = 2
                
        #Remove controller screen
        self.controllerScreen.place_forget()
        
toggleButton = False
class ImageProcessingToggleButton():
    def __init__(self, window):
        self.window = window
        
    def toggle(self, imageProcessingToggleButton, frontProcessedImgLabel, bottomProcessedImgLabel, filterScales, filterNames, objectDetectScales, objectDetectNames):
        global toggleButton
        
        toggleButton = not toggleButton
        
        if toggleButton == True: #In object detect panel
            
            for x in range(len(filterScales)): #Remove filter scales and names
                filterScales[x].grid_remove()
                filterNames[x].grid_remove()
                
            for x in range(len(objectDetectScales)): #Add object detect scales and names
                objectDetectScales[x].grid()
                objectDetectNames[x].grid()
            
            imageProcessingToggleButton.config(text="Filters")
            
        elif toggleButton == False: #In Filter panel
            
            for x in range(len(filterScales)): #Add filter scales and names
                filterScales[x].grid()
                filterNames[x].grid()
                
            for x in range(len(objectDetectScales)): #Remove object detect scales and names
                objectDetectScales[x].grid_remove()
                objectDetectNames[x].grid_remove()

            imageProcessingToggleButton.config(text="Object Detection")

class Refresh():
    def __init__(self, event, args):
        args[0].update()

class StdoutRedirector(object): #This is to take the stdout away from eclipse and give it to the GUI
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

class clear:
    def __init__(self, consolText):
        self.text = consolText.delete("1.0", "end") #get text from line 1, character 0
        
class export: #This is to export the console text to a file
    def __init__(self, consolText):
        self.top = Tkinter.Toplevel(window)
        self.top.geometry("220x30+690+250")
        self.text = consolText.get("1.0", "end") #get text from line 1, character 0
        if not os.path.exists('_Console_Logs_'):
            os.mkdir('_Console_Logs_')
        
        self.userInput = 0
        
        self.writeToFile()
        
    def writeToFile(self):
        self.userInput = Tkinter.Entry(self.top)
        self.userInput.grid(row=0, column=1)
        self.userInput.focus_set()

        popUp = Tkinter.Label(self.top, text = "File name:")
        popUp.grid(row=0, column=0)
        self.userInput.bind("<Return>", self.ok)
        
        button = Tkinter.Button(self.top, text="OK", command = self.ok)
        button.grid(row=0, column=3, columnspan=2)

    def ok(self, *event):
        f = open('_Console_Logs_/'+self.userInput.get(), 'a')
        f.write(self.text)
        f.close()  
        self.top.destroy()
            

class GuiCreation:
    def __init__(self):
        self.parent_conn = parent_conn
        self.process = process
        
    def setQuitFlag(self):
        window.quitFlag = True
        
    def updateGUI(self, window):
        if window.quitFlag:
            if not DEBUG:
                self.process.terminate()
            window.destroy()  #This avoids the update event being in limbo
    
        else:
            GUI.run()
            if not DEBUG:
                if self.parent_conn.poll() == True:
                    window.externalDevicesData = self.parent_conn.recv()
            window.after(0, func=lambda: self.updateGUI(window))
        
    def guiSetup(self):
        global GUI
        
        #CREATE GUI OBJECT
        window.geometry(str(guiWidth)+"x"+str(guiHeight)+"+"+str(guiXPosition)+"+"+str(guiYPosition)) #"1590x870+0+0"
        window.title("Mechatronics RoboSub GUI")
        eventHandlers.initilizeGuiEvents(window)
        window.bind("<Key>", eventHandlers.guiKeyboardEvent)
        setattr(window, 'quitFlag', False) #A main Python function that gives functions new attributes/variables
        setattr(window, 'spaceBar', False)
        setattr(window, 'captureImg', [False, False])
        setattr(window, 'recordImg', [False, False])
        setattr(window, 'pictureCount', [0, 0])
        setattr(window, 'recordCount', [0, 0])
        setattr(window, 'secondsPerFrame', [0, 0])
        
        
        #CREATE TOOLBAR
        toolBar = Tkinter.Menu(window)
        window.config(menu=toolBar)
        
        fileMenu = Tkinter.Menu(toolBar)
        fileMenu.add_command(label="Freeze Raw Images                               space")
        fileMenu.add_command(label="Capture Front Image                            c")
        fileMenu.add_command(label="Capture Bottom Image                        ctrl+c")
        fileMenu.add_command(label="Record Front Image                              r")
        fileMenu.add_command(label="Record Bottom Image                          ctrl+r")
        fileMenu.add_command(label="Next Processed Front Image                z")
        fileMenu.add_command(label="Previous Processed Front Image         x")
        fileMenu.add_command(label="Next Processed Bottom Image           ctrl+z")
        fileMenu.add_command(label="Previous Processed Bottom Image    ctrl+x")
        fileMenu.add_command(label="Exit                                                          esc")
        toolBar.add_cascade(label="Window", menu=fileMenu)
        
        fileMenu = Tkinter.Menu(toolBar)
        fileMenu.add_command(label="Add User             ctrl+a")
        fileMenu.add_command(label="Delete User         ctrl+d")
        toolBar.add_cascade(label="Users", menu=fileMenu)
        
        fileMenu = Tkinter.Menu(toolBar)
        toolBar.add_cascade(label="Help", menu=fileMenu)

        
        #LABEL FOR FRONT CAMERA
        frontRawImgLabel = Tkinter.Label(window, background = "gray")  #The raw image for the front camera will go here
        frontRawImgLabel.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 0.5) #Can only choose pack, grid, place, or grid & place in one Tk() instance only    
        eventHandlers.initilizeFrontRawImgEvents(frontRawImgLabel)
        frontRawImgLabel.bind("<Button-1>", eventHandlers.frontRawImgMouseEvent)
        frontRawImgLabel.bind("<ButtonRelease-1>", eventHandlers.frontRawImgMouseEvent)
        frontRawImgLabel.bind("<B1-Motion>", eventHandlers.frontRawImgDraw)
        setattr(window, "frontRawImgLabel", frontRawImgLabel)
        setattr(frontRawImgLabel, 'mouseDragLocation', [0, 0])
        setattr(frontRawImgLabel, 'boxPoint1', [0, 0])
        setattr(frontRawImgLabel, 'boxPoint2', [0, 0])
        setattr(frontRawImgLabel, 'buttonPressed', False)
        setattr(frontRawImgLabel, 'buttonReleased', False)
        
        #LABEL FOR BOTTOM CAMERA
        bottomRawImgLabel = Tkinter.Label(window, background = "gray")  #The raw image for the front camera will go here
        bottomRawImgLabel.place(relx = 0.5, rely = 0, relwidth = 0.5, relheight = 0.5)
        eventHandlers.initilizeBottomRawImgEvents(bottomRawImgLabel)
        bottomRawImgLabel.bind("<Button-1>", eventHandlers.bottomRawImgMouseEvent)
        bottomRawImgLabel.bind("<ButtonRelease-1>", eventHandlers.bottomRawImgMouseEvent)
        bottomRawImgLabel.bind("<B1-Motion>", eventHandlers.bottomRawImgDraw)
        setattr(window, "bottomRawImgLabel", bottomRawImgLabel)
        setattr(bottomRawImgLabel, 'mouseDragLocation', [0, 0])
        setattr(bottomRawImgLabel, 'boxPoint1', [0, 0])
        setattr(bottomRawImgLabel, 'boxPoint2', [0, 0])
        setattr(bottomRawImgLabel, 'buttonPressed', False)
        setattr(bottomRawImgLabel, 'buttonReleased', False)
        
        setattr(window, 'frontXZCounter', 0)
        setattr(window, 'bottomXZCounter', 0)
        setattr(window, 'imagingFilterCount', 0)
          
        #CREATING TABS
        notebook = ttk.Notebook(window)
        notebook.place(relx = 0, rely = 0.5, relwidth = 1, relheight = 0.5)
        
        tab1 = Tkinter.Frame(notebook, width=1000, height=200)
        tab1.place()
        notebook.add(tab1, text="Image Processing")
        
        tab2 = Tkinter.Frame(notebook, width=1000, height=200)
        tab2.place()
        notebook.add(tab2, text="Mission Selector")
        
        tab3 = Tkinter.Frame(notebook, width=1000, height=200)
        tab3.place()
        notebook.add(tab3, text="Vehicle Tests")
        
        tab4 = Tkinter.Frame(notebook, width=1000, height=200)
        tab4.place()
        notebook.add(tab4, text="Console")
        
        tab5 = Tkinter.Frame(notebook, width=1000, height=200)
        tab5.place()
        notebook.add(tab5, text="Graphics Settings")
        
        tab6 = Tkinter.Frame(notebook, width=1000, height=200)
        tab6.place()
        notebook.add(tab6, text="Manual Control")
        
        #processed img 1
        filterScales = []
        filterNames = []
        frontProcessedImgFrame = Tkinter.Frame(tab1)
        frontProcessedImgFrame.place(relx = 0.22, rely = 0.52, anchor = "center")
        
        names = ["Min Hue", "Min Saturation", "Min Value", "Max Hue", "Max Saturation", "Max Value", "  Erode 1/Dilate 1", "     Intensity 1", "  Erode 2/Dilate 2", "     Intensity 2"]
        for x in range(3):
            filterScales.append(Tkinter.Scale(frontProcessedImgFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")) #Creating sliders
            filterScales[x].grid(row = x*2, column = 0)
            filterNames.append(Tkinter.Label(frontProcessedImgFrame, text = names[x], font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
            filterNames[x].grid(row = x*2 + 1, column = 0)
        
        frontProcessedImgLabel = Tkinter.Label(frontProcessedImgFrame) #The processed image for the front camera will go here
        frontProcessedImgLabel.grid(row = 0, column = 1, rowspan = 6, columnspan = 4)
        setattr(window, "frontProcessedImgLabel", frontProcessedImgLabel)
        
        for x in range(3):
            filterScales.append(Tkinter.Scale(frontProcessedImgFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")) #Creating sliders
            filterScales[3+x].grid(row = x*2, column = 5)
            filterNames.append(Tkinter.Label(frontProcessedImgFrame, text = names[x+3], font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
            filterNames[3+x].grid(row = x*2 + 1, column = 5)
            
        for x in range(4):
            filterScales.append(Tkinter.Scale(frontProcessedImgFrame, from_ = 0, to = 1 + 24*(x%2), width = 15, length=90)) #Creating sliders
            filterScales[6+x].grid(row = 7, column = x+1)
            filterNames.append(Tkinter.Label(frontProcessedImgFrame, text = names[x+6], font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
            filterNames[6+x].grid(row = 8, column = x+1)
        
        #drop down menu
        dropBoxImageProcessingValue = Tkinter.StringVar(tab1)
        dropBoxImageProcessingValue.set("") # default value
        optionMenu = Tkinter.OptionMenu(tab1, dropBoxImageProcessingValue, "")
        optionMenu.place(relx = 0.5, rely = 0.2, anchor = "center")
        optionMenu.bind("<Button-1>", lambda event, args=[window]: Refresh(event, args)) #This is to stop the gui from flickering
        
        setattr(window, "optionMenu", optionMenu) #This is so the mission selector system can update tab1
        setattr(window, "dropBoxImageProcessingValue", dropBoxImageProcessingValue) #This is so the mission selector system can update tab1

        #processed img 2
        bottomProcessedImgFrame = Tkinter.Frame(tab1)
        bottomProcessedImgFrame.place(relx = 0.78, rely = 0.52, anchor = "center")
        
        for x in range(3):
            filterScales.append(Tkinter.Scale(bottomProcessedImgFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")) #Creating sliders
            filterScales[10+x].grid(row = x*2, column = 0)
            filterNames.append(Tkinter.Label(bottomProcessedImgFrame, text = names[x], font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
            filterNames[10+x].grid(row = x*2 + 1, column = 0)
        
        bottomProcessedImgLabel = Tkinter.Label(bottomProcessedImgFrame) #The processed image for the bottom camera will go here
        bottomProcessedImgLabel.grid(row = 0, column = 1, rowspan = 6, columnspan = 4)
        setattr(window, "bottomProcessedImgLabel", bottomProcessedImgLabel)
        
        for x in range(3):
            filterScales.append(Tkinter.Scale(bottomProcessedImgFrame, from_ = 0, to = 255, width = 15, orient = "horizontal")) #Creating sliders
            filterScales[13+x].grid(row = x*2, column = 5)
            filterNames.append(Tkinter.Label(bottomProcessedImgFrame, text = names[x+3], font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
            filterNames[13+x].grid(row = x*2 + 1, column = 5)
            
        for x in range(4):
            filterScales.append(Tkinter.Scale(bottomProcessedImgFrame, from_ = 0, to = 1 + 49*(x%2), width = 15, length=90)) #Creating sliders
            filterScales[16+x].grid(row = 7, column = x+1)
            filterNames.append(Tkinter.Label(bottomProcessedImgFrame, text = names[x+6], font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
            filterNames[16+x].grid(row = 8, column = x+1)
        
        setattr(window, "filterScales", filterScales)
        
        #TAB 1 OBJECT DETECTION
        objectDetectScales = []
        objectDetectNames = []
        objectDetectScales_CheckBoxes = []
        
        names = ["Rect Thresh 1", "Rect Min Width", "Rect Min Height", "Rect Thresh 2", "Rect Max Width", "Rect Max Height", "Rect Blur", "    Blank1", "    Blank2", "    Blank3"]
        scaleValues = [1000, processedImgWidth, processedImgHeight]
        for x in range(3): #For front img
            objectDetectScales.append(Tkinter.Scale(frontProcessedImgFrame, from_ = 1, to = scaleValues[x], width = 15, orient = "horizontal")) #Creating sliders
            objectDetectScales[x].grid(row = x*2, column = 0)
            objectDetectNames.append(Tkinter.Label(frontProcessedImgFrame, text = names[x], font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
            objectDetectNames[x].grid(row = x*2 + 1, column = 0)
            
        for x in range(3): #For front img
            objectDetectScales.append(Tkinter.Scale(frontProcessedImgFrame, from_ = 1, to = scaleValues[x], width = 15, orient = "horizontal")) #Creating sliders
            objectDetectScales[3+x].grid(row = x*2, column = 5)
            objectDetectNames.append(Tkinter.Label(frontProcessedImgFrame, text = names[x+3], font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
            objectDetectNames[3+x].grid(row = x*2 + 1, column = 5)
            
        for x in range(4): #For front img
            objectDetectScales.append(Tkinter.Scale(frontProcessedImgFrame, from_ = 1, to = 13, width = 15, length=90)) #Creating sliders
            objectDetectScales[6+x].grid(row = 11, column = x+1)
            objectDetectNames.append(Tkinter.Label(frontProcessedImgFrame, text = names[x+6], font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
            objectDetectNames[6+x].grid(row = 12, column = x+1)
            
        for x in range(3): #For bottom img
            objectDetectScales.append(Tkinter.Scale(bottomProcessedImgFrame, from_ = 1, to = scaleValues[x], width = 15, orient = "horizontal")) #Creating sliders
            objectDetectScales[10+x].grid(row = x*2, column = 0)
            objectDetectNames.append(Tkinter.Label(bottomProcessedImgFrame, text = names[x], font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
            objectDetectNames[10+x].grid(row = x*2 + 1, column = 0)
            
        for x in range(3): #For bottom img
            objectDetectScales.append(Tkinter.Scale(bottomProcessedImgFrame, from_ = 1, to = scaleValues[x], width = 15, orient = "horizontal")) #Creating sliders
            objectDetectScales[13+x].grid(row = x*2, column = 5)
            objectDetectNames.append(Tkinter.Label(bottomProcessedImgFrame, text = names[x+3], font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
            objectDetectNames[13+x].grid(row = x*2 + 1, column = 5)
            
        for x in range(4): #For bottom img
            objectDetectScales.append(Tkinter.Scale(bottomProcessedImgFrame, from_ = 1, to = 13, width = 15, length=90)) #Creating sliders
            objectDetectScales[16+x].grid(row = 11, column = x+1)
            objectDetectNames.append(Tkinter.Label(bottomProcessedImgFrame, text = names[x+6], font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
            objectDetectNames[16+x].grid(row = 12, column = x+1)

            
        objectDetectCheckboxFrame = Tkinter.Frame(tab1)
        objectDetectCheckboxFrame.place(relx = 0.5, rely = 0.45, anchor = "center")
        
        objectDetectScales_CheckBoxes.append(Tkinter.IntVar())
        objectDetectScales.append(Tkinter.Checkbutton(objectDetectCheckboxFrame, variable = objectDetectScales_CheckBoxes[0]))
        objectDetectScales[20].grid(row = 0, column = 0, padx = int(screenRes[0]/795))
        objectDetectNames.append(Tkinter.Label(objectDetectCheckboxFrame, text = "Camshift Detection", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        objectDetectNames[20].grid(row = 1, column = 0, sticky = "N", padx = int(screenRes[0]/795))
        
        objectDetectScales_CheckBoxes.append(Tkinter.IntVar())
        objectDetectScales.append(Tkinter.Checkbutton(objectDetectCheckboxFrame, variable = objectDetectScales_CheckBoxes[1]))
        objectDetectScales[21].grid(row = 2, column = 0, padx = int(screenRes[0]/795))
        objectDetectNames.append(Tkinter.Label(objectDetectCheckboxFrame, text = "Rectangle Detection", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        objectDetectNames[21].grid(row = 3, column = 0, sticky = "N", padx = int(screenRes[0]/795))  
            
        for x in range(len(objectDetectScales)): #Remove object detect scales and names initially
            objectDetectScales[x].grid_remove()
            objectDetectNames[x].grid_remove()
            
        #Button
        imageProcessingToggleButton = Tkinter.Button(tab1, text = "Object Detect", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), width = 25, command = lambda: ImageProcessingToggleButton(window).toggle(imageProcessingToggleButton, frontProcessedImgLabel, bottomProcessedImgLabel, filterScales, filterNames, objectDetectScales, objectDetectNames))
        imageProcessingToggleButton.place(relx = 0.5, rely = 0.04, anchor = "center")
        
        setattr(window, "objectDetectScales", objectDetectScales)
        setattr(window, "objectDetectScales_CheckBoxes", objectDetectScales_CheckBoxes)

        #TAB 2 MISSION SELECTOR
        
        #mission selector frame
        missionSelectorFrame = Tkinter.Frame(tab2)
        missionSelectorFrame.grid(row = 0, column = 0, ipadx = int(screenRes[0]/15.9), sticky = "w")
        
        label = Tkinter.Label(missionSelectorFrame, text = "Mission Selector", font=("TkDefaultFont", int(round(screenRes[0]/176.667))))
        label.grid(row = 0, column = 0, columnspan = 4)
        missionListBox = Tkinter.Listbox(missionSelectorFrame, width = int(screenRes[0]/53), height = int(screenRes[1]/40))
        missionListBox.grid(row = 1, column = 0, rowspan = 9, columnspan = 4)
        
        #up/down button
        upButton = Tkinter.Button(missionSelectorFrame, text = "up", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), command = lambda: mission_selector_system.MoveUpDown().moveUp(window))
        upButton.grid(row = 4, column = 5, pady = int(screenRes[1]/174), sticky = "esw")
        downButton = Tkinter.Button(missionSelectorFrame, text = "dwn", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), command = lambda: mission_selector_system.MoveUpDown().moveDown(window))
        downButton.grid(row = 5, column = 5, pady = int(screenRes[1]/174), sticky = "new")
        
        #bottom buttons
        addButton = Tkinter.Button(missionSelectorFrame, text = "Add", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), command = lambda: mission_selector_system.MissionSelectorType(window, missionListBox))
        addButton.grid(row = 10, column = 0, pady = int(screenRes[1]/200))
        deleteButton = Tkinter.Button(missionSelectorFrame, text = "Delete", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), command = lambda: mission_selector_system.DeleteMissionType(window))
        deleteButton.grid(row = 10, column = 1, pady = int(screenRes[1]/200))
        loadButton = Tkinter.Button(missionSelectorFrame, text = "Load", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), command = lambda: mission_selector_system.loadList(window))
        loadButton.grid(row = 10, column = 2, pady = int(screenRes[1]/200))
        loadButton.bind("<Button-1>", lambda event, args=[window]: Refresh(event, args)) #This is to stop the gui from flickering
        exportButton = Tkinter.Button(missionSelectorFrame, text = "Export", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), command = lambda: mission_selector_system.ExportList(window))
        exportButton.grid(row = 10, column = 3, pady = int(screenRes[1]/200))
        
        #mission selector buttons
        missionSelectorButtonList = [upButton, downButton, addButton, deleteButton, loadButton]
        
        #param/value frame
        paramFrame = Tkinter.Frame(tab2)
        paramFrame.grid(row = 0, column = 1, sticky = "n")
        
        paramLabel = Tkinter.Label(paramFrame, text = "Parameters", font=("TkDefaultFont", int(round(screenRes[0]/176.667))))
        paramLabel.grid(row = 0, column = 0)
        paramListBox = Tkinter.Listbox(paramFrame, width = int(screenRes[0]/39.75), height = int(screenRes[1]/39.5))
        paramListBox.grid(row = 1, column = 0)
        
        valueLabel = Tkinter.Label(paramFrame, text = "Values", font=("TkDefaultFont", int(round(screenRes[0]/176.667))))
        valueLabel.grid(row = 0, column = 1)
        valueListBox = Tkinter.Listbox(paramFrame, width = int(screenRes[0]/39.75), height = int(screenRes[1]/39.5))
        valueListBox.grid(row = 1, column = 1)
        valueListBox.bind("<Double-Button-1>", lambda event, args=[window, valueListBox, paramListBox]: mission_selector_system.MissionSelectorValues(event, args))
        valueListBox.bind("<Return>", lambda event, args=[window, valueListBox, paramListBox]: mission_selector_system.MissionSelectorValues(event, args))
        
        #description box
        descriptionFrame = Tkinter.Frame(tab2)
        descriptionFrame.grid(row = 0, column = 2, padx = int(screenRes[0]/7.95), sticky = "n")
        
        descriptionLabel = Tkinter.Label(descriptionFrame, text = "Description", font=("TkDefaultFont", int(round(screenRes[0]/176.667))))
        descriptionLabel.grid(row = 0, column = 0)
        scrollBar = Tkinter.Scrollbar(descriptionFrame)
        scrollBar.grid(row = 1, column = 1, sticky='ns')
        discriptionText = Tkinter.Text(descriptionFrame, yscrollcommand=scrollBar.set, borderwidth = 7, width = int(screenRes[0]/31.8), height = int(screenRes[1]/39.5), wrap="word")
        discriptionText.grid(row = 1, column = 0, sticky = "nesw")
        scrollBar.config(command=discriptionText.yview)
        
        text = ''.join(["This mission selector system is capable of adding various mission types to a list by ",
        "pressing the 'Add' button. The order of the missions that are placed in the list will be the order in which they are executed when ",
        "the vehicle starts. It is possible to change the order of missions after being added to the list by the 'Up' and 'Dwn' buttons. ",
        "It is possible to change the parameter values of a mission type by double clicking on its values in the value list box. ",
        "The 'Delete' button will delete the mission that is highlighted from the list and remove its parameters ",
        "and values. The 'Load' and 'Export' buttons can load in and export the list you created."])
        
        discriptionText.insert("insert", text)
        discriptionText.config(state = "disable")
        
        #attributes to gui
        setattr(window, "missionListBox", missionListBox)
        setattr(window, "paramListBox", paramListBox)
        setattr(window, "paramLabel", paramLabel)
        setattr(window, "valueListBox", valueListBox)
        setattr(window, "valueLabel", valueLabel)
        setattr(window, "discriptionText", discriptionText)
        
        
        #TAB 3 VHEICLE TESTS
        motorTestButton = Tkinter.Button(tab3, text = "Motor Test", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), width = int(screenRes[0]/63.6), height = int(screenRes[1]/174))
        motorTestButton.grid(row = 0, column = 0, padx = int(screenRes[0]/79.5), pady = int(screenRes[1]/34.8))
        
        audioTestButton = Tkinter.Button(tab3, text = "Audio Test", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), width = int(screenRes[0]/63.6), height = int(screenRes[1]/174))
        audioTestButton.grid(row = 1, column = 0, padx = int(screenRes[0]/79.5), pady = int(screenRes[1]/34.8))
        
        ledTestButton = Tkinter.Button(tab3, text = "LED Display Test", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), width = int(screenRes[0]/63.6), height = int(screenRes[1]/174))
        ledTestButton.grid(row = 2, column = 0, padx = int(screenRes[0]/79.5), pady = int(screenRes[1]/34.8))
        
        rainbowduinoTestButton = Tkinter.Button(tab3, text = "Rainbowduino Display Test", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), width = int(screenRes[0]/63.6), height = int(screenRes[1]/174))
        rainbowduinoTestButton.grid(row = 0, column = 1, padx = int(screenRes[0]/79.5), pady = int(screenRes[1]/34.8))

        #TAB 4 CONSOLE
        scrollBar = Tkinter.Scrollbar(tab4)
        scrollBar.grid(row = 0, column = 1, rowspan = 10, sticky='ns')
        consolText = Tkinter.Text(tab4, borderwidth = 7, yscrollcommand=scrollBar.set, width = int(screenRes[0]/11.367), height = int(screenRes[1]/36.251))
        consolText.grid(row = 0, column = 0, rowspan = 10, sticky = "nesw")
        #sys.stdout = StdoutRedirector(consolText) #COMMENT THIS LINE OUT TO STOP PRINTING TO GUI
        scrollBar.config(command=consolText.yview)
        
        #PRINT OPTIONS
        names = ["Heading, Pitch, Roll, Depth", "Position (x, y, z)", "Velocity (u, v, w)", "Battery 1 Status", "Battery 2 Status", "Temperature Status", "Current Rotation Matrix"]
        printOptionCheckbox = []
        printOptionCheckboxValues = []
        
        printOptionCheckboxValues.append(Tkinter.IntVar())
        printOptionCheckbox.append(Tkinter.Checkbutton(tab4, text = names[0], font=("TkDefaultFont", int(round(screenRes[0]/176.667))), variable = printOptionCheckboxValues[0]))
        printOptionCheckbox[0].grid(row = 0, column = 2, sticky = "W", padx = int(screenRes[0]/795))
        
        printOptionCheckboxValues.append(Tkinter.IntVar())
        printOptionCheckbox.append(Tkinter.Checkbutton(tab4, text = names[1], font=("TkDefaultFont", int(round(screenRes[0]/176.667))), variable = printOptionCheckboxValues[1]))
        printOptionCheckbox[1].grid(row = 0, column = 3, sticky = "W", padx = int(screenRes[0]/795))
        
        printOptionCheckboxValues.append(Tkinter.IntVar())
        printOptionCheckbox.append(Tkinter.Checkbutton(tab4, text = names[2], font=("TkDefaultFont", int(round(screenRes[0]/176.667))), variable = printOptionCheckboxValues[2]))
        printOptionCheckbox[2].grid(row = 0, column = 4, sticky = "W", padx = int(screenRes[0]/795))
        
        printOptionCheckboxValues.append(Tkinter.IntVar())
        printOptionCheckbox.append(Tkinter.Checkbutton(tab4, text = names[3], font=("TkDefaultFont", int(round(screenRes[0]/176.667))), variable = printOptionCheckboxValues[3]))
        printOptionCheckbox[3].grid(row = 1, column = 2, sticky = "W", padx = int(screenRes[0]/795))
        
        printOptionCheckboxValues.append(Tkinter.IntVar())
        printOptionCheckbox.append(Tkinter.Checkbutton(tab4, text = names[4], font=("TkDefaultFont", int(round(screenRes[0]/176.667))), variable = printOptionCheckboxValues[4]))
        printOptionCheckbox[4].grid(row = 1, column = 3, sticky = "W", padx = int(screenRes[0]/795))
        
        printOptionCheckboxValues.append(Tkinter.IntVar())
        printOptionCheckbox.append(Tkinter.Checkbutton(tab4, text = names[5], font=("TkDefaultFont", int(round(screenRes[0]/176.667))), variable = printOptionCheckboxValues[5]))
        printOptionCheckbox[5].grid(row = 1, column = 4, sticky = "W", padx = int(screenRes[0]/795))
        
        printOptionCheckboxValues.append(Tkinter.IntVar())
        printOptionCheckbox.append(Tkinter.Checkbutton(tab4, text = names[6], font=("TkDefaultFont", int(round(screenRes[0]/176.667))), variable = printOptionCheckboxValues[6]))
        printOptionCheckbox[6].grid(row = 2, column = 2, columnspan = 2, sticky = "W", padx = int(screenRes[0]/795))
    
        setattr(window, 'printOptionCheckbox', printOptionCheckbox)
        setattr(window, 'printOptionCheckboxValues', printOptionCheckboxValues)
        
        clearButton = Tkinter.Button(tab4, width = int(screenRes[0]/227.143), text = "Clear", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), command = lambda: clear(consolText))
        clearButton.grid(row = 9, column=2, padx = int(screenRes[0]/63.6), sticky = "w")
        
        exportButton = Tkinter.Button(tab4, width = int(screenRes[0]/227.143), text = "Export", font=("TkDefaultFont", int(round(screenRes[0]/176.667))), command = lambda: export(consolText))
        exportButton.grid(row = 9, column=4, padx = int(screenRes[0]/63.6), sticky = "e")
            
        #TAB 5 SETTINGS
        configurationGaugeScales = []
        configurationGaugeNames = []
        configurationGaugeScales_CheckBoxes = []
        configurationGaugeScales_RadioButtons = []
        
        #CONFIG GAUGE SLIDERS
        graphicsOverlaySettingsFrame = Tkinter.Frame(tab5)
        graphicsOverlaySettingsFrame.grid(row = 0, column = 0)
        
        graphicsOverlayTitle = Tkinter.Label(graphicsOverlaySettingsFrame, text = "Graphics Configuration", font=("TkDefaultFont", int(round(screenRes[0]/176.667))))
        graphicsOverlayTitle.grid(row = 0, column = 2, columnspan = 10)
        
        configurationGaugeScales_CheckBoxes.append(Tkinter.IntVar())
        configurationGaugeScales.append(Tkinter.Checkbutton(graphicsOverlaySettingsFrame, variable = configurationGaugeScales_CheckBoxes[0]))
        configurationGaugeScales[0].grid(row = 1, column = 0, padx = int(screenRes[0]/795))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Heading Gauge", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[0].grid(row = 2, column = 0, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 3, to = 10, width = 15, orient = "horizontal"))
        configurationGaugeScales[1].grid(row = 3, column = 0, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Heading Tick Num", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[1].grid(row = 4, column = 0, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 1, to = 60, width = 15, orient = "horizontal"))
        configurationGaugeScales[2].grid(row = 5, column = 0, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Heading Increment Num", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[2].grid(row = 6, column = 0, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 1, width = 15, orient = "horizontal"))
        configurationGaugeScales[3].grid(row = 7, column = 0, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Heading Position", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[3].grid(row = 8, column = 0, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 10, to = rawImgWidth, width = 15, orient = "horizontal"))
        configurationGaugeScales[4].grid(row = 9, column = 0, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Heading Width", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[4].grid(row = 10, column = 0, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales_CheckBoxes.append(Tkinter.IntVar())
        configurationGaugeScales.append(Tkinter.Checkbutton(graphicsOverlaySettingsFrame, variable = configurationGaugeScales_CheckBoxes[1]))
        configurationGaugeScales[5].grid(row = 1, column = 1, padx = int(screenRes[0]/795))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Pitch Gauge", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[5].grid(row = 2, column = 1, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 3, to = 15, width = 15, orient = "horizontal"))
        configurationGaugeScales[6].grid(row = 3, column = 1, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Pitch Tick Num", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[6].grid(row = 4, column = 1, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 1, to = 15, width = 15, orient = "horizontal"))
        configurationGaugeScales[7].grid(row = 5, column = 1, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Pitch Increment Num", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[7].grid(row = 6, column = 1, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 15, to = rawImgHeight-140, width = 15, orient = "horizontal"))
        configurationGaugeScales[8].grid(row = 7, column = 1, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Pitch Length", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[8].grid(row = 8, column = 1, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales_CheckBoxes.append(Tkinter.IntVar())
        configurationGaugeScales.append(Tkinter.Checkbutton(graphicsOverlaySettingsFrame, variable = configurationGaugeScales_CheckBoxes[2]))
        configurationGaugeScales[9].grid(row = 1, column = 2, columnspan = 2, padx = int(screenRes[0]/795))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Roll Gauge", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[9].grid(row = 2, column = 2, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 3, to = 13, width = 15, orient = "horizontal"))
        configurationGaugeScales[10].grid(row = 3, column = 2, columnspan = 2, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Roll Tick Num", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[10].grid(row = 4, column = 2, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales_RadioButtons.append(Tkinter.IntVar())
        configurationGaugeScales.append(Tkinter.Radiobutton(graphicsOverlaySettingsFrame, variable=configurationGaugeScales_RadioButtons[0], text = "90", value = 0))
        configurationGaugeScales[11].grid(row = 5, column = 2, padx = int(screenRes[0]/318))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Roll Range Num", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[11].grid(row = 6, column = 2, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        configurationGaugeScales.append(Tkinter.Radiobutton(graphicsOverlaySettingsFrame, variable=configurationGaugeScales_RadioButtons[0], text = "180", value = 1))
        configurationGaugeScales[12].grid(row = 5, column = 3, padx = int(screenRes[0]/318))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Roll Range Num", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[12].grid(row = 6, column = 2, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 1, width = 15, orient = "horizontal"))
        configurationGaugeScales[13].grid(row = 7, column = 2, columnspan = 2, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Roll Position", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[13].grid(row = 8, column = 2, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 2, to = rawImgWidth/2-39, width = 15, orient = "horizontal"))
        configurationGaugeScales[14].grid(row = 9, column = 2, columnspan = 2, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Roll Width", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[14].grid(row = 10, column = 2, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales_CheckBoxes.append(Tkinter.IntVar())
        configurationGaugeScales.append(Tkinter.Checkbutton(graphicsOverlaySettingsFrame, variable = configurationGaugeScales_CheckBoxes[3]))
        configurationGaugeScales[15].grid(row = 1, column = 4, padx = int(screenRes[0]/795))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Depth Gauge", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[15].grid(row = 2, column = 4, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 3, to = 20, width = 15, orient = "horizontal"))
        configurationGaugeScales[16].grid(row = 3, column = 4, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Depth Tick Num", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[16].grid(row = 4, column = 4, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 1, to = 50, width = 15, orient = "horizontal"))
        configurationGaugeScales[17].grid(row = 5, column = 4, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Depth Increment Num", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[17].grid(row = 6, column = 4, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 1, width = 15, orient = "horizontal"))
        configurationGaugeScales[18].grid(row = 7, column = 4, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Depth Position", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[18].grid(row = 8, column = 4, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 20, to = rawImgHeight, width = 15, orient = "horizontal"))
        configurationGaugeScales[19].grid(row = 9, column = 4, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Depth Length", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[19].grid(row = 10, column = 4, sticky = "N",  padx = int(screenRes[0]/318))
        
        configurationGaugeScales_CheckBoxes.append(Tkinter.IntVar())
        configurationGaugeScales.append(Tkinter.Checkbutton(graphicsOverlaySettingsFrame, variable = configurationGaugeScales_CheckBoxes[4]))
        configurationGaugeScales[20].grid(row = 1, column = 5, columnspan = 2, padx = int(screenRes[0]/795))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Attitude Gauge", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[20].grid(row = 2, column = 5, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 5, to = 50, width = 15, orient = "horizontal"))
        configurationGaugeScales[21].grid(row = 3, column = 5, columnspan = 2, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Attitude Length", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[21].grid(row = 4, column = 5, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales_RadioButtons.append(Tkinter.IntVar())
        configurationGaugeScales.append(Tkinter.Radiobutton(graphicsOverlaySettingsFrame, variable=configurationGaugeScales_RadioButtons[1], text = "Yes", value = 1))
        configurationGaugeScales[22].grid(row = 5, column = 5, padx = int(screenRes[0]/318))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Display Pos/Vel", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[22].grid(row = 6, column = 5, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        configurationGaugeScales.append(Tkinter.Radiobutton(graphicsOverlaySettingsFrame, variable=configurationGaugeScales_RadioButtons[1], text = "No", value = 0))
        configurationGaugeScales[23].grid(row = 5, column = 6, padx = int(screenRes[0]/318))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Display Pos/Vel", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[23].grid(row = 6, column = 5, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 3, width = 15, orient = "horizontal"))
        configurationGaugeScales[24].grid(row = 7, column = 5, columnspan = 2, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Attitude Position", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[24].grid(row = 8, column = 5, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 50, width = 15, orient = "horizontal"))
        configurationGaugeScales[25].grid(row = 9, column = 5, columnspan = 2, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Attitude Letter Size", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[25].grid(row = 10, column = 5, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 10, width = 15, orient = "horizontal"))
        configurationGaugeScales[26].grid(row = 11, column = 5, columnspan = 2, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Attitude Letter Ratio", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[26].grid(row = 12, column = 5, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales_CheckBoxes.append(Tkinter.IntVar())
        configurationGaugeScales.append(Tkinter.Checkbutton(graphicsOverlaySettingsFrame, variable = configurationGaugeScales_CheckBoxes[5]))
        configurationGaugeScales[27].grid(row = 1, column = 7, columnspan = 2, padx = int(screenRes[0]/795))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Battery Gauge", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[27].grid(row = 2, column = 7, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 1, to = 100, width = 15, orient = "horizontal"))
        configurationGaugeScales[28].grid(row = 3, column = 7, columnspan = 2, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Battery Length", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[28].grid(row = 4, column = 7, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales_RadioButtons.append(Tkinter.IntVar())
        configurationGaugeScales.append(Tkinter.Radiobutton(graphicsOverlaySettingsFrame, variable=configurationGaugeScales_RadioButtons[2], text = "Yes", value = 1))
        configurationGaugeScales[29].grid(row = 5, column = 7, padx = int(screenRes[0]/318))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Display Battery Current", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[29].grid(row = 6, column = 7, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        configurationGaugeScales.append(Tkinter.Radiobutton(graphicsOverlaySettingsFrame, variable=configurationGaugeScales_RadioButtons[2], text = "No", value = 0))
        configurationGaugeScales[30].grid(row = 5, column = 8, padx = int(screenRes[0]/318))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Display Battery Current", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[30].grid(row = 6, column = 7, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 3, width = 15, orient = "horizontal"))
        configurationGaugeScales[31].grid(row = 7, column = 7, columnspan = 2, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Battery Position", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[31].grid(row = 8, column = 7, columnspan = 2, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales_CheckBoxes.append(Tkinter.IntVar())
        configurationGaugeScales.append(Tkinter.Checkbutton(graphicsOverlaySettingsFrame, variable = configurationGaugeScales_CheckBoxes[6]))
        configurationGaugeScales[32].grid(row = 1, column = 9, padx = int(screenRes[0]/795))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Temperature Gauge", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[32].grid(row = 2, column = 9, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 10, to = 50, width = 15, orient = "horizontal"))
        configurationGaugeScales[33].grid(row = 3, column = 9, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Temperature Size", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[33].grid(row = 4, column = 9, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 3, width = 15, orient = "horizontal"))
        configurationGaugeScales[34].grid(row = 5, column = 9, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Temperature Position", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[34].grid(row = 6, column = 9, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales_CheckBoxes.append(Tkinter.IntVar())
        configurationGaugeScales.append(Tkinter.Checkbutton(graphicsOverlaySettingsFrame, variable = configurationGaugeScales_CheckBoxes[7]))
        configurationGaugeScales[35].grid(row = 1, column = 10, padx = int(screenRes[0]/795))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Motor Gauge", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[35].grid(row = 2, column = 10, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 10, to = 50, width = 15, orient = "horizontal"))
        configurationGaugeScales[36].grid(row = 3, column = 10, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Motor Size", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[36].grid(row = 4, column = 10, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 1, width = 15, orient = "horizontal"))
        configurationGaugeScales[37].grid(row = 5, column = 10, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Motor Position", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[37].grid(row = 6, column = 10, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales_CheckBoxes.append(Tkinter.IntVar())
        configurationGaugeScales.append(Tkinter.Checkbutton(graphicsOverlaySettingsFrame, variable = configurationGaugeScales_CheckBoxes[8]))
        configurationGaugeScales[38].grid(row = 1, column = 11, padx = int(screenRes[0]/795))
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Status Gauge", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[38].grid(row = 2, column = 11, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 3, width = 15, orient = "horizontal"))
        configurationGaugeScales[39].grid(row = 3, column = 11, padx = int(screenRes[0]/318)) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Status Position", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[39].grid(row = 4, column = 11, sticky = "N", padx = int(screenRes[0]/318))
        
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Color", font=("TkDefaultFont", int(round(screenRes[0]/100.667)))))
        configurationGaugeNames[40].grid(row = 1, column = 12, rowspan = 2, padx = int(screenRes[0]/318)+50)
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 255, width = 15, orient = "horizontal"))
        configurationGaugeScales[40].grid(row = 3, column = 12, padx = int(screenRes[0]/318)+50) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Red Gauge Color", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[41].grid(row = 4, column = 12, padx = int(screenRes[0]/318)+50)
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 255, width = 15, orient = "horizontal"))
        configurationGaugeScales[41].grid(row = 5, column = 12, columnspan = 4, padx = int(screenRes[0]/318)+50) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Green Gauge Color", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[42].grid(row = 6, column = 12, columnspan = 4, padx = int(screenRes[0]/318)+50)
        
        configurationGaugeScales.append(Tkinter.Scale(graphicsOverlaySettingsFrame, from_ = 0, to = 255, width = 15, orient = "horizontal"))
        configurationGaugeScales[42].grid(row = 7, column = 12, padx = int(screenRes[0]/318)+50) 
        configurationGaugeNames.append(Tkinter.Label(graphicsOverlaySettingsFrame, text = "Blue Gauge Color", font=("TkDefaultFont", int(round(screenRes[0]/176.667)))))
        configurationGaugeNames[43].grid(row = 8, column = 12, padx = int(screenRes[0]/318)+50)
        
        setattr(window, "configurationGaugeScales", configurationGaugeScales)
        setattr(window, "configurationGaugeScales_RadioButtons", configurationGaugeScales_RadioButtons)
        setattr(window, "configurationGaugeScales_CheckBoxes", configurationGaugeScales_CheckBoxes)

        #TAB 6 SETTINGS
        setattr(window, "setToManual", 3)
        
        startManualButton = Tkinter.Button(tab6, text = "MANUAL CONTROL", width = screenRes[0]/73, height = screenRes[1]/180)
        startManualButton.place(relx = 0, rely = 0)
        
        stopManualButton = Tkinter.Button(tab6, text = "STOP", fg='black', width = screenRes[0]/73, height = screenRes[1]/180, state = "disable")
        stopManualButton.place(relx = 0, rely = 0.78)
        
        controllerScreen = Tkinter.Label(tab6, background = "gray")  #The raw image for the front camera will go here
        setattr(window, "controllerScreen", controllerScreen)
        
        startManualClass = StartManual(window, tab6, notebook, missionSelectorButtonList)
        startManualButton.config(command=lambda: startManualClass.start(startManualButton, stopManualButton))
        stopManualButton.config(command=lambda: startManualClass.stop(startManualButton, stopManualButton))

        #AUV START/STOP
        if not DEBUG:
            #START ALL EXTERNAL PROCESSES
            self.parent_conn, child_conn = multiprocessing.Pipe() 
            self.process = multiprocessing.Process(target=NMS.start, args=(child_conn,))
            self.process.start()
            
        userLabel = Tkinter.Label(window, text = "User", font=("Calibri", int(screenRes[0]/123)), background = "gray", foreground = "black")
        userLabel.place(relx = 0.5, rely = 0.02, anchor="center")
        
        lastUserLog = previous_state_logging_system.Log('_Saved_Settings_/_Last_User_.txt') #Need to created separate file to keep track of last user so that I know what file to load in for all settings
        lastUserValues = lastUserLog.getParameters("lastUser") #Get the lastUser variable in file
        
        if lastUserValues.lastUser == 0: #If no value in _Last_User_.txt file...
            lastUserValues.lastUser = "Austin Owens"
                          
        dropBoxUserValue = Tkinter.StringVar(window)
        dropBoxUserValue.set(lastUserValues.lastUser) # default value
        options = Tkinter.OptionMenu(window, dropBoxUserValue, "Austin Owens", "Josh Pritts", "Drew Smith", "Rodrigo Alvarez", "Maryann Ibrahim", "Jacob Marlay", "Matt Wnuk", "Joseph Clements", "Petar Tasev", "Akash Khatawate")
        options.place(relx = 0.5, rely = 0.05, anchor="center")
        options.bind("<Button-1>", lambda event, args=[window]: Refresh(event, args)) #This is to stop the gui from flickering
        
        setattr(window, "lastUser", dropBoxUserValue) #This is so I can write the last user into a file in 'update gui' file
        setattr(window, "lastUserLog", lastUserLog) #This is so I can write the last user into a file in 'update gui' file
        
        startRobosubButton = Tkinter.Button(window, text = "START VEHICLE", width = screenRes[0]/73, height = screenRes[1]/180)
        startRobosubButton.place(relx = 0.5, rely = 0.2, anchor="center")
        
        stopRobosubButton = Tkinter.Button(window, text = "STOP VEHICLE", width = screenRes[0]/73, height = screenRes[1]/180, state = "disable")
        stopRobosubButton.place(relx = 0.5, rely = 0.3, anchor="center")
        
        authorLabel = Tkinter.Label(window, text = "By: Austin Owens", font=("Calibri", int(screenRes[0]/123)), background = "gray", foreground = "black")
        authorLabel.place(relx = 0.5, rely = 0.48, anchor="center")
        
        frontRecording = Tkinter.Label(window, text = "Rec.", font=("Calibri", int(screenRes[0]/50)), background = "gray", foreground = "gray")
        frontRecording.place(relx = 0, rely = 0.05)
        bottomRecording = Tkinter.Label(window, text = "Rec.", font=("Calibri", int(screenRes[0]/50)), background = "gray", foreground = "gray")
        bottomRecording.place(relx = 1, rely = 0.07, anchor="e")
        setattr(window, "recording", [frontRecording, bottomRecording])
        
        startVehicleClass = StartVehicle(notebook, missionSelectorButtonList)
        startRobosubButton.config(command=lambda: startVehicleClass.start(startRobosubButton, stopRobosubButton))
        stopRobosubButton.config(command=lambda: startVehicleClass.stop(startRobosubButton, stopRobosubButton))
        
        #MAIN FUNCTION
        setattr(window, "externalDevicesData", None)
        GUI = update_gui.UpdateGUI(window, rawImgWidth, rawImgHeight, processedImgWidth, processedImgHeight) #This needs to be here so that the 'window' variable has all its setattr
        window.after(0, func=lambda: self.updateGUI(window))
        
        #EXITING CONDITION
        window.protocol('WM_DELETE_WINDOW', self.setQuitFlag)  # avoid errors on exit

if __name__ == "__main__":
    gui = GuiCreation()
    gui.guiSetup()
    window.mainloop()