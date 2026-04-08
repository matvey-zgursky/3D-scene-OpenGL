from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from surface import WaveSurface


class Scene:
    """Stores the rendering logic of the base 3D scene."""

    def __init__(self, width=900, height=700):
        self.width = width
        self.height = height
        self.surface = WaveSurface()

    def setup_projection(self, width, height):
        """Configures a perspective projection for the 3D scene."""
        safe_height = max(height, 1)
        aspect_ratio = width / safe_height

        glViewport(0, 0, width, safe_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, aspect_ratio, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def setup_camera(self):
        """Places the camera so the scene is viewed in perspective."""
        glLoadIdentity()
        gluLookAt(
            0.0,
            4.5,
            10.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
        )

    def initialize(self):
        """Sets the base OpenGL state for future 3D rendering."""
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        self.setup_projection(self.width, self.height)

    def display(self):
        """Clears the buffers and renders the 3D scene."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.setup_camera()
        self.surface.draw()
        glutSwapBuffers()

    def reshape(self, width, height):
        """Updates the projection when the window size changes."""
        self.width = width
        self.height = max(height, 1)
        self.setup_projection(width, height)
