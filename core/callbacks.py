import numpy as np
import glfw
import glm
from OpenGL.GL import *
from OpenGL.GLU import *
import core.globals
import imgui
from imgui.integrations.glfw import GlfwRenderer

import math



grid_size_half = int(core.globals.grid_size/2)

def get_window_center(window):
    """Gets the absolute screen position of the center of the application window."""
    window_x, window_y = glfw.get_window_pos(window)
    center_x = window_x + core.globals.width / 2
    center_y = window_y + core.globals.height / 2
    return center_x, center_y


def init_lighting():
    """Sets up basic OpenGL lighting with configurable intensity."""
    glEnable(GL_LIGHTING)  # Enable lighting
    glEnable(GL_LIGHT0)    # Enable light source 0
    glEnable(GL_COLOR_MATERIAL)  # Allow object colors to interact with light

    # Light color and intensity (R, G, B, Strength)
    core.globals.light_ambient = [0.2, 0.2, 0.2, 1.0]  # Soft ambient light
    core.globals.light_diffuse = [0.8, 0.8, 0.8, 1.0]  # Brighter diffuse light
    core.globals.light_specular = [1.0, 1.0, 1.0, 1.0]  # Shiny specular highlights

    # Apply light properties
    glLightfv(GL_LIGHT0, GL_POSITION, core.globals.light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, core.globals.light_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, core.globals.light_diffuse)
    glLightfv(GL_LIGHT2, GL_SPECULAR, core.globals.light_specular)

    # Enable depth testing for proper 3D rendering
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)  # Normalize normals for correct lighting


def update_lighting():
    """Updates the light color, intensity, and position dynamically."""

    # Multiply colors by intensity
    core.globals.scaled_ambient = [c * core.globals.light_intensity for c in core.globals.light_ambient] + [1.0]
    core.globals.scaled_diffuse = [c * core.globals.light_intensity for c in core.globals.light_diffuse] + [1.0]
    core.globals.scaled_specular = [c * core.globals.light_intensity for c in core.globals.light_specular] + [1.0]

    # Apply updated lighting properties
    glLightfv(GL_LIGHT0, GL_AMBIENT, core.globals.scaled_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, core.globals.scaled_diffuse)
    glLightfv(GL_LIGHT2, GL_SPECULAR, core.globals.scaled_specular)



# Function to recalculate the camera vectors
def calculate_camera_vectors():
    """Calculates front and right vectors based on yaw and pitch."""
    front = glm.vec3(
        math.cos(math.radians(core.globals.yaw)) * math.cos(math.radians(core.globals.pitch)),
        math.sin(math.radians(core.globals.pitch)),
        math.sin(math.radians(core.globals.yaw)) * math.cos(math.radians(core.globals.pitch))
    )
    front = glm.normalize(front)  # Normalize the front vector

    up = glm.vec3(0.0, 1.0, 0.0)
    right = glm.normalize(glm.cross(front, up))  # Right vector

    return front, right



def update_camera_position(front, right):
    """Updates camera position based on key presses."""
    # global camera_pos
    speed = core.globals.speed
    keys_pressed = core.globals.keys_pressed
    
    if glfw.KEY_W in keys_pressed:
        core.globals.camera_pos += speed * front
    if glfw.KEY_S in keys_pressed:
        core.globals.camera_pos -= speed * front
    if glfw.KEY_A in keys_pressed:
        core.globals.camera_pos -= speed * right
    if glfw.KEY_D in keys_pressed:
        core.globals.camera_pos += speed * right
    if glfw.KEY_SPACE in keys_pressed:
        core.globals.camera_pos[1] += speed
    if glfw.KEY_LEFT_CONTROL in keys_pressed:
        core.globals.camera_pos[1] -= speed


def scroll_callback(window, xoffset, yoffset):
    """Handles zooming in and out using the scroll wheel."""
    core.globals.mouse_scrolled = True
    core.globals.fov -= yoffset * 2.0
    core.globals.fov = max(20.0, min(90.0, core.globals.fov))


def mouse_callback(window, xpos, ypos):
    """Handles mouse movement to update yaw and pitch."""
    # global first_mouse, ignore_mouse_callback, mouse_active_camera_control
    # print("xpos: {}, ypos: {}".format(xpos, ypos))
    
    if core.globals.mouse_first_time_enters_the_window: # core.globals.mouse_active_camera_control:
        # if not (core.globals.width / 2 - 50 < xpos < core.globals.width / 2 + 50) or not (core.globals.height / 2 - 50 < ypos < core.globals.height / 2 + 50):
        glfw.set_cursor_pos(window, core.globals.width / 2, core.globals.height / 2)
        core.globals.mouse_first_time_enters_the_window = False
        return
    
    if core.globals.ignore_mouse_callback:
        core.globals.ignore_mouse_callback = False
        return
    # Prevent camera movement if ImGui is active or left mouse button isn't pressed
    if not core.globals.mouse_active_camera_control:# or not left_mouse_pressed:
        return

    if core.globals.first_mouse:
        core.globals.last_mouse_x, core.globals.last_mouse_y = xpos, ypos
        core.globals.first_mouse = False

    x_offset = (xpos - core.globals.last_mouse_x) * core.globals.sensitivity
    y_offset = (core.globals.last_mouse_y - ypos) * core.globals.sensitivity

    # Set cursor position to center of the window
    core.globals.last_mouse_x, core.globals.last_mouse_y = core.globals.width / 2, core.globals.height / 2

    core.globals.yaw += x_offset
    core.globals.pitch += y_offset

    core.globals.pitch = max(-89.0, min(89.0, core.globals.pitch))

    if core.globals.mouse_hidden:
        core.globals.ignore_mouse_callback = True
        # Set cursor position to center of the window so the cursor not move in the hidden mode
        glfw.set_cursor_pos(window, core.globals.width / 2, core.globals.height / 2)


def key_callback(window, key, scancode, action, mods):
    """Handles key press and release events."""
    # global mouse_hidden, mouse_active_camera_control

    if action == glfw.PRESS:
        core.globals.keys_pressed.add(key)
        core.globals.keys_released.discard(key)
        # print("p")
    elif action == glfw.RELEASE:
        core.globals.keys_pressed.discard(key)
        core.globals.keys_released.add(key)
        # print("r")
    elif action == glfw.REPEAT:
        # print("rr")
        return

    # Windows key (Super key) -> Show the cursor
    if glfw.KEY_LEFT_SUPER in core.globals.keys_pressed or glfw.KEY_LEFT_ALT in core.globals.keys_pressed:
        core.globals.mouse_hidden = False
        core.globals.mouse_active_camera_control = False
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)

    # if glfw.KEY_O in core.globals.keys_pressed and glfw.KEY_O not in core.globals.keys_released:
    #     # Instantly retrieve and modify visibility by class
    #     gui_element = core.globals.gui_manager.get_gui_by_class(GuiLightsSettings)
    #     if gui_element:
    #         gui_element.visible = not gui_element.visible  # Toggle visibility




# # Ray-sphere intersection check
# def intersect_ray_sphere(ray_origin, ray_dir, sphere):
#     L = sphere["position"] - ray_origin
#     tca = glm.dot(L, ray_dir)
#     d2 = glm.dot(L, L) - tca * tca
#     return d2 <= sphere["radius"] * sphere["radius"]

# # Converts screen space coordinates to normalized device coordinates
# def screen_to_world_ray(mouse_x, mouse_y):
#     # Convert screen coordinates to normalized device coordinates (NDC)
#     x = (2.0 * mouse_x) / window_width - 1.0
#     y = 1.0 - (2.0 * mouse_y) / window_height  # Flip Y axis for OpenGL
#     z = 1.0  # Assume the ray starts at the far plane
    
#     # Convert to homogeneous clip coordinates
#     ray_clip = glm.vec4(x, y, -1.0, 1.0)
    
#     # Transform to eye space
#     ray_eye = glm.inverse(projection_matrix) * ray_clip
#     ray_eye = glm.vec4(ray_eye.x, ray_eye.y, -1.0, 0.0)  # Keep direction
    
#     # Transform to world space
#     ray_world = glm.vec3(glm.inverse(view_matrix) * ray_eye)
#     ray_world = glm.normalize(ray_world)
    
#     return ray_world



def mouse_button_callback(window, button, action, mods):
    """Handles mouse button clicks to enable/disable camera movement."""
    # global mouse_hidden, left_mouse_pressed, mouse_active_camera_control, last_mouse_x, last_mouse_y, already_setted_mouse_out_of_gui
    
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            if not core.globals.mouse_hover_gui:
                core.globals.left_mouse_pressed = True
                core.globals.mouse_active_camera_control = True
                core.globals.last_mouse_x, core.globals.last_mouse_y = glfw.get_cursor_pos(window)
                
                if not core.globals.mouse_hidden:
                    # ray_dir = screen_to_world_ray(x, y)
                    
                    # for obj in objects:
                    #     if intersect_ray_sphere(camera_pos, ray_dir, obj):
                    #         print(f"Object selected at {obj['position']}")
                    core.globals.mouse_hidden = True
                    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
            else:
                core.globals.already_setted_mouse_out_of_gui = False
        elif action == glfw.RELEASE:
            core.globals.left_mouse_pressed = False


def update_cursor_state(window):
    """Dynamically show or hide the cursor based on ImGui interaction."""
    # global mouse_hidden, mouse_hover_gui, already_setted_mouse_out_of_gui, mouse_active_camera_control

    if not core.globals.mouse_active_camera_control:
        if imgui.get_io().want_capture_mouse:
            # print("on gui")
            core.globals.mouse_hidden = False
            core.globals.mouse_hover_gui = True
            core.globals.already_setted_mouse_out_of_gui = False
        elif not core.globals.already_setted_mouse_out_of_gui:
            # print("out of gui 1")
            core.globals.mouse_hover_gui = False
            core.globals.already_setted_mouse_out_of_gui = True

def render_scene():
    """Renders all loaded objects in the scene."""
    for obj in core.globals.scene_objects:
        obj.update()  # update the object

    for obj in core.globals.scene_objects:
        obj.draw()  # Render the object