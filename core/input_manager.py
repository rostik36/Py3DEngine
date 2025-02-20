import glfw


class InputManager:
    def __init__(self, app):
        self.app = app
        self.keys_pressed = set()  # key pressed stored here
        self.keys_released = set()  # key released stored here
        self.mouse_buttons_pressed = set()  # mouse button pressed stored here
        self.mouse_buttons_released = set()  # mouse button released stored here
        self.mouse_scrolled = False  # mouse scroll state
        self.mouse_last_x = 0  # mouse position
        self.mouse_last_y = 0  # mouse position
        self.mouse_hover_gui = False
        self.mouse_hidden = False
        self.first_mouse = True  # first time mouse entered the window
        self.ignore_mouse_callback = False  # ignore mouse callback when ImGui is active

        # Set callbacks
        glfw.set_cursor_pos_callback(self.app.window, self.mouse_callback)
        glfw.set_key_callback(self.app.window, self.key_callback)
        glfw.set_mouse_button_callback(self.app.window, self.mouse_button_callback)
        glfw.set_scroll_callback(self.app.window, self.scroll_callback)
        glfw.set_input_mode(self.app.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        
        glfw.set_cursor_pos(self.app.window, 0, 0)
        # self.last_mouse_x, self.last_mouse_y = 0, 0


    def update_camera_position(self, front, right):
        """Updates camera position based on key presses."""
        # global camera_pos
        speed = self.speed
        keys_pressed = self.keys_pressed
        
        if glfw.KEY_W in keys_pressed:
            self.app.camera_pos += speed * front
        if glfw.KEY_S in keys_pressed:
            self.app.camera_pos -= speed * front
        if glfw.KEY_A in keys_pressed:
            self.app.camera_pos -= speed * right
        if glfw.KEY_D in keys_pressed:
            self.app.camera_pos += speed * right
        if glfw.KEY_SPACE in keys_pressed:
            self.app.camera_pos[1] += speed
        if glfw.KEY_LEFT_CONTROL in keys_pressed:
            self.app.camera_pos[1] -= speed


    def scroll_callback(self, window, xoffset, yoffset):
        """Handles zooming in and out using the scroll wheel."""
        self.mouse_scrolled = True
        self.app.camera.fov -= yoffset * 2.0
        self.app.camera.fov = max(20.0, min(90.0, self.app.camera.fov))


    def mouse_callback(self, window, xpos, ypos):
        """Handles mouse movement to update yaw and pitch."""
        # global first_mouse, ignore_mouse_callback, mouse_active_camera_control
        # print("xpos: {}, ypos: {}".format(xpos, ypos))
        
        if self.app.camera.mouse_first_time_enters_the_window: # self.mouse_active_camera_control:
            # if not (self.width / 2 - 50 < xpos < self.width / 2 + 50) or not (self.height / 2 - 50 < ypos < self.height / 2 + 50):
            glfw.set_cursor_pos(window, self.app.width / 2, self.app.height / 2)
            self.mouse_first_time_enters_the_window = False
            return
        
        if self.ignore_mouse_callback:
            self.ignore_mouse_callback = False
            return
        # Prevent camera movement if ImGui is active or left mouse button isn't pressed
        if not self.mouse_active_camera_control:# or not left_mouse_pressed:
            return

        if self.first_mouse:
            self.last_mouse_x, self.last_mouse_y = xpos, ypos
            self.first_mouse = False

        x_offset = (xpos - self.last_mouse_x) * self.sensitivity
        y_offset = (self.last_mouse_y - ypos) * self.sensitivity

        # Set cursor position to center of the window
        self.last_mouse_x, self.last_mouse_y = self.width / 2, self.height / 2

        self.yaw += x_offset
        self.pitch += y_offset

        self.pitch = max(-89.0, min(89.0, self.pitch))

        if self.mouse_hidden:
            self.ignore_mouse_callback = True
            # Set cursor position to center of the window so the cursor not move in the hidden mode
            glfw.set_cursor_pos(window, self.width / 2, self.height / 2)


    def key_callback(self, window, key, scancode, action, mods):
        """Handles key press and release events."""
        # global mouse_hidden, mouse_active_camera_control

        if action == glfw.PRESS:
            self.keys_pressed.add(key)
            self.keys_released.discard(key)
            # print("p")
        elif action == glfw.RELEASE:
            self.keys_pressed.discard(key)
            self.keys_released.add(key)
            # print("r")
        elif action == glfw.REPEAT:
            # print("rr")
            return

        # Windows key (Super key) -> Show the cursor
        if glfw.KEY_LEFT_SUPER in self.keys_pressed or glfw.KEY_LEFT_ALT in self.keys_pressed:
            self.mouse_hidden = False
            self.mouse_active_camera_control = False
            glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)



    def mouse_button_callback(self, window, button, action, mods):
        """Handles mouse button clicks to enable/disable camera movement."""
        # global mouse_hidden, left_mouse_pressed, mouse_active_camera_control, last_mouse_x, last_mouse_y, already_setted_mouse_out_of_gui
        
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                if not self.mouse_hover_gui:
                    self.left_mouse_pressed = True
                    self.mouse_active_camera_control = True
                    self.last_mouse_x, self.last_mouse_y = glfw.get_cursor_pos(window)
                    
                    if not self.mouse_hidden:
                        # ray_dir = screen_to_world_ray(x, y)
                        
                        # for obj in objects:
                        #     if intersect_ray_sphere(camera_pos, ray_dir, obj):
                        #         print(f"Object selected at {obj['position']}")
                        self.mouse_hidden = True
                        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
                else:
                    self.already_setted_mouse_out_of_gui = False
            elif action == glfw.RELEASE:
                self.left_mouse_pressed = False