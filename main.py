from scene import Basic3DScene
from window import OpenGLWindow


def main():
    """Runs the OpenGL application."""
    scene = Basic3DScene()
    window = OpenGLWindow(scene)
    window.run()


if __name__ == "__main__":
    main()
