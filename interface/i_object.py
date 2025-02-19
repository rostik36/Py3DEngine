import glm
from core.mesh import Mesh
from core.shader import Shader
from interface.i_physics import IPhysics



class IObject:
    def __init__(self, position=(1.0,1.0, 1.0), scale=(1.0, 1.0, 1.0), 
                rotation=(0.0, 0.0, 0.0), physics=None, mesh:Mesh=None):
        self.position = glm.vec3(*position)
        self.rotation = glm.vec3(*rotation)
        self.scale = glm.vec3(*scale)
        self.physics = physics
        self.mesh = mesh
        self.visible = True

    def __init__(self, position=(1.0,1.0, 1.0), scale=(1.0, 1.0, 1.0), 
                rotation=(0.0, 0.0, 0.0), physics:IPhysics=None, shader:Shader=None, mesh:Mesh=None):
        self.position = glm.vec3(*position)
        self.rotation = glm.vec3(*rotation)
        self.scale = glm.vec3(*scale)
        self.physics = physics 
        self.shader = shader
        self.mesh = mesh
        self.visible = True

    def update(self):
        """Method to be implemented by subclasses."""
        raise NotImplementedError

    def render(self, shader: Shader=None):
        """Method to be implemented by subclasses."""
        raise NotImplementedError

