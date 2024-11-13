#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
from math import fmod, pi, sin, cos


viewer = [0.0, 0.0, 10.0]

camerapos = [0.0, 0.0, 0.0]

theta = 0.0
phi = 0.0
thetas = 0.0
phis = 0.0
pix2angle = 1.0
scale = 1.1
r = 1.0
moving = "camera"

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

mouse_x_pos_olds = 0
mouse_y_pos_olds= 0
delta_xs= 0
delta_ys= 0

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


objclrx = 0.0
objclry = 0.0
objclrz = 0.0
def example_object():
    glColor3f(objclrx, objclry, objclrz)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)

xeye=0.0
yeye=0.0
zeye=10.0

def render(time):
    global theta
    global phi
    global thetas
    global phis
    global scale
    global r
    global xeye, yeye, zeye
    global camerapos
    global objclrx, objclry, objclrz

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if (moving == "camera"):
        objclrx = 1.0
        objclry = 1.0
        objclrz = 1.0
    else:
        objclrx =0.0
        objclry = 1.0
        objclrz = 1.0
    glLoadIdentity()

    # gluLookAt(viewer[0], viewer[1], viewer[2],
              # 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


    if (moving == "camera"):
        xeye=r*sin(theta*pi/180)*cos(phi*pi/180)
        yeye=r*sin(phi*pi/180)
        zeye=r*cos(theta*pi/180)*cos(phi*pi/180)
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * pix2angle
            phi = max(-90.0, min(90.0, phi))
            theta = fmod(theta, 360.0)
        if right_mouse_button_pressed:
            r += delta_y * pix2angle
            r += delta_x * pix2angle
            r = max(1.0, abs(r))
            r = min(10.0, abs(r))
    else:
        if left_mouse_button_pressed:
            thetas += delta_xs * pix2angle
            phis += delta_ys * pix2angle

        if right_mouse_button_pressed:
            scale += delta_ys * pix2angle/100
            scale += delta_xs * pix2angle/100

    gluLookAt(xeye, yeye, zeye, camerapos[0],camerapos[1], camerapos[2], 0.0, 1.0, 0.0)
    # gluLookAt(xeye, yeye, zeye, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glRotatef(thetas, 0.0, 1.0, 0.0)
    glRotatef(phis, 1.0, 0.0, 0.0)
    glScalef(scale,scale,scale)

    axes()
    example_object()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global moving
    global camerapos
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_W :
        camerapos[1] -= 0.1
    if key == GLFW_KEY_S :
        camerapos[1] += 0.1
    if key == GLFW_KEY_A :
        camerapos[0] -= 0.1
    if key == GLFW_KEY_D :
        camerapos[0] += 0.1
    if key == GLFW_KEY_Q :
        camerapos[0] =0.0
        camerapos[1] =0.0
        camerapos[2] =0.0
    if key == GLFW_KEY_M and action == GLFW_PRESS:
        if (moving == "camera"):
            moving = "object"
        else:
            moving = "camera"


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global delta_xs
    global delta_ys
    global mouse_x_pos_old
    global mouse_y_pos_old
    global mouse_x_pos_olds
    global mouse_y_pos_olds

    if moving=="camera":
        delta_x = x_pos - mouse_x_pos_old
        mouse_x_pos_old = x_pos
        delta_y = y_pos - mouse_y_pos_old
        mouse_y_pos_old = y_pos
    else:
        delta_xs = x_pos - mouse_x_pos_olds
        mouse_x_pos_olds = x_pos
        delta_ys = y_pos - mouse_y_pos_olds
        mouse_y_pos_olds= y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
