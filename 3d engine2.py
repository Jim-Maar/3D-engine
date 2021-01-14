# Die berechnung der Tiefe jedes Pixels Falsch, deshalb können Flächen die weiter hinten sind weiter vorne angezeigt werden.
# Ich habe angefangen alles richtig zu machen, habe aber jeztz ne weile nicht weiter daran gearbeitet.


import pygame
import sys
import math
from math import sin
from math import cos
from random import randint
import time

pov = 1
speed = 0.4
rotspeed = math.pi / 90
size = width, height = (800, 800)


def randomcolor():
    return (randint(0, 255), randint(0, 255), randint(0, 255))


Körper = []
Dreiecke = [
    [0, 1, 2, randomcolor()],
    [0, 1, 3, randomcolor()],
    [0, 4, 2, randomcolor()],
    [0, 4, 3, randomcolor()],
    [5, 1, 2, randomcolor()],
    [5, 1, 3, randomcolor()],
    [5, 4, 2, randomcolor()],
    [5, 4, 3, randomcolor()],
]
"""
    [1, 2, 3, randomcolor()],
    [4, 2, 3, randomcolor()],
]
"""
"""
Dreiecke = [
    [0, 1, 2, randomcolor()],
    [0, 1, 3, randomcolor()],
    [0, 1, 6, randomcolor()],
    [0, 1, 8, randomcolor()],
    [0, 4, 2, randomcolor()],
    [0, 4, 3, randomcolor()],
    [0, 4, 7, randomcolor()],
    [0, 4, 9, randomcolor()],
    [5, 1, 2, randomcolor()],
    [5, 1, 3, randomcolor()],
    [5, 4, 2, randomcolor()],
    [5, 4, 3, randomcolor()],
]
"""


def VektorPlus(Vektor1, Vektor2):
    return [Vektor1[i] + Vektor2[i] for i in range(0, 3)]


def VektorMinus(Vektor1, Vektor2):
    return [Vektor1[i] - Vektor2[i] for i in range(0, 3)]


def Pyramide(Mittelpunkt, höhe, breite, länge):
    Punkte = []
    Punkte += [VektorPlus(Mittelpunkt, [0, 0, höhe])]
    Punkte += [VektorPlus(Mittelpunkt, [länge, breite, 0])]
    Punkte += [VektorPlus(Mittelpunkt, [-länge, breite, 0])]
    Punkte += [VektorPlus(Mittelpunkt, [länge, -breite, 0])]
    Punkte += [VektorPlus(Mittelpunkt, [-länge, -breite, 0])]
    Punkte += [VektorPlus(Mittelpunkt, [0, 0, 0])]
    """
    Punkte += [VektorPlus(Mittelpunkt, [länge, 0, 0])]
    Punkte += [VektorPlus(Mittelpunkt, [-länge, 0, 0])]
    Punkte += [VektorPlus(Mittelpunkt, [0, breite, 0])]
    Punkte += [VektorPlus(Mittelpunkt, [0, -breite, 0])]
    """
    return Punkte


for i in range(0, 2):
    Mittelpunkt = [randint(-50, 50), randint(-50, 50), randint(-50, 50)]
    höhe, breite, länge = (
        randint(-35, 35),
        randint(-35, 35),
        randint(-35, 35),
    )
    Körper += [Pyramide(Mittelpunkt, höhe, breite, länge)]


def projectpoint(Punkt):
    t = 1 / Punkt[0]
    xWert = Punkt[0]
    Punkt = [t * i for i in Punkt]
    Punkt2D = [i * (width / 2 / pov) + width / 2 for i in Punkt[1:]] + [xWert]
    if abs(Punkt[0]) <= pov and abs(Punkt[1] <= pov):
        return True, Punkt2D
    return False, Punkt2D


pygame.init()
screen = pygame.display.set_mode(size)
PixAr = pygame.PixelArray(screen)
pygame.display.set_caption("3D Renderer")

lasttime = time.time()

running = True
# Uhr = pygame.time.Clock()
while running:
    # Uhr.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = time.time() - lasttime
    dt *= 60
    lasttime = time.time()

    keys = pygame.key.get_pressed()

    moveVektor = [0, 0, 0]

    alpha = 0
    beta = 0

    if keys[pygame.K_w]:
        moveVektor[0] -= speed * dt

    if keys[pygame.K_s]:
        moveVektor[0] += speed * dt

    if keys[pygame.K_a]:
        moveVektor[1] += speed * dt

    if keys[pygame.K_d]:
        moveVektor[1] -= speed * dt

    if keys[pygame.K_SPACE]:
        moveVektor[2] += speed * dt

    if keys[pygame.K_LSHIFT]:
        moveVektor[2] -= speed * dt

    if keys[pygame.K_LEFT]:
        alpha += rotspeed * dt

    if keys[pygame.K_RIGHT]:
        alpha -= rotspeed * dt

    if keys[pygame.K_DOWN]:
        beta += rotspeed * dt

    if keys[pygame.K_UP]:
        beta -= rotspeed * dt

    if keys[pygame.K_p]:
        pov += 0.1 * dt
        print(pov)

    if keys[pygame.K_o]:
        pov -= 0.1 * dt
        print(pov)

    for Punkte in Körper:
        for Punkt in Punkte:
            Punkt[0], Punkt[1], Punkt[2] = (
                Punkt[0] * cos(beta) * cos(alpha)
                - Punkt[1] * sin(alpha)
                + Punkt[2] * sin(beta) * cos(alpha)
                + moveVektor[0],
                Punkt[0] * cos(beta) * sin(alpha)
                + Punkt[1] * cos(alpha)
                + Punkt[2] * sin(beta) * sin(alpha)
                + moveVektor[1],
                Punkt[0] * -sin(beta) + Punkt[2] * cos(beta) + moveVektor[2],
            )

    screen.fill((0, 0, 0))
    liste = [[1000] * height for i in range(width)]
    for Punkte in Körper:
        """
        for Punkt in Punkte:
            if Punkt[0] >= 1:
                Sichtbar, Punkt = projectpoint(Punkt)
                if Sichtbar:
                    pygame.draw.rect(
                        screen, (255, 255, 255), (Punkt[0] - 2, Punkt[1] - 2, 5, 5)
                    )
        """
        for Dreieck in Dreiecke:
            if (
                Punkte[Dreieck[0]][0] >= 1
                and Punkte[Dreieck[1]][0] >= 1
                and Punkte[Dreieck[2]][0] >= 1
            ):
                Dreieckpunkte = [projectpoint(Punkte[Dreieck[i]]) for i in range(0, 3)]
                minY = min([int(Dreieck[1][0]) for Dreieck in Dreieckpunkte])
                maxY = max([int(Dreieck[1][0]) for Dreieck in Dreieckpunkte])
                listeklein = [{} for _ in range(0, int(maxY - minY) + 3)]
                for Linie in [[0, 1], [0, 2], [1, 2]]:
                    Sichtbar1, Punkt1 = Dreieckpunkte[Linie[0]]
                    Sichtbar2, Punkt2 = Dreieckpunkte[Linie[1]]
                    if Sichtbar1 or Sichtbar2:
                        deltaX = int(Punkt2[2] - Punkt1[2])
                        deltaY = int(Punkt2[0] - Punkt1[0])
                        deltaZ = int(Punkt2[1] - Punkt1[1])
                        if deltaY < 0:
                            signY = -1
                        else:
                            signY = 1
                        if deltaZ < 0:
                            signZ = -1
                        else:
                            signZ = 1
                        if deltaY != 0:
                            Steigung = deltaZ / deltaY
                            XSteigung = 0
                            # a = 0
                            if abs(Steigung) <= 1:
                                if deltaY != 0:
                                    XSteigung = deltaX / deltaY
                                    # a = deltaX / (deltaY ** 2)
                                # billige Lösung, eigentlich range(0,deltaY) unten genauso
                                for i in range(signY * -2, deltaY + 2 * signY, signY):
                                    xWert = Punkt1[2] + i * XSteigung
                                    # xWert = Punkt1[2] + a * (i ** 2)
                                    y = int(Punkt1[0]) + i
                                    z = int(Punkt1[1] + i * Steigung)
                                    if 0 < y < width and 0 < z < height:
                                        listeklein[y - minY][z] = xWert
                            else:
                                if deltaZ != 0:
                                    XSteigung = deltaX / deltaZ
                                    # a = deltaX / (deltaZ ** 2)
                                for i in range(signZ * -2, deltaZ + 2 * signZ, signZ):
                                    xWert = Punkt1[2] + i * XSteigung
                                    # xWert = Punkt1[2] + a * (i ** 2)
                                    y = int(Punkt1[0] + i / Steigung)
                                    z = int(Punkt1[1]) + i
                                    if 0 < y < width and 0 < z < height:
                                        # print(minY)
                                        listeklein[y - minY][z] = xWert

                for y in range(minY, maxY + 1):
                    Zdic = listeklein[y - minY]
                    if len(Zdic) > 1:
                        minZ = min(Zdic)
                        maxZ = max(Zdic)
                        minZXwert = Zdic[minZ]
                        maxZXwert = Zdic[maxZ]
                        if maxZ != minZ:
                            XSteigung = (maxZXwert - minZXwert) / (maxZ - minZ)
                            # a = (maxZXwert - minZXwert) / ((maxZ - minZ) ** 2)
                        else:
                            XSteigung = 0
                        for z in range(minZ, maxZ + 1):
                            xWert = minZXwert + (z - minZ) * XSteigung
                            # xWert = minZXwert + a * ((z - minZ) ** 2)
                            if xWert <= liste[y][z]:
                                PixAr[y][z] = Dreieck[3]
                                # screen.set_at((y, z), Dreieck[3])
                                liste[y][z] = xWert

    pygame.display.update()

pygame.quit()