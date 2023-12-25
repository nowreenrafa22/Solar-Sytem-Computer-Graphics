from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import numpy as np
import random

star = int(input("Number of stars: "))
planet_no_satellite = int(input("Name the planet number from which satellite will be launched: "))
choto = False
satellite_creation = False
satellite_coordinate = [0, 0]


def draw_points(x, y):
    glPointSize(1.5)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def DrawLine(x1, y1, x2, y2):
    zone = FindZone(x1, y1, x2, y2)
    x1, y1 = ConvertToZone0(x1, y1, zone)
    x2, y2 = ConvertToZone0(x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    x = x1
    y = y1
    while x <= x2:
        p, q = OriginalZone(x, y, zone)
        draw_points(p, q)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1


def FindZone(x1, y1, x2, y2):
    zone = 0
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 <= dy:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 > dy:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 <= dy:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 > dy:
            zone = 6
    return zone


def ConvertToZone0(x1, y1, zone):
    if zone == 0:
        p = x1
        q = y1
    elif zone == 1:
        p = y1
        q = x1
    elif zone == 2:
        p = y1
        q = -x1
    elif zone == 3:
        p = -x1
        q = y1
    elif zone == 4:
        p = -x1
        q = -y1
    elif zone == 5:
        p = -y1
        q = -x1
    elif zone == 6:
        p = -y1
        q = x1
    elif zone == 7:
        p = x1
        q = -y1
    return p, q


def OriginalZone(x1, y1, zone):
    p, q = 0, 0
    if zone == 0:
        p = x1
        q = y1
    elif zone == 1:
        p = y1
        q = x1
    elif zone == 2:
        p = -y1
        q = x1
    elif zone == 3:
        p = -x1
        q = y1
    elif zone == 4:
        p = -x1
        q = -y1
    elif zone == 5:
        p = -y1
        q = -x1
    elif zone == 6:
        p = y1
        q = -x1
    elif zone == 7:
        p = x1
        q = -y1
    return p, q


def MidpointCircle(r, cx, cy):
    d = 1 - r
    x = 0
    y = r
    Circlepoints(x, y, cx, cy)
    while x <= y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * x - 2 * y + 5
            y -= 1
        x += 1
        Circlepoints(x, y, cx, cy)


def Circlepoints(x, y, cx, cy):
    draw_points(x + cx, y + cy)
    draw_points(y + cx, x + cy)
    draw_points(y + cx, -x + cy)
    draw_points(x + cx, -y + cy)
    draw_points(-x + cx, -y + cy)
    draw_points(-y + cx, -x + cy)
    draw_points(-y + cx, x + cy)
    draw_points(-x + cx, y + cy)


def DrawOrbit(radius, cx, cy, angle_displacement):
    glColor3f(1.000, 0.980, 0.980)
    MidpointCircle(radius, cx, cy)
    x, y = rotation(radius, angle_displacement)
    return (x, y)


def DrawPlanet(radius, cx, cy):
    noOfCircles = radius
    for i in range(noOfCircles):
        MidpointCircle(noOfCircles - i, cx, cy)


angle = 0.0


def iterate():
    global angle, choto
    if (choto == False):
        choto = True
    else:
        choto = False
    angle += 0.8


def translation(x, y, dx, dy):
    T = np.array([[1, 0, dx],
                  [0, 1, dy],
                  [0, 0, 1]])

    P = np.array([x, y, 1])

    P_prime = np.dot(T, P)

    x_prime, y_prime, _ = P_prime

    return x_prime, y_prime


def rotation(displacement, angle_displacement):
    global angle
    a = math.cos(math.radians(angle * angle_displacement))
    b = math.sin(math.radians(angle * angle_displacement))

    r = np.array([[a, -b, 0],
                  [b, a, 0],
                  [0, 0, 1]])

    v1 = np.array([[displacement],
                   [0],
                   [1]])

    v11 = np.matmul(r, v1)

    return v11[0][0], v11[1][0]


def satellite():
    global satellite_coordinate
    x, y = satellite_coordinate[0], satellite_coordinate[1]

    x1, y1 = translation(3, 3, x, y)
    x2 = x1 + 10
    y2 = y1
    x3 = x1
    y3 = y1 + 10
    x4 = x1 + 10
    y4 = y1 + 10
    x5 = x1 + 20
    y5 = y1 + 5
    DrawLine(x1, y1, x2, y2)
    DrawLine(x1, y1, x3, y3)
    DrawLine(x4, y4, x5, y5)
    DrawLine(x2, y2, x5, y5)
    DrawLine(x3, y3, x4, y4)

    satellite_coordinate[0] = x1
    satellite_coordinate[1] = y1


def scaling(x1, y1, x2, y2):
    sc = 0.5

    # Translation matrix to move A to the origin
    T1 = np.array([[1, 0, -x1],
                   [0, 1, -y1],
                   [0, 0, 1]])

    S = np.array([[sc, 0, 0],
                  [0, sc, 0],
                  [0, 0, 1]])

    # Translation matrix to move A back to its original position
    T2 = np.array([[1, 0, x1],
                   [0, 1, y1],
                   [0, 0, 1]])

    M = T2.dot(S).dot(T1)

    B = np.array([x2, y2, 1])

    B_scaled = M.dot(B)

    return x1, y1, B_scaled[0], B_scaled[1]


def showScreen():
    global angle, choto, planet_no_satellite, satellite_creation, satellite_coordinate

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    # star
    global star
    for i in range(star):
        glColor3f(1.0, 1.0, 1.0)
        draw_points(random.randint(0, 1080), random.randint(0, 1080))

    # Sun
    glColor3f(1.0, 1.0, 0.0)
    noOfCircles = 40
    for i in range(noOfCircles):
        MidpointCircle(noOfCircles - i, 500, 500)

    glColor3f(1.000, 0.549, 0.000)

    # Sun-Rays
    if (choto != True):
        x1, y1, x2, y2 = scaling(500, 540, 500, 565)
        DrawLine(x1, y1, x2, y2)
    else:
        DrawLine(500, 540, 500, 565)

    if (choto != True):
        x1, y1, x2, y2 = scaling(540, 500, 565, 500)
        DrawLine(x1, y1, x2, y2)
    else:
        DrawLine(540, 500, 565, 500)

    if (choto != True):
        x1, y1, x2, y2 = scaling(500, 460, 500, 435)
        DrawLine(x1, y1, x2, y2)
    else:
        DrawLine(500, 460, 500, 435)

    if (choto != True):
        x1, y1, x2, y2 = scaling(460, 500, 435, 500)
        DrawLine(x1, y1, x2, y2)
    else:
        DrawLine(460, 500, 435, 500)

    theta = noOfCircles * math.cos(math.radians(45))

    if choto != True:
        x1, y1, x2, y2 = scaling(500 - theta, 500 + theta, (500 - theta) - theta / 1.5, (500 + theta) + theta / 1.5)
        DrawLine(x1, y1, x2, y2)
    else:
        DrawLine(500 - theta, 500 + theta, (500 - theta) - theta / 1.5, (500 + theta) + theta / 1.5)
    if choto != True:
        x1, y1, x2, y2 = scaling(500 + theta, 500 + theta, (500 + theta) + theta / 1.5, (500 + theta) + theta / 1.5)
        DrawLine(x1, y1, x2, y2)
    else:
        DrawLine(500 + theta, 500 + theta, (500 + theta) + theta / 1.5, (500 + theta) + theta / 1.5)
    if (choto != True):
        x1, y1, x2, y2 = scaling(500 + theta, 500 - theta, (500 + theta) + theta / 1.5, (500 - theta) - theta / 1.5)
        DrawLine(x1, y1, x2, y2)
    else:
        DrawLine(500 + theta, 500 - theta, (500 + theta) + theta / 1.5, (500 - theta) - theta / 1.5)
    if (choto != True):
        x1, y1, x2, y2 = scaling(500 - theta, 500 - theta, (500 - theta) - theta / 1.5, (500 - theta) - theta / 1.5)
        DrawLine(x1, y1, x2, y2)
    else:
        DrawLine(500 - theta, 500 - theta, (500 - theta) - theta / 1.5, (500 - theta) - theta / 1.5)

    # Mercury

    x, y = DrawOrbit(120, 500, 500, 1)
    glColor3f(1.000, 0.855, 0.725)
    DrawPlanet(20, x + 500, y + 500)

    ox, oy = DrawOrbit(35, x + 500, y + 500, 2)
    glColor3f(0.498, 1.000, 0.831)
    DrawPlanet(5, ox + x + 500, oy + y + 500)

    # Saturn
    x, y = DrawOrbit(240, 500, 500, 0.8)
    glColor3f(0.933, 0.510, 0.933)
    DrawPlanet(20, x + 500, y + 500)

    ox, oy = DrawOrbit(35, x + 500, y + 500, 2)
    glColor3f(0.498, 1.000, 0.831)
    DrawPlanet(5, ox + x + 500, oy + y + 500)

    # Earth
    x, y = DrawOrbit(360, 500, 500, 0.6)
    glColor3f(0.196, 0.804, 0.196)
    DrawPlanet(20, x + 500, y + 500)

    ox, oy = DrawOrbit(35, x + 500, y + 500, 2)
    glColor3f(0.498, 1.000, 0.831)
    DrawPlanet(5, ox + x + 500, oy + y + 500)

    # Mars
    x, y = DrawOrbit(480, 500, 500, 0.4)
    glColor3f(0.412, 0.412, 0.412)
    DrawPlanet(20, x + 500, y + 500)

    ox, oy = DrawOrbit(35, x + 500, y + 500, 2)
    glColor3f(0.498, 1.000, 0.831)
    DrawPlanet(5, ox + x + 500, oy + y + 500)

    # Satellite
    glColor3f(0.000, 0.749, 1.000)
    if (satellite_creation == False):
        satellite_coordinate[0], satellite_coordinate[1] = 520 + (planet_no_satellite * 120), 500
        satellite()
        satellite_creation = True
    else:
        satellite()

    glutSwapBuffers()


def init():
    glViewport(0, 0, 1200, 1080)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1200, 0.0, 1080, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1200, 1080)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Solar System")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
init()

glutMainLoop()
