from interface.i_scene import IScene


class SceneManager:
    def __init__(self):
        self.scenes:list[IScene] = []

    def add_scene(self, scene):
        if isinstance(scene, IScene):
            self.scenes.append(scene)
            print(f"Added {scene.__class__.__name__} to SceneManager.")
        else:
            print("Error: Selected class does not implement IScene.")

    def remove_scene(self, scene):
        if isinstance(scene, IScene) and scene in self.scenes:
            self.scenes.remove(scene)
            print(f"Removed {scene.__class__.__name__} from SceneManager.")
        else:
            print("Error: Selected class does not implement IScene or does not exist in SceneManager.")

    def update_all(self):
        for scene in self.scenes:
            scene.update()

    def render_all(self):
        for scene in self.scenes:
            scene.render()

    def clear(self):
        self.scenes.clear()
        print("Cleared all scenes from SceneManager.")