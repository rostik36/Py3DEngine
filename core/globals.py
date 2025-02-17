import numpy as np
import math
import glm
from gui_manager import GuiManager
from scene_manager import SceneManager
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
scene_manager = SceneManager()
# Create a GUI manager and add GUI elements
gui_manager = GuiManager()

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