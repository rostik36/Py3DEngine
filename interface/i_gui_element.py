class IGuiElement:
    def __init__(self, visible=False):
        self.visible = visible  # Control visibility of each GUI element

    def render(self):
        """Method to be implemented by subclasses."""
        raise NotImplementedError
