'''
Created on Jun 18, 2015

@author: Osten
'''

from direct.showbase.ShowBase import ShowBase #ShowBase Import

from direct.task import Task
from direct.showbase.InputStateGlobal import inputState

from panda3d.bullet import *# Imports for specific shapes in Bullet
from panda3d.core import *


class buildMe(ShowBase):  # basic construction
    def __init__(self):
        ShowBase.__init__(self)
        
        #disable camera and set perspective
        #self.disableMouse()
        self.camera.setPos(0,-60,60)
        self.camera.lookAt(self.render)
        
        # add a watcher for keyboard input
        inputState.watchWithModifiers('forward', 'w')
        inputState.watchWithModifiers('left', 'a')
        inputState.watchWithModifiers('right', 'd')
        inputState.watchWithModifiers('back', 's')
        inputState.watchWithModifiers('down', 'q')
        inputState.watchWithModifiers('up', 'e')
        
        # __DEBUG CODE__
        self.debugNode = BulletDebugNode('Debug')
        self.debugNode.showWireframe(True)
        self.debugNode.showNormals(True)
        self.debugNode.showBoundingBoxes(False)
        self.debugNode.showConstraints(True)
        self.debugNP = self.render.attachNewNode(self.debugNode)
        self.debugNP.show()
        
        # add the BulletWorld object and start stacking nodes
        self.world = BulletWorld() # instantiate the engine
        self.world.setGravity(Vec3(0, 0, 0)) # set the gravity
        self.world.setDebugNode(self.debugNP.node())
        
        # self.planeShape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        
        self.p0 = Point3(-20, -20, 0)
        self.p1 = Point3(-20, 20, 0)
        self.p2 = Point3(20, -20, 0)
        self.p3 = Point3(20, 20, 0)
        self.mesh = BulletTriangleMesh()
        self.mesh.addTriangle(self.p0, self.p1, self.p2)
        self.mesh.addTriangle(self.p1, self.p2, self.p3)
        self.planeShape = BulletTriangleMeshShape(self.mesh, dynamic=False)

        self.planeNode = BulletRigidBodyNode('ground')
        self.planeNode.setMass(0)
        self.planeNode.addShape(self.planeShape)
        self.gp = self.render.attachNewNode(self.planeNode)
        self.gp.setPos(0, 0, -3)
        self.gp.setHpr(0,0,0)
        self.world.attachRigidBody(self.planeNode)
        #try to load my wierd pool
        self.myPool = self.loader.loadModel('models/misc/BlenderPool.egg')
        self.myPool.setScale(10,10,10)
        self.myPool.setHpr(0,0,0)
        self.myPool.reparentTo(self.gp)
        
        self.boxShape = BulletBoxShape(Vec3(5, 5, 5)) # Built in shape
        self.boxNode = BulletCharacterControllerNode(self.boxShape, 0, 'PlayerBox') # player node Body creation
        #self.boxNode.setMass(100)
        #self.boxNode.addShape(self.boxShape) # Apply the shape
        self.np = self.render.attachNewNode(self.boxNode) # attach the rigid body plus shape to the sceneGraph
        self.np.setPos(0,0,30)
        self.world.attachCharacter(self.boxNode)
        #Load a simple model
        self.firstItem = self.loader.loadModel('models/RoboSubDownscaleAttempt.egg')
        self.firstItem.setPos(0,0,0)
        self.firstItem.setHpr(180,0,0)
        self.firstItem.setScale(14,14,14)
        self.firstItem.reparentTo(self.np)
        
        self.taskMgr.add(self.update, 'update') #add the task into the per frame operations
        self.globalClock = ClockObject.getGlobalClock() # create the clock
        
        #self.render.ls()
        
    def processInput(self, dt): # function to process input from inputState object
        speed = Vec3(0.0,0.0,0.0)
        omega = 0.0
        v = 2000.0
        
        if inputState.isSet('forward'): speed.setY(v)
        if inputState.isSet('left'): speed.setX(-v)
        if inputState.isSet('right'): speed.setX(v)
        if inputState.isSet('back'): speed.setY(-v)
        if inputState.isSet('up'): speed.setZ(v)
        if inputState.isSet('down'): speed.setZ(-v)
        
        self.boxNode.setLinearMovement(speed, True)
        
    def update(self, task): # define the change in time and call doPhysics every interval
        dt = self.globalClock.getDt()
        self.processInput(dt)
        self.world.doPhysics(dt)
        return task.cont

buildInstance = buildMe()
buildInstance.run()
