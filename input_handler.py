from OpenGL.GLUT import glutPostRedisplay

from scene import Scene


class KeyboardHandler:
    """Handles keyboard input for the scene."""

    def __init__(self, scene: Scene) -> None:
        self.scene: Scene = scene

    def on_key(self, key: bytes, _x: int, _y: int) -> None:
        """Toggles the light motion when the space bar is pressed."""
        if key == b" ":
            self.scene.toggle_light_motion()
            glutPostRedisplay()
