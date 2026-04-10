import math
import random
from collections.abc import Iterator
from typing import TypeAlias

from OpenGL.GL import *

FloatRange: TypeAlias = tuple[float, float]
Vector3f: TypeAlias = tuple[float, float, float]
WaveComponent: TypeAlias = tuple[float, float, float, float]
MaterialPreset: TypeAlias = tuple[
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    float,
]
Color4f: TypeAlias = tuple[float, float, float, float]


class WaveSurface:
    """Представляет волнообразную поверхность для отрисовки в 3D-сцене."""

    COLOR_PRESETS: tuple[Color4f, ...] = (
        (0.3, 0.75, 0.9, 1.0),
        (0.92, 0.47, 0.36, 1.0),
        (0.95, 0.78, 0.3, 1.0),
        (0.4, 0.8, 0.48, 1.0),
        (0.62, 0.52, 0.92, 1.0),
        (0.88, 0.38, 0.72, 1.0),
    )

    MATERIAL_PRESETS: tuple[MaterialPreset, ...] = (
        (
            (0.5, 0.5, 0.58, 1.0),
            18.0,
        ),
        (
            (0.76, 0.76, 0.84, 1.0),
            36.0,
        ),
        (
            (0.01, 0.008, 0.002, 1.0),
            0.0,
        ),
        (
            (0.98, 1.0, 0.99, 1.0),
            128.0,
        ),
    )

    def __init__(
        self,
        x_range: FloatRange = (-4.5, 4.5),
        z_range: FloatRange = (-4.5, 4.5),
        step: float = 0.25,
        components: tuple[WaveComponent, ...] | None = None,
    ) -> None:
        self.x_range: FloatRange = x_range
        self.z_range: FloatRange = z_range
        self.step: float = step
        self.components: tuple[WaveComponent, ...] = components or (
            (0.4, 1.0, 1.0, 0.0),
        )
        self.material_index: int = 0
        self.color_index: int = 0

    @classmethod
    def create_random(cls) -> "WaveSurface":
        """Создаёт поверхность со случайной комбинацией волн."""
        component_count = random.randint(2, 3)
        components = tuple(
            (
                random.uniform(0.12, 0.28),
                random.uniform(0.6, 1.8),
                random.uniform(0.6, 1.8),
                random.uniform(0.0, 2.0 * math.pi),
            )
            for _ in range(component_count)
        )
        return cls(components=components)

    def _get_height_derivatives(self, x: float, z: float) -> tuple[float, float]:
        """Возвращает частные производные высоты по x и z."""
        derivative_x = 0.0
        derivative_z = 0.0

        for amplitude, frequency_x, frequency_z, phase in self.components:
            angle_x = frequency_x * x + phase
            angle_z = frequency_z * z + phase

            derivative_x += (
                amplitude
                * frequency_x
                * math.cos(angle_x)
                * math.cos(angle_z)
            )
            derivative_z -= (
                amplitude
                * frequency_z
                * math.sin(angle_x)
                * math.sin(angle_z)
            )

        return derivative_x, derivative_z

    def get_height(self, x: float, z: float) -> float:
        """Возвращает высоту волны для заданных координат."""
        height = 0.0

        for amplitude, frequency_x, frequency_z, phase in self.components:
            height += (
                amplitude
                * math.sin(frequency_x * x + phase)
                * math.cos(frequency_z * z + phase)
            )

        return height

    def get_normal(self, x: float, z: float) -> Vector3f:
        """Возвращает вектор нормали к поверхности в заданной точке."""
        derivative_x, derivative_z = self._get_height_derivatives(x, z)

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

    def next_material(self) -> None:
        """Переключает активный материал поверхности."""
        self.material_index = (self.material_index + 1) % len(self.MATERIAL_PRESETS)

    def next_color(self) -> None:
        """Переключает активный цвет материала поверхности."""
        self.color_index = (self.color_index + 1) % len(self.COLOR_PRESETS)

    def draw(self) -> None:
        """Отрисовывает поверхность как сетку из quad strip-полос."""
        specular, shininess = self.MATERIAL_PRESETS[
            self.material_index
        ]
        color = self.COLOR_PRESETS[self.color_index]
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, shininess)

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
