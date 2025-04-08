'''
Created on Nov 7, 2014

@author: Austin

These functions are only supposed to be called by the binding functions offered by the Tkinter library
'''
import os, shutil, fnmatch
import Tkinter

buttonPressedToggle = False #Used for knowing when the user is pressing or releasing the mouse button
class EventHandlers:
    def __init__(self, guiWidth, imgWidth):
        self.guiWidth = guiWidth
        self.imgWidth = imgWidth
        
    def initilizeGuiEvents(self, window):
        self.window = window
        
    def initilizeFrontRawImgEvents(self, frontRawImgLabel):
        self.frontRawImgLabel = frontRawImgLabel
    
    def initilizeBottomRawImgEvents(self, bottomRawImgLabel):
        self.bottomRawImgLabel = bottomRawImgLabel
        
    def frontRawImgDraw(self, event):
        halfOfGui = self.guiWidth/2
        whiteSpace = halfOfGui - self.imgWidth
        
        x = event.x-int(whiteSpace/2)
        y = event.y
        
        if x < 0:
            x = 0  
              
        elif x > self.imgWidth:
            x = self.imgWidth
            
        self.frontRawImgLabel.mouseDragLocation[0] = x
        self.frontRawImgLabel.mouseDragLocation[1] = y
        
    def bottomRawImgDraw(self, event):
        halfOfGui = self.guiWidth/2
        whiteSpace = halfOfGui - self.imgWidth
        
        x = event.x-int(whiteSpace/2)
        y = event.y

        if x < 0:
            x = 0  
              
        elif x > self.imgWidth:
            x = self.imgWidth
            
        self.bottomRawImgLabel.mouseDragLocation[0] = x
        self.bottomRawImgLabel.mouseDragLocation[1] = y
        
    def guiKeyboardEvent(self, event):
        
        if chr(event.keycode) == " ": 
            self.window.spaceBar = not self.window.spaceBar
        
        if chr(event.keycode) == "C" and not event.char == chr(3): #If key reads as c or C and is not ctrl+c
            if not os.path.exists('_Pictures_/Front/'):
                os.makedirs('_Pictures_/Front/')
            self.window.pictureCount[0] = len(fnmatch.filter(os.listdir('_Pictures_/Front/'), '*.png'))
            self.window.captureImg[0] = True  
            
        if event.char == chr(3): #If key reads as ctrl+c
            if not os.path.exists('_Pictures_/Bottom/'):
                os.makedirs('_Pictures_/Bottom/')    
            self.window.pictureCount[1] = len(fnmatch.filter(os.listdir('_Pictures_/Bottom/'), '*.png'))
            self.window.captureImg[1] = True  
            
        if chr(event.keycode) == "R" and not event.char == chr(18): #If R is pressed, start recording
            if self.window.recordImg[0] == False: #If not already recording
                if not os.path.exists('_Recordings_/Front/'):
                    os.makedirs('_Recordings_/Front/')
                
                self.top = Tkinter.Toplevel(self.window)
                self.top.geometry("265x30+690+250")
                self.top.title("Recording Front Cam")
                #Pop up window object and size
                self.userInput = Tkinter.Entry(self.top)
                self.userInput.grid(row=0, column=1)
                self.userInput.focus_set()
                
                popUp = Tkinter.Label(self.top, text = "Seconds Per Frame:")
                popUp.grid(row=0, column=0)
                self.userInput.bind("<Return>", self.recordFrontOk)
                
                button = Tkinter.Button(self.top, text="OK", command = self.recordFrontOk)
                button.grid(row=0, column=3, columnspan=2)
                
            elif self.window.recordImg[0] == True: #If already recording
                self.window.recording[0].config(state = "normal", foreground = "gray")
                self.window.recordImg[0] = False
            
        if event.char == chr(18): #Ctrl-r
            if self.window.recordImg[1] == False: #If not already recording
                if not os.path.exists('_Recordings_/Bottom/'):
                    os.makedirs('_Recordings_/Bottom/')
                
                self.top = Tkinter.Toplevel(self.window)
                self.top.geometry("278x30+690+250")
                self.top.title("Recording Bottom Cam")
                #Pop up window object and size
                self.userInput = Tkinter.Entry(self.top)
                self.userInput.grid(row=0, column=1)
                self.userInput.focus_set()
                
                popUp = Tkinter.Label(self.top, text = "Seconds Per Frame:")
                popUp.grid(row=0, column=0)
                self.userInput.bind("<Return>", self.recordBottomOk)
                
                button = Tkinter.Button(self.top, text="OK", command = self.recordBottomOk)
                button.grid(row=0, column=3, columnspan=2)
                
            elif self.window.recordImg[1] == True: #If already recording
                self.window.recording[1].config(state = "normal", foreground = "gray")
                self.window.recordImg[1] = False
            
        if event.keycode == 27: #Escape character; terminate program
            self.window.quitFlag = True
            
    def recordFrontOk(self, *event):
        if self.userInput.get().replace(".", "", 1).isdigit(): #If the string is a digit or float
            self.window.recordCount[0] = len(fnmatch.filter(os.listdir('_Recordings_/Front/'), '*.png')) #Puts existing amount of pictures into variable
            self.window.secondsPerFrame[0] = self.userInput.get()
            self.window.recordImg[0] = True
            self.window.recording[0].config(foreground = "red")
        self.top.destroy()
        
    def recordBottomOk(self, *event):
        if self.userInput.get().replace(".", "", 1).isdigit(): #If the string is a digit or float
            self.window.recordCount[1] = len(fnmatch.filter(os.listdir('_Recordings_/Bottom/'), '*.png')) #Puts existing amount of pictures into variable
            self.window.secondsPerFrame[1] = self.userInput.get()
            self.window.recordImg[1] = True
            self.window.recording[1].config(foreground = "red")
        self.top.destroy()

    def frontRawImgMouseEvent(self, event):
        global buttonPressedToggle
        
        buttonPressedToggle = not buttonPressedToggle
        
        halfOfGui = self.guiWidth/2
        whiteSpace = halfOfGui - self.imgWidth
        
        x = event.x-int(whiteSpace/2)
        y = event.y
        
        if x < 0:
            x = 0
        
        if y < 0:
            y = 0
              
        elif x > self.imgWidth:
            x = self.imgWidth
            
        self.frontRawImgLabel.mouseDragLocation = [x, y] #This is so this variable can initially start with these locations so the box wont start at [0, 0]
            
        if buttonPressedToggle == True:
            self.frontRawImgLabel.boxPoint1 = [x, y]
            self.frontRawImgLabel.buttonReleased = False
            self.frontRawImgLabel.buttonPressed = True
        
        elif buttonPressedToggle == False:
            self.frontRawImgLabel.boxPoint2 = [x, y]
            if self.frontRawImgLabel.boxPoint1[0] != self.frontRawImgLabel.boxPoint2[0] and self.frontRawImgLabel.boxPoint1[1] != self.frontRawImgLabel.boxPoint2[1]: #As long as boxPoint1 is not the same as boxPoint2
                if self.frontRawImgLabel.boxPoint2[0] > self.frontRawImgLabel.boxPoint1[0] and self.frontRawImgLabel.boxPoint2[1] > self.frontRawImgLabel.boxPoint1[1]: #As long as going from quadrant 2 to 4
                    self.frontRawImgLabel.boxPoint2 = [x, y]
                elif self.frontRawImgLabel.boxPoint2[0] < self.frontRawImgLabel.boxPoint1[0] and self.frontRawImgLabel.boxPoint2[1] < self.frontRawImgLabel.boxPoint1[1]: #As long as going from quadrant 4 to 2
                    self.frontRawImgLabel.boxPoint2 = self.frontRawImgLabel.boxPoint1 #Switch coordinates with boxPoint1
                    self.frontRawImgLabel.boxPoint1 = [x, y] #Switch x coordinates with boxPoint2
                elif self.frontRawImgLabel.boxPoint2[0] > self.frontRawImgLabel.boxPoint1[0] and self.frontRawImgLabel.boxPoint2[1] < self.frontRawImgLabel.boxPoint1[1]: #As long as going from quadrant 3 to 1
                    self.frontRawImgLabel.boxPoint2[1] = self.frontRawImgLabel.boxPoint1[1] #Switch y coordinates with boxPoint1
                    self.frontRawImgLabel.boxPoint1[1] = y #Switch y coordinates with boxPoint2
                elif self.frontRawImgLabel.boxPoint2[0] < self.frontRawImgLabel.boxPoint1[0] and self.frontRawImgLabel.boxPoint2[1] > self.frontRawImgLabel.boxPoint1[1]: #As long as going from quadrant 1 to 3
                    self.frontRawImgLabel.boxPoint2[0] = self.frontRawImgLabel.boxPoint1[0] #Switch x coordinates with boxPoint1
                    self.frontRawImgLabel.boxPoint1[0] = x  #Switch x coordinates with boxPoint2
                
                self.frontRawImgLabel.buttonReleased = True
                self.frontRawImgLabel.buttonPressed = False   
                     
            else: #If boxPoint1 and boxPoint2 are the same
                self.frontRawImgLabel.buttonReleased = False #Pretend it never happened
                self.frontRawImgLabel.buttonPressed = False #Pretend it never happened
                
    def bottomRawImgMouseEvent(self, event):
        global buttonPressedToggle
        
        buttonPressedToggle = not buttonPressedToggle
        
        halfOfGui = self.guiWidth/2
        whiteSpace = halfOfGui - self.imgWidth
        
        x = event.x-int(whiteSpace/2)
        y = event.y

        if x < 0:
            x = 0
        
        if y < 0:
            y = 0
              
        elif x > self.imgWidth:
            x = self.imgWidth
            
        self.bottomRawImgLabel.mouseDragLocation = [x, y] #This is so this variable can initially start with these locations so the box wont start at [0, 0]

        if buttonPressedToggle == True:
            self.bottomRawImgLabel.boxPoint1 = [x, y]
            self.bottomRawImgLabel.buttonReleased = False
            self.bottomRawImgLabel.buttonPressed = True
        
        elif buttonPressedToggle == False:
            self.bottomRawImgLabel.boxPoint2 = [x, y]
            if self.bottomRawImgLabel.boxPoint1[0] != self.bottomRawImgLabel.boxPoint2[0] and self.bottomRawImgLabel.boxPoint1[1] != self.bottomRawImgLabel.boxPoint2[1]: #As long as boxPoint1 is not the same as boxPoint2
                if self.bottomRawImgLabel.boxPoint2[0] > self.bottomRawImgLabel.boxPoint1[0] and self.bottomRawImgLabel.boxPoint2[1] > self.bottomRawImgLabel.boxPoint1[1]: #As long as going from quadrant 2 to 4
                    self.bottomRawImgLabel.boxPoint2 = [x, y]
                elif self.bottomRawImgLabel.boxPoint2[0] < self.bottomRawImgLabel.boxPoint1[0] and self.bottomRawImgLabel.boxPoint2[1] < self.bottomRawImgLabel.boxPoint1[1]: #As long as going from quadrant 4 to 2
                    self.bottomRawImgLabel.boxPoint2 = self.bottomRawImgLabel.boxPoint1 #Switch coordinates with boxPoint1
                    self.bottomRawImgLabel.boxPoint1 = [x, y] #Switch x coordinates with boxPoint2
                elif self.bottomRawImgLabel.boxPoint2[0] > self.bottomRawImgLabel.boxPoint1[0] and self.bottomRawImgLabel.boxPoint2[1] < self.bottomRawImgLabel.boxPoint1[1]: #As long as going from quadrant 3 to 1
                    self.bottomRawImgLabel.boxPoint2[1] = self.bottomRawImgLabel.boxPoint1[1] #Switch y coordinates with boxPoint1
                    self.bottomRawImgLabel.boxPoint1[1] = y #Switch y coordinates with boxPoint2
                elif self.bottomRawImgLabel.boxPoint2[0] < self.bottomRawImgLabel.boxPoint1[0] and self.bottomRawImgLabel.boxPoint2[1] > self.bottomRawImgLabel.boxPoint1[1]: #As long as going from quadrant 1 to 3
                    self.bottomRawImgLabel.boxPoint2[0] = self.bottomRawImgLabel.boxPoint1[0] #Switch x coordinates with boxPoint1
                    self.bottomRawImgLabel.boxPoint1[0] = x  #Switch x coordinates with boxPoint2
                
                self.bottomRawImgLabel.buttonReleased = True
                self.bottomRawImgLabel.buttonPressed = False   
                     
            else: #If boxPoint1 and boxPoint2 are the same
                self.bottomRawImgLabel.buttonReleased = False #Pretend it never happened
                self.bottomRawImgLabel.buttonPressed = False #Pretend it never happened