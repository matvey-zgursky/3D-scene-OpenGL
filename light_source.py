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
        self.color: Color4f = (1.0, 0.9, 0.65, 1.0)
        self.intensity: float = 1.0
        self.radius: float = 0.15
        self.orbit_radius: float = 3.2
        self.height: float = 1.8
        self.angle: float = 0.0
        self.angle_step: float = 0.01
        self.is_moving: bool = False
        self.position: Position4f = (0.0, self.height, 0.0, 1.0)
        self.update_position()

    def initialize_opengl(self) -> None:
        """Настраивает базовые параметры источника света OpenGL."""
        color = self.get_color_with_intensity()
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.08, 0.08, 0.08, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.12, 0.12, 0.12, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, color)
        glLightfv(GL_LIGHT0, GL_SPECULAR, color)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.08)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.02)

    def get_color_with_intensity(self) -> Color4f:
        """Возвращает цвет источника света с учётом текущей интенсивности."""
        return (
            self.color[0] * self.intensity,
            self.color[1] * self.intensity,
            self.color[2] * self.intensity,
            self.color[3],
        )

    def update_position(self) -> None:
        """Пересчитывает положение источника света на круговой орбите."""
        self.position = (
            self.orbit_radius * math.cos(self.angle),
            self.height,
            self.orbit_radius * math.sin(self.angle),
            1.0,
        )

    def animate(self) -> None:
        """Сдвигает источник света вдоль орбиты и обновляет его положение."""
        if self.is_moving:
            self.angle = (self.angle + self.angle_step) % (
                2.0 * math.pi
            )
            self.update_position()

    def toggle_motion(self) -> None:
        """Переключает состояние движения источника света."""
        self.is_moving = not self.is_moving

    def increase_intensity(self) -> None:
        """Увеличивает интенсивность источника света."""
        self.intensity = min(
            self.intensity + self.LIGHT_INTENSITY_STEP,
            self.MAX_LIGHT_INTENSITY,
        )

    def decrease_intensity(self) -> None:
        """Уменьшает интенсивность источника света."""
        self.intensity = max(
            self.intensity - self.LIGHT_INTENSITY_STEP,
            self.MIN_LIGHT_INTENSITY,
        )

    def apply(self) -> None:
        """Обновляет положение и параметры источника света OpenGL."""
        color = self.get_color_with_intensity()
        glLightfv(GL_LIGHT0, GL_DIFFUSE, color)
        glLightfv(GL_LIGHT0, GL_SPECULAR, color)
        glLightfv(GL_LIGHT0, GL_POSITION, self.position)

    def draw(self) -> None:
        """Отрисовывает светящуюся сферу в позиции источника света."""
        color = self.get_color_with_intensity()

        glPushMatrix()
        glTranslatef(*self.position[:3])

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, color)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)
        glutSolidSphere(self.radius, 32, 32)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))

        glPopMatrix()
