import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import imgui
from imgui.integrations.glfw import GlfwRenderer

import core.globals
from gui_manager import GuiManager
from shader import Shader
from callbacks import *
from gui import *
from load_object import load_object_from_file

from objects.grid import Grid




class Engine:
    def __init__(self):
        self.window = None
        self.shader = None
        self.grid = None
        pass

    def init(self):
        if not glfw.init():
            return -1
        self.window = glfw.create_window(core.globals.width, core.globals.height, "Py3DEngine", None, None)
        if not self.window:
            glfw.terminate()
            return -1

        glfw.make_context_current(self.window)
        # ✅ Ensure correct OpenGL settings
        glEnable(GL_DEPTH_TEST)  # ✅ Enable depth test
        glDepthFunc(GL_LESS)     # ✅ Accept fragments closer to the camera
        # glEnable(GL_CULL_FACE)   # ✅ Cull back faces (performance boost)
        # glCullFace(GL_BACK)
        glDisable(GL_CULL_FACE)  # Disable face culling for testing
        glDepthMask(GL_TRUE)     # ✅ Ensure depth writing is enabled
        
        # Create Shader Program (can be created after the window only)
        self.shader = Shader("shaders/basic_shader.glsl", "shaders/basic_fragment.glsl")
        core.globals.shader = self.shader
        # print(self.shader)
        # print(core.globals.shader)

        imgui.create_context()
        self.impl = GlfwRenderer(self.window)
        
        # Set callbacks
        glfw.set_cursor_pos_callback(self.window, mouse_callback)
        glfw.set_key_callback(self.window, key_callback)
        glfw.set_mouse_button_callback(self.window, mouse_button_callback)
        glfw.set_scroll_callback(self.window, scroll_callback)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        
        glfw.set_cursor_pos(self.window, 0, 0)
        core.globals.last_mouse_x, core.globals.last_mouse_y = 0, 0
        init_lighting()

        # add gui elements
        core.globals.gui_manager.add_gui(GuiMenuBar(core.globals.gui_manager))
        core.globals.gui_manager.add_gui(GuiLightsSettings("Window 1"))
        
        self.grid = Grid()
        
        return 0


    def run(self):
        while not glfw.window_should_close(self.window):
            # 1️⃣ Poll window events (keyboard, mouse, etc.)
            glfw.poll_events()

            # 2️⃣ Process ImGui inputs
            self.impl.process_inputs()
            
            # 3️⃣ Dynamically update cursor visibility
            update_cursor_state(self.window) 

            # 4️⃣ Update physics (object positions, velocities, etc.)
            # physics_manager.update()

            # 5️⃣ Update lighting position from GUI controls
            update_lighting()

            # 6️⃣ Clear buffers before drawing the next frame
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Update logic
            dt = glfw.get_time()


            # Calculate camera vectors once per frame
            front, right = calculate_camera_vectors()

            # Update camera position using precomputed vectors
            update_camera_position(front, right)

            # Update view matrix dynamically
            target = core.globals.camera_pos + front  # Update target position
            # Update the view matrix
            core.globals.view_matrix = glm.lookAt(
                core.globals.camera_pos,  # Camera position
                target,  # Where the camera is looking
                glm.vec3(0, 1, 0)  # Up vector (Y-axis)
            )
            
            if core.globals.mouse_scrolled:
                # update camera FOV
                core.globals.projection_matrix = glm.perspective(glm.radians(core.globals.fov), core.globals.width / core.globals.height, core.globals.zNear, core.globals.zFar)
    

            # 9️⃣ Render Scene Objects
            core.globals.shader.use()

            core.globals.shader.set_uniform_matrix4fv("view", core.globals.view_matrix)
            core.globals.shader.set_uniform_matrix4fv("projection", core.globals.projection_matrix)
            core.globals.shader.set_uniform3fv("viewPos", core.globals.camera_pos)

            # Set global sunlight
            
            if core.globals.sun_light_updated:
                print("Updating sunlight direction and color...")
                core.globals.sun_light_updated = False
                self.shader.set_uniform3fv("sunlight.direction", glm.normalize(glm.vec3(-1.0, -1.0, -1.0)))
                self.shader.set_uniform3fv("sunlight.color", glm.vec3(1.0, 1.0, 1.0))
            
            # glDisable(GL_DEPTH_TEST)
            # glDisable(GL_BLEND)
            self.grid.render(self.shader)
            # glEnable(GL_DEPTH_TEST)
            # glEnable(GL_BLEND)
            
            # render_scene()
            core.globals.scene_manager.update_all()  # Update all scene objects
            core.globals.scene_manager.render_all()  # Render all scene objects

            # 🔟 Render ImGui UI (sliders, controls, etc.)
            imgui.new_frame()
            core.globals.gui_manager.render_all()
            imgui.render()
            self.impl.render(imgui.get_draw_data())

            # 1️⃣1️⃣ Swap buffers to display frame
            glfw.swap_buffers(self.window)

        self.impl.shutdown()
        glfw.terminate()



# def app():
#     if not glfw.init():
#         return -1
#     window = glfw.create_window(core.globals.width, core.globals.height, "3D Trajectory Simulation", None, None)
#     if not window:
#         glfw.terminate()
#         return -1

#     # imgui.create_context()
#     # impl = GlfwRenderer(window)

#     # Set callbacks
#     glfw.set_cursor_pos_callback(window, mouse_callback)
#     glfw.set_key_callback(window, key_callback)
#     glfw.set_mouse_button_callback(window, mouse_button_callback)
#     glfw.set_scroll_callback(window, scroll_callback)
#     glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    
#     # glfw.set_cursor_pos(window, 0, 0)
#     core.globals.last_mouse_x, core.globals.last_mouse_y = 0, 0
#     # init_lighting()
    
    
#     # load_object_from_file(missle_file_path, 0.1, (0, 90, 0))
#     # core.globals.scene_objects.append(Ci
    
#     # add gui elements
#     # core.globals.gui_manager.add_gui(GuiMenuBar(core.globals.gui_manager))
#     # core.globals.gui_manager.add_gui(GuiLightsSettings("Window 1"))
    
    

#     while not glfw.window_should_close(window):
#         # 1️⃣ Poll window events (keyboard, mouse, etc.)
#         glfw.poll_events()

#         # 2️⃣ Process ImGui inputs
#         # impl.process_inputs()

#         # 3️⃣ Update physics (object positions, velocities, etc.)
#         # physics_manager.update()

#         # 4️⃣ Update lighting position from GUI controls
#         # update_lighting()
        
#         # Dynamically update cursor visibility
#         update_cursor_state(window) 
        
#         # 5️⃣ Update camera transformation (handle WASD movement)
#         # update_camera_position()

#         # 6️⃣ Clear buffers before drawing the next frame
#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


#         # Update logic
#         dt = glfw.get_time()


#         # 9️⃣ Render Scene Objects
#         core.globals.shader.use()
#         core.globals.shader.set_uniform_matrix4fv("view", core.globals.view_matrix)
#         core.globals.shader.set_uniform_matrix4fv("projection", core.globals.projection_matrix)
#         # draw_grid()
#         # render_scene()  
#         core.globals.scene_manager.update_all()  # Update all scene objects
#         core.globals.scene_manager.render_all()  # Render all scene objects

#         # 🔟 Render ImGui UI (sliders, controls, etc.)
#         # imgui.new_frame()
#         # core.globals.gui_manager.render_all()
#         # imgui.render()
#         # impl.render(imgui.get_draw_data())

#         # 1️⃣1️⃣ Swap buffers to display frame
#         glfw.swap_buffers(window)

#     impl.shutdown()
#     glfw.terminate()