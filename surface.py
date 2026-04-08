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

    def get_normal(self, x, z):
        """Returns the normal vector for the wave surface at the point."""
        derivative_x = self.amplitude * math.cos(x) * math.cos(z)
        derivative_z = -self.amplitude * math.sin(x) * math.sin(z)

        normal_x = -derivative_x
        normal_y = 1.0
        normal_z = -derivative_z

        length = math.sqrt(
            normal_x * normal_x + normal_y * normal_y + normal_z * normal_z
        )

        return (
            normal_x / length,
            normal_y / length,
            normal_z / length,
        )

    def _frange(self, start, stop, step):
        """Yields floating-point values including the final segment boundary."""
        current = start

        while current < stop:
            yield current
            current += step

    def draw(self):
        """Draws the surface as a grid of quad polygons."""
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.08, 0.18, 0.22, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.3, 0.75, 0.9, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.9, 0.9, 0.95, 1.0))
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 48.0)

        x_start, x_end = self.x_range
        z_start, z_end = self.z_range

        for x in self._frange(x_start, x_end, self.step):
            next_x = min(x + self.step, x_end)

            glBegin(GL_QUAD_STRIP)
            for z in self._frange(z_start, z_end, self.step):
                next_z = min(z + self.step, z_end)

                glNormal3f(*self.get_normal(x, z))
                glVertex3f(x, self.get_height(x, z), z)
                glNormal3f(*self.get_normal(next_x, z))
                glVertex3f(next_x, self.get_height(next_x, z), z)

                if next_z == z_end:
                    glNormal3f(*self.get_normal(x, next_z))
                    glVertex3f(x, self.get_height(x, next_z), next_z)
                    glNormal3f(*self.get_normal(next_x, next_z))
                    glVertex3f(next_x, self.get_height(next_x, next_z), next_z)

            glEnd()
