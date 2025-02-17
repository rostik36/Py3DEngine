import pyassimp
# from OpenGL.GL import *
# from OpenGL.GLU import *

# import core.globals
from core.mesh import *



# class Object(IObject):
#     """Represents an object loaded from a file."""
#     def __init__(self, vertices, faces, position=(0, 0, 0), scale=0.01, rotation=(0, 0, 0)):
#         super().__init__(position=position, scale=scale, rotation=rotation)  # Call parent constructor
#         self.vertices = vertices  # List of vertex positions
#         self.faces = faces  # List of faces (indices)

#     def draw(self):
#         """Draws the object using OpenGL."""
#         glPushMatrix()
#         glTranslatef(*self.position)  # Move object to its position
#         glRotatef(self.rotation[0], 1, 0, 0)  # Rotate around X-axis
#         glRotatef(self.rotation[1], 0, 1, 0)  # Rotate around Y-axis
#         glRotatef(self.rotation[2], 0, 0, 1)  # Rotate around Z-axis
#         glScalef(self.scale, self.scale, self.scale)  # Scale the object down
#         self.draw_model()  # Render the model
#         glPopMatrix()
#         # print(self.vertices)


#     def draw_model(self):
#         """Draws a 3D model from its vertex data."""
#         glBegin(GL_TRIANGLES)
#         for face in self.faces:
#             for index in face:
#                 glVertex3f(*self.vertices[index])  # Use each vertex index
#         glEnd()


#     def update(self):
#         """Updates the object's position, rotation, and scale."""
#         # Update object's position, rotation, and scale here
#         pass


def load_object_from_file(file_path, scale, rotation):
    """Loads a 3D object from a file and stores its vertices & faces."""
    try:
        with pyassimp.load(file_path) as scene:  # ✅ Use 'with' to avoid context manager errors
            for mesh in scene.meshes:
                vertices = mesh.vertices.tolist()
                faces = mesh.faces.tolist()
                print(f"Loaded {len(vertices)} vertices and {len(faces)} faces from {file_path}")
                return Mesh(vertices, faces)
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")