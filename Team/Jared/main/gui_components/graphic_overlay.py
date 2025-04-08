'''
Copyright 2014, Austin Owens, All rights reserved.

Created on Nov 5, 2014

@author: Austin
'''
import cv2
import math
import main.utility_package.utilities as utilities
import time, datetime
import numpy

advM = utilities.AdvancedMath()
e1 = advM.e1 #Unit vector for x
e2 = advM.e2 #Unit vector for y
e3 = advM.e3 #Unit vector for z

#Heading
stringAddHeading, counterHeading = 0, 0

#Pitch
counterPitch, stringAddPitch = 0, 0

#Roll
counterRoll, stringAddRoll = 0, 0

#Depth
stringAddDepth, counterDepth = 0, 0

class GraphicOverlay:
    def __init__(self, window, screenWidth, screenHeight):
        self.window = window
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        
        self.setInitialTickPosition = [True, True, True]
        self.compassNames = ["N", "E", "S", "W"]
        
    def drawHeadingGauge(self, scaledMainImg, numOfTicks, increments, position, gaugeWidth, rgbValues, sensorInput): #(img, number of tick marks, increments of the scale, gauge width, sensor input)
        global counterHeading, stringAddHeading
        
        #Creating points for the line
        lineLength = gaugeWidth #Originally 381
        x1 = self.screenWidth/2 - lineLength/2
        x2 = self.screenWidth/2 + lineLength/2
        
        if position == 0:
            y1 = self.screenHeight-24
            y2 = self.screenHeight-24
            graphicNumberCorrection = -13
            compassCorrectionValue = -28
            cv2.line(scaledMainImg, (self.screenWidth/2, y1+10), ((self.screenWidth/2)-10, y1+20), rgbValues)#Creating top line for arrow
            cv2.line(scaledMainImg, (self.screenWidth/2, y1+10), ((self.screenWidth/2)+10, y1+20), rgbValues)#Creating bottom line for arrow
            cv2.line(scaledMainImg, ((self.screenWidth/2)-10, y1+20), ((self.screenWidth/2)+10, y1+20), rgbValues)#Creating closing line for triangle
            
        elif position == 1:
            y1 = 20
            y2 = 20
            graphicNumberCorrection = 25
            compassCorrectionValue = 40
            cv2.line(scaledMainImg, (self.screenWidth/2, y1-10), ((self.screenWidth/2)-10, y1-20), rgbValues)#Creating top line for arrow
            cv2.line(scaledMainImg, (self.screenWidth/2, y1-10), ((self.screenWidth/2)+10, y1-20), rgbValues)#Creating bottom line for arrow
            cv2.line(scaledMainImg, ((self.screenWidth/2)-10, y1-20), ((self.screenWidth/2)+10, y1-20), rgbValues)#Creating closing line for triangle
            
        tickMarkGapDistance = lineLength/numOfTicks #Distance between tick marks
        heading = sensorInput
        
        if self.setInitialTickPosition[0]:
            stringAddHeading = (numOfTicks*increments)/2.0 #The amount of tick marks above the middle tick mark
            self.setInitialTickPosition[0] = False
            counterHeading = 0
            
        cv2.line(scaledMainImg, (x1, y1), (x2, y2), rgbValues) #Creating line
        
        for x in range(numOfTicks+1):
            tickMarkHeight = x1 + (lineLength*x)/numOfTicks #The INITIAL height of each tick mark
            tickMarkMoving = int(tickMarkHeight - ((heading-counterHeading)*tickMarkGapDistance)/increments) #The height of each tick mark after moving them based on sensor input
    
            if x == 0 and tickMarkMoving <= x1 - tickMarkGapDistance: #As the tick marks are moving up; once the tick mark's distance away from the top of the line is the difference between the tick mark gaps...
                counterHeading += increments*((x1 - tickMarkMoving)/tickMarkGapDistance) #Increment a counter that will move the ticks marks back down to their initial position and adjust the tick mark numbers. If the user doesnt enter a high enough increment, the tick marks will run behind. To catch them up, we find out how many tickMarkGaps ahead it is and multiply that to increment
                
            elif x == numOfTicks and tickMarkMoving >= x2 + tickMarkGapDistance: #As the tick marks are moving down; once the tick mark's distance away from the bottom of the line is the difference between the tick mark gaps...
                counterHeading -= increments*((x2 + tickMarkMoving)/tickMarkGapDistance) #Decrement a counter that will move the ticks marks back up to their initial position and adjust the tick mark numbers
                    
            elif tickMarkMoving >= x1 and tickMarkMoving <= x2: #As long as the tick marks don't go past the line upper or lower bounds of the line...
                graphicNumbers = round((360-stringAddHeading+counterHeading+(x*increments))%360, 5)
                cv2.line(scaledMainImg, (tickMarkMoving, y1-10), (tickMarkMoving, y1+10), rgbValues) #Draw the tick mark
                if graphicNumbers - int(graphicNumbers) == 0: #Get rid of decimals when not using them
                    graphicNumbers = int(graphicNumbers)
                if graphicNumbers == 0: #This centers the zero
                    cv2.putText(scaledMainImg, str(graphicNumbers), (tickMarkMoving-4, y1+graphicNumberCorrection), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues) #Write the number
                if graphicNumbers != 0:
                    cv2.putText(scaledMainImg, str(graphicNumbers), (tickMarkMoving-11, y1+graphicNumberCorrection), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues) #Write the number
                for x in range(4):
                    if graphicNumbers == x*90: #Put north south east west
                        cv2.putText(scaledMainImg, self.compassNames[x], (tickMarkMoving-4, y1+compassCorrectionValue), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues)
    
    def drawPitchGauge(self, scaledMainImg, numOfTicks, increments, gaugeLength, rgbValues, sensorInput): #(img, number of tick marks, increments of the scale, gauge length, sensor input)
        global counterPitch, stringAddPitch
        
        #Creating points for the line
        lineLength = gaugeLength #Originally 361
        x1 = self.screenWidth/2
        y1 = self.screenHeight/2 - lineLength/2
        y2 = self.screenHeight/2 + lineLength/2
            
        tickMarkGapDistance = lineLength/numOfTicks #Distance between tick marks
        pitch = sensorInput
        
        
        cv2.line(scaledMainImg, (x1-7, self.screenHeight/2), (x1+7, self.screenHeight/2), rgbValues) #Creating Plus Sign
        cv2.line(scaledMainImg, (x1, self.screenHeight/2 + 7), (x1, self.screenHeight/2 - 7), rgbValues) #Creating Plus Sign
        if self.setInitialTickPosition[1]:
            stringAddPitch = -(numOfTicks*increments)/2.0 #The amount of tick marks above the middle tick mark
            self.setInitialTickPosition[1] = False
            counterPitch = 0
        
        for x in range(numOfTicks+1):
            tickMarkHeight = y1 + (lineLength*x)/numOfTicks #The INITIAL height of each tick mark
            tickMarkMoving = int(tickMarkHeight + ((pitch+counterPitch)*tickMarkGapDistance)/increments) #The height of each tick mark after moving them based on sensor input

            if x == 0 and tickMarkMoving <= y1 - tickMarkGapDistance: #As the tick marks are moving up; once the tick mark's distance away from the top of the line is the difference between the tick mark gaps...
                counterPitch += increments*((y1 - tickMarkMoving)/tickMarkGapDistance) #Increment a counter that will move the ticks marks back down to their initial position and adjust the tick mark numbers. If the user doesnt enter a high enough increment, the tick marks will run behind. To catch them up, we find out how many tickMarkGaps ahead it is and multiply that to increment

            elif x == numOfTicks and tickMarkMoving >= y2 + tickMarkGapDistance: #As the tick marks are moving down; once the tick mark's distance away from the bottom of the line is the difference between the tick mark gaps...
                counterPitch -= increments*((y2 + tickMarkMoving)/tickMarkGapDistance) #Decrement a counter that will move the ticks marks back up to their initial position and adjust the tick mark numbers
                    
            elif tickMarkMoving >= y1 and tickMarkMoving <= y2: #As long as the tick marks don't go past the line upper or lower bounds of the line...
                graphicNumbers = -round(stringAddPitch+counterPitch+(x*increments), 5) 
                if graphicNumbers -  int(graphicNumbers) == 0: #Get rid of decimals when not using them
                    graphicNumbers = int(graphicNumbers) 
                if graphicNumbers >= -90 and graphicNumbers <= 90:
                    if graphicNumbers == 0: #Draw the big tick mark if graphicNumbers = 0
                        cv2.line(scaledMainImg, (x1-50, tickMarkMoving), (x1+50, tickMarkMoving), rgbValues) #Draw the tick mark
                    else:
                        if graphicNumbers > 0:
                            cv2.line(scaledMainImg, (x1-25, tickMarkMoving), (x1-5, tickMarkMoving), rgbValues) #Draw the tick mark
                            cv2.line(scaledMainImg, (x1-5, tickMarkMoving), (x1-5, tickMarkMoving-5), rgbValues) #Draw the tick mark
                            cv2.line(scaledMainImg, (x1+5, tickMarkMoving), (x1+25, tickMarkMoving), rgbValues) #Draw the tick mark 
                            cv2.line(scaledMainImg, (x1+5, tickMarkMoving), (x1+5, tickMarkMoving-5), rgbValues) #Draw the tick mark
                        elif graphicNumbers < 0:
                            cv2.line(scaledMainImg, (x1-25, tickMarkMoving), (x1-5, tickMarkMoving), rgbValues) #Draw the tick mark
                            cv2.line(scaledMainImg, (x1-5, tickMarkMoving), (x1-5, tickMarkMoving+5), rgbValues) #Draw the tick mark
                            cv2.line(scaledMainImg, (x1+5, tickMarkMoving), (x1+25, tickMarkMoving), rgbValues) #Draw the tick mark 
                            cv2.line(scaledMainImg, (x1+5, tickMarkMoving), (x1+5, tickMarkMoving+5), rgbValues) #Draw the tick mark 
                    cv2.putText(scaledMainImg, str(graphicNumbers), (x1+55, tickMarkMoving+5), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues) #Write the number
    
    def drawRollGauge(self, scaledMainImg, numOfTicks, incrementRange, position, gaugeWidth, rgbValues, sensorInput): #(img, number of tick marks, increments of the scale, gauge width, sensor input)
        
        roll = sensorInput
        
        #Creating points for the line
        ellipseWidth = gaugeWidth #Originally 90
        ellipseHeight = 50
           
        if position == 0:#BOTTOM
            x1 = self.screenWidth/2 #Center of ellipse in the x direction
            y1 = self.screenHeight-75 #Center of ellipse in the y direction
            changingMiddleNumberCorrection = 20
            graphicCorrectionsX = -5, -20, -10
            graphicCorrectionsY = 11, 11, 11
        elif position == 1: #TOP
            x1 = self.screenWidth/2 #Center of ellipse in the x direction
            y1 = 75 #Center of ellipse in the y direction
            changingMiddleNumberCorrection = -20
            graphicCorrectionsX = -5, 0, -40
            graphicCorrectionsY = -2, -3, -3
        
        a = ellipseWidth/2
        b = ellipseHeight/2
        
        if incrementRange == 1:
            roll = (roll*90)/180.0
        else:
            if roll <= -90:
                roll = -90
            if roll >= 90:
                roll = 90
                
        if position == 0:
            ellipseXEquRoll = -((roll*ellipseWidth)/90.0)+x1
            ellipseYEquRoll = math.sqrt((ellipseHeight**2)*(1-((((roll*a)/90.0)**2)/(a**2))))+(y1-self.screenHeight+15)+self.screenHeight
            startAngle, endAngle = 0, 180
            correctingAngle = 0
        elif position == 1:
            ellipseXEquRoll = ((roll*ellipseWidth)/90.0)+x1
            ellipseYEquRoll = -math.sqrt((ellipseHeight**2)*(1-((((roll*a)/90.0)**2)/(a**2))))+(y1-self.screenHeight+15)+self.screenHeight
            startAngle, endAngle = 180, 360
            correctingAngle = 180
            
        xRoll = a*math.cos(math.radians(roll))
        yRoll = b*math.sin(math.radians(roll))
        angle = math.degrees(math.acos(-yRoll/(math.sqrt((xRoll**2)+(yRoll**2)))))-90
        x1Triangle = int(round(-10*math.cos(math.radians(angle))-10*math.sin(math.radians(angle))+ellipseXEquRoll))
        y1Triangle = int(round(10*math.cos(math.radians(angle))-10*math.sin(math.radians(angle))+(ellipseYEquRoll-15)))
        x2Triangle = int(round(10*math.cos(math.radians(angle))-10*math.sin(math.radians(angle))+(ellipseXEquRoll)))
        y2Triangle = int(round(10*math.cos(math.radians(angle))+10*math.sin(math.radians(angle))+(ellipseYEquRoll-15)))
        cv2.ellipse(scaledMainImg, (x1, y1), (ellipseWidth, ellipseHeight), 0, startAngle, endAngle, rgbValues) #(image, center, axes, angle, startAngle, endAngle, color)
        
        #Triangle
        cv2.line(scaledMainImg, (int(round(ellipseXEquRoll)), int(round(ellipseYEquRoll-15))), (x1Triangle, y1Triangle), rgbValues)
        cv2.line(scaledMainImg, (int(round(ellipseXEquRoll)), int(round(ellipseYEquRoll-15))), (x2Triangle, y2Triangle), rgbValues)
        cv2.line(scaledMainImg, (x1Triangle, y1Triangle), (x2Triangle, y2Triangle), rgbValues)
        #cv2.line(scaledMainImg, (x1, y1), (int(round(ellipseXEquRoll)), int(round(ellipseYEquRoll-15))), rgbValues)
        
        #Tick Marks
        tickMarkNum = numOfTicks-1
        for x in range(tickMarkNum+1):
            tickAngle = 90.0 - (180.0/tickMarkNum)*x #DONT WANT TO GO IN EVEN INTERVALS WITH THE ELLIPSE, INSTEAD, NEED TO GO WITH EVEN INTERVALS WITH CIRCLE AND TRANSCRIBE THAT ON ELLIPSE
            if position == 0:
                xTick = -ellipseWidth*math.sin(math.radians(tickAngle))
                yTick = ellipseHeight*math.cos(math.radians(tickAngle))
            elif position == 1:
                xTick = ellipseWidth*math.sin(math.radians(tickAngle))
                yTick = -ellipseHeight*math.cos(math.radians(tickAngle))
                
            angle = math.degrees(math.atan2(yTick,xTick))-90
            x1Tick = 10*math.sin(math.radians(angle))+x1+xTick
            y1Tick = -10*math.cos(math.radians(angle))+y1+yTick
            x2Tick = -10*math.sin(math.radians(angle))+x1+xTick
            y2Tick = 10*math.cos(math.radians(angle))+y1+yTick
            cv2.line(scaledMainImg, (int(round(x1Tick)), int(round(y1Tick))), (int(round(x2Tick)), int(round(y2Tick))), rgbValues)
            graphicNumbers = int(round(angle)) + correctingAngle
            
            if incrementRange == 1: # Means user picked 180
                
                cv2.putText(scaledMainImg, str(int(round(sensorInput))), (x1-10, y1+changingMiddleNumberCorrection), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues) #writes the AHRS roll unrestricted by 90 deg
                if graphicNumbers == 0:
                    cv2.putText(scaledMainImg, str(graphicNumbers*2), (int(round(x2Tick+graphicCorrectionsX[0])), int(round(y2Tick+graphicCorrectionsY[0]))), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues) #Write the number
                elif graphicNumbers == 90: #Just 90, not 180, since I scale it to 90. 90 is to 180 as 0 is to 0.
                    cv2.putText(scaledMainImg, str(graphicNumbers*2), (int(round(x2Tick+graphicCorrectionsX[1])), int(round(y2Tick+graphicCorrectionsY[1]))), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues) #Write the number
                elif graphicNumbers == -90: #Just 90, not 180, since I scale it to 90. 90 is to 180 as 0 is to 0.
                    cv2.putText(scaledMainImg, str(graphicNumbers*2), (int(round(x2Tick+graphicCorrectionsX[2])), int(round(y2Tick+graphicCorrectionsY[2]))), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues) #Write the number
            else:
                cv2.putText(scaledMainImg, str(int(round(roll))), (x1-10, y1+changingMiddleNumberCorrection), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues) #Write the AHRS roll restricted by 90 deg
                if graphicNumbers == 0:
                    cv2.putText(scaledMainImg, str(graphicNumbers), (int(round(x2Tick+graphicCorrectionsX[0])), int(round(y2Tick+graphicCorrectionsY[0]))), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues) #Write the number
                elif graphicNumbers == 90:
                    cv2.putText(scaledMainImg, str(graphicNumbers), (int(round(x2Tick+graphicCorrectionsX[1])), int(round(y2Tick+graphicCorrectionsY[1]))), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues) #Write the number
                elif graphicNumbers == -90:
                    cv2.putText(scaledMainImg, str(graphicNumbers), (int(round(x2Tick+graphicCorrectionsX[2])), int(round(y2Tick+graphicCorrectionsY[2]))), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues) #Write the number
                    
    def drawDepthGauge(self, scaledMainImg, numOfTicks, increments, position, gaugeLength, rgbValues, sensorInput):
        global counterDepth, stringAddDepth
        
        lineLength = gaugeLength #Originally 261
        
        if position == 0:
            x1 = 19
            x2 = 19
            correctedTickMarkPosition = 15
            cv2.line(scaledMainImg, (x1-10, (self.screenHeight)/2), (x1-19, (self.screenHeight/2)+9), rgbValues)#Creating top line for arrow
            cv2.line(scaledMainImg, (x1-10, (self.screenHeight)/2), (x1-19, (self.screenHeight/2)-9), rgbValues)#Creating bottom line for arrow
            cv2.line(scaledMainImg, (x1-19, (self.screenHeight/2)+9), (x1-19, ((self.screenHeight)/2)-9), rgbValues)#Creating closing line for triangle
        elif position == 1:
            x1 = self.screenWidth-20
            x2 = self.screenWidth-20
            correctedTickMarkPosition = -40
            cv2.line(scaledMainImg, (x1+10, (self.screenHeight)/2), (x1+19, (self.screenHeight/2)+9), rgbValues)#Creating top line for arrow
            cv2.line(scaledMainImg, (x1+10, (self.screenHeight)/2), (x1+19, (self.screenHeight/2)-9), rgbValues)#Creating bottom line for arrow
            cv2.line(scaledMainImg, (x1+19, (self.screenHeight/2)+9), (x1+19, ((self.screenHeight)/2)-9), rgbValues)#Creating closing line for triangle
            
            
        y1 = self.screenHeight/2 - lineLength/2
        y2 = self.screenHeight/2 + lineLength/2
            
        tickMarkGapDistance = lineLength/numOfTicks #Distance between tick marks
        depth = sensorInput#round((sensorInput - 14.6959)/0.4332, 2)#PSI to feet under water
        
                
        if self.setInitialTickPosition[2]:
            stringAddDepth = -(numOfTicks*increments)/2.0 #The amount of tick marks above the middle tick mark
            self.setInitialTickPosition[2] = False
            counterDepth = 0
            
        cv2.line(scaledMainImg, (x1, y1), (x2, y2), rgbValues) #Creating line
        
        for x in range(numOfTicks+1):
            tickMarkHeight = y1 + (lineLength*x)/numOfTicks #The INITIAL height of each tick mark
            tickMarkMoving = int(tickMarkHeight - ((depth-counterDepth)*tickMarkGapDistance)/increments) #The height of each tick mark after moving them based on sensor input

            if x == 0 and tickMarkMoving <= y1 - tickMarkGapDistance: #As the tick marks are moving up; once the tick mark's distance away from the top of the line is the difference between the tick mark gaps...
                counterDepth += increments*((y1 - tickMarkMoving)/tickMarkGapDistance) #Increment a counter that will move the ticks marks back down to their initial position and adjust the tick mark numbers. If the user doesnt enter a high enough increment, the tick marks will run behind. To catch them up, we find out how many tickMarkGaps ahead it is and multiply that to increment

            elif x == numOfTicks and tickMarkMoving >= y2 + tickMarkGapDistance: #As the tick marks are moving down; once the tick mark's distance away from the bottom of the line is the difference between the tick mark gaps...
                counterDepth -= increments*((y2 + tickMarkMoving)/tickMarkGapDistance) #Decrement a counter that will move the ticks marks back up to their initial position and adjust the tick mark numbers
                    
            elif tickMarkMoving >= y1 and tickMarkMoving <= y2: #As long as the tick marks don't go past the line upper or lower bounds of the line...
                graphicNumbers = round(stringAddDepth+counterDepth+(x*increments), 5)
                cv2.line(scaledMainImg, (x1-10, tickMarkMoving), (x1+10, tickMarkMoving), rgbValues) #Draw the tick mark
                if graphicNumbers -  int(graphicNumbers) == 0: #Get rid of decimals when not using them
                    graphicNumbers = int(graphicNumbers)
                cv2.putText(scaledMainImg, str(graphicNumbers), (x1+correctedTickMarkPosition, tickMarkMoving+5), cv2.FONT_HERSHEY_PLAIN, 0.9, rgbValues) #Write the number
                
    def drawAttitude(self, scaledMainImg, length, displayPosVel, position, letterSize, letterScale, rgbValues, orientationData, positionData, velocityData):
        T = advM.matrixMultiply(advM.Rot(e2, orientationData[0]), advM.Rot(e1, orientationData[1]), advM.Rot(e3, orientationData[2]))
        xxAngle = math.degrees(math.acos(T[0, 0]))
        yyAngle = math.degrees(math.acos(T[1, 1]))
        zzAngle = math.degrees(math.acos(T[2, 2]))
        
        if self.window.printOptionCheckboxValues[6].get() == 1:
            R, P = advM.extractData(T)
            numpy.set_printoptions(precision=4, suppress=True)
            print "Time:", datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')
            print "Current Rotation Matrix:"
            print R
            print "x to x Angle:", round(xxAngle, 4)
            print "y to y Angle:", round(yyAngle, 4)
            print "z to z Angle:", round(zzAngle, 4), "\n"
        
        if displayPosVel:
            attitudeCorrection = 20
        else:
            attitudeCorrection = 0
            
        if position == 0:
            x = length+10
            y = self.screenHeight-(length+10+attitudeCorrection)
            
            xPosVelText = 0
            yPosVelText = self.screenHeight-15
            
            textCorrection = 0
            
        if position == 1:
            x = self.screenWidth-(length+30)
            y = self.screenHeight-(length+10+attitudeCorrection)
            
            xPosVelText = self.screenWidth-128
            yPosVelText = self.screenHeight-15
            
            posString = "Pos: {0:.2f}, {0:.2f}, {0:.2f} m".format(positionData[0], positionData[1], positionData[2])
            velString = "Vel: {0:.2f}, {0:.2f}, {0:.2f} m/s".format(velocityData[0], velocityData[1], velocityData[2])
            
            if len(posString) > len(velString):
                greaterString = len(posString)
                
            elif len(velString) >= len(posString):
                greaterString = len(velString)
            
            textCorrection = (greaterString-22)*6-5
            
        if position == 2:
            x = self.screenWidth-(length+30)
            y = length+20+attitudeCorrection
            
            xPosVelText = self.screenWidth-128
            yPosVelText = 15
            
            posString = "Pos: {0:.2f}, {0:.2f}, {0:.2f} m".format(positionData[0], positionData[1], positionData[2])
            velString = "Vel: {0:.2f}, {0:.2f}, {0:.2f} m/s".format(velocityData[0], velocityData[1], velocityData[2])
            
            if len(posString) > len(velString):
                greaterString = len(posString)
                
            elif len(velString) >= len(posString):
                greaterString = len(velString)
            
            textCorrection = (greaterString-22)*6-5
            
        if position == 3:
            x = length+10
            y = length+20+attitudeCorrection
            
            xPosVelText = 0
            yPosVelText = 15

            textCorrection = 0
            
        if displayPosVel:
            posString = "Pos: {0:.2f}, {0:.2f}, {0:.2f} m".format(positionData[0], positionData[1], positionData[2])
            velString = "Vel: {0:.2f}, {0:.2f}, {0:.2f} m/s".format(velocityData[0], velocityData[1], velocityData[2])
            
            if len(posString) > len(velString):
                greaterString = len(posString)
                
            elif len(velString) >= len(posString):
                greaterString = len(velString)

            cv2.putText(scaledMainImg, posString, (xPosVelText-textCorrection, yPosVelText), cv2.FONT_HERSHEY_PLAIN, 0.7, rgbValues)
            cv2.putText(scaledMainImg, velString, (xPosVelText-textCorrection, yPosVelText+10), cv2.FONT_HERSHEY_PLAIN, 0.7, rgbValues)
         
        
        x1 = int(x + T[0, 0]*length)
        x2 = int(y + T[1, 0]*length)
        y1 = int(x + T[0, 1]*length)
        y2 = int(y + T[1, 1]*length)
        z1 = int(x + T[0, 2]*length)
        z2 = int(y + T[1, 2]*length)
        
        x3 = int(x + -T[0, 0]*length)
        x4 = int(y + -T[1, 0]*length)
        y3 = int(x + -T[0, 1]*length)
        y4 = int(y + -T[1, 1]*length)
        z3 = int(x + -T[0, 2]*length)
        z4 = int(y + -T[1, 2]*length)
        
        tmp = ((-0.8 * length) + 40) / 45
        attitudeLetterSizeAdjust = (letterSize/10.0) # Multiply Factor, 1 for default
        
        cv2.line(scaledMainImg, (x, y), (x1, x2), rgbValues) #Draw the tick mark
        cv2.putText(scaledMainImg, "X", (x1, x2), cv2.FONT_HERSHEY_PLAIN, (1.1 - T[2, 0]*(letterScale/10.0) - tmp)*attitudeLetterSizeAdjust, rgbValues) #Write the number
        cv2.line(scaledMainImg, (x, y), (y1, y2), rgbValues) #Draw the tick mark
        cv2.putText(scaledMainImg, "Y", (y1, y2), cv2.FONT_HERSHEY_PLAIN, (1.1 - T[2, 1]*(letterScale/10.0) - tmp)*attitudeLetterSizeAdjust, rgbValues) #Write the number
        cv2.line(scaledMainImg, (x, y), (z1, z2), rgbValues) #Draw the tick mark
        cv2.putText(scaledMainImg, "Z", (z1, z2), cv2.FONT_HERSHEY_PLAIN, (1.1 - T[2, 2]*(letterScale/10.0) - tmp)*attitudeLetterSizeAdjust, rgbValues) #Write the number
        cv2.line(scaledMainImg, (x, y), (x3, x4), rgbValues) #Draw the tick mark
        cv2.putText(scaledMainImg, "-X", (x3, x4), cv2.FONT_HERSHEY_PLAIN, (1.1 + T[2, 0]*(letterScale/10.0) - tmp)*attitudeLetterSizeAdjust, rgbValues) #Write the number
        cv2.line(scaledMainImg, (x, y), (y3, y4), rgbValues) #Draw the tick mark
        cv2.putText(scaledMainImg, "-Y", (y3, y4), cv2.FONT_HERSHEY_PLAIN, (1.1 + T[2, 1]*(letterScale/10.0) - tmp)*attitudeLetterSizeAdjust, rgbValues) #Write the number
        cv2.line(scaledMainImg, (x, y), (z3, z4), rgbValues) #Draw the tick mark
        cv2.putText(scaledMainImg, "-Z", (z3, z4), cv2.FONT_HERSHEY_PLAIN, (1.1 + T[2, 2]*(letterScale/10.0) - tmp)*attitudeLetterSizeAdjust, rgbValues) #Write the number
        
        
    def drawBatteryGauge(self, scaledMainImg, batteryLength, batteryCurrent, batteryPosition, rgbValues, batteryData):

        batery1VoltageCapacity, batery1CurrentCapacity, batery2VoltageCapacity, batery2CurrentCapacity = batteryData[0], batteryData[1], batteryData[2], batteryData[3]
        
        if batteryCurrent == 0:
            if batteryPosition == 0:
                x1 = 60
                y1 = self.screenHeight-30
                
            elif batteryPosition == 1:
                x1 = self.screenWidth-batteryLength-40
                y1 = self.screenHeight-30
                
            elif batteryPosition == 2:
                x1 = self.screenWidth-batteryLength-40
                y1 = 5
                
            elif batteryPosition == 3:
                x1 = 60
                y1 = 5
                
            x2 = x1
            y2 = y1+15
            
        elif batteryCurrent == 1:
            if batteryPosition == 0:
                x1 = 60
                y1 = self.screenHeight-50
                
            elif batteryPosition == 1:
                x1 = self.screenWidth-batteryLength-40
                y1 = self.screenHeight-50
                
            elif batteryPosition == 2:
                x1 = self.screenWidth-batteryLength-40
                y1 = 5
                
            elif batteryPosition == 3:
                x1 = 60
                y1 = 5
                
            x2 = x1
            y2 = y1+25

        cv2.putText(scaledMainImg, "Batt 1 (V)", (x1-60, y1+8), cv2.FONT_HERSHEY_PLAIN, 0.7, rgbValues)
        cv2.rectangle(scaledMainImg, (x1, y1), (int(x1+batteryLength*(batery1VoltageCapacity/100.0)), y1+10), rgbValues, thickness=-1)
        cv2.rectangle(scaledMainImg, (x1, y1), (x1+batteryLength, y1+10), (255, 255, 255))
        cv2.putText(scaledMainImg, str(batery1VoltageCapacity)+"%", (x1+batteryLength+2, y1+9), cv2.FONT_HERSHEY_PLAIN, 0.8, rgbValues)
        
        if batteryCurrent == 1:
            cv2.putText(scaledMainImg, "Batt 1 (I)", (x1-60, y1+20), cv2.FONT_HERSHEY_PLAIN, 0.7, rgbValues)
            cv2.rectangle(scaledMainImg, (x1, y1+10), (int(x1+batteryLength*(batery1CurrentCapacity/100.0)), y1+20), rgbValues, thickness=-1)
            cv2.rectangle(scaledMainImg, (x1, y1+10), (x1+batteryLength, y1+20), (255, 255, 255))
            cv2.putText(scaledMainImg, str(batery1CurrentCapacity)+"%", (x1+batteryLength+2, y1+20), cv2.FONT_HERSHEY_PLAIN, 0.8, rgbValues)
        
        #Battery 2
        
        cv2.putText(scaledMainImg, "Batt 2 (V)", (x2-60, y2+8), cv2.FONT_HERSHEY_PLAIN, 0.7, rgbValues)
        cv2.rectangle(scaledMainImg, (x2, y2), (int(x2+batteryLength*(batery2VoltageCapacity/100.0)), y2+10), rgbValues, thickness=-1)
        cv2.rectangle(scaledMainImg, (x2, y2), (x2+batteryLength, y2+10), (255, 255, 255))
        cv2.putText(scaledMainImg, str(batery2VoltageCapacity)+"%", (x2+batteryLength+2, y2+9), cv2.FONT_HERSHEY_PLAIN, 0.8, rgbValues)
        
        if batteryCurrent == 1:
            cv2.putText(scaledMainImg, "Batt 2 (I)", (x2-60, y2+20), cv2.FONT_HERSHEY_PLAIN, 0.7, rgbValues)
            cv2.rectangle(scaledMainImg, (x2, y2+10), (int(x2+batteryLength*(batery2CurrentCapacity/100.0)), y2+20), rgbValues, thickness=-1)
            cv2.rectangle(scaledMainImg, (x2, y2+10), (x2+batteryLength, y2+20), (255, 255, 255))
            cv2.putText(scaledMainImg, str(batery2CurrentCapacity)+"%", (x2+batteryLength+2, y2+20), cv2.FONT_HERSHEY_PLAIN, 0.8, rgbValues)
            
    def drawTemperature(self, scaledMainImg, size, position, rgbValues, temperatureData):
        
        scaledSize = 4.0*(size/50.0)
        
        #3 is to 138 as 1 is to 48
        if position == 0:
            x1 = 0
            y1 = int(self.screenHeight - scaledSize/0.07 - (5*scaledSize)/3 - 1)
            
        elif position == 1:
            x1 = int(self.screenWidth-(scaledSize/0.022))
            y1 = int(self.screenHeight - scaledSize/0.07 - (5*scaledSize)/3 - 1)
            
        elif position == 2:
            x1 = int(self.screenWidth-(scaledSize/0.022))
            y1 = int(scaledSize/0.07 - (5*scaledSize)/3 + 2)
            
        elif position == 3:
            x1 = 0
            y1 = int(scaledSize/0.07 - (5*scaledSize)/3 + 2)
        
        
        x2 = x1
        y2 = y1+int(scaledSize/0.076)
        
        #3 is to 40 as 1 is to 13
        cv2.putText(scaledMainImg, str(temperatureData)+"C", (x1, y1), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
        cv2.putText(scaledMainImg, str(temperatureData*(9.0/5.0)+32.0)+"F", (x2, y2), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
        
        
    def drawMotorGauges(self, scaledMainImg, size, position, rgbValues, motorDutyCycleData, motorDirectionData):
        
        scaledSize = 2.0*(size/50.0)
        
        y = self.screenHeight/2 + 6
        
        if position == 0:
            x = 0
            cv2.putText(scaledMainImg, "M1: "+str(motorDutyCycleData[0])+"%", (x, int(y-(scaledSize/0.15)*7)), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M2: "+str(motorDutyCycleData[1])+"%", (x, int(y-(scaledSize/0.15)*5)), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M3: "+str(motorDutyCycleData[2])+"%", (x, int(y-(scaledSize/0.15)*3)), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M4: "+str(motorDutyCycleData[3])+"%", (x, int(y-(scaledSize/0.15))), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M5: "+str(motorDutyCycleData[4])+"%", (x, int(y+(scaledSize/0.15))), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M6: "+str(motorDutyCycleData[5])+"%", (x, int(y+(scaledSize/0.15)*3)), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M7: "+str(motorDutyCycleData[6])+"%", (x, int(y+(scaledSize/0.15)*5)), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M8: "+str(motorDutyCycleData[7])+"%", (x, int(y+(scaledSize/0.15)*7)), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
        
        elif position == 1:
            x = int(self.screenWidth-(scaledSize/0.0112)+10)
            cv2.putText(scaledMainImg, "M1: "+str(motorDutyCycleData[0])+"%", (x+(4-len(str(motorDutyCycleData[0])+"%"))*9, int(y-(scaledSize/0.15)*7)), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M2: "+str(motorDutyCycleData[1])+"%", (x+(4-len(str(motorDutyCycleData[1])+"%"))*9, int(y-(scaledSize/0.15)*5)), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M3: "+str(motorDutyCycleData[2])+"%", (x+(4-len(str(motorDutyCycleData[2])+"%"))*9, int(y-(scaledSize/0.15)*3)), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M4: "+str(motorDutyCycleData[3])+"%", (x+(4-len(str(motorDutyCycleData[3])+"%"))*9, int(y-(scaledSize/0.15))), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M5: "+str(motorDutyCycleData[4])+"%", (x+(4-len(str(motorDutyCycleData[4])+"%"))*9, int(y+(scaledSize/0.15))), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M6: "+str(motorDutyCycleData[5])+"%", (x+(4-len(str(motorDutyCycleData[5])+"%"))*9, int(y+(scaledSize/0.15)*3)), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M7: "+str(motorDutyCycleData[6])+"%", (x+(4-len(str(motorDutyCycleData[6])+"%"))*9, int(y+(scaledSize/0.15)*5)), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
            cv2.putText(scaledMainImg, "M8: "+str(motorDutyCycleData[7])+"%", (x+(4-len(str(motorDutyCycleData[7])+"%"))*9, int(y+(scaledSize/0.15)*7)), cv2.FONT_HERSHEY_PLAIN, scaledSize, rgbValues)
        
        for i in range(8):
            if motorDirectionData[i] == 1:
                motorDutyCycleData[i] = -motorDutyCycleData[i]
        
        
        
        
    def drawStatus(self, scaledMainImg, position, rgbValues, name, alertNum):
        
        if position == 0:
            x1 = 6
            y1 = self.screenHeight-45
            xMissionName = 5
            yMissionName = self.screenHeight-10
        #3 is to 30, 4 is to 36, 1 is to 15, 2 is to 21
        elif position == 1:
            x1 = self.screenWidth-30
            y1 = self.screenHeight-45
            xMissionName = self.screenWidth-(15+len(name)*6)
            yMissionName = self.screenHeight-10

        elif position == 2:
            x1 = self.screenWidth-30
            y1 = 25
            xMissionName = self.screenWidth-(15+len(name)*6)
            yMissionName = 15
            
        elif position == 3:
            x1 = 6
            y1 = 25
            xMissionName = 5
            yMissionName = 15
            
        x2 = x1+20
        y2 = y1+20
        
        
        #12 to 90 as 6 to 55
        cv2.putText(scaledMainImg, name, (xMissionName, yMissionName), cv2.FONT_HERSHEY_SIMPLEX, 0.4, rgbValues)
        
        cv2.rectangle(scaledMainImg, (x1, y1), (x2, y2), rgbValues, thickness = 1)
        
        alertNum = alertNum/25.0
        
        if alertNum <= 1: #High Current
            cv2.rectangle(scaledMainImg, (x1+1, y1+1), (x2-1, y2-1), (0, 255, 255), thickness = -1) #Yellow
        elif alertNum <= 2: #Over heating
            cv2.rectangle(scaledMainImg, (x1+1, y1+1), (x2-1, y2-1), (0, 150, 255), thickness = -1) #Orange
        elif alertNum <= 3: #Low Battery
            cv2.rectangle(scaledMainImg, (x1+1, y1+1), (x2-1, y2-1), (0, 0, 255), thickness = -1) #Red
        
            
        
            
        #cv2.rectangle(scaledMainImg, (x1+1, y1+1), (x2-1, y2-1), (0, 0, 255), thickness = -1)
        
        
        
        
        