#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import random


def startup():
    update_viewport(None,200, 200)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def rectangle(x,y,a,b):
    # glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, y+b)
    glVertex2f(x+a,y)
    x= x+a
    y=y+b
    # glColor3f(0, 0, 0.5)
    glVertex2f(x, y)
    glVertex2f(x, y-b)
    glVertex2f(x-a,y)
    glEnd()

def sierpinski(depth,screenx,screeny):
    if depth==0:
        glColor3f(0.5, 0, 0.5)
        rectangle(-screenx/2,-screeny/2,screenx,screeny)
        glColor3f(0.5, 0.5, 0.5)
        return
    else:
       sierpinski(depth-1,screenx,screeny)
       mystarx = -screenx/2
       mystarty = -screeny/2
       jumpx = screenx/pow(3,depth)
       jumpy = screeny/pow(3,depth)
       mystarty += jumpy
       mystarx += jumpx
       while mystarx < screenx/2:
           while mystarty < screeny/2:
               rectangle(mystarx,mystarty,jumpx,jumpy)
               mystarty += 3*jumpy
           mystarx += 3*jumpx
           mystarty = -screeny/2 + jumpy

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)


    sierpinski(4,200,200)


    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
