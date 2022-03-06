import numpy as pb
import matplotlib.pyplot as plt
import cv2


def plot_grid(start, goal, grid):
    '''plot borders, goal and start location on empty map'''
    ox, oy = [], []
    for i in range(-1, grid[0]):
        ox.append(i)
        oy.append(-1)
    for i in range(-1, grid[1]):
        ox.append(400)
        oy.append(i)
    for i in range(-1, grid[0] + 1):
        ox.append(i)
        oy.append(250)
    for i in range(-1, grid[1] + 1):
        ox.append(-1)
        oy.append(i)
    plt.figure(figsize=(8.5, 5.25))
    plt.plot(ox, oy, ".k")
    plt.plot(goal[0], goal[1], "xy")
    plt.plot(start[0], start[1], "+y")


def halfplane(map, p1, p2, region=True):
    '''Returns updated map by checking points on line with open and closed half-plane'''
    cpy_map = map.copy()
    xa = pb.arange(250)
    ya = pb.arange(400)
    y, x = pb.meshgrid(xa, ya)
    m = (p1[1] - p2[1]) / (p1[0] - p2[0] + 1e-10)
    diff = y - m * x - (p1[1] - m * p1[0])
    if region:
        cpy_map[diff > 0] = 1
    else:
        cpy_map[diff <= 0] = 1
    return cpy_map


def obstacle(map):
    '''Returns map with updated obstacles on map'''
    cpy_map = map.copy()

    # Cirlce
    center_x = 300
    center_y = 185
    circle_dia = 80
    xa = pb.arange(250)
    ya = pb.arange(400)
    xc, yc = pb.meshgrid(xa, ya)
    circle_radius = int((circle_dia / 2))

    plot_map = map.copy()
    plot_map[(xc - center_y)**2 + (yc - center_x) **
             2 - (circle_radius * 2 // 2)**2 <= 0] = 1

    x1 = []
    y1 = []

    # Hexagon
    side = 70
    p1 = [200, 100 + side // pb.sqrt(3)]
    p2 = [200 + side // 2, 100 + (side / pb.sqrt(3)) // 2]
    p3 = [200 + side // 2, 100 - (side / pb.sqrt(3)) // 2]
    p4 = [200, 100 - side // pb.sqrt(3)]
    p5 = [200 - side // 2, 100 - (side / pb.sqrt(3)) // 2]
    p6 = [200 - side // 2, 100 + (side / pb.sqrt(3)) // 2]

    line1 = halfplane(cpy_map, p1, p2, True)
    line2 = halfplane(line1, p2, p3, False)
    line3 = halfplane(line2, p3, p4, False)
    line4 = halfplane(line3, p4, p5, False)
    line5 = halfplane(line4, p5, p6, False)
    line6 = halfplane(line5, p6, p1, True)

    # polygon
    p1 = [36, 185]
    p2 = [115, 210]
    p3 = [80, 180]
    p4 = [105, 100]

    # Upper triangle
    utline1 = halfplane(
        cpy_map,
        p1,
        p2,
        True)

    utline2 = halfplane(
        utline1,
        p2,
        p3,
        False)

    utline3 = halfplane(
        utline2,
        p3,
        p1,
        False)

    # Lower triangle
    ltline1 = halfplane(
        cpy_map,
        p1,
        p3,
        True)

    ltline2 = halfplane(
        ltline1,
        p3,
        p4,
        True)

    ltline3 = halfplane(
        ltline2,
        p4,
        p1,
        False)

    ploygon = cv2.bitwise_and(
        line6, cv2.bitwise_and(
            utline3, ltline3))

    for x in range(400):
        for y in range(250):
            if ploygon[x, y] == 0:
                ploygon[x, y] = 1
            else:
                ploygon[x, y] = 0

    merged_map = cv2.bitwise_or(plot_map, ploygon)
    for x in range(400):
        for y in range(250):
            if merged_map[x, y] == 1:
                x1.append(x)
                y1.append(y)

    plt.plot(x1, y1, ".k")
    plt.grid(b=None)
    kernel = pb.ones((11, 11), pb.uint8)
    # Inflate the obstacle
    inflated_map = cv2.dilate(merged_map, kernel, iterations=1)
    return inflated_map
