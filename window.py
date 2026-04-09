import sys

from OpenGL.GLUT import *

from input_handler import KeyboardHandler
from scene import Scene


class Window:
    """Creates the GLUT window and connects it to a scene object."""

    def __init__(
        self,
        scene: Scene,
        width: int = 1400,
        height: int = 900,
        title: str = "Basic 3D Scene",
    ) -> None:
        self.scene: Scene = scene
        self.width: int = width
        self.height: int = height
        self.title: str = title
        self.timer_interval_ms: int = 16
        self.keyboard_handler: KeyboardHandler = KeyboardHandler(scene)

    def on_timer(self, _value: int) -> None:
        """Updates animated scene state and schedules the next frame."""
        self.scene.animate_light()
        glutPostRedisplay()
        glutTimerFunc(self.timer_interval_ms, self.on_timer, 0)

    def initialize(self) -> None:
        """Initializes GLUT, creates the window and registers callbacks."""
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(self.title.encode("utf-8"))

        self.scene.initialize()

        glutDisplayFunc(self.scene.display)
        glutReshapeFunc(self.scene.reshape)
        glutKeyboardFunc(self.keyboard_handler.on_key)
        glutTimerFunc(self.timer_interval_ms, self.on_timer, 0)

    def run(self) -> None:
        """Starts the OpenGL application loop."""
        self.initialize()
        glutMainLoop()
