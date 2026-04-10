from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from light_source import LightSource
from surface import WaveSurface


class Scene:
    """Содержит логику отрисовки 3D-сцены."""

    def __init__(self, width: int = 900, height: int = 700) -> None:
        self.width: int = width
        self.height: int = height
        self.surface: WaveSurface = WaveSurface()
        self.light_source: LightSource = LightSource()

    def setup_projection(self, width: int, height: int) -> None:
        """Настраивает перспективную проекцию для 3D-сцены."""
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
        """Задаёт базовое состояние OpenGL для последующей 3D-отрисовки."""
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)

        self.light_source.initialize_opengl()
        self.setup_projection(self.width, self.height)

    def animate_light(self) -> None:
        """Сдвигает источник света вдоль орбиты и обновляет его положение."""
        self.light_source.animate()

    def toggle_light_motion(self) -> None:
        """Переключает состояние движения источника света."""
        self.light_source.toggle_motion()

    def increase_light_intensity(self) -> None:
        """Увеличивает интенсивность источника света."""
        self.light_source.increase_intensity()

    def decrease_light_intensity(self) -> None:
        """Уменьшает интенсивность источника света."""
        self.light_source.decrease_intensity()

    def regenerate_surface(self) -> None:
        """Создаёт новую случайную поверхность без сброса состояния сцены."""
        current_color_index = self.surface.color_index
        current_material_index = self.surface.material_index
        self.surface = WaveSurface.create_random()
        self.surface.color_index = current_color_index
        self.surface.material_index = current_material_index

    def toggle_surface_material(self) -> None:
        """Переключает материал поверхности."""
        self.surface.next_material()

    def toggle_surface_color(self) -> None:
        """Переключает цвет материала поверхности."""
        self.surface.next_color()

    def setup_light(self) -> None:
        """Обновляет положение и параметры источника света OpenGL."""
        self.light_source.apply()

    def draw_light_source(self) -> None:
        """Отрисовывает светящуюся сферу в позиции источника света."""
        self.light_source.draw()

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
