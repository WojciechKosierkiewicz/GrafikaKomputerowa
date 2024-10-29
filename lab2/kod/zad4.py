#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import time


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def getx(u,v):
    return (-90 * pow(u,5)+225 * pow(u,4) -270 * pow(u,3) + 180 * u*u - 45*u)*math.cos(math.pi*v)

def gety(u,v):
    return (160 * pow(u,4) - 320 * pow(u,3) + 160 * u * u - 5)

def getz(u,v):
    return (-90 * pow(u,5) + 225 * pow(u,4) - 270 * pow(u,3) +180 * pow(u,2) - 45*u) * math.sin(math.pi*v)

N = 31
points = [[[0] * 3 for i in range(N+1)] for j in range(N+1)];
clrs = [[[0.0] * 3 for i in range(N+1)] for j in range(N+1)];
def colors(N):
    for i in range(N):
        for j in range(N):
            random.seed(i*j)
            clrs[i][j][0]= random.uniform(0.0,1.0)
            clrs[i][j][1]= random.uniform(0.0,1.0)
            clrs[i][j][2]= random.uniform(0.0,1.0)

def fillpoints(N):
    for i in range(N):
        for j in range(N):
            points[i][j][0]= getx(i/(N-1),j/(N-1))
            points[i][j][1]= gety(i/(N-1),j/(N-1))
            points[i][j][2]= getz(i/(N-1),j/(N-1))

fillpoints(N)
colors(N)
def spin(angle):
    glRotatef(angle,1.0,0.0,0.0)
    glRotatef(angle,0.0,1.0,0.0)
    glRotatef(angle,0.0,0.0,1.0)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / 3.1415)
    glPointSize(5)
    # axes()
    glBegin(GL_TRIANGLE_STRIP)
    # glVertex3f(0,0,1)
    # glVertex3f(0,-5,1)
    for i in range(N):
        for j in range(N):
            glColor3fv(clrs[i+1][j+1])

            glVertex3fv(points[i][j])
            glVertex3fv(points[i+1][j])
            glVertex3fv(points[i][j+1])
            glVertex3fv(points[i+1][j+1])

            # glVertex3f(points[i][j][0],points[i][j][1],points[i][j][2])
            # glVertex3f(points[i][j][0],points[i][j][1],points[i][j][2])

            # glVertex3f(points[i][j][0],points[i][j][1],points[i][j][2])
            # glVertex3f(points[i+1][j][0],points[i+1][j][1],points[i+1][j][2])

            # glVertex3f(points[i][j][0],points[i][j][1],points[i][j][2])
            # glVertex3f(points[i][j+1][0],points[i][j+1][1],points[i][j+1][2])


            # # odwrotny trójkąt
            # glVertex3f(points[i][j][0],points[i][j][1],points[i][j][2])
            # glVertex3f(points[i][j][0],points[i][j][1],points[i][j][2])

            # glVertex3f(points[i][j][0],points[i][j][1],points[i][j][2])
            # glVertex3f(points[i+1][j+1][0],points[i+1][j+1][1],points[i+1][j+1][2])

            # glVertex3f(points[i][j+1][0],points[i][j+1][1],points[i][j+1][2])
            # glVertex3f(points[i][j+1][0],points[i][j+1][1],points[i][j+1][2])
    glEnd()
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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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
