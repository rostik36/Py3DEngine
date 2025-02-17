from abc import ABC, abstractmethod

class IScene: #(ABC):
    def __init(self):
        pass
    # @abstractmethod
    # def init(self):
    #     """Initialize the scene (load resources, setup objects, etc.)."""
    #     pass

    # @abstractmethod
    def update(self, delta_time: float = 0.0):
        """Update the scene logic (e.g., physics, animations)."""
        pass

    # @abstractmethod
    def render(self):
        """Render the scene to the screen."""
        pass

    # @abstractmethod
    # def handle_input(self, event):
    #     """Handle user input (keyboard, mouse, etc.)."""
    #     pass

    # @abstractmethod
    # def cleanup(self):
    #     """Cleanup resources when the scene is removed or changed."""
    #     pass