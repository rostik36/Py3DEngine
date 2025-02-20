from globals import *
# from core.view_frustum import Frustum


class Camera:
    def __init__(self, position, yaw, pitch):
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

        # self.frustum = Frustum(self)


# Calculate camera vectors once per frame
            # front, right = calculate_camera_vectors()

            # # Update camera position using precomputed vectors
            # update_camera_position(front, right)

            # # Update view matrix dynamically
            # target = core.globals.camera_pos + front  # Update target position
            # # Update the view matrix
            # core.globals.view_matrix = glm.lookAt(
            #     core.globals.camera_pos,  # Camera position
            #     target,  # Where the camera is looking
            #     glm.vec3(0, 1, 0)  # Up vector (Y-axis)
            # )


# Function to recalculate the camera vectors
# def calculate_camera_vectors():
#     """Calculates front and right vectors based on yaw and pitch."""
#     front = glm.vec3(
#         math.cos(math.radians(core.globals.yaw)) * math.cos(math.radians(core.globals.pitch)),
#         math.sin(math.radians(core.globals.pitch)),
#         math.sin(math.radians(core.globals.yaw)) * math.cos(math.radians(core.globals.pitch))
#     )
#     front = glm.normalize(front)  # Normalize the front vector

#     up = glm.vec3(0.0, 1.0, 0.0)
#     right = glm.normalize(glm.cross(front, up))  # Right vector

#     return front, right

    def update(self):
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y):
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x

    def move_left(self, velocity):
        self.position -= self.right * velocity

    def move_right(self, velocity):
        self.position += self.right * velocity

    def move_up(self, velocity):
        self.position += self.up * velocity

    def move_down(self, velocity):
        self.position -= self.up * velocity

    def move_forward(self, velocity):
        self.position += self.forward * velocity

    def move_back(self, velocity):
        self.position -= self.forward * velocity
