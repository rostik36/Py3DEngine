import numpy as np
import math
import glm
# from gui_manager import GuiManager
# from scene_manager import SceneManager
from shader import *


#####################################################################
# Window and Camera settings
#####################################################################
width, height = 1400, 800
speed = 1
sensitivity = 0.2
fov = 45.0
zNear = 0.1
zFar = 150.0


#####################################################################
# Light settings
#####################################################################
sun_light_updated = False
sun_light_color = glm.vec3(1.0, 1.0, 1.0)

light_position = [10.0, 10.0, 10.0]  # Position of the light source
# Light color variables
light_ambient = [0.2, 0.2, 0.2]
light_diffuse = [0.8, 0.8, 0.8]
light_specular = [1.0, 1.0, 1.0]
light_intensity = 10.0  # Light brightness multiplier

# Light color and intensity (R, G, B, Strength)
light_ambient = [0.2, 0.2, 0.2, 1.0]  # Soft ambient light
light_diffuse = [0.8, 0.8, 0.8, 1.0]  # Brighter diffuse light
light_specular = [1.0, 1.0, 1.0, 1.0]  # Shiny specular highlights

# ambient light - Soft background light that fills the entire scene. Not directional (it comes from everywhere)
# diffuse light - Main light source that simulates sunlight or lamps. Directional—affects surfaces facing the light source.
# specular highlights - Creates shiny reflections on glossy surfaces. Depends on camera position (highlights move as you move the camera).



#####################################################################
# mouse settings
#####################################################################
left_mouse_pressed = False  # Track left mouse button press
last_mouse_x, last_mouse_y = width / 2, height / 2
first_mouse = True
mouse_hidden = True  # Track mouse visibility state
mouse_active_camera_control = True
mouse_hover_gui = False  # mouse on top of gui
already_setted_mouse_out_of_gui = True
ignore_mouse_callback = False  # ignore mouse callback when ImGui is active
mouse_first_time_enters_the_window = True

mouse_scrolled = False  # Track mouse scroll state

#####################################################################
# Keyboard settings
#####################################################################
keys_pressed = set() # key pressed stored here
keys_released = set() # key released stored here




#####################################################################
# Grid settings
#####################################################################
grid_size = 100



####################################################################
# scene setting
####################################################################


shader = None


# Set up projection matrix
projection_matrix = glm.perspective(glm.radians(fov), width / height, zNear, zFar)

# Camera setup
camera_pos = glm.vec3(20.0, 50.0, 20.0)
target = glm.vec3(0.0, 0.0, 0.0)
# Compute direction vector
direction = glm.normalize(target - camera_pos)

# Compute yaw and pitch
yaw = math.degrees(math.atan2(direction.z, direction.x))  # Yaw (rotation around Y-axis)
pitch = math.degrees(math.asin(direction.y))  # Pitch (rotation around X-axis)

view_matrix = glm.lookAt(camera_pos, glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))



scene_update_needed = False

scene_objects = []





# from numba import njit
import numpy as np
import glm
import math

# OpenGL settings
MAJOR_VER, MINOR_VER = 3, 3
DEPTH_SIZE = 24
NUM_SAMPLES = 1  # antialiasing

# resolution
WIN_RES = glm.vec2(1600, 900)

# world generation
SEED = 16

# ray casting
MAX_RAY_DIST = 6

# chunk
CHUNK_SIZE = 48
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE
CHUNK_SPHERE_RADIUS = H_CHUNK_SIZE * math.sqrt(3)

# world
WORLD_W, WORLD_H = 20, 2
WORLD_D = WORLD_W
WORLD_AREA = WORLD_W * WORLD_D
WORLD_VOL = WORLD_AREA * WORLD_H

# world center
CENTER_XZ = WORLD_W * H_CHUNK_SIZE
CENTER_Y = WORLD_H * H_CHUNK_SIZE

# camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG)  # vertical FOV
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # horizontal FOV
NEAR = 0.1
FAR = 200.0
PITCH_MAX = glm.radians(89)

# player
PLAYER_SPEED = 0.005
PLAYER_ROT_SPEED = 0.003
# PLAYER_POS = glm.vec3(CENTER_XZ, WORLD_H * CHUNK_SIZE, CENTER_XZ)
PLAYER_POS = glm.vec3(CENTER_XZ, CHUNK_SIZE, CENTER_XZ)
MOUSE_SENSITIVITY = 0.002

# colors
BG_COLOR = glm.vec3(0.58, 0.83, 0.99)

# textures
SAND = 1
GRASS = 2
DIRT = 3
STONE = 4
SNOW = 5
LEAVES = 6
WOOD = 7

# terrain levels
SNOW_LVL = 54
STONE_LVL = 49
DIRT_LVL = 40
GRASS_LVL = 8
SAND_LVL = 7

# tree settings
TREE_PROBABILITY = 0.02
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2

# water
WATER_LINE = 5.6
WATER_AREA = 5 * CHUNK_SIZE * WORLD_W

# cloud
CLOUD_SCALE = 25
CLOUD_HEIGHT = WORLD_H * CHUNK_SIZE * 2