'''
Copyright 2014, Austin Owens, All rights reserved.

Created on Nov 8, 2014

@author: Austin
'''
import cv2, numpy
import PIL.ImageTk, PIL.Image
import graphic_overlay
import object_detection
import previous_state_logging_system
import time, datetime
import mission_selector_system
import main.utility_package.utilities as utilities
import controller_screen

frontRecordingTimer = utilities.Timer()
bottomRecordingTimer = utilities.Timer()
frontRecordingTextPulseTimer = utilities.Timer()
bottomRecordingTextPulseTimer = utilities.Timer()


fakeHeadingInput, fakePitchInput, fakeRollInput, fakeBatteryInput, fakeMotorInput = 0, 0, 0, 0, 0
scaleUpDownBattery, scaleUpDownHeading, scaleUpDownRoll, scaleUpDownMotor, toggleDirection = True, True, True, True, False
fakePitchInput = 0

previousHeadingPosition, previousRollPosition, previousDepthPosition, previousMotorPosition, previousAttitudePosition, previousBatteryPosition, previousTemperaturePosition, previousStatusPosition = None, None, None, None, None, None, None, None

scaledFrontImg = 0
scaledBottomImg = 0

previousDropBoxImageProcessingValue = None

previousConfigScaleNum = [0]*43 #*Config scales
configScaleValue = [0]*43
track_window = (0, 0, 0, 0)

updateIPScales = True
setInitialImageProcessingList = True
setInitialGaugeTrackBarPosition = True
setInitialHSVTrackBarPosition = True
setInitialFilterTrackBarPosition = True
setInitialConsoleCheckBoxOptions = True

class UpdateGUI():
    def __init__(self, window, rawImgWidth, rawImgHeight, processedImgWidth, processedImgHeight):
        #GUI Window Object
        self.window = window
        
        #Mission selector system objects
        self.missionSelectorSystem = mission_selector_system.MissionSelector(self.window)
        self.imageProcessingMissionSelector = mission_selector_system.ImageProcessingMissionSelector(self.window)
        
        #Open Camera
        self.cap1 = cv2.VideoCapture(0)
        self.cap2 = cv2.VideoCapture(1)
        #time.sleep(1)
        if not self.cap2.isOpened(): #if second camera DOES exist
            self.cam2 = False
        elif self.cap2.isOpened(): #if second camera DOESN'T exist
            self.cam2 = True
           
        #Logging system for mission selector 
        mission_selector_system.PreviousMissionListLogging(self.window).load(self.window.lastUser.get())
        
        #previous state logging system gui params
        self.logGuiParams = previous_state_logging_system.Log('_Saved_Settings_/_GUI_Parameters_({}).txt'.format(window.lastUser.get()))
        self.previousUser = window.lastUser.get()
        
        #Graphics
        self.HUD = graphic_overlay.GraphicOverlay(window, rawImgWidth, rawImgHeight)
        
        #Camshift
        self.camshiftFront = object_detection.Camshift()
        self.camshiftBottom = object_detection.Camshift()
        self.circleFront = object_detection.CircleDetect()
        
        #Img Sizes
        self.rawImgWidth = rawImgWidth
        self.rawImgHeight = rawImgHeight
        self.processedImgWidth = processedImgWidth
        self.processedImgHeight = processedImgHeight
        
        #Recording states
        self.recordingState = ["normal", "disabled"]
        self.toggleStates = False
        
        #temp
        self.previousTempVal = None
        
    def run(self):
        global fakeHeadingInput, fakePitchInput, fakeRollInput, scaledFrontImg, scaledBottomImg, scaleUpDownHeading, scaleUpDownRoll
        
        #RAW IMG
        flagFront, frontImg = self.cap1.read()
        if self.cam2 == False: #if second camera DOESN'T exist
            bottomImg = frontImg
        else: #if second camera DOES exist
            flagBottom, bottomImg = self.cap2.read()
            
            
        if self.window.spaceBar == False: #If space bar is pressed, scaledFrontImg and scaledBottomImg will maintain the same image which will imitate freezing the video stream
            scaledFrontImg = cv2.resize(frontImg, (self.rawImgWidth, self.rawImgHeight)) #resize image
            scaledBottomImg = cv2.resize(bottomImg, (self.rawImgWidth, self.rawImgHeight)) #resize image
        
        #ROI SAMPLING  
        self.__roiSample__(3, self.window.frontRawImgLabel, self.window.bottomRawImgLabel, self.window.filterScales) #(Tolerance, frontRawImgLabel, bottomRawImgLabel, filterScales)            
        
        #DRAWING ALL GAUGES
        if self.window.externalDevicesData != None:
            #if self.window.externalDevicesData[0][0][2] != self.previousTempVal:
                #print self.window.externalDevicesData
                #self.previousTempVal = self.window.externalDevicesData[0][0][2]
                
            self.__drawAllGauges__(self.window.configurationGaugeScales, 
                                   self.window.externalDevicesData[1], #Orientation data
                                   [fakeBatteryInput, fakeBatteryInput, fakeBatteryInput], #Position data
                                   [fakeBatteryInput, fakeBatteryInput, fakeBatteryInput], #Velocity data
                                   fakeHeadingInput*0.1, #Depth data
                                   (fakeBatteryInput, fakeBatteryInput, fakeBatteryInput, fakeBatteryInput), #Battery data
                                   round(fakeBatteryInput*0.1+25, 1), #Temperature data
                                   [[fakeMotorInput, fakeMotorInput, fakeMotorInput, fakeMotorInput, fakeMotorInput, fakeMotorInput, fakeMotorInput, fakeMotorInput], #Motor data
                                    [toggleDirection, toggleDirection, toggleDirection, toggleDirection, toggleDirection, toggleDirection, toggleDirection, toggleDirection]], #Motor data
                                   ["Navigation 1", fakeBatteryInput]) #Status data
        else:
            self.__drawAllGauges__(self.window.configurationGaugeScales, 
                                   [fakeHeadingInput, fakePitchInput, fakeRollInput], #Orientation data
                                   [fakeBatteryInput, fakeBatteryInput, fakeBatteryInput], #Position data
                                   [fakeBatteryInput, fakeBatteryInput, fakeBatteryInput], #Velocity data
                                   fakeHeadingInput*0.1, #Depth data
                                   (fakeBatteryInput, fakeBatteryInput, fakeBatteryInput, fakeBatteryInput), #Battery data
                                   round(fakeBatteryInput*0.1+25, 1), #Temperature data
                                   [[fakeMotorInput, fakeMotorInput, fakeMotorInput, fakeMotorInput, fakeMotorInput, fakeMotorInput, fakeMotorInput, fakeMotorInput], #Motor data
                                    [toggleDirection, toggleDirection, toggleDirection, toggleDirection, toggleDirection, toggleDirection, toggleDirection, toggleDirection]], #Motor data
                                   ["Navigation 1", fakeBatteryInput]) #Status data
        
        #LOOKING FOR KEYBOARD INPUT
        self.__keyboardInput__()    
            
        #GUI UPDATES
        self.__guiUpdates__()
        
#<<<<<<< .mine
        #print self.missionSelectorSystem.getAllMissionSelectorData()
        
#=======
#>>>>>>> .r1365
        #IMAGE PROCESSING       
        imageProcValues = self.__imageProcessing__(frontImg, bottomImg, self.window.frontRawImgLabel, self.window.bottomRawImgLabel, self.window.frontProcessedImgLabel, self.window.bottomProcessedImgLabel, self.window.filterScales)
        
        #CONTROLLER UPDATES
        self.__controllerUpdates__()
    
    def __roiSample__(self, tolerance, frontRawImgLabel, bottomRawImgLabel, filterScales):
        global updateIPScales, setInitialHSVTrackBarPosition, previousDropBoxImageProcessingValue
            
        if self.window.dropBoxImageProcessingValue.get() != previousDropBoxImageProcessingValue or updateIPScales == True: #If the image processing drop down box is changed or the user is changed, update sliders
            self.imageProcessingMissionSelector.updateIPSliders()

            updateIPScales = False
            
          
        if frontRawImgLabel.buttonReleased == True:
            x1, y1 = frontRawImgLabel.boxPoint1
            x2, y2 = frontRawImgLabel.boxPoint2
            tolerance = 3
            
            roiBGR = scaledFrontImg[y1:y2, x1:x2] #position (x, y) in matrix
            
            roiHSV = cv2.cvtColor(roiBGR, cv2.COLOR_BGR2HSV)
            
            minHSV = numpy.amin((numpy.amin(roiHSV, 1)), 0)
            maxHSV = numpy.amax((numpy.amax(roiHSV, 1)), 0)
            
            filterScales[0].set(minHSV[0] - tolerance)
            filterScales[1].set(minHSV[1] - tolerance) 
            filterScales[2].set(minHSV[2] - tolerance) 
            filterScales[3].set(maxHSV[0] + tolerance) 
            filterScales[4].set(maxHSV[1] + tolerance) 
            filterScales[5].set(maxHSV[2] + tolerance)

            frontRawImgLabel.mouseDragLocation = [0, 0] #Reset so box doesn't start in a weird location when I start to draw again
            frontRawImgLabel.buttonReleased = False
        
        elif bottomRawImgLabel.buttonReleased == True:
            x1, y1 = bottomRawImgLabel.boxPoint1
            x2, y2 = bottomRawImgLabel.boxPoint2
            tolerance = 3
            
            roiBGR = scaledBottomImg[y1:y2, x1:x2] #position (x, y) in matrix
            
            roiHSV = cv2.cvtColor(roiBGR, cv2.COLOR_BGR2HSV)
            
            minHSV = numpy.amin((numpy.amin(roiHSV, 1)), 0)
            maxHSV = numpy.amax((numpy.amax(roiHSV, 1)), 0)
            
            filterScales[11].set(minHSV[0] - tolerance)
            filterScales[12].set(minHSV[1] - tolerance) 
            filterScales[13].set(minHSV[2] - tolerance) 
            filterScales[14].set(maxHSV[0] + tolerance) 
            filterScales[15].set(maxHSV[1] + tolerance) 
            filterScales[16].set(maxHSV[2] + tolerance)
        
            bottomRawImgLabel.mouseDragLocation = [0, 0] #Reset so box doesn't start in a weird location when I start to draw again
            bottomRawImgLabel.buttonReleased = False
        
        #Write IP values to file
        self.imageProcessingMissionSelector.writeIPValuesToFile("Front")
        self.imageProcessingMissionSelector.writeIPValuesToFile("Bottom")
        
        if frontRawImgLabel.buttonPressed == True and self.window.spaceBar == False: #Draws the box on the front raw img
            point1 = frontRawImgLabel.boxPoint1
            point2 = frontRawImgLabel.mouseDragLocation
            cv2.rectangle(scaledFrontImg, (point1[0], point1[1]), (point2[0], point2[1]), (0, 0, 255))
            
        if bottomRawImgLabel.buttonPressed == True and self.window.spaceBar == False: #Draws the box on the button raw img
            point1 = bottomRawImgLabel.boxPoint1
            point2 = bottomRawImgLabel.mouseDragLocation
            cv2.rectangle(scaledBottomImg, (point1[0], point1[1]), (point2[0], point2[1]), (0, 0, 255))
            
        previousDropBoxImageProcessingValue = self.window.dropBoxImageProcessingValue.get()

    def __drawAllGauges__(self, configurationGaugeScales, orientationData, positionData, velocityData, depthData, batteryData, temperatureData, motorData, statusData):
        global previousHeadingPosition, previousRollPosition, previousDepthPosition, previousMotorPosition, previousAttitudePosition, previousBatteryPosition, previousTemperaturePosition, previousStatusPosition, previousConfigScaleNum, configScaleValue, setInitialGaugeTrackBarPosition, scaleUpDownBattery, fakeHeadingInput, fakePitchInput, fakeRollInput, fakeBatteryInput, fakeMotorInput, scaleUpDownHeading, scaleUpDownRoll, scaleUpDownMotor, toggleDirection

        if setInitialGaugeTrackBarPosition == True:
            values = self.logGuiParams.getParameters("headingGauge", "headingTickNum", "headingIncrement", "headingPosition", "headingWidth", 
                                            "pitchGauge", "pitchTickNum", "pitchIncrement", "pitchLength", 
                                            "rollGauge", "rollTickNum", "rollRange1", "rollRange2", "rollPosition", "rollWidth", 
                                            "depthGauge", "depthTickNum", "depthIncrement", "depthPosition", "depthLength",
                                            "attitudeGauge", "attitudeLength", "displayPosVel1", "displayPosVel2", "attitudePosition", "attitudeLetterSize", "attitudeLetterRatio",
                                            "batteryGauge", "batteryGaugeLength", "displayBatteryCurrent1", "displayBatteryCurrent2", "batteryPosition",
                                            "temperatureGauge", "temperatureSize", "temperaturePosition",
                                            "motorGauge", "motorSize", "motorPosition",
                                            "statusGauge", "statusPosition",
                                            "redGaugeColor", "greenGaugeColor", "blueGaugeColor")
            
            configScaleValues = [values.headingGauge, values.headingTickNum, values.headingIncrement, values.headingPosition, values.headingWidth, 
                                 values.pitchGauge, values.pitchTickNum, values.pitchIncrement, values.pitchLength, 
                                 values.rollGauge, values.rollTickNum, values.rollRange1, values.rollRange2, values.rollPosition, values.rollWidth, 
                                 values.depthGauge, values.depthTickNum, values.depthIncrement, values.depthPosition, values.depthLength, 
                                 values.attitudeGauge, values.attitudeLength, values.displayPosVel1, values.displayPosVel2, values.attitudePosition, values.attitudeLetterSize, values.attitudeLetterRatio, 
                                 values.batteryGauge, values.batteryGaugeLength, values.displayBatteryCurrent1, values.displayBatteryCurrent2, values.batteryPosition,
                                 values.temperatureGauge, values.temperatureSize, values.temperaturePosition,
                                 values.motorGauge, values.motorSize, values.motorPosition,
                                 values.statusGauge, values.statusPosition,
                                 values.redGaugeColor, values.greenGaugeColor, values.blueGaugeColor]

            for x in range(len(configurationGaugeScales)):
                checkBoxes = x == 0 or x == 5 or x == 9 or x == 15 or x == 20 or x == 27 or x == 32 or x == 35 or x == 38
                radioButtons = x == 11 or x == 12 or x == 22 or x == 23 or x == 29 or x == 30
                
                if checkBoxes:
                    if configScaleValues[x] == 1:
                        configurationGaugeScales[x].select()
                    
                    if configScaleValues[x] == 0:
                        configurationGaugeScales[x].deselect()
                
                elif radioButtons:
                    
                    if configScaleValues[11] == 0: #If radio button 1 was on in last session, keep it on
                        configurationGaugeScales[11].select() #Must be solid numbers (not x)
                    if configScaleValues[12] == 1: #If radio button 2 was on in last session, keep it on
                        configurationGaugeScales[12].select() #Must be solid numbers (not x)
                    if configScaleValues[22] == 1: #If radio button 1 was on in last session, keep it on
                        configurationGaugeScales[22].select() #Must be solid numbers (not x)
                    if configScaleValues[23] == 0: #If radio button 2 was on in last session, keep it on
                        configurationGaugeScales[23].select() #Must be solid numbers (not x)
                    if configScaleValues[29] == 1:
                        configurationGaugeScales[29].select() #Must be solid numbers (not x)
                    if configScaleValues[30] == 0: #If radio button 2 was on in last session, keep it on
                        configurationGaugeScales[30].select() #Must be solid numbers (not x)
                        
                else:
                    configurationGaugeScales[x].set(configScaleValues[x])
                    
            setInitialGaugeTrackBarPosition = False
            
              
            
        if self.window.spaceBar == False: #As long as space bar is NOT pressed this statement is True. If the space bar is pressed, the graphics will freeze
            if self.window.printOptionCheckboxValues[0].get() == 1:
                print "Time:", datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f'),"\t  Heading Data:  %6.2f  \t Pitch Data:  %6.2f  \t Roll Data:  %6.2f  \t Depth Data:  %6.2f" % (orientationData[0], orientationData[1], orientationData[2], depthData)
                
            for x in range(len(configurationGaugeScales)): #Put values into array for logging system
                checkBoxes = x == 0 or x == 5 or x == 9 or x == 15 or x == 20 or x == 27 or x == 32 or x == 35 or x == 38
                radioButtons = x == 11 or x == 12 or x == 22 or x == 23 or x == 29 or x == 30
                
                if checkBoxes:
                    if x == 0:
                        configScaleValue[x] = self.window.configurationGaugeScales_CheckBoxes[0].get()
                    elif x == 5:
                        configScaleValue[x] = self.window.configurationGaugeScales_CheckBoxes[1].get()
                    elif x == 9:
                        configScaleValue[x] = self.window.configurationGaugeScales_CheckBoxes[2].get()
                    elif x == 15:
                        configScaleValue[x] = self.window.configurationGaugeScales_CheckBoxes[3].get()
                    elif x == 20:
                        configScaleValue[x] = self.window.configurationGaugeScales_CheckBoxes[4].get()
                    elif x == 27:
                        configScaleValue[x] = self.window.configurationGaugeScales_CheckBoxes[5].get()
                    elif x == 32:
                        configScaleValue[x] = self.window.configurationGaugeScales_CheckBoxes[6].get()
                    elif x == 35:
                        configScaleValue[x] = self.window.configurationGaugeScales_CheckBoxes[7].get()
                    elif x == 38:
                        configScaleValue[x] = self.window.configurationGaugeScales_CheckBoxes[8].get()
                
                elif radioButtons:
                    if x == 11 or x == 12:
                        configScaleValue[x] = self.window.configurationGaugeScales_RadioButtons[0].get()
                    elif x == 22 or x == 23:
                        configScaleValue[x] = self.window.configurationGaugeScales_RadioButtons[1].get()
                    elif x == 29 or x == 30:
                        configScaleValue[x] = self.window.configurationGaugeScales_RadioButtons[2].get()
                        
                else:
                    configScaleValue[x] = configurationGaugeScales[x].get()
                    
    
                if previousConfigScaleNum[x] != configScaleValue[x]: #I need to check if the previous value equals the current value, if not, I need to initialize some variables
                    if x == 1: #Heading tick number config array position (Must match array index of tick number)
                        self.HUD.setInitialTickPosition[0] = True #Need index to increment every even number since there are only 4 values
                    elif x == 6: #Pitch tick number config array position (Must match array index of tick number)
                        self.HUD.setInitialTickPosition[1] = True #Need index to increment every even number since there are only 4 values
                    elif x == 16: #Depth tick number config array position (Must match array index of tick number)
                        self.HUD.setInitialTickPosition[2] = True #Need index to increment every even number since there are only 4 values
                
                previousConfigScaleNum[x] = configScaleValue[x]
                
            
            
            #Making assumptions based on user control   
            
            horizontalVerticalPositionScales = [configurationGaugeScales[3], configurationGaugeScales[13], configurationGaugeScales[18], configurationGaugeScales[37]]
            horizontalVerticalPositionValues = [configScaleValue[3], configScaleValue[13], configScaleValue[18], configScaleValue[37]]
            cornerPositionScales = [configurationGaugeScales[24], configurationGaugeScales[31], configurationGaugeScales[34], configurationGaugeScales[39]]
            cornerPositionValues = [configScaleValue[24], configScaleValue[31], configScaleValue[34], configScaleValue[39]]
            
            #If the position value is equal to another  position value, and the previous heading position is equal 
            #to the same thing, that means it was the roll that was being moved by the user and that the heading should be 
            #the one to move automatically to the roll position
            
            #Horizontal/Vertical 
            if horizontalVerticalPositionValues[0] == horizontalVerticalPositionValues[1] and previousHeadingPosition == horizontalVerticalPositionValues[0] and previousRollPosition != horizontalVerticalPositionValues[1]:
                horizontalVerticalPositionScales[0].set(previousRollPosition)  
            elif horizontalVerticalPositionValues[0] == horizontalVerticalPositionValues[1] and previousRollPosition == horizontalVerticalPositionValues[1] and previousHeadingPosition != horizontalVerticalPositionValues[0]:
                horizontalVerticalPositionScales[1].set(previousHeadingPosition)

            elif horizontalVerticalPositionValues[2] == horizontalVerticalPositionValues[3] and previousMotorPosition == horizontalVerticalPositionValues[3] and previousDepthPosition != horizontalVerticalPositionValues[2]:
                horizontalVerticalPositionScales[3].set(previousDepthPosition)  
            elif horizontalVerticalPositionValues[2] == horizontalVerticalPositionValues[3] and previousDepthPosition == horizontalVerticalPositionValues[2] and previousMotorPosition != horizontalVerticalPositionValues[3]:
                horizontalVerticalPositionScales[2].set(previousMotorPosition)
            
            #Corners
            elif cornerPositionValues[0] == cornerPositionValues[1] and previousAttitudePosition == cornerPositionValues[0] and previousBatteryPosition != cornerPositionValues[1]:
                cornerPositionScales[0].set(previousBatteryPosition)  
            elif cornerPositionValues[0] == cornerPositionValues[1] and previousBatteryPosition == cornerPositionValues[1] and previousAttitudePosition != cornerPositionValues[0]:
                cornerPositionScales[1].set(previousAttitudePosition)

            elif cornerPositionValues[0] == cornerPositionValues[2] and previousAttitudePosition == cornerPositionValues[0] and previousTemperaturePosition != cornerPositionValues[2]:
                cornerPositionScales[0].set(previousTemperaturePosition)
            elif cornerPositionValues[0] == cornerPositionValues[2] and previousTemperaturePosition == cornerPositionValues[2] and previousAttitudePosition != cornerPositionValues[0]:
                cornerPositionScales[2].set(previousAttitudePosition)
                
            elif cornerPositionValues[0] == cornerPositionValues[3] and previousAttitudePosition == cornerPositionValues[0] and previousStatusPosition != cornerPositionValues[3]:
                cornerPositionScales[0].set(previousStatusPosition)
            elif cornerPositionValues[0] == cornerPositionValues[3] and previousStatusPosition == cornerPositionValues[3] and previousAttitudePosition != cornerPositionValues[0]:
                cornerPositionScales[3].set(previousAttitudePosition)
                
            elif cornerPositionValues[1] == cornerPositionValues[2] and previousBatteryPosition == cornerPositionValues[1] and previousTemperaturePosition != cornerPositionValues[2]:
                cornerPositionScales[1].set(previousTemperaturePosition)
            elif cornerPositionValues[1] == cornerPositionValues[2] and previousTemperaturePosition == cornerPositionValues[2] and previousBatteryPosition != cornerPositionValues[1]:
                cornerPositionScales[2].set(previousBatteryPosition)
                
            elif cornerPositionValues[1] == cornerPositionValues[3] and previousBatteryPosition == cornerPositionValues[1] and previousStatusPosition != cornerPositionValues[3]:
                cornerPositionScales[1].set(previousStatusPosition)
            elif cornerPositionValues[1] == cornerPositionValues[3] and previousStatusPosition == cornerPositionValues[3] and previousBatteryPosition != cornerPositionValues[1]:
                cornerPositionScales[3].set(previousBatteryPosition)
                
            elif cornerPositionValues[2] == cornerPositionValues[3] and previousTemperaturePosition == cornerPositionValues[2] and previousStatusPosition != cornerPositionValues[3]:
                cornerPositionScales[2].set(previousStatusPosition)
            elif cornerPositionValues[2] == cornerPositionValues[3] and previousStatusPosition == cornerPositionValues[3] and previousTemperaturePosition != cornerPositionValues[2]:
                cornerPositionScales[3].set(previousTemperaturePosition)
                
            elif cornerPositionValues[0] == cornerPositionValues[1] and cornerPositionValues[0] == cornerPositionValues[2] and cornerPositionValues[0] == cornerPositionValues[3]: #When starting out, all corner gauges are on top of one another, this will move them other places initially 
                cornerPositionScales[0].set(0)  
                cornerPositionScales[1].set(1)
                cornerPositionScales[2].set(2)
                cornerPositionScales[3].set(3)
            
            
            previousHeadingPosition = configScaleValue[3]
            previousRollPosition = configScaleValue[13]
            previousDepthPosition = configScaleValue[18]
            previousMotorPosition = configScaleValue[37]
            previousAttitudePosition = configScaleValue[24]
            previousBatteryPosition = configScaleValue[31]
            previousTemperaturePosition = configScaleValue[34]
            previousStatusPosition = configScaleValue[39]
            
            #DRAWING ON IMGS
            if configScaleValue[0] == 1:
                self.HUD.drawHeadingGauge(scaledFrontImg, configScaleValue[1], configScaleValue[2], configScaleValue[3], configScaleValue[4], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), orientationData[0])
                self.HUD.drawHeadingGauge(scaledBottomImg, configScaleValue[1], configScaleValue[2], configScaleValue[3], configScaleValue[4], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), orientationData[0])
                
            if configScaleValue[5] == 1:
                self.HUD.drawPitchGauge(scaledFrontImg, configScaleValue[6], configScaleValue[7], configScaleValue[8], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), orientationData[1])
                self.HUD.drawPitchGauge(scaledBottomImg, configScaleValue[6], configScaleValue[7], configScaleValue[8], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), orientationData[1])
                
            if configScaleValue[9] == 1:
                self.HUD.drawRollGauge(scaledFrontImg, configScaleValue[10], configScaleValue[12], configScaleValue[13], configScaleValue[14], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), orientationData[2]) #Skip 8 (second radio button) since you only need to pass in the value of one of them to know which one is on
                self.HUD.drawRollGauge(scaledBottomImg, configScaleValue[10], configScaleValue[12], configScaleValue[13], configScaleValue[14], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), orientationData[2])
                
            if configScaleValue[15] == 1:
                self.HUD.drawDepthGauge(scaledFrontImg, configScaleValue[16], configScaleValue[17], configScaleValue[18], configScaleValue[19], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), depthData)
                self.HUD.drawDepthGauge(scaledBottomImg, configScaleValue[16], configScaleValue[17], configScaleValue[18], configScaleValue[19], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), depthData)
            
            if configScaleValue[20] == 1:
                self.HUD.drawAttitude(scaledFrontImg, configScaleValue[21], configScaleValue[23], configScaleValue[24], configScaleValue[25], configScaleValue[26], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), orientationData, positionData, velocityData)
                self.HUD.drawAttitude(scaledBottomImg, configScaleValue[21], configScaleValue[23], configScaleValue[24], configScaleValue[25], configScaleValue[26], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), orientationData, positionData, velocityData)
            
            if configScaleValue[27] == 1:
                self.HUD.drawBatteryGauge(scaledFrontImg, configScaleValue[28], configScaleValue[30], configScaleValue[31], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), batteryData)
                self.HUD.drawBatteryGauge(scaledBottomImg, configScaleValue[28], configScaleValue[30], configScaleValue[31], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), batteryData)
            
            if configScaleValue[32] == 1:
                self.HUD.drawTemperature(scaledFrontImg, configScaleValue[33], configScaleValue[34], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), temperatureData)
                self.HUD.drawTemperature(scaledBottomImg, configScaleValue[33], configScaleValue[34], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), temperatureData)
               
            if configScaleValue[35] == 1:
                self.HUD.drawMotorGauges(scaledFrontImg, configScaleValue[36], configScaleValue[37], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), motorData[0], motorData[1])
                self.HUD.drawMotorGauges(scaledBottomImg, configScaleValue[36], configScaleValue[37], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), motorData[0], motorData[1])
            
            if configScaleValue[38] == 1:
                self.HUD.drawStatus(scaledFrontImg, configScaleValue[39], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), statusData[0], statusData[1])
                self.HUD.drawStatus(scaledBottomImg, configScaleValue[39], (configScaleValue[42], configScaleValue[41], configScaleValue[40]), statusData[0], statusData[1])
               
            #FAKE DATA  
            fakeHeadingInput += 1
                
            if fakePitchInput >= 90 and scaleUpDownHeading == True:
                scaleUpDownHeading = False
            if fakePitchInput <= -90 and scaleUpDownHeading == False:
                scaleUpDownHeading = True
            if scaleUpDownHeading == True:
                fakePitchInput += 1
            if scaleUpDownHeading == False:
                fakePitchInput -= 1
                
            if fakeRollInput >= 180 and scaleUpDownRoll == True:
                scaleUpDownRoll = False
            if fakeRollInput <= -180 and scaleUpDownRoll == False:
                scaleUpDownRoll = True
            if scaleUpDownRoll == True:
                fakeRollInput += 5
            if scaleUpDownRoll == False:
                fakeRollInput -= 5
            
            if fakeBatteryInput >= 100 and scaleUpDownBattery == True:
                scaleUpDownBattery = False
            if fakeBatteryInput <= 0 and scaleUpDownBattery == False:
                scaleUpDownBattery = True
            if scaleUpDownBattery == True:
                fakeBatteryInput += 1
            if scaleUpDownBattery == False:
                fakeBatteryInput -= 1
                
            if fakeMotorInput >= 100 and scaleUpDownMotor == True:
                scaleUpDownMotor = False
            if fakeMotorInput <= 0 and scaleUpDownMotor == False:
                scaleUpDownMotor = True
                toggleDirection = not toggleDirection
            if scaleUpDownMotor == True:
                fakeMotorInput += 1
            if scaleUpDownMotor == False:
                fakeMotorInput -= 1
            
            #LOGGING GAUGE PARAMS
            self.logGuiParams.writeParameters(headingGauge=configScaleValue[0], headingTickNum=configScaleValue[1], headingIncrement=configScaleValue[2], headingPosition=configScaleValue[3], headingWidth=configScaleValue[4],
                                    pitchGauge=configScaleValue[5], pitchTickNum=configScaleValue[6], pitchIncrement=configScaleValue[7], pitchLength=configScaleValue[8],
                                    rollGauge=configScaleValue[9], rollTickNum=configScaleValue[10], rollRange1=configScaleValue[11], rollRange2=configScaleValue[12], rollPosition=configScaleValue[13], rollWidth=configScaleValue[14],
                                    depthGauge=configScaleValue[15], depthTickNum=configScaleValue[16], depthIncrement=configScaleValue[17], depthPosition=configScaleValue[18], depthLength=configScaleValue[19],
                                    attitudeGauge=configScaleValue[20], attitudeLength=configScaleValue[21], displayPosVel1=configScaleValue[22], displayPosVel2=configScaleValue[23], attitudePosition=configScaleValue[24], attitudeLetterSize=configScaleValue[25], attitudeLetterRatio=configScaleValue[26],
                                    batteryGauge=configScaleValue[27], batteryGaugeLength=configScaleValue[28], displayBatteryCurrent1=configScaleValue[29], displayBatteryCurrent2=configScaleValue[30], batteryPosition=configScaleValue[31],
                                    temperatureGauge=configScaleValue[32], temperatureSize=configScaleValue[33], temperaturePosition=configScaleValue[34],
                                    motorGauge=configScaleValue[35], motorSize=configScaleValue[36], motorPosition=configScaleValue[37],
                                    statusGauge=configScaleValue[38], statusPosition=configScaleValue[39],
                                    redGaugeColor=configScaleValue[40], greenGaugeColor=configScaleValue[41], blueGaugeColor=configScaleValue[42])
    
    def __keyboardInput__(self):
        if self.window.captureImg[0] == True: #If "c" is pressed, take a print screen of the img
            xString = int(self.rawImgWidth-self.rawImgWidth*0.22)
            yString = int(self.rawImgHeight-self.rawImgHeight*0.23)
            cv2.putText(scaledFrontImg, str("Property Of"), (xString, yString), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
            cv2.putText(scaledFrontImg, str("SDSU Mechatronics"), (xString-25, yString+13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
            cv2.putText(scaledFrontImg, datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), (xString-40, yString+25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
            
            cv2.imwrite('_Pictures_/Front/Image{}.png'.format(self.window.pictureCount[0] + 1), scaledFrontImg) #Write image to file in a .png format
            self.window.captureImg[0] = False
            
        if self.window.captureImg[1] == True: #If "ctrl-c" is pressed, take a print screen of the img
            xString = int(self.rawImgWidth-self.rawImgWidth*0.22)
            yString = int(self.rawImgHeight-self.rawImgHeight*0.23)
            cv2.putText(scaledBottomImg, str("Property Of"), (xString, yString), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
            cv2.putText(scaledBottomImg, str("SDSU Mechatronics"), (xString-25, yString+13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
            cv2.putText(scaledBottomImg, datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), (xString-40, yString+25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
            
            cv2.imwrite('_Pictures_/Bottom/Image{}.png'.format(self.window.pictureCount[1] + 1), scaledBottomImg) #Write image to file in a .png format
            self.window.captureImg[1] = False
            
        if self.window.recordImg[0] == True: #If "r" is pressed, start recording front image
            xString = int(self.rawImgWidth-self.rawImgWidth*0.22)
            yString = int(self.rawImgHeight-self.rawImgHeight*0.23)
            cv2.putText(scaledFrontImg, str("Property Of"), (xString, yString), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
            cv2.putText(scaledFrontImg, str("SDSU Mechatronics"), (xString-25, yString+13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
            cv2.putText(scaledFrontImg, datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), (xString-40, yString+25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
            
            netRecordingTextPulseTimer = frontRecordingTextPulseTimer.netTimer(frontRecordingTextPulseTimer.cpuClockTimeInSeconds())
            if netRecordingTextPulseTimer >= 1:
                self.toggleStates = not self.toggleStates
                self.window.recording[0].config(state=self.recordingState[self.toggleStates])
                frontRecordingTextPulseTimer.restartTimer()
            
            netRecordingTime = frontRecordingTimer.netTimer(frontRecordingTimer.cpuClockTimeInSeconds())
            if netRecordingTime >= float(self.window.secondsPerFrame[0]): #Waits for as long as the user requested to record an image
                cv2.imwrite('_Recordings_/Front/Image{}.png'.format(self.window.recordCount[0]), scaledFrontImg) #Write image to file in a .png format
                self.window.recordCount[0]+=1
                frontRecordingTimer.restartTimer()
            
        if self.window.recordImg[1] == True: #If "ctrl-r" is pressed, start recording bottom image
            xString = int(self.rawImgWidth-self.rawImgWidth*0.22)
            yString = int(self.rawImgHeight-self.rawImgHeight*0.23)
            cv2.putText(scaledBottomImg, str("Property Of"), (xString, yString), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
            cv2.putText(scaledBottomImg, str("SDSU Mechatronics"), (xString-25, yString+13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
            cv2.putText(scaledBottomImg, datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), (xString-40, yString+25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255))
                
            netRecordingTextPulseTimer = bottomRecordingTextPulseTimer.netTimer(bottomRecordingTextPulseTimer.cpuClockTimeInSeconds())
            if netRecordingTextPulseTimer >= 1:
                self.toggleStates = not self.toggleStates
                self.window.recording[1].config(state=self.recordingState[self.toggleStates])
                bottomRecordingTextPulseTimer.restartTimer()
                
            netRecordingTime = bottomRecordingTimer.netTimer(bottomRecordingTimer.cpuClockTimeInSeconds())
            if netRecordingTime >= float(self.window.secondsPerFrame[1]): #Waits for as long as the user requested to record an image
                cv2.imwrite('_Recordings_/Bottom/Image{}.png'.format(self.window.recordCount[1]), scaledBottomImg) #Write image to file in a .png format
                self.window.recordCount[1]+=1
                bottomRecordingTimer.restartTimer()
    
    
    def __guiUpdates__(self):
        global updateIPScales, setInitialImageProcessingList, setInitialGaugeTrackBarPosition, setInitialHSVTrackBarPosition, setInitialFilterTrackBarPosition, setInitialConsoleCheckBoxOptions
        
        #UPDATES LISTS IN MISSION SELECTOR TAB
        self.missionSelectorSystem.updateParamValueLists()
        
        if setInitialImageProcessingList == True:
            
            #UPDATES LIST IN IMAGE PROCESSING TAB
            self.imageProcessingMissionSelector.updateIPDropDownList()
            
            setInitialImageProcessingList = False
        
        if self.window.lastUser.get() != self.previousUser: #If the program changes users...
            self.logGuiParams = previous_state_logging_system.Log('_Saved_Settings_/_GUI_Parameters_({}).txt'.format(self.window.lastUser.get()))
            mission_selector_system.PreviousMissionListLogging(self.window).load(self.window.lastUser.get())
            mission_selector_system.indexTracker = None
            setInitialImageProcessingList = True
            setInitialGaugeTrackBarPosition = True
            setInitialHSVTrackBarPosition = True
            setInitialFilterTrackBarPosition = True
            setInitialConsoleCheckBoxOptions = True
            updateIPScales = True
            
        if setInitialConsoleCheckBoxOptions == True:
            values = self.logGuiParams.getParameters("checkBoxOption1", "checkBoxOption2", "checkBoxOption3", 
                                            "checkBoxOption4", "checkBoxOption5", "checkBoxOption6", 
                                            "checkBoxOption7")
            
            checkBoxOptionValues = [values.checkBoxOption1, values.checkBoxOption2, values.checkBoxOption3, 
                                    values.checkBoxOption4, values.checkBoxOption5, values.checkBoxOption6,
                                    values.checkBoxOption7]
            
            for x in range(len(checkBoxOptionValues)):
                if checkBoxOptionValues[x] == 1: #If the check boxes were on in the last session, turn them on in this session
                    self.window.printOptionCheckbox[x].select()
                if checkBoxOptionValues[x] == 0:
                    self.window.printOptionCheckbox[x].deselect()
                    
            setInitialConsoleCheckBoxOptions = False
            
        self.previousUser = self.window.lastUser.get()
            
        self.window.lastUserLog.writeParameters(lastUser = "\""+self.window.lastUser.get()+"\"")
            
        #LOGGING GAUGE PARAMS
        self.logGuiParams.writeParameters(checkBoxOption1=self.window.printOptionCheckboxValues[0].get(), checkBoxOption2=self.window.printOptionCheckboxValues[1].get(), 
                                checkBoxOption3=self.window.printOptionCheckboxValues[2].get(), checkBoxOption4=self.window.printOptionCheckboxValues[3].get(),
                                checkBoxOption5=self.window.printOptionCheckboxValues[4].get(), checkBoxOption6=self.window.printOptionCheckboxValues[5].get(),
                                checkBoxOption7=self.window.printOptionCheckboxValues[6].get())
    
    
    def __imageProcessing__(self, frontImg, bottomImg, frontRawImgLabel, bottomRawImgLabel, frontProcessedImgLabel, bottomProcessedImgLabel, filterScales):
        global track_window
        
        
        #RAW IMGS TO TK
        bgrToRgbFrontImg = cv2.cvtColor(scaledFrontImg, cv2.COLOR_BGR2RGB)
        tkFrontRawImg = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(bgrToRgbFrontImg))
        bgrToRgbBottomImg = cv2.cvtColor(scaledBottomImg, cv2.COLOR_BGR2RGB)
        tkBottomRawImg = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(bgrToRgbBottomImg))
        
        #PROCESSED IMG 1
        #hsv filter
        scaledTabbedFrontImg = cv2.resize(frontImg, (self.processedImgWidth, self.processedImgHeight))
        HSVFrontImg = cv2.cvtColor(scaledTabbedFrontImg, cv2.COLOR_BGR2HSV)
        lowerBound = (filterScales[0].get(), filterScales[1].get(), filterScales[2].get())
        upperBound = (filterScales[3].get(), filterScales[4].get(), filterScales[5].get())
        maskFrontImg = cv2.inRange(HSVFrontImg, lowerBound , upperBound) #Black and white image
        maskHSV3rdAxisFrontImg = maskFrontImg[:, :, numpy.newaxis] #Adding 3rd axis to make RGB compatible
        HSVBitwiseAndFrontImg = numpy.bitwise_and(scaledTabbedFrontImg, maskHSV3rdAxisFrontImg)
        
        #morphology filter
        morphologyFrontImg = cv2.morphologyEx(HSVBitwiseAndFrontImg, filterScales[6].get(), numpy.ones((5,5), numpy.uint8), iterations = filterScales[7].get())
        #JAREDS CODE 8-epsilon 9-min curves 10-max curves
        HSVFrontImg = cv2.cvtColor(morphologyFrontImg, cv2.COLOR_BGR2HSV)
        maskFrontImg = cv2.inRange(HSVFrontImg, lowerBound , upperBound) #Black and white image
        shape_centerFrontImg = []
        targetsFrontImg = []
        epsilon = filterScales[8].get()#Factor to multiply epsilon by
        if epsilon != 0:#turns off Contour Analysis if epsilon trackbar is zero
            blurFrontImg = cv2.blur(maskFrontImg, (2,2))
            ret,thresh = cv2.threshold(blurFrontImg,127,255,0)
            flag, contours, h = cv2.findContours(thresh,3,2)#Contour detection using Retr_Tree and Chain_Approx_Simple
            squares_cont = []
            minCurves = filterScales[9].get()#Minimum number of curves wanted
            maxCurves = filterScales[10].get()#Max number of curves wanted
            for n, cnt in enumerate(contours):
                approx = cv2.approxPolyDP(cnt,epsilon*0.001*cv2.arcLength(cnt,True),True)#Number of curves in the contour
                if len(approx)>=minCurves and len(approx)<=maxCurves:
                    squares_cont.append([n,cnt])#Add the contour to the list if it's within the specified range of curves
            if squares_cont != None:
                for i, cnt in squares_cont:
                    if h[0][i][3] == -1:#If there is no parent contour
                        M = cv2.moments(cnt)
                        if M['m00'] > 500:#Ignores extremely small contours
                            cv2.drawContours(morphologyFrontImg,[cnt],0,(255,0,0),3)#Draw outline of contour
                            cx = int(M['m10']/M['m00'])#x-position of center
                            cy = int(M['m01']/M['m00'])#y-position of center
                            shape_centerFrontImg.append((cx,cy))#add shape coordinates to list
                    elif h[0][i][3] > -1:#If this is a child/inner contour
                        M = cv2.moments(cnt)
                        if M['m00'] > 400:#Ignores extremely small contours
                            cx = int(M['m10']/M['m00'])
                            cy = int(M['m01']/M['m00'])
                            ellipse = cv2.fitEllipse(cnt)#create an ellipse around the contour
                            cv2.ellipse(morphologyFrontImg,ellipse,(0,255,0),2)#draw the ellipse
                            targetsFrontImg.append((cx,cy))#add target coordinates to list
        
        trackBoxFrontImg = self.camshiftFront.camshift(morphologyFrontImg, HSVFrontImg, maskFrontImg, self.processedImgWidth, self.processedImgHeight)
        if trackBoxFrontImg[0][0] != 0 and trackBoxFrontImg[0][1] != 0: #If their is something to track onto 
            cv2.putText(morphologyFrontImg, "(" + str(trackBoxFrontImg[0][0]) + ", " + str(trackBoxFrontImg[0][1]) + ")", (int(trackBoxFrontImg[0][0]), int(trackBoxFrontImg[0][1])), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
            cv2.putText(morphologyFrontImg, "(" + str(round(trackBoxFrontImg[1][0], 1)) + ", " + str(round(trackBoxFrontImg[1][1], 1)) + ")", (int(trackBoxFrontImg[0][0]), int(trackBoxFrontImg[0][1]+15)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
            cv2.putText(morphologyFrontImg, "(" + str(round(trackBoxFrontImg[2], 1)) + ")", (int(trackBoxFrontImg[0][0]), int(trackBoxFrontImg[0][1]+30)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))   
        
            
        bgrToRgbFrontImg = cv2.cvtColor(morphologyFrontImg, cv2.COLOR_BGR2RGB)
        tkHSVFrontImg = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(bgrToRgbFrontImg))
        
        #PROCESSED IMG 2
        #hsv filter
        scaledTabbedBottomImg = cv2.resize(bottomImg, (self.processedImgWidth, self.processedImgHeight))
        HSVBottomImg = cv2.cvtColor(scaledTabbedBottomImg, cv2.COLOR_BGR2HSV)
        lowerBound = (filterScales[11].get(), filterScales[12].get(), filterScales[13].get())
        upperBound = (filterScales[14].get(), filterScales[15].get(), filterScales[16].get())
        maskBottomImg = cv2.inRange(HSVBottomImg, lowerBound , upperBound)
        maskHSV3rdAxisBottomImg = maskBottomImg[:, :, numpy.newaxis]
        HSVBitwiseAndBottomImg = numpy.bitwise_and(scaledTabbedBottomImg, maskHSV3rdAxisBottomImg)
        
        #morphology filter
        morphologyBottomImg = cv2.morphologyEx(HSVBitwiseAndBottomImg, filterScales[17].get(), numpy.ones((5,5), numpy.uint8), iterations = filterScales[18].get())
        #JAREDS CODE 19-epsilon 20-min curves 21-max curves
        HSVBottomImg = cv2.cvtColor(morphologyBottomImg, cv2.COLOR_BGR2HSV)
        maskBottomImg = cv2.inRange(HSVBottomImg, lowerBound , upperBound) #Black and white image
        shape_centerBottomImg = []
        targetsBottomImg = []
        epsilonb = filterScales[19].get()#Factor to multiply epsilon by
        if epsilonb != 0:#turns off Contour Analysis if epsilon trackbar is zero
            blurBottomImg = cv2.blur(maskBottomImg, (2,2))
            retb,threshb = cv2.threshold(blurBottomImg,127,255,0)
            flagb, contoursb, hb = cv2.findContours(threshb,3,2)#Contour detection using Retr_Tree and Chain_Approx_Simple
            squares_contb = []
            minCurvesb = filterScales[20].get()#Minimum number of curves wanted
            maxCurvesb = filterScales[21].get()#Max number of curves wanted
            for nb, cntb in enumerate(contoursb):
                approxb = cv2.approxPolyDP(cntb,epsilonb*0.001*cv2.arcLength(cntb,True),True)#Number of curves in the contour
                if len(approxb)>=minCurvesb and len(approxb)<=maxCurvesb:#Add the contour to the list if it's within the specified range of curves
                    squares_contb.append([nb,cntb])
            if squares_contb != None:
                for ib, cntb in squares_contb:
                    if hb[0][ib][3] == -1:#If there is no parent contour
                        M = cv2.moments(cntb)
                        if M['m00'] > 500:#Ignores extremely small contours
                            cv2.drawContours(morphologyBottomImg,[cntb],0,(255,0,0),3)#Draw outline of contour
                            cx = int(M['m10']/M['m00'])#x-position of center
                            cy = int(M['m01']/M['m00'])#y-position of center
                            shape_centerBottomImg.append((cx,cy))#add shape coordinates to list
                    elif hb[0][ib][3] > -1:#If this is a child/inner contour
                        M = cv2.moments(cntb)
                        if M['m00'] > 400:#Ignores extremely small contours
                            cx = int(M['m10']/M['m00'])
                            cy = int(M['m01']/M['m00'])
                            ellipse = cv2.fitEllipse(cntb)#create an ellipse around the contour
                            cv2.ellipse(morphologyBottomImg,ellipse,(0,255,0),2)#draw the ellipse
                            targetsBottomImg.append((cx,cy))#add target coordinates to list
        
        trackBoxBottomImg = self.camshiftBottom.camshift(morphologyBottomImg, HSVBottomImg, maskBottomImg, self.processedImgWidth, self.processedImgHeight)
        if trackBoxBottomImg[0][0] != 0 and trackBoxBottomImg[0][1] != 0:
            cv2.putText(morphologyBottomImg, "(" + str(trackBoxBottomImg[0][0]) + ", " + str(trackBoxBottomImg[0][1]) + ")", (int(trackBoxBottomImg[0][0]), int(trackBoxBottomImg[0][1])), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
            cv2.putText(morphologyBottomImg, "(" + str(round(trackBoxBottomImg[1][0], 1)) + ", " + str(round(trackBoxBottomImg[1][1], 1)) + ")", (int(trackBoxBottomImg[0][0]), int(trackBoxBottomImg[0][1]+15)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
            cv2.putText(morphologyBottomImg, "(" + str(round(trackBoxBottomImg[2], 1)) + ")", (int(trackBoxBottomImg[0][0]), int(trackBoxBottomImg[0][1]+30)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255)) 
        
        
        #PROCESSED IMG 2 TO TK IMG        bgrToRgbBottomImg = cv2.cvtColor(morphologyBottomImg, cv2.COLOR_BGR2RGB)        tkHSVBottomImg = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(bgrToRgbBottomImg))
        
    
        #SHOW ALL IMGS
        frontRawImgLabel.config(image = tkFrontRawImg)
        bottomRawImgLabel.config(image = tkBottomRawImg)
        frontProcessedImgLabel.config(image = tkHSVFrontImg)
        bottomProcessedImgLabel.config(image = tkHSVBottomImg)
        
        self.window.update()
        
        return trackBoxFrontImg, trackBoxBottomImg, shape_centerFrontImg, shape_centerBottomImg, targetsFrontImg, targetsBottomImg
    
    def __controllerUpdates__(self):
        controller = controller_screen.controller(self.window.controllerScreen, self.window)
        if self.window.setToManual == 0:
            controller.setup()
            self.window.setToManual = 1
        elif self.window.setToManual == 1:
            controller.run()
        elif self.window.setToManual == 2:
            controller.stop()
            self.window.setToManual = 3
        else:
            pass