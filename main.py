import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def display():
    """Отрисовывает пустой кадр и меняет буферы местами."""
    glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()


def init_window():
    """Инициализирует GLUT и создаёт окно OpenGL."""
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(900, 700)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OpenGL Window")
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glutDisplayFunc(display)


def main():
    """Запускает приложение и главный цикл GLUT."""
    init_window()
    glutMainLoop()


if __name__ == "__main__":
    main()
