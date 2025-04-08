from cv2 import *
import math
import Depth
import Position
import GenState

class GUI:

    def __init__(self):
        self.camActive = false
        self.depth = Depth.Depth(self.testCam())
        self.pos = Position.Position(self.cam, []'''ahrs''')
        self.state = GenState.GeneralState(self.cam) #needs class
                                                     #variables initialized
        
    def testCam(self):
        if self.camActive == false:
            self.cam = VideoCapture(0)
            self.camActive = true
        
        a, b = cam.read()
        return b

    def update(self):
        self.state.update('''data''')
        self.pos.update('''data''')
        self.depth.update('''data''')

    
    


        
        
        
