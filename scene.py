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
        self.light_position = (2.5, 1.5, 2.0, 1.0)
        self.light_color = (1.0, 0.9, 0.65, 1.0)
        self.light_radius = 0.15

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
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.08, 0.08, 0.08, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.12, 0.12, 0.12, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.light_color)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.light_color)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.08)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.02)

        self.setup_projection(self.width, self.height)

    def setup_light(self):
        """Updates the OpenGL light position in the current camera space."""
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)

    def draw_light_source(self):
        """Draws a glowing sphere at the light source position."""
        glPushMatrix()
        glTranslatef(*self.light_position[:3])

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.light_color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, self.light_color)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)
        glutSolidSphere(self.light_radius, 32, 32)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))

        glPopMatrix()

    def display(self):
        """Clears the buffers and renders the 3D scene."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.setup_camera()
        self.setup_light()
        self.surface.draw()
        self.draw_light_source()
        glutSwapBuffers()

    def reshape(self, width, height):
        """Updates the projection when the window size changes."""
        self.width = width
        self.height = max(height, 1)
        self.setup_projection(width, height)
