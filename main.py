from scene import Scene
from window import Window


def main() -> None:
    """Runs the OpenGL application."""
    scene = Scene()
    window = Window(scene)
    window.run()


if __name__ == "__main__":
    main()
