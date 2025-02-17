import glm
from core.mesh import Mesh
from core.shader import Shader

class IObject:
    def __init__(self, position=(1.0,1.0, 1.0), scale=(1.0, 1.0, 1.0), 
                rotation=(0.0, 0.0, 0.0), physics=False, mass=1.0, mesh=Mesh()):
        self.position = glm.vec3(*position)
        self.rotation = glm.vec3(*rotation)
        self.scale = glm.vec3(*scale)
        self.physics = physics
        self.mass = mass
        self.mesh = mesh


    def update(self):
        """Method to be implemented by subclasses."""
        raise NotImplementedError

    def render(self):
        """Method to be implemented by subclasses."""
        raise NotImplementedError

    def render(self, shader: Shader):
        """Method to be implemented by subclasses."""
        raise NotImplementedError

