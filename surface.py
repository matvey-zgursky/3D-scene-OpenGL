import math

from OpenGL.GL import *


class WaveSurface:
    """Represents a wave-like surface that can be rendered in the 3D scene."""

    def __init__(
        self,
        x_range=(-4.5, 4.5),
        z_range=(-4.5, 4.5),
        step=0.25,
        amplitude=0.4,
    ):
        self.x_range = x_range
        self.z_range = z_range
        self.step = step
        self.amplitude = amplitude

    def get_height(self, x, z):
        """Returns the wave height for the provided coordinates."""
        return self.amplitude * math.sin(x) * math.cos(z)

    def _frange(self, start, stop, step):
        """Yields floating-point values including the final segment boundary."""
        current = start

        while current < stop:
            yield current
            current += step

    def draw(self):
        """Draws the surface as a grid of quad polygons."""
        glColor3f(0.3, 0.75, 0.9)

        x_start, x_end = self.x_range
        z_start, z_end = self.z_range

        for x in self._frange(x_start, x_end, self.step):
            next_x = min(x + self.step, x_end)

            glBegin(GL_QUAD_STRIP)
            for z in self._frange(z_start, z_end, self.step):
                next_z = min(z + self.step, z_end)

                glVertex3f(x, self.get_height(x, z), z)
                glVertex3f(next_x, self.get_height(next_x, z), z)

                if next_z == z_end:
                    glVertex3f(x, self.get_height(x, next_z), next_z)
                    glVertex3f(next_x, self.get_height(next_x, next_z), next_z)

            glEnd()
