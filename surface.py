import math
from collections.abc import Iterator
from typing import TypeAlias

from OpenGL.GL import *

FloatRange: TypeAlias = tuple[float, float]
Vector3f: TypeAlias = tuple[float, float, float]


class WaveSurface:
    """Представляет волнообразную поверхность для отрисовки в 3D-сцене."""

    def __init__(
        self,
        x_range: FloatRange = (-4.5, 4.5),
        z_range: FloatRange = (-4.5, 4.5),
        step: float = 0.25,
        amplitude: float = 0.4,
    ) -> None:
        self.x_range: FloatRange = x_range
        self.z_range: FloatRange = z_range
        self.step: float = step
        self.amplitude: float = amplitude

    def get_height(self, x: float, z: float) -> float:
        """Возвращает высоту волны для заданных координат."""
        return self.amplitude * math.sin(x) * math.cos(z)

    def get_normal(self, x: float, z: float) -> Vector3f:
        """Возвращает вектор нормали к поверхности в заданной точке."""
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

    def _frange(self, start: float, stop: float, step: float) -> Iterator[float]:
        """Последовательно выдаёт значения с плавающей точкой от start до stop, не включая stop."""
        current = start

        while current < stop:
            yield current
            current += step

    def draw(self) -> None:
        """Отрисовывает поверхность как сетку из quad strip-полос."""
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
