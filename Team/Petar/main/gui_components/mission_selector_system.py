'''
Created on Nov 17, 2014

@author: Austin
'''
import Tkinter, tkFileDialog 
import previous_state_logging_system
import os, shutil

logger = previous_state_logging_system.Log('gui_components/_GUI_Parameters_.txt')

kwargsValueList = {}
imageProcessingMissionList = []
previousIndex = None
indexTracker = None
missionNames = ["Navigation", "Buoy", "Path", "Maneuvering", "Torpedo", "Dropper", "Peg Manipulation", "Pinger", "Pick Up"]
missionTypeCounters = [0, 0, 0, 0, 0, 0, 0, 0, 0]

navigationIndex, buoyIndex, pathIndex, maneuveringIndex, torpedoIndex, dropperIndex, pegManipulationIndex, pingerIndex, pickUp = 0,0,0,0,0,0,0,0,0

frontPreviousKwargsValueList, bottomPreviousKwargsValueList = None, None

class MissionSelector:
    def __init__(self, window):
        self.window = window
        
    def updateParamValueLists(self):
        '''
        This function is responsible for updating the parameter and value lists in the mission selector tab when a mission in the mission
        list is highlighted.
        '''
        global previousIndex, missionTypeCounters, indexTracker, navigationIndex, buoyIndex, pathIndex, maneuveringIndex, torpedoIndex, dropperIndex, pegManipulationIndex, pingerIndex, pickUp
        
        if (self.window.missionListBox.size() == 0): #If there is nothing in the list

            self.window.paramLabel.config(text = "Parameters")
            self.window.valueLabel.config(text = "Values")
            
            previousIndex = None
            
        elif ("Navigation" in self.window.missionListBox.get("active") and previousIndex != indexTracker):
            
            self.window.discriptionText.config(state = "normal")
            self.window.discriptionText.delete("1.0", "end")
            self.window.discriptionText.insert("insert", "Navigation Description.")
            self.window.discriptionText.config(state = "disable")
            
            missionCounter = [int(s) for s in self.window.missionListBox.get("active").split() if s.isdigit()][0]
            
            self.window.paramLabel.config(text = "Navigation {} Parameters".format(missionCounter))
            self.window.valueLabel.config(text = "Navigation {} Values".format(missionCounter))
            
            self.window.paramListBox.delete(0, "end")
            self.window.valueListBox.delete(0, "end")
            self.window.paramListBox.insert("end", "Time")
            self.window.valueListBox.insert("end", self.getSavedValues("navigationTime {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "X")
            self.window.valueListBox.insert("end", self.getSavedValues("navigationX {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "Y")
            self.window.valueListBox.insert("end", self.getSavedValues("navigationY {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "Z")
            self.window.valueListBox.insert("end", self.getSavedValues("navigationZ {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "FSD?")
            self.window.valueListBox.insert("end", self.getSavedValues("navigationFSD {}".format(missionCounter))[0])
            
            previousIndex = indexTracker
            
        elif ("Buoy" in self.window.missionListBox.get("active") and previousIndex != indexTracker):
            
            self.window.discriptionText.config(state = "normal")
            self.window.discriptionText.delete("1.0", "end")
            self.window.discriptionText.insert("insert", "Buoy Description.")
            self.window.discriptionText.config(state = "disable")
            
            missionCounter = [int(s) for s in self.window.missionListBox.get("active").split() if s.isdigit()][0]
            
            self.window.paramLabel.config(text = "Buoy {} Parameters".format(missionCounter))
            self.window.valueLabel.config(text = "Buoy {} Values".format(missionCounter))
            
            self.window.paramListBox.delete(0, "end")
            self.window.valueListBox.delete(0, "end")
            self.window.paramListBox.insert("end", "Time")
            self.window.valueListBox.insert("end", self.getSavedValues("buoyTime {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "LED?")
            self.window.valueListBox.insert("end", self.getSavedValues("buoyLED {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "SPT")
            self.window.valueListBox.insert("end", self.getSavedValues("buoySPT {}".format(missionCounter))[0])
            
            previousIndex = indexTracker
        
        elif ("Path" in self.window.missionListBox.get("active") and previousIndex != indexTracker):
            
            self.window.discriptionText.config(state = "normal")
            self.window.discriptionText.delete("1.0", "end")
            self.window.discriptionText.insert("insert", "Path Description.")
            self.window.discriptionText.config(state = "disable")
            
            missionCounter = [int(s) for s in self.window.missionListBox.get("active").split() if s.isdigit()][0]

            self.window.paramLabel.config(text = "Path {} Parameters".format(missionCounter))
            self.window.valueLabel.config(text = "Path {} Values".format(missionCounter))
            
            self.window.paramListBox.delete(0, "end")
            self.window.valueListBox.delete(0, "end")
            self.window.paramListBox.insert("end", "Time")
            self.window.valueListBox.insert("end", self.getSavedValues("pathTime {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "SPT")
            self.window.valueListBox.insert("end", self.getSavedValues("pathSPT {}".format(missionCounter))[0])
            
            previousIndex = indexTracker
            
        elif ("Maneuvering" in self.window.missionListBox.get("active") and previousIndex != indexTracker):
            
            self.window.discriptionText.config(state = "normal")
            self.window.discriptionText.delete("1.0", "end")
            self.window.discriptionText.insert("insert", "Maneuvering Description.")
            self.window.discriptionText.config(state = "disable")
            
            missionCounter = [int(s) for s in self.window.missionListBox.get("active").split() if s.isdigit()][0]
            
            self.window.paramLabel.config(text = "Maneuvering {} Parameters".format(missionCounter))
            self.window.valueLabel.config(text = "Maneuvering {} Values".format(missionCounter))
            
            self.window.paramListBox.delete(0, "end")
            self.window.valueListBox.delete(0, "end")
            self.window.paramListBox.insert("end", "Time")
            self.window.valueListBox.insert("end", self.getSavedValues("maneuveringTime {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "SPT")
            self.window.valueListBox.insert("end", self.getSavedValues("maneuveringSPT {}".format(missionCounter))[0])
            
            previousIndex = indexTracker
            
        elif ("Torpedo" in self.window.missionListBox.get("active") and previousIndex != indexTracker):
            
            self.window.discriptionText.config(state = "normal")
            self.window.discriptionText.delete("1.0", "end")
            self.window.discriptionText.insert("insert", "Torpedo Description.")
            self.window.discriptionText.config(state = "disable")
            
            missionCounter = [int(s) for s in self.window.missionListBox.get("active").split() if s.isdigit()][0]

            self.window.paramLabel.config(text = "Torpedo {} Parameters".format(missionCounter))
            self.window.valueLabel.config(text = "Torpedo {} Values".format(missionCounter))
            
            self.window.paramListBox.delete(0, "end")
            self.window.valueListBox.delete(0, "end")
            self.window.paramListBox.insert("end", "Time")
            self.window.valueListBox.insert("end", self.getSavedValues("torpedoTime {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "SPT")
            self.window.valueListBox.insert("end", self.getSavedValues("torpedoSPT {}".format(missionCounter))[0])
            
            previousIndex = indexTracker
            
        elif ("Dropper" in self.window.missionListBox.get("active") and previousIndex != indexTracker):
            
            self.window.discriptionText.config(state = "normal")
            self.window.discriptionText.delete("1.0", "end")
            self.window.discriptionText.insert("insert", "Dropper Description.")
            self.window.discriptionText.config(state = "disable")
            
            missionCounter = [int(s) for s in self.window.missionListBox.get("active").split() if s.isdigit()][0]

            self.window.paramLabel.config(text = "Dropper {} Parameters".format(missionCounter))
            self.window.valueLabel.config(text = "Dropper {} Values".format(missionCounter))
            
            self.window.paramListBox.delete(0, "end")
            self.window.valueListBox.delete(0, "end")
            self.window.paramListBox.insert("end", "Time")
            self.window.valueListBox.insert("end", self.getSavedValues("dropperTime {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "SPT")
            self.window.valueListBox.insert("end", self.getSavedValues("dropperSPT {}".format(missionCounter))[0])
            
            previousIndex = indexTracker
            
        elif ("Peg Manipulation" in self.window.missionListBox.get("active") and previousIndex != indexTracker):
            
            self.window.discriptionText.config(state = "normal")
            self.window.discriptionText.delete("1.0", "end")
            self.window.discriptionText.insert("insert", "Peg Manipulation Description.")
            self.window.discriptionText.config(state = "disable")
            
            missionCounter = [int(s) for s in self.window.missionListBox.get("active").split() if s.isdigit()][0]
            
            self.window.paramLabel.config(text = "Peg Manipulation {} Parameters".format(missionCounter))
            self.window.valueLabel.config(text = "Peg Manipulation {} Values".format(missionCounter))
            
            self.window.paramListBox.delete(0, "end")
            self.window.valueListBox.delete(0, "end")
            self.window.paramListBox.insert("end", "Time")
            self.window.valueListBox.insert("end", self.getSavedValues("pegManipulationTime {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "SPT")
            self.window.valueListBox.insert("end", self.getSavedValues("pegManipulationSPT {}".format(missionCounter))[0])
            
            previousIndex = indexTracker
            
        elif ("Pinger" in self.window.missionListBox.get("active") and previousIndex != indexTracker):
            
            self.window.discriptionText.config(state = "normal")
            self.window.discriptionText.delete("1.0", "end")
            self.window.discriptionText.insert("insert", "Pinger Description.")
            self.window.discriptionText.config(state = "disable")
            
            missionCounter = [int(s) for s in self.window.missionListBox.get("active").split() if s.isdigit()][0]
            
            self.window.paramLabel.config(text = "Pinger {} Parameters".format(missionCounter))
            self.window.valueLabel.config(text = "Pinger {} Values".format(missionCounter))
            
            self.window.paramListBox.delete(0, "end")
            self.window.valueListBox.delete(0, "end")
            self.window.paramListBox.insert("end", "Time")
            self.window.valueListBox.insert("end", self.getSavedValues("pingerTime {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "SPT")
            self.window.valueListBox.insert("end", self.getSavedValues("pingerSPT {}".format(missionCounter))[0])
            
            previousIndex = indexTracker
            
        elif ("Pick Up" in self.window.missionListBox.get("active") and previousIndex != indexTracker):
            
            self.window.discriptionText.config(state = "normal")
            self.window.discriptionText.delete("1.0", "end")
            self.window.discriptionText.insert("insert", "Pick Up Description.")
            self.window.discriptionText.config(state = "disable")
            
            missionCounter = [int(s) for s in self.window.missionListBox.get("active").split() if s.isdigit()][0]

            self.window.paramLabel.config(text = "Pick Up {} Parameters".format(missionCounter))
            self.window.valueLabel.config(text = "Pick Up {} Values".format(missionCounter))
            
            self.window.paramListBox.delete(0, "end")
            self.window.valueListBox.delete(0, "end")
            self.window.paramListBox.insert("end", "Time")
            self.window.valueListBox.insert("end", self.getSavedValues("pickUpTime {}".format(missionCounter))[0])
            self.window.paramListBox.insert("end", "SPT")
            self.window.valueListBox.insert("end", self.getSavedValues("pickUpSPT {}".format(missionCounter))[0])
            
            previousIndex = indexTracker
        
        indexTracker = self.window.missionListBox.index("active")
        
    def saveValues(self, name, value):
        '''
        Adds a key and value pair to a dictionary
        '''
        global kwargsValueList
        
        kwargsValueList[name] = value
        
    def getSavedValues(self, *args):
        '''
        Retrieves the value from the key and value pair.
        '''
        global kwargsValueList
        
        valueList = []
        for i, name in enumerate(args):
            if kwargsValueList.get(name) == None:
                valueList.append(0) 
            else:
                valueList.append(kwargsValueList.get(name))  
        return valueList
        
class ImageProcessingMissionSelector:
    '''
    This class handles the image processing aspect of the mission selector system. 
    '''
    def __init__(self, window):
        self.window = window
        
    def writeIPValuesToFile(self, camera):
        global frontPreviousKwargsValueList, bottomPreviousKwargsValueList
        
        #Removing space in the drop down box value
        imageProcessingDropDownListValue = self.window.dropBoxImageProcessingValue.get().replace(" ", "") 
        
        frontKwargsValueList={'minHueFront': self.window.filterScales[0].get(), 'minSatFront': self.window.filterScales[1].get(), 'minValFront': self.window.filterScales[2].get(), 
                              'maxHueFront': self.window.filterScales[3].get(), 'maxSatFront': self.window.filterScales[4].get(), 'maxValFront': self.window.filterScales[5].get(), 
                              'operation1Front': self.window.filterScales[6].get(), 'iteration1Front': self.window.filterScales[7].get(), 'operation2Front': self.window.filterScales[8].get(), 'iteration2Front': self.window.filterScales[9].get(), 
                              'rectCannyThresh1Front': self.window.objectDetectScales[0].get(), 'rectMinWidthFront': self.window.objectDetectScales[1].get(), 'rectMinHeightFront': self.window.objectDetectScales[2].get(), 'rectCannyThresh2Front': self.window.objectDetectScales[3].get(), 'rectMaxWidthFront': self.window.objectDetectScales[4].get(), 'rectMaxHeightFront': self.window.objectDetectScales[5].get(), 
                              'rectBlurFront': self.window.objectDetectScales[6].get(), 'blank1Front': self.window.objectDetectScales[7].get(), 'blank2Front': self.window.objectDetectScales[8].get(), 'blank3Front': self.window.objectDetectScales[9].get(),
                              'camshiftDetectFront': self.window.objectDetectScales_CheckBoxes[0].get(), 'rectDetectFront': self.window.objectDetectScales_CheckBoxes[1].get()}
        
        bottomKwargsValueList={'minHueBottom': self.window.filterScales[10].get(), 'minSatBottom': self.window.filterScales[11].get(), 'minValBottom': self.window.filterScales[12].get(), 
                               'maxHueBottom': self.window.filterScales[13].get(), 'maxSatBottom': self.window.filterScales[14].get(), 'maxValBottom': self.window.filterScales[15].get(), 
                               'operation1Bottom': self.window.filterScales[16].get(), 'iteration1Bottom': self.window.filterScales[17].get(), 'operation2Bottom': self.window.filterScales[18].get(), 'iteration2Bottom': self.window.filterScales[19].get(),
                               'rectCannyThresh1Bottom': self.window.objectDetectScales[10].get(), 'rectMinWidthBottom': self.window.objectDetectScales[11].get(), 'rectMinHeightBottom': self.window.objectDetectScales[12].get(), 'rectCannyThresh2Bottom': self.window.objectDetectScales[13].get(), 'rectMaxWidthBottom': self.window.objectDetectScales[14].get(), 'rectMaxHeightBottom': self.window.objectDetectScales[15].get(),
                               'rectBlurBottom': self.window.objectDetectScales[16].get(), 'blank1Bottom': self.window.objectDetectScales[17].get(), 'blank2Bottom': self.window.objectDetectScales[18].get(), 'blank3Bottom': self.window.objectDetectScales[19].get()}
          
        #Checks if values are for front camera and check if sliders have been moved
        if camera == "Front" and frontKwargsValueList != frontPreviousKwargsValueList:

            tempList = {imageProcessingDropDownListValue+"Front": frontKwargsValueList}
            
            #Writing image processing mission list
            previous_state_logging_system.Log('_Saved_Missions_/_Last_Mission_List_({})'.format(self.window.lastUser.get())).writeParameters(**tempList)
            
            frontPreviousKwargsValueList = frontKwargsValueList
                
        if camera == "Bottom" and bottomKwargsValueList != bottomPreviousKwargsValueList:
            
            tempList = {imageProcessingDropDownListValue+"Bottom": bottomKwargsValueList}
            
            #Writing image processing mission list
            previous_state_logging_system.Log('_Saved_Missions_/_Last_Mission_List_({})'.format(self.window.lastUser.get())).writeParameters(**tempList)
            
            bottomPreviousKwargsValueList = bottomKwargsValueList
    
    def updateIPSliders(self):
        
        #Gets the logging file of the user
        missionListLog = previous_state_logging_system.Log('_Saved_Missions_/_Last_Mission_List_({})'.format(self.window.lastUser.get())) 
        
        #Removing space in the drop down box value
        imageProcessingDropDownName = self.window.dropBoxImageProcessingValue.get().replace(" ", "")
        
        #Get all value objects in file that consist of the current IP drop down lost value with a Front/Bottom added to it
        frontValues = missionListLog.getParameters(imageProcessingDropDownName+"Front")
        bottomValues = missionListLog.getParameters(imageProcessingDropDownName+"Bottom")
        
        #Obtain actual values from objects
        frontKwargsValues = getattr(frontValues, self.window.dropBoxImageProcessingValue.get().replace(" ", "")+"Front") #Can not call method with string with dot operator, this is an elegant soultion to this
        bottomKwargsValues = getattr(bottomValues, self.window.dropBoxImageProcessingValue.get().replace(" ", "")+"Bottom") #Can not call method with string with dot operator, this is an elegant soultion to this

        iterateFilterList = 10 #How many front filters there are to iterate through in front or bottom
        iterateObjectDetectList = 10 #How many front object detects there are to iterate through in front or bottom
        iterateObjectDetectCheckBoxList = 2 #How many front object detect check boxes to iterate through
        
        if frontKwargsValues != 0:
            frontImageProcValues = [frontKwargsValues["minHueFront"], frontKwargsValues["minSatFront"], frontKwargsValues["minValFront"], frontKwargsValues["maxHueFront"], frontKwargsValues["maxSatFront"], frontKwargsValues["maxValFront"], 
                                    frontKwargsValues["operation1Front"], frontKwargsValues["iteration1Front"], frontKwargsValues["operation2Front"], frontKwargsValues["iteration2Front"],
                                    frontKwargsValues["rectCannyThresh1Front"], frontKwargsValues["rectMinWidthFront"], frontKwargsValues["rectMinHeightFront"], frontKwargsValues["rectCannyThresh2Front"], frontKwargsValues["rectMaxWidthFront"], frontKwargsValues["rectMaxHeightFront"], 
                                    frontKwargsValues["rectBlurFront"], frontKwargsValues["blank1Front"], frontKwargsValues["blank2Front"], frontKwargsValues["blank3Front"],
                                    frontKwargsValues["camshiftDetectFront"], frontKwargsValues["rectDetectFront"]]
        
            for x in range(iterateFilterList):
                self.window.filterScales[x].set(frontImageProcValues[x]) #Iterate through filter list for front camera and set sliders
            for x in range(iterateObjectDetectList): #Iterate through object detect list for front camera and set sliders
                self.window.objectDetectScales[x].set(frontImageProcValues[x+iterateFilterList])
            for x in range(iterateObjectDetectCheckBoxList): #Iterate through object detect check boxes and set check boxes. Only need to do this once, don't need to do set this for bottom camera.
                if frontImageProcValues[x+iterateFilterList+iterateObjectDetectList] == 1: #If the check boxes were on in the last session, turn them on in this session
                    self.window.objectDetectScales[x+(len(self.window.objectDetectScales)-iterateObjectDetectCheckBoxList)].select()
                if frontImageProcValues[x+iterateFilterList+iterateObjectDetectList] == 0:
                    self.window.objectDetectScales[x+(len(self.window.objectDetectScales)-iterateObjectDetectCheckBoxList)].deselect()
        
        if bottomKwargsValues != 0:  
            bottomImageProcValues = [bottomKwargsValues["minHueBottom"], bottomKwargsValues["minSatBottom"], bottomKwargsValues["minValBottom"], bottomKwargsValues["maxHueBottom"], bottomKwargsValues["maxSatBottom"], bottomKwargsValues["maxValBottom"],
                                     bottomKwargsValues["operation1Bottom"], bottomKwargsValues["iteration1Bottom"], bottomKwargsValues["operation2Bottom"], bottomKwargsValues["iteration2Bottom"],
                                     bottomKwargsValues["rectCannyThresh1Bottom"], bottomKwargsValues["rectMinWidthBottom"], bottomKwargsValues["rectMinHeightBottom"], bottomKwargsValues["rectCannyThresh2Bottom"], bottomKwargsValues["rectMaxWidthBottom"], bottomKwargsValues["rectMaxHeightBottom"], 
                                     bottomKwargsValues["rectBlurBottom"], bottomKwargsValues["blank1Bottom"], bottomKwargsValues["blank2Bottom"], bottomKwargsValues["blank3Bottom"]]
            
            for x in range(iterateFilterList):
                self.window.filterScales[x+iterateFilterList].set(bottomImageProcValues[x])
            for x in range(iterateObjectDetectList):
                self.window.objectDetectScales[x+iterateObjectDetectList].set(bottomImageProcValues[x+iterateFilterList])
        
        #These statements make it so that when the IP drop down list is changed, is won't copy over the values from the previous drop down value
        if frontKwargsValues == 0:
            for x in range(iterateFilterList):
                self.window.filterScales[x].set(0)
            for x in range(iterateObjectDetectList):
                self.window.objectDetectScales[x].set(0)
            
        
        if bottomKwargsValues == 0:  
            for x in range(iterateFilterList):
                self.window.filterScales[x+iterateFilterList].set(0)
            for x in range(iterateObjectDetectList):
                self.window.objectDetectScales[x+iterateObjectDetectList].set(0)
                
    
    def updateIPDropDownList(self):
        
        menu = self.window.optionMenu["menu"]
        
        if len(self.window.missionListBox.get(0, "end")) > 0:
            menu.delete(0, "end")
            for string in self.window.missionListBox.get(0, "end"):
                menu.add_command(label=string, command=lambda value=string:self.window.dropBoxImageProcessingValue.set(value))
                
            self.window.dropBoxImageProcessingValue.set(self.window.missionListBox.get(0, "end")[0])
            
        else:
            menu.delete(0, "end")
            self.window.dropBoxImageProcessingValue.set("")
            
class PreviousMissionListLogging:
    '''
    Exports and loads the mission list from previous sessions automatically from different user accounts. This is not to be confused with the
    export and load classes when the buttons are pressed so that the user can manually export and save missions
    '''
    
    def __init__(self, window):
        self.window = window
        self.log = previous_state_logging_system.Log('_Saved_Missions_/_Last_Mission_List_({})'.format(self.window.lastUser.get()))
        
    def export(self):
        global kwargsValueList
        if not os.path.exists('_Saved_Missions_'):
            os.mkdir('_Saved_Missions_')
        
        try:
            self.log.writeParameters(missionList = str(self.window.missionListBox.get(0, "end")), paramValueList = kwargsValueList)
        except:
            pass
        
    def load(self, name):
        global kwargsValueList, missionNames
        
        #Get rid of everything
        kwargsValueList = {}
        self.window.missionListBox.delete(0, "end")
        self.window.paramListBox.delete(0, "end")
        self.window.valueListBox.delete(0, "end")
        
        try:
            if not os.path.exists('_Saved_Missions_'):
                os.mkdir('_Saved_Missions_')
                        
            values = MissionSelector(self.window)

            logValues = self.log.getParameters("missionList", "paramValueList")
            savedMissionTypes = logValues.missionList
            savedMissionValues = logValues.paramValueList
            
            
            for x in range(len(savedMissionTypes)):
                self.window.missionListBox.insert(x, savedMissionTypes[x])
            for i, name in enumerate(savedMissionValues.keys()):
                values.saveValues(name, savedMissionValues[name])
                
            #Increments iteration counter when variable is loaded so when the same type of mission that was loaded in is added again, it wont forget to count the ones the user loaded in
            for x in range(self.window.missionListBox.size()):
                name = ''.join([i for i in self.window.missionListBox.get(x) if not i.isdigit()]).rstrip().partition(' ')[0]
                for y in range(len(missionNames)):
                    if name in missionNames[y]:
                        missionTypeCounters[y]+=1
              
            #Selects the first element on the list
            self.window.missionListBox.selection_set(0) 
            
        except:
            print "{} does not have a mission list from last session.".format(name)
            
  
#Needs to be a class since this piece of code is being activated by a widget in Tkinter
class MissionSelectorType:
    '''
    Allows the ability to select which mission type is desired when pressing the add button.
    '''
    def __init__(self, window, missionListBox):
        global missionNames
        self.missionListBox = missionListBox
        self.window = window
        
        #Pop up window object and size
        self.top = Tkinter.Toplevel(window)
        self.top.geometry("285x35+690+250")
        self.top.focus()

        #Pop up window
        missionLabel = Tkinter.Label(self.top, text = "Select a mission type:")
        missionLabel.grid(row = 0, column = 0)
        self.value = Tkinter.StringVar(self.top)
        self.value.set(missionNames[0]) # default value
        options = Tkinter.OptionMenu(self.top, self.value, missionNames[0], missionNames[1], missionNames[2], missionNames[3], missionNames[4], missionNames[5], missionNames[6], missionNames[7], missionNames[8])
        options.grid(row = 0, column = 1)
        options.bind("<Button-1>", self.refresh) #This is to stop the gui from flickering
        self.top.bind("<Return>", self.ok) #Allows me to push enter instead of push OK if desired
        okButton = Tkinter.Button(self.top, text = "OK", command = self.ok)
        okButton.grid(row = 0, column = 2)
        
        
    def ok(self, *event):
        global missionTypeCounters, missionNames
        
        for x in range(len(missionNames)):
            if self.value.get() == missionNames[x]:
                index = x
                missionTypeCounters[index]+=1
                #print self.value.get()+" 1", self.window.missionListBox.get(0, "end")
                if self.window.missionListBox.size() == 0:
                    missionTypeCounters[index] = 1
                
                #This block of code will make sure that the mission listbox will contain mission types with the lowest number
                for y in range(missionTypeCounters[index]+1):
                    if self.value.get()+" {}".format(y+1) not in self.window.missionListBox.get(0, "end") and self.window.missionListBox.size() != 0:
                        missionTypeCounters[index] -= (missionTypeCounters[index] - (y+1))
                        break
                
                #This block of code will make sure that the mission listbox will NOT contain mission types with duplicate numbers
                while self.value.get()+" "+str(missionTypeCounters[index]) in self.window.missionListBox.get(0, "end"):
                    missionTypeCounters[index]+=1
                        
        self.missionListBox.insert("end", self.value.get()+" "+str(missionTypeCounters[index]))   
        self.top.destroy()
        
        #Highlights and activates the last entry in the list
        self.window.missionListBox.select_clear(0, "end")
        self.window.missionListBox.select_set("end")
        self.window.missionListBox.activate("end")
        
        #Updating image processing list
        ImageProcessingMissionSelector(self.window).updateIPDropDownList()
        
        #Logs data in list to bring up last session when program restarts
        PreviousMissionListLogging(self.window).export()
        
    def refresh(self, *event):#This is to stop the gui from flickering
        self.window.update()
        
#Needs to be a class since this piece of code is being activated by a widget in Tkinter
class MissionSelectorValues:
    '''
    Allows the ability to select what values are desired when double clicking the items in the value list.
    '''
    def __init__(self, event, args):
        self.window = args[0]
        self.valueListBox = args[1]
        self.paramListBox = args[2]
        
        
        #Pop up window object and size
        self.top = Tkinter.Toplevel(self.window)
        self.top.geometry("230x35+690+250")
        
        #Pop up window
        valueLabel = Tkinter.Label(self.top, text = "New Value: ")
        valueLabel.grid(row = 0, column = 0)
        self.valueEntry = Tkinter.Entry(self.top)
        self.valueEntry.grid(row = 0, column = 1)
        self.valueEntry.focus()
        self.top.bind("<Return>", self.ok) #Allows me to push enter instead of push OK if desired
        okButton = Tkinter.Button(self.top, text = "OK", command = self.ok)
        okButton.grid(row = 0, column = 2)
        
    def ok(self, *events):
        global kwargsValueList, missionTypeCounters, indexTracker, navigationIndex, buoyIndex, pathIndex, maneuveringIndex, torpedoIndex, dropperIndex, pegManipulationIndex, pingerIndex, pickUp
        
        values = MissionSelector(self.window)
        
        index = self.valueListBox.index("active")
        self.valueListBox.delete("active")
        try:
            if float(self.valueEntry.get()).is_integer():
                newValue = int(self.valueEntry.get())
            else:
                newValue = float(self.valueEntry.get())
        except:
            newValue = 0
        print 
        self.valueListBox.insert(index, newValue)
        
        missionCounter = [int(s) for s in self.window.missionListBox.get("active").split() if s.isdigit()][0]
        
        if "Navigation" in self.window.paramLabel.cget("text"): #If the parameter label name above the listbox equals "Navigation Parameters"
            if self.paramListBox.get(index) == "Time": #Once a value is selected, that index is put into the paramListBox. If paramListBox(index) equals "Time"
                values.saveValues("navigationTime {}".format(missionCounter), newValue) #Save the values in an appending dictionary
            if self.paramListBox.get(index) == "X":
                values.saveValues("navigationX {}".format(missionCounter), newValue)
            if self.paramListBox.get(index) == "Y":
                values.saveValues("navigationY {}".format(missionCounter), newValue)
            if self.paramListBox.get(index) == "Z":
                values.saveValues("navigationZ {}".format(missionCounter), newValue)
            if self.paramListBox.get(index) == "FSD?":
                values.saveValues("navigationFSD {}".format(missionCounter), newValue)
                
        elif "Buoy" in self.window.paramLabel.cget("text"):
            if self.paramListBox.get(index) == "Time":
                values.saveValues("buoyTime {}".format(missionCounter), newValue)
            if self.paramListBox.get(index) == "LED?":
                values.saveValues("buoyLED {}".format(missionCounter), newValue)
            if self.paramListBox.get(index) == "SPT":
                values.saveValues("buoySPT {}".format(missionCounter), newValue)
                
        elif "Path" in self.window.paramLabel.cget("text"):
            if self.paramListBox.get(index) == "Time":
                values.saveValues("pathTime {}".format(missionCounter), newValue)
            if self.paramListBox.get(index) == "SPT":
                values.saveValues("pathSPT {}".format(missionCounter), newValue)
                
        elif "Maneuvering" in self.window.paramLabel.cget("text"):
            if self.paramListBox.get(index) == "Time":
                values.saveValues("maneuveringTime {}".format(missionCounter), newValue)
            if self.paramListBox.get(index) == "SPT":
                values.saveValues("maneuveringSPT {}".format(missionCounter), newValue)
                
        elif "Torpedo" in self.window.paramLabel.cget("text"):
            if self.paramListBox.get(index) == "Time":
                values.saveValues("torpedoTime {}".format(missionCounter), newValue)
            if self.paramListBox.get(index) == "SPT":
                values.saveValues("torpedoSPT {}".format(missionCounter), newValue)
                
        elif "Dropper" in self.window.paramLabel.cget("text"):
            if self.paramListBox.get(index) == "Time":
                values.saveValues("dropperTime {}".format(missionCounter), newValue)
            if self.paramListBox.get(index) == "SPT":
                values.saveValues("dropperSPT {}".format(missionCounter), newValue)
                
        elif "Peg Manipulation" in self.window.paramLabel.cget("text"):
            if self.paramListBox.get(index) == "Time":
                values.saveValues("pegManipulationTime {}".format(missionCounter), newValue)
            if self.paramListBox.get(index) == "SPT":
                values.saveValues("pegManipulationSPT {}".format(missionCounter), newValue)
        
        elif "Pinger" in self.window.paramLabel.cget("text"):
            if self.paramListBox.get(index) == "Time":
                values.saveValues("pingerTime {}".format(missionCounter), newValue)
            if self.paramListBox.get(index) == "SPT":
                values.saveValues("pingerSPT {}".format(missionCounter), newValue)
                
        elif "Pick Up" in self.window.paramLabel.cget("text"):
            if self.paramListBox.get(index) == "Time":
                values.saveValues("pickUpTime {}".format(missionCounter), newValue)
            if self.paramListBox.get(index) == "SPT":
                values.saveValues("pickUpSPT {}".format(missionCounter), newValue)
                
        #Logs data in list to bring up last session when program restarts
        PreviousMissionListLogging(self.window).export()
        
        self.top.destroy()
  
#Needs to be a class since this piece of code is being activated by a widget in Tkinter      
class MoveUpDown:
    '''
    Allows the ability change the order in which missions are executed when pressing the up or down button. This will also change 
    the order in the image processing drop down list in the image processing tab.
    '''
    def moveUp(self, window):
        
        #kwargsValueList = {key: value for key,value in kwargsValueList.iteritems() if window.missionListBox.index("active") not in key}
        #print kwargsValueList
        
        pos = window.missionListBox.index("active")
        if pos == 0: #Cant go any higher
            return #Break out of function
        missionTypeName = window.missionListBox.get(pos)
        window.missionListBox.delete(pos)
        window.missionListBox.insert(pos-1, missionTypeName)
        window.missionListBox.select_clear(pos-1)
        window.missionListBox.select_set(pos-1)
        window.missionListBox.activate(pos-1)
        
        #Updating image processing list
        ImageProcessingMissionSelector(window).updateIPDropDownList()
        
        #Logs data in list to bring up last session when program restarts
        PreviousMissionListLogging(window).export()
        
    def moveDown(self, window):
        
        #kwargsValueList = {key: value for key,value in kwargsValueList.iteritems() if window.missionListBox.index("active") not in key}
        #print kwargsValueList
        
        pos = window.missionListBox.index("active")
        if pos == window.missionListBox.size()-1: #Cant go any lower
            return #Break out of function
        missionTypeName = window.missionListBox.get(pos)
        window.missionListBox.delete(pos)
        window.missionListBox.insert(pos+1, missionTypeName)
        window.missionListBox.select_clear(pos+1)
        window.missionListBox.select_set(pos+1)
        window.missionListBox.activate(pos+1)
        
        #Updating image processing list
        ImageProcessingMissionSelector(window).updateIPDropDownList()
        
        #Logs data in list to bring up last session when program restarts
        PreviousMissionListLogging(window).export()

#Needs to be a class since this piece of code is being activated by a widget in Tkinter      
class DeleteMissionType:
    '''
    Allows the ability to press the delete button to delete missions from both the mission list and the image processing drop down list. 
    This will also remove the values in the logging system so that when missions are added back, you get to select mission and image 
    processing values from scratch.
    '''
    def __init__(self, window):
        global kwargsValueList, missionTypeCounters, previousIndex
        
        if window.missionListBox.size() > 0: #If there is something to delete
            number = str([int(s) for s in window.missionListBox.get("active").split() if s.isdigit()][0])
            name = ''.join([i for i in window.missionListBox.get("active").lower() if not i.isdigit()]).rstrip().partition(' ')[0] #rstrip removes extra space, partition(' ')[0] just takes first work if the string is two words (peg manipulation)
                 
            #This line creates a new list but without any of the params or values saved from before that is associated with the mission type you deleted.
            #It is important to note that this method is assuming you stick to the naming convention of button the mission types name before each variable when you save it.
            kwargsValueList = {key: value for key,value in kwargsValueList.iteritems() if name not in key or number not in key}
            
            #Decrements iteration counter when variable is deleted so next time when the same type of mission that was deleted is added again, it wont count the one the user deleted
            for x in range(len(missionNames)): 
                if name in missionNames[x].lower():
                    missionTypeCounters[x]-=1
            
            #Delete lines in file
            f = open("_Saved_Missions_/_Last_Mission_List_({})".format(window.lastUser.get()), "r")
            lines = f.readlines()
            f.close()
            f = open("_Saved_Missions_/_Last_Mission_List_({})".format(window.lastUser.get()), "w")
            for line in lines:
                if window.missionListBox.get("active").replace(" ", "")+"Front" not in line and window.missionListBox.get("active").replace(" ", "")+"Bottom" not in line:
                    f.write(line)
            f.close()
            
            #If I didn't set previousIndex to None, the new variable would fall into the same index as the one I just deleted. 
            #This means I would not be able to view missions params or values because of the checks I do in MissionSelector class        
            previousIndex = None  
            index = window.missionListBox.index("active")
            window.missionListBox.delete(index)
            window.paramListBox.delete(0, "end")
            window.valueListBox.delete(0, "end") 
            window.missionListBox.selection_set("active") #Highlights the mission type that is now in the place of the last mission type
            
            #Updating image processing list
            ImageProcessingMissionSelector(window).updateIPDropDownList()
            
            #Logs data in list to bring up last session when program restarts
            PreviousMissionListLogging(window).export()

#Needs to be a class since this piece of code is being activated by a widget in Tkinter       
class ExportList:
    '''
    Allows the ability to export both the mission/parameter/value lists and the image processing drop down list and values by
    clicking on the export button.
    '''
    def __init__(self, window):
        #Pop up window object and size
        self.top = Tkinter.Toplevel(window)
        self.top.geometry("220x35+690+250")
        self.window = window
        
        #Pop up window
        missionLabel = Tkinter.Label(self.top, text = "File name:")
        missionLabel.grid(row = 0, column = 0)
        self.userInput = Tkinter.Entry(self.top)
        self.userInput.grid(row=0, column=1)
        self.userInput.focus_set()
        self.top.bind("<Return>", self.ok) #Allows me to push enter instead of push OK if desired
        okButton = Tkinter.Button(self.top, text = "OK", command = self.ok)
        okButton.grid(row = 0, column = 2)
        
        #Make file if not exist
        if not os.path.exists('_Saved_Missions_'):
            os.mkdir('_Saved_Missions_')
        
    def ok(self, *event):
        global kwargsValueList
        
        #Copying data from _Last_Mission_List_ to saved file
        shutil.copy('_Saved_Missions_/_Last_Mission_List_({})'.format(self.window.lastUser.get()), '_Saved_Missions_/'+self.userInput.get())

        self.top.destroy()

#Needs to be a class since this piece of code is being activated by a widget in Tkinter       
class loadList:
    '''
    Allows the ability to load in both the mission/parameter/value lists and the image processing drop down list and values by
    clicking on the load button.
    '''
    def __init__(self, window):
        global kwargsValueList, missionNames
        fileLocation = tkFileDialog.askopenfilename()
        
        try:
            log = previous_state_logging_system.Log(fileLocation)
            values = MissionSelector(window)
            
            
            logValues = log.getParameters("missionList", "paramValueList")
            savedMissionTypes = logValues.missionList #Need a literal eval or else ill be getting characters
            savedMissionValues = logValues.paramValueList
            
            #Get rid of everything
            kwargsValueList = {}
            window.missionListBox.delete(0, "end")
            window.paramListBox.delete(0, "end")
            window.valueListBox.delete(0, "end")
    
            for x in range(len(savedMissionTypes)):
                window.missionListBox.insert(x, savedMissionTypes[x])
            for i, name in enumerate(savedMissionValues.keys()):
                values.saveValues(name, savedMissionValues[name])
                
            #Increments iteration counter when variable is loaded so when the same type of mission that was loaded in is added again, it wont forget to count the ones the user loaded in
            for x in range(window.missionListBox.size()):
                name = ''.join([i for i in window.missionListBox.get(x) if not i.isdigit()]).rstrip().partition(' ')[0]
                for y in range(len(missionNames)):
                    if name in missionNames[y]:
                        missionTypeCounters[y]+=1
            
            #Copying data from saved file to _Last_Mission_List_ 
            shutil.copy(fileLocation, '_Saved_Missions_/_Last_Mission_List_({})'.format(window.lastUser.get()))
            
            window.missionListBox.selection_set(0) #Selects the first element on the list
            
            #Updating image processing list
            ImageProcessingMissionSelector(window).updateIPDropDownList()
            
            #Logs data in list to bring up last session when program restarts
            PreviousMissionListLogging(window).export()
                
        except:
            print "Can't open file."

