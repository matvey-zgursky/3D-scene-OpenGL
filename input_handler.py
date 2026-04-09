from OpenGL.GLUT import glutPostRedisplay

from scene import Scene


class KeyboardHandler:
    """Обрабатывает ввод с клавиатуры для сцены."""

    def __init__(self, scene: Scene) -> None:
        self.scene: Scene = scene

    def _decode_key(self, key: bytes) -> str:
        """Преобразует код клавиши в символ независимо от используемой кодировки."""
        for encoding in ("utf-8", "cp1251", "latin-1"):
            try:
                return key.decode(encoding).lower()
            except UnicodeDecodeError:
                continue

        return ""

    def on_key(self, key: bytes, _x: int, _y: int) -> None:
        """Обрабатывает клавиши управления светом и свойствами поверхности."""
        decoded_key = self._decode_key(key)

        if key == b" ":
            self.scene.toggle_light_motion()
            glutPostRedisplay()
        elif key in {b"+", b"="}:
            self.scene.increase_light_intensity()
            glutPostRedisplay()
        elif key == b"-":
            self.scene.decrease_light_intensity()
            glutPostRedisplay()
        elif decoded_key in {"g", "п"}:
            self.scene.regenerate_surface()
            glutPostRedisplay()
        elif decoded_key in {"c", "с"}:
            self.scene.toggle_surface_color()
            glutPostRedisplay()
        elif decoded_key in {"m", "ь"}:
            self.scene.toggle_surface_material()
            glutPostRedisplay()
