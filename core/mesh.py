import numpy as np
import glm
from core.shader import Shader
from OpenGL.GL import *
from OpenGL.GLU import *


# TODO: may add texture coordinates  to this class and may be create interface for mesh

class Mesh:
    """Represents a 3D mesh with vertices and faces."""
    
    def __init__(self, vertices=None, indices=None, position=[0,0,0], draw_mode=GL_TRIANGLES):
        """
        Initialize a mesh.
        :param vertices: List of (x, y, z) tuples representing vertex positions.
        :param indices(faces): List of (v1, v2, v3) tuples representing triangle indices.
        """
        self.vertices = np.array(vertices, dtype=np.float32) if vertices is not None else np.array([], dtype=np.float32)
        self.indices = np.array(indices, dtype=np.int32) if indices is not None else np.array([], dtype=np.int32)
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)
        
        self.position = glm.vec3(position)
        self.model_matrix = glm.translate(glm.mat4(1.0), self.position)
        # self.model_matrix = glm.mat4(1.0)
        self.draw_mode = draw_mode  # Allow different draw modes (triangles or lines)
        self.length = len(self.indices) if draw_mode==GL_TRIANGLES else (len(self.vertices) // 6)
        
        glBindVertexArray(self.VAO)

        # Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Element Buffer Object
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        # Position attribute (3 floats)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Normal attribute (3 floats)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)


        # # Position attribute
        # glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
        # glEnableVertexAttribArray(0)

        # # Normal attribute
        # glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(12))
        # glEnableVertexAttribArray(1)

    def update_position(self, new_position):
        """Update the mesh position in the scene."""
        self.position = glm.vec3(new_position)
        self.model_matrix = glm.translate(glm.mat4(1.0), self.position)

    # def render(self):
    #     """Render the mesh using OpenGL."""
    #     pass

    def render(self, shader: Shader, material: dict):
        """Render the object using the provided shader"""
        shader.set_uniform_matrix4fv("model", self.model_matrix)
        shader.set_uniform3fv("material.ambient", material["ambient"])
        shader.set_uniform3fv("material.diffuse", material["diffuse"])
        shader.set_uniform3fv("material.specular", material["specular"])
        shader.set_uniform1f("material.shininess", material["shininess"])

        glBindVertexArray(self.VAO)
        
        if self.draw_mode == GL_TRIANGLES:
            glDrawElements(self.draw_mode, self.length, GL_UNSIGNED_INT, None)
        else:
            glDrawArrays(self.draw_mode, 0, self.length)