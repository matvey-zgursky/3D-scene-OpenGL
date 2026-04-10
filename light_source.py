import math
from typing import TypeAlias

from OpenGL.GL import *
from OpenGL.GLUT import *

Color4f: TypeAlias = tuple[float, float, float, float]
Position4f: TypeAlias = tuple[float, float, float, float]


class LightSource:
    """Хранит состояние источника света и управляет его поведением."""

    LIGHT_INTENSITY_STEP: float = 0.2
    MIN_LIGHT_INTENSITY: float = 0.1
    MAX_LIGHT_INTENSITY: float = 2.0

    def __init__(self) -> None:
        self.light_color: Color4f = (1.0, 0.9, 0.65, 1.0)
        self.light_intensity: float = 1.0
        self.light_radius: float = 0.15
        self.light_orbit_radius: float = 3.2
        self.light_height: float = 1.8
        self.light_angle: float = 0.0
        self.light_angle_step: float = 0.01
        self.is_light_moving: bool = False
        self.light_position: Position4f = (0.0, self.light_height, 0.0, 1.0)
        self.update_position()

    def initialize_opengl(self) -> None:
        """Настраивает базовые параметры источника света OpenGL."""
        light_color = self.get_color_with_intensity()
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.08, 0.08, 0.08, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.12, 0.12, 0.12, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_color)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.08)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.02)

    def get_color_with_intensity(self) -> Color4f:
        """Возвращает цвет источника света с учётом текущей интенсивности."""
        return (
            self.light_color[0] * self.light_intensity,
            self.light_color[1] * self.light_intensity,
            self.light_color[2] * self.light_intensity,
            self.light_color[3],
        )

    def update_position(self) -> None:
        """Пересчитывает положение источника света на круговой орбите."""
        self.light_position = (
            self.light_orbit_radius * math.cos(self.light_angle),
            self.light_height,
            self.light_orbit_radius * math.sin(self.light_angle),
            1.0,
        )

    def animate(self) -> None:
        """Сдвигает источник света вдоль орбиты и обновляет его положение."""
        if self.is_light_moving:
            self.light_angle = (self.light_angle + self.light_angle_step) % (
                2.0 * math.pi
            )
            self.update_position()

    def toggle_motion(self) -> None:
        """Переключает состояние движения источника света."""
        self.is_light_moving = not self.is_light_moving

    def increase_intensity(self) -> None:
        """Увеличивает интенсивность источника света."""
        self.light_intensity = min(
            self.light_intensity + self.LIGHT_INTENSITY_STEP,
            self.MAX_LIGHT_INTENSITY,
        )

    def decrease_intensity(self) -> None:
        """Уменьшает интенсивность источника света."""
        self.light_intensity = max(
            self.light_intensity - self.LIGHT_INTENSITY_STEP,
            self.MIN_LIGHT_INTENSITY,
        )

    def apply(self) -> None:
        """Обновляет положение и параметры источника света OpenGL."""
        light_color = self.get_color_with_intensity()
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_color)
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)

    def draw(self) -> None:
        """Отрисовывает светящуюся сферу в позиции источника света."""
        light_color = self.get_color_with_intensity()

        glPushMatrix()
        glTranslatef(*self.light_position[:3])

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, light_color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, light_color)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)
        glutSolidSphere(self.light_radius, 32, 32)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))

        glPopMatrix()
