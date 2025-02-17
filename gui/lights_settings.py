from interface.i_gui_element import *
import core.globals as globals


class GuiLightsSettings(IGuiElement):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.open = False


    def render(self):
        pass
        # flags = imgui.WINDOW_NO_COLLAPSE # Prevent minimization
        # imgui.begin("Lighting Controls", False, flags)

        # # Control ambient light (soft background lighting)
        # _, globals.light_ambient[0] = imgui.slider_float("Ambient R", globals.light_ambient[0], 0.0, 1.0)
        # _, globals.light_ambient[1] = imgui.slider_float("Ambient G", globals.light_ambient[1], 0.0, 1.0)
        # _, globals.light_ambient[2] = imgui.slider_float("Ambient B", globals.light_ambient[2], 0.0, 1.0)

        # # Control diffuse light (main lighting effect)
        # _, globals.light_diffuse[0] = imgui.slider_float("Diffuse R", globals.light_diffuse[0], 0.0, 1.0)
        # _, globals.light_diffuse[1] = imgui.slider_float("Diffuse G", globals.light_diffuse[1], 0.0, 1.0)
        # _, globals.light_diffuse[2] = imgui.slider_float("Diffuse B", globals.light_diffuse[2], 0.0, 1.0)

        # # Control specular light (shiny highlights)
        # _, globals.light_specular[0] = imgui.slider_float("Specular R", globals.light_specular[0], 0.0, 1.0)
        # _, globals.light_specular[1] = imgui.slider_float("Specular G", globals.light_specular[1], 0.0, 1.0)
        # _, globals.light_specular[2] = imgui.slider_float("Specular B", globals.light_specular[2], 0.0, 1.0)

        # # Control overall light intensity
        # _, globals.light_intensity = imgui.slider_float("Light Strength", globals.light_intensity, 0.1, 5.0)

        # imgui.end()