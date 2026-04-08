from OpenGL.GLUT import glutPostRedisplay


class KeyboardHandler:
    """Handles keyboard input for the scene."""

    def __init__(self, scene):
        self.scene = scene

    def on_key(self, key, _x, _y):
        """Toggles the light motion when the space bar is pressed."""
        if key == b" ":
            self.scene.toggle_light_motion()
            glutPostRedisplay()
