import sys

from OpenGL.GLUT import *


class Window:
    """Creates the GLUT window and connects it to a scene object."""

    def __init__(self, scene, width=1400, height=900, title=b"Basic 3D Scene"):
        self.scene = scene
        self.width = width
        self.height = height
        self.title = title
        self.timer_interval_ms = 16

    def on_timer(self, _value):
        """Updates animated scene state and schedules the next frame."""
        self.scene.animate_light()
        glutPostRedisplay()
        glutTimerFunc(self.timer_interval_ms, self.on_timer, 0)

    def initialize(self):
        """Initializes GLUT, creates the window and registers callbacks."""
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(self.title)

        self.scene.initialize()

        glutDisplayFunc(self.scene.display)
        glutReshapeFunc(self.scene.reshape)
        glutTimerFunc(self.timer_interval_ms, self.on_timer, 0)

    def run(self):
        """Starts the OpenGL application loop."""
        self.initialize()
        glutMainLoop()
