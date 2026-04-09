import math
from typing import TypeAlias

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from surface import WaveSurface

Color4f: TypeAlias = tuple[float, float, float, float]
Position4f: TypeAlias = tuple[float, float, float, float]


class Scene:
    """содержит логику отрисовки 3D-сцены."""

    def __init__(self, width: int = 900, height: int = 700) -> None:
        self.width: int = width
        self.height: int = height
        self.surface: WaveSurface = WaveSurface()
        self.light_color: Color4f = (1.0, 0.9, 0.65, 1.0)
        self.light_radius: float = 0.15
        self.light_orbit_radius: float = 3.2
        self.light_height: float = 1.8
        self.light_angle: float = 0.0
        self.light_angle_step: float = 0.01
        self.is_light_moving: bool = False
        self.light_position: Position4f = (0.0, self.light_height, 0.0, 1.0)
        self.update_light_position()

    def setup_projection(self, width: int, height: int) -> None:
        """Насстраивает перспективную проекцию для 3D-сцены."""
        safe_height = max(height, 1)
        aspect_ratio = width / safe_height

        glViewport(0, 0, width, safe_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, aspect_ratio, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def setup_camera(self) -> None:
        """Размещает камеру для отображения сцены в перспективе."""
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

    def initialize(self) -> None:
        """Задает базовое состояние OpenGL для отрисовки последующей 3D-отрисовки."""
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

    def update_light_position(self) -> None:
        """Пересчитывает положение источника света на круговой орбите."""
        self.light_position = (
            self.light_orbit_radius * math.cos(self.light_angle),
            self.light_height,
            self.light_orbit_radius * math.sin(self.light_angle),
            1.0,
        )

    def animate_light(self) -> None:
        """Сдвигает источник света вдоль орбиты и обнвляет его положение"""
        if self.is_light_moving:
            self.light_angle = (
                self.light_angle + self.light_angle_step
            ) % (2.0 * math.pi)
            self.update_light_position()

    def toggle_light_motion(self) -> None:
        """Переключает состояние движения источника света."""
        self.is_light_moving = not self.is_light_moving

    def regenerate_surface(self) -> None:
        """Создает новую случайную поверхность без сброса состояния сцены."""
        current_color_index = self.surface.color_index
        self.surface = WaveSurface.create_random()
        self.surface.color_index = current_color_index

    def toggle_surface_material(self) -> None:
        """Переключает материал поверхности."""
        self.surface.next_material()

    def toggle_surface_color(self) -> None:
        """Переключает цвет материала поверхности."""
        self.surface.next_color()

    def setup_light(self) -> None:
        """Обновляет положение источника света OpenGL в текущей системе камеры."""
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)

    def draw_light_source(self) -> None:
        """Отрисовывает светящуюся сферу в позиции источника света."""
        glPushMatrix()
        glTranslatef(*self.light_position[:3])

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.light_color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, self.light_color)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)
        glutSolidSphere(self.light_radius, 32, 32)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))

        glPopMatrix()

    def display(self) -> None:
        """Очищает буферы и отрисовывает 3D-сцену."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.setup_camera()
        self.setup_light()
        self.surface.draw()
        self.draw_light_source()
        glutSwapBuffers()

    def reshape(self, width: int, height: int) -> None:
        """Обновляет проекцию при изменении размера окна."""
        self.width = width
        self.height = max(height, 1)
        self.setup_projection(width, height)
