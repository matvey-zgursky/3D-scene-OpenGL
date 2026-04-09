from OpenGL.GLUT import glutPostRedisplay

from scene import Scene


class KeyboardHandler:
    """Обрабатывает ввод с клавиатуры для сцены."""

    def __init__(self, scene: Scene) -> None:
        self.scene: Scene = scene

    def on_key(self, key: bytes, _x: int, _y: int) -> None:
        """Переключает движение источника света при нажатии пробела."""
        if key == b" ":
            self.scene.toggle_light_motion()
            glutPostRedisplay()
