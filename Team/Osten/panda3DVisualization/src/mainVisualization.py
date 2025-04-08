'''
Created on May 24, 2015

testing for use on robosub / learning what this panda3D is all about :)

@author: Osten
'''

from math import pi, sin, cos
#import sparton_ahrs

from panda3d.core import PandaNode,NodePath,Camera,TextNode,ClockObject
from panda3d.core import CollisionSphere, CollisionNode, CollisionTraverser, CollisionHandlerQueue
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from pandac.PandaModules import Point3  #don't know why it can't find Point3 cause it works...
from direct.distributed.ClockDelta import globalClockDelta

"""spartonResponseThread = sparton_ahrs.SpartonAhrsResponse("COM28")
spartonResponseThread.start()"""

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        
        # __________VARIABLES______________
        self.setFrameRateMeter(True)
        
        self.ahrsData = [0,0,0]  #set ahrsData so that I don't have to error check
        self.isMoving = False  #sub state variables
        self.disableMouse() #Disable the camera track-ball controls
        # "floater" object to hold a phantom position above the panda
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(self.render)
        
        self.environ = self.loader.loadModel("models/TRANSDEC.egg") #Load the environment 
        self.environ.reparentTo(self.render)     #Re-parent the model to render which is default base.
        self.environ.setScale(20, 20, 20)  #Apply scale and position transforms on the environment
        self.environ.setPos(0, 0, 0)
        
        #self.pandaActor = Actor("models/cubeTest") # to test the .egg file i made
        self.pandaActor = Actor("models/RoboSubDownscaleAttempt.egg")
        self.pandaActor.setScale(7, 7, 7)
        self.pandaActor.setPos(0, 0, 0)
        self.pandaActor.setHpr(0, 0, 0)
        self.pandaActor.reparentTo(self.render)
        self.pandaActor.loop("walk")  #Loop its animation
        
        #_________test to add collision to the panda START_________
        self.cs = CollisionSphere(0,0,0,.5)
        self.cs2 = CollisionSphere(0,0,0,8)
        self.pandaNodePath = self.pandaActor.attachNewNode(CollisionNode('subSphere'))
        self.pandaNodePath.node().addSolid(self.cs)
        self.pandaNodePath.show()
        
        self.cNodePath = self.render.attachNewNode(CollisionNode('groundSphere'))
        self.cNodePath.node().addSolid(self.cs2)
        self.cNodePath.show()
        
        self.cTrav = CollisionTraverser()
        self.collisionHandler = CollisionHandlerQueue()
        # Add the collider to cTrav and target the queue
        self.cTrav.addCollider(self.pandaNodePath, self.collisionHandler)
        self.cTrav.addCollider(self.cNodePath, self.collisionHandler)
        
        def traverseTask(task=None):
            self.collisionHandler.sortEntries()
            for i in range(self.collisionHandler.getNumEntries()):
                entry = self.collisionHandler.getEntry(i)
                print entry
                self.collisionHandler.clearEntries()
                if task: return task.cont
            if task: return task.cont
        
        self.taskMgr.add(traverseTask, "testTraversalCheck")
        
    
        # collision test stuff END____________
         
        global textObject #to test on-screen-objects
        textObject = OnscreenText(text = '', pos = (-0.8, 0.08), scale = 0.07, fg=(45, 45, 45, 1))
        
        self.forwardSpeedModifier = 2  # actor movement modifiers
        self.swivelSpeedModifier = 200
        self.heightSpeedModifier = 9
        
        # __________VARIABLES______________END
        
        # _______ACCEPT KEY INPUT___________
        self.keymap = {"firstPerson":0, "thirdPerson":1, # Key-map to hold current state of input
                       "skyView":0, "forward":0,
                       "left":0, "right":0, "reverse":0,
                       "vert_up":0, "vert_down":0, }
        
        self.accept("1", self.setKey, ["firstPerson",1])    #These are keys for predetermined perspectives
        self.accept("3", self.setKey, ["thirdPerson",1])
        self.accept("0", self.setKey, ["skyView",1])
         
        self.accept("w", self.setKey, ["forward",1])  #These are directional movement keys
        self.accept("w-up", self.setKey, ["forward",0])
        self.accept("a", self.setKey, ["left",1])
        self.accept("a-up", self.setKey, ["left",0])
        self.accept("d", self.setKey, ["right",1])
        self.accept("d-up", self.setKey, ["right",0])
        self.accept("s", self.setKey, ["reverse",1])
        self.accept("s-up", self.setKey, ["reverse",0])
        self.accept("arrow_up", self.setKey, ["vert_up",1])
        self.accept("arrow_up-up", self.setKey, ["vert_up",0])
        self.accept("arrow_down", self.setKey, ["vert_down",1])
        self.accept("arrow_down-up", self.setKey, ["vert_down",0])         
        # _______ACCEPT KEY INPUT___________END 
       
        # _______________ACTIVE TASKS___________
        self.taskMgr.add(self.positionCameraTask, "PositionCameraTask")
        #self.taskMgr.add(self.updatePositionTask, "updatePositionTask")
        #self.taskMgr.add(self.displayCameraPosition, "displayCameraPosition")
        #self.taskMgr.add(self.ahrsFunction, "generateAHRS")
        self.taskMgr.add(self.move, "movementKeyTracking")
        # _______________ACTIVE TASKS___________END  
    
    #  ______TASK DEFINITIONS_________________
    """def displayCameraPosition(self, task):
        textObject.setText(str(self.camera.getPos()))
        return Task.cont"""
    
    def updatePositionTask(self, task):  # for automated movement / ahrs values input
        angleDegrees = task.time * 0
        angleRadians = angleDegrees * (pi/180.0)
        self.pandaActor.setPos(20 * sin(angleRadians), 0 * cos(angleRadians), 3)
        self.pandaActor.setHpr(20*sin(angleRadians),
                               0*cos(angleRadians),
                               1*sin(angleRadians))
        return Task.cont 
        
        # Procedure to move the camera now includes use of a floating object above the actor
        # to provide a better camera angle
    def positionCameraTask(self, task):
        self.floater.setPos(self.pandaActor.getPos())  #set the position of the float node
        self.floater.setZ(self.pandaActor.getZ() + 2.0)
        
        if(self.keymap["thirdPerson"]!=0):             # checks for predefined perspectives
            self.camera.setX(self.floater.getX())
            self.camera.setY(self.floater.getY() + 30)
            self.camera.setZ(self.floater.getZ() + 20)
            self.camera.lookAt(self.floater)                #set the camera to target the float
        
        if(self.keymap["firstPerson"]!=0):
            self.camera.setPos(self.pandaActor.getPos())
            self.camera.setHpr(self.pandaActor.getHpr())
            self.camera.setH(180 + self.pandaActor.getH())
        
        if(self.keymap["skyView"]!=0):
            self.camera.setPos(self.pandaActor.getPos())
            self.camera.setZ(400)
            self.camera.setP(270)        
        
        return task.cont
    
    """def ahrsFunction(self, task):
        while len(spartonResponseThread.getList) > 0:
            self.ahrsData = spartonResponseThread.getList.pop(0)
        return Task.cont"""
        
    def move(self, task): # Handles all the Key Events
        if (self.keymap["forward"]!=0):
            self.pandaActor.setY(self.pandaActor, -self.forwardSpeedModifier * globalClock.getDt())            
        if (self.keymap["left"]!=0):
            self.pandaActor.setH(self.pandaActor.getH() + self.swivelSpeedModifier * globalClock.getDt())
        if (self.keymap["right"]!=0):
            self.pandaActor.setH(self.pandaActor.getH() - self.swivelSpeedModifier * globalClock.getDt())
        if (self.keymap["reverse"]!=0):
            self.pandaActor.setY(self.pandaActor, self.forwardSpeedModifier * globalClock.getDt())
        if (self.keymap["vert_up"]!=0):
            self.pandaActor.setZ(self.pandaActor.getZ() + self.heightSpeedModifier * globalClock.getDt())
        if (self.keymap["vert_down"]!=0):
            self.pandaActor.setZ(self.pandaActor.getZ() - self.heightSpeedModifier * globalClock.getDt())    

        return task.cont
    
    # ______TASK DEFINITIONS_______END
    
    #__________FUNCTION DEFINITIONS__________
        
    def setKey(self, key, value):
        self.keymap[key] = value #assign value based on key press
        
        if key == "thirdPerson":              #would be nice to do this differently but here it is for now
            self.keymap["firstPerson"] = 0    #this checks for viewing angles and disables others
            self.keymap["skyView"] = 0
        if key == "firstPerson":
            self.keymap["thirdPerson"] = 0
            self.keymap["skyView"] = 0
        if key == "skyView":
            self.keymap["firstPerson"] = 0
            self.keymap["thirdPerson"] = 0
        
    # __________FUNCTION DEFINITIONS__________end
        
app = MyApp()
app.run()


