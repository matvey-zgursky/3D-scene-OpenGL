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
        """Обрабатывает клавиши управления движением света и генерацией поверхности."""
        decoded_key = self._decode_key(key)

        if key == b" ":
            self.scene.toggle_light_motion()
            glutPostRedisplay()
        elif decoded_key in {"g", "п"}:
            self.scene.regenerate_surface()
            glutPostRedisplay()
