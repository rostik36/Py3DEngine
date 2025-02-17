import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class Mesh:
    """Represents a 3D mesh with vertices and faces."""
    
    def __init__(self, vertices=None, faces=None):
        """
        Initialize a mesh.
        :param vertices: List of (x, y, z) tuples representing vertex positions.
        :param faces: List of (v1, v2, v3) tuples representing triangle indices.
        """
        self.vertices = np.array(vertices, dtype=np.float32) if vertices is not None else np.array([], dtype=np.float32)
        self.faces = np.array(faces, dtype=np.int32) if faces is not None else np.array([], dtype=np.int32)
        self.vao = self.vbo = self.ebo = None

    def setup_gl(self):
        """Setup OpenGL buffers."""
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Vertex Buffer Object
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Element Buffer Object
        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.faces.nbytes, self.faces, GL_STATIC_DRAW)

        # Vertex Attribute (position)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, None)

        glBindVertexArray(0)  # Unbind VAO

    def draw(self):
        """Render the mesh using OpenGL."""
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.faces) * 3, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)



# class Mesh:
#     """Represents a 3D mesh with vertices and faces."""
    
#     def __init__(self, vertices=None, faces=None):
#         """
#         Initialize a mesh.
#         :param vertices: List of (x, y, z) tuples representing vertex positions.
#         :param faces: List of (v1, v2, v3) tuples representing triangle indices.
#         """
#         self.vertices = np.array(vertices, dtype=np.float32) if vertices else np.array([])
#         self.faces = np.array(faces, dtype=np.int32) if faces else np.array([])

#     def render(self):
#         """Draws the mesh using OpenGL."""
#         glPushMatrix()
#         glTranslatef(*self.position)  # Move object to its position
#         glRotatef(self.rotation[0], 1, 0, 0)  # Rotate around X-axis
#         glRotatef(self.rotation[1], 0, 1, 0)  # Rotate around Y-axis
#         glRotatef(self.rotation[2], 0, 0, 1)  # Rotate around Z-axis
#         glScalef(self.scale, self.scale, self.scale)  # Scale the object down
#         self.draw_model()  # Render the model
#         glPopMatrix()


#     def draw_model(self):
#         """Draws a 3D model from its vertex data."""
#         glBegin(GL_TRIANGLES)
#         for face in self.faces:
#             for index in face:
#                 glVertex3f(*self.vertices[index])  # Use each vertex index
#         glEnd()

#     def add_vertices(self, vertices):
#         """Adds a list of vertices (x, y, z) to the mesh."""
#         self.vertices = np.concatenate((self.vertices, vertices), axis=0)

#     def add_vertex(self, vertex):
#         """Adds a single vertex (x, y, z) to the mesh."""
#         self.vertices = np.append(self.vertices, [vertex], axis=0)

#     def add_face(self, face):
#         """Adds a face (triangle) defined by three vertex indices."""
#         self.faces = np.append(self.faces, [face], axis=0)

#     def __repr__(self):
#         return f"Mesh(vertices={len(self.vertices)}, faces={len(self.faces)})"
