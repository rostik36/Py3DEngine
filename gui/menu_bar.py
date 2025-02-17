import os
import imgui
import core.globals
from interface.i_gui_element import *
from interface.i_scene import *
from gui.menu_bar import *
from gui.about import *
from gui.settings import *

import tkinter as tk
from tkinter import filedialog
import importlib.util
# from enum import Enum


# class MenuItem(Enum):
#     LOAD_SCENE = 1
#     CLEAR_SCENE = 2
#     AUTUMN = 3
#     WINTER = 4

class WrapperMenuItem:
    def __init__(self, text, function):
        self.text = text
        self.function = function


class GuiMenuBar(IGuiElement):
    def __init__(self, gui_manager):
        super().__init__(visible=True)
        self.gui_manager = gui_manager
        self.show_settings = False  # Track if settings window is open
        self.menus_items = {
            "File": [
                WrapperMenuItem("Load Scene", self.load_scene_function),
                WrapperMenuItem("Clear Scene", self.clear_scene_function),
                WrapperMenuItem("Settings", self.settings_function),
                WrapperMenuItem("Exit", self.exit_function)
            ],
            "View": [
                WrapperMenuItem("Grid", self.about_function),
                WrapperMenuItem("Lights", None)
            ],
            "Help": [
                WrapperMenuItem("About", self.about_function)
            ],
        }

    def render(self):
        if imgui.begin_main_menu_bar():
            for menu in self.menus_items:
                if imgui.begin_menu(menu, True):
                    for menu_item in self.menus_items[menu]:
                        clicked, _ = imgui.menu_item(menu_item.text, None, False, True)
                        if clicked:
                            menu_item.function() # call the function associated with the menu item
                    imgui.end_menu()
            imgui.end_main_menu_bar()




# def open_imgui_file_dialog():
#     ImGuiFileDialog.IGFD_Create()  # Initialize file dialog
#     ImGuiFileDialog.IGFD_OpenDialog("ChooseFileDlg", "Select a Python File", ".py", ".")

# def load_scene_from_file(file_path):
#     module_name = os.path.splitext(os.path.basename(file_path))[0]
#     spec = importlib.util.spec_from_file_location(module_name, file_path)
    
#     if spec and spec.loader:
#         module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(module)
        
#         # Find class that implements IScene
#         for name in dir(module):
#             obj = getattr(module, name)
#             if isinstance(obj, type) and issubclass(obj, IScene) and obj is not IScene:
#                 instance = obj()  # Create an instance
#                 # scene_manager.add_scene(instance)
#                 print(f"Loaded scene: {obj.__name__}")
#                 return
    
#     print("No valid scene class found.")

# def handle_file_selection():
#     if ImGuiFileDialog.IGFD_IsOk():
#         selected_file = ImGuiFileDialog.IGFD_GetFilePathName()
#         print(f"Selected file: {selected_file}")
#         load_scene_from_file(selected_file)
#     ImGuiFileDialog.IGFD_CloseDialog()


# def load_scene_function():
#     print("Load scene")
#     if imgui.button("Open Scene File"):
#         open_imgui_file_dialog()

#     # Render the file dialog
#     if ImGuiFileDialog.IGFD_Display("ChooseFileDlg"):
#         handle_file_selection()


    def load_scene_from_file(self, file_path):
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find class that implements IScene
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, type) and issubclass(obj, IScene) and obj is not IScene:
                    instance = obj()  # Create an instance
                    core.globals.scene_manager.add_scene(instance)
                    print(f"Loaded scene: {obj.__name__}")
                    return
        
        print("No valid scene class found.")

    def load_scene_function(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])

        if file_path:
            print(f"Selected file: {file_path}")
            self.load_scene_from_file(file_path)




    def clear_scene_function(self):
        print("Clear Scene")
        core.globals.scene_manager.clear()

    def exit_function(self):
        exit(0)  # Terminate the application when Exit is clicked

    def settings_function(self):
        self.gui_manager.add_gui(GuiSettings(self.gui_manager, self))

    def about_function(self):
        self.gui_manager.add_gui(GuiAbout(self.gui_manager, self))