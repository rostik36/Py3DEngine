from interface.i_gui_element import *
import imgui

class GuiAbout(IGuiElement):
    def __init__(self, gui_manager, menu_bar):
        super().__init__(visible=True)
        self.gui_manager = gui_manager
        self.menu_bar = menu_bar
        self.window_name = "About"

    def render(self):
        imgui.set_next_window_size(600, 400)
        imgui.set_next_window_position(200, 100)

        _, open_state  = imgui.begin(self.window_name, True)

        if not open_state:  # If "X" is clicked, close the window
            imgui.end()
            self.gui_manager.remove_gui(self)
            return

        imgui.text("About:")
        imgui.end()
