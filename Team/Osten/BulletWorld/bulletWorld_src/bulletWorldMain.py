'''
Created on Jun 12, 2015

@author: Osten
'''
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Vec3, ClockObject
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

# test materials
from panda3d.core import Material
from panda3d.core import VBase4


class MyBulletWorld(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.cam.setPos(0, -30, 0)
        self.cam.lookAt(0,0,0)

        # World
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0,0,-9.8))

        # Plane
        self.shape = BulletPlaneShape(Vec3(0,0,1), 1)
        self.node = BulletRigidBodyNode('Ground')
        self.node.addShape(self.shape)
        self.np = self.render.attachNewNode(self.node)
        self.np.setPos(0, 0, -2)
        self.planeTexture = self.loader.loadTexture("models/maps/envir-groundcover1.png")
        self.np.setTexture(self.planeTexture)
        self.world.attachRigidBody(self.node)
        
        # Box  and Materials
        
        self.material = Material()
        self.material.setShininess(5.0)
        self.material.setAmbient(VBase4(0,0,1,1))
        
        self.shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        self.node = BulletRigidBodyNode('Box')
        self.node.setMass(1.0)
        self.node.addShape(self.shape)
        self.np = self.render.attachNewNode(self.node)
        self.np.setPos(0,0,2)
        self.world.attachRigidBody(self.node)
        self.model = self.loader.loadModel('models/box.egg')
        self.model.flattenLight()
        self.model.reparentTo(self.np)
            
        
        # define the clock
        self.globalClock = ClockObject.getGlobalClock()
        
        def update(task):
            dt = self.globalClock.getDt()
            self.world.doPhysics(dt)
            return task.cont
        
        self.taskMgr.add(update, 'update')
        

MyBulletWorldInstance = MyBulletWorld()
MyBulletWorldInstance.run()