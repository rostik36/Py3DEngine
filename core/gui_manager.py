from collections import defaultdict

class GuiManager:
    def __init__(self):
        self.gui_by_class = defaultdict(list)
        self.gui_by_name = {}
        self.to_add = []
        self.to_remove = []

    def add_gui(self, gui_element):
        """Queue new GUI elements to be added after the current frame."""
        self.to_add.append(gui_element)

    def remove_gui(self, gui_element):
        """Queue GUI elements for removal."""
        self.to_remove.append(gui_element)

    def render_all(self):
        """Draws GUI elements safely by processing queued additions/removals after each frame."""
        
        # Process pending removals
        for gui in self.to_remove:
            if gui.__class__ in self.gui_by_class and gui in self.gui_by_class[gui.__class__]:
                self.gui_by_class[gui.__class__].remove(gui)
            if hasattr(gui, "window_name") and gui.window_name in self.gui_by_name:
                del self.gui_by_name[gui.window_name]
        self.to_remove.clear()

        # Draw existing elements
        for gui_list in list(self.gui_by_class.values()):  # ✅ Safe copy
            for gui in gui_list:
                if gui.visible:
                    gui.render()

        # Process pending additions
        for gui in self.to_add:
            self.gui_by_class[gui.__class__].append(gui)
            if hasattr(gui, "window_name"):
                self.gui_by_name[gui.window_name] = gui
        self.to_add.clear()





# class GuiManager:
#     def __init__(self):
#         # self.guis = []  # List to maintain drawing order
#         self.gui_by_class = {}  # Dictionary to store by class
#         self.gui_by_name = {}  # Dictionary to store by name

#     def add_gui(self, gui_element):
#         """Adds a new GUI element to the list and indexes it for fast retrieval."""
#         # self.guis.append(gui_element)
        
#         # Store by class (overwrite if multiple of the same class exist)
#         self.gui_by_class[gui_element.__class__] = gui_element
        
#         # Store by name if it has a 'window_name' attribute
#         if hasattr(gui_element, "window_name"):
#             self.gui_by_name[gui_element.window_name] = gui_element

#     def get_gui_by_class(self, class_type):
#         """Returns the GUI element of the given class instantly."""
#         return self.gui_by_class.get(class_type, None)

#     def get_gui_by_name(self, name):
#         """Returns the GUI element by name instantly."""
#         return self.gui_by_name.get(name, None)

#     def remove_gui(self, gui_element):
#         """Removes a GUI element from the manager."""
#         # Remove by class if it exists
#         if gui_element.__class__ in self.gui_by_class:
#             del self.gui_by_class[gui_element.__class__]

#         # Remove by name if applicable
#         if hasattr(gui_element, "window_name") and gui_element.window_name in self.gui_by_name:
#             del self.gui_by_name[gui_element.window_name]

#     def draw_all(self):
#         """Draws all visible GUI elements in the order they were added."""
#         for gui in self.gui_by_class.values():
#             if gui.visible:
#                 gui.draw()

