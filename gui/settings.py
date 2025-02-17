from interface.i_gui_element import *
import imgui
import glm
import core.globals as globals

class GuiSettings(IGuiElement):
    def __init__(self, gui_manager, menu_bar):
        super().__init__(visible=True)
        self.gui_manager = gui_manager
        self.menu_bar = menu_bar
        self.window_name = "Settings"
        self.selected_option = "General"  # Default selected option
        self.options = ["General", "Appearance", "Lights", "Controls", "Advanced"]

    def render(self):
        imgui.set_next_window_size(600, 400)
        imgui.set_next_window_position(200, 100)

        _, open_state  = imgui.begin(self.window_name, True)

        if not open_state:  # If "X" is clicked, close the window
            imgui.end()
            self.gui_manager.remove_gui(self)
            return
        
        # Create a two-column layout
        imgui.columns(2, border=True)

        # Left Side: Sidebar with menu options
        for option in self.options:
            clicked, _ = imgui.selectable(option, self.selected_option == option)
            if clicked:
                self.selected_option = option

        imgui.next_column()

        # Right Side: Display settings based on selection
        if self.selected_option == "General":
            imgui.text("General Settings")
            _, value = imgui.checkbox("Enable Feature X", True)
        elif self.selected_option == "Appearance":
            imgui.text("Appearance Settings")
            _, color = imgui.color_edit3("Background Color", 1.0, 1.0, 1.0)
        elif self.selected_option == "Lights":
            self.lights_settings()
        elif self.selected_option == "Controls":
            imgui.text("Control Settings")
            _, key = imgui.input_text("Shortcut Key", "Ctrl+X", 256)
        elif self.selected_option == "Advanced":
            imgui.text("Advanced Settings")
            _, value = imgui.slider_float("Threshold", 0.5, 0.0, 1.0)

        imgui.columns(1)
        imgui.end()


    def lights_settings(self):
        imgui.text("Lights Settings")
        # Control sun light
        updated, sun_light_color = imgui.color_edit3("Sun light color", globals.sun_light_color[0],globals.sun_light_color[1], globals.sun_light_color[2])
        if updated:
            globals.sun_light_updated = True
            globals.sun_light_color = glm.vec3(sun_light_color[0], sun_light_color[1], sun_light_color[2])
            
        # Control diffuse light (main lighting effect)
        _, globals.light_diffuse[0] = imgui.slider_float("Diffuse R", globals.light_diffuse[0], 0.0, 1.0)
        _, globals.light_diffuse[1] = imgui.slider_float("Diffuse G", globals.light_diffuse[1], 0.0, 1.0)
        _, globals.light_diffuse[2] = imgui.slider_float("Diffuse B", globals.light_diffuse[2], 0.0, 1.0)

        # Control specular light (shiny highlights)
        _, globals.light_specular[0] = imgui.slider_float("Specular R", globals.light_specular[0], 0.0, 1.0)
        _, globals.light_specular[1] = imgui.slider_float("Specular G", globals.light_specular[1], 0.0, 1.0)
        _, globals.light_specular[2] = imgui.slider_float("Specular B", globals.light_specular[2], 0.0, 1.0)

        
        # Control ambient light (soft background lighting)
        _, globals.light_ambient[0] = imgui.slider_float("Ambient R", globals.light_ambient[0], 0.0, 1.0)
        _, globals.light_ambient[1] = imgui.slider_float("Ambient G", globals.light_ambient[1], 0.0, 1.0)
        _, globals.light_ambient[2] = imgui.slider_float("Ambient B", globals.light_ambient[2], 0.0, 1.0)

        # Control diffuse light (main lighting effect)
        _, globals.light_diffuse[0] = imgui.slider_float("Diffuse R", globals.light_diffuse[0], 0.0, 1.0)
        _, globals.light_diffuse[1] = imgui.slider_float("Diffuse G", globals.light_diffuse[1], 0.0, 1.0)
        _, globals.light_diffuse[2] = imgui.slider_float("Diffuse B", globals.light_diffuse[2], 0.0, 1.0)

        # Control specular light (shiny highlights)
        _, globals.light_specular[0] = imgui.slider_float("Specular R", globals.light_specular[0], 0.0, 1.0)
        _, globals.light_specular[1] = imgui.slider_float("Specular G", globals.light_specular[1], 0.0, 1.0)
        _, globals.light_specular[2] = imgui.slider_float("Specular B", globals.light_specular[2], 0.0, 1.0)

        # Control overall light intensity
        _, globals.light_intensity = imgui.slider_float("Light Strength", globals.light_intensity, 0.1, 20.0)
