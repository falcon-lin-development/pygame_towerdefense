"""
helper functions
"""
import pygame
from config import *


# Item function
def calcVertices(x, y, w, h):
    return (x, y), (x + w, y), (x, y + h), (x + w, y + h)


def isInside(v, vertices):
    x, y = v
    if vertices[0][0] < x < vertices[3][0]:
        if vertices[0][1] < y < vertices[3][1]:
            return True
    return False


def isCollide(vertices1, vertices2):
    # rect to rect
    for v in vertices1:
        if isInside(v, vertices2):
            return True
    for v in vertices2:
        if isInside(v, vertices1):
            return True
    return False


def calcDistance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x1-x2)**2 + (y1-y2)**2)**0.5


def calcNextPos(c1, c2, vel):
    x1, y1 = c1
    x2, y2 = c2
    disTravel = vel
    disTotal = calcDistance((x1, y1),(x2, y2))
    disLeft = disTotal - disTravel
    xNew, yNew = int((x1*disLeft + x2*disTravel)/disTotal), int((y1*disLeft + y2*disTravel)/disTotal)
    return xNew, yNew


def calcAlignPos(center, dim):
    """

    :param center: center
    :param dim: dimension
    :return: corresponding pos
    """
    cx, cy = center
    w, h = dim
    return cx - w // 2, cy - h // 2


def calcAlignCenter(pos, dim):
    """

    :param pos:
    :param dim:
    :return: corresponding center
    """
    x, y = pos
    w, h = dim
    return x + w//2, y + h//2


# image func
def save_load_image(obj, path):
    try:
        return pygame.image.load(path)
    except pygame.error:
        return obj.make_image()


def calcAlignImgPos(center, pygame_image):
    """find the centered pos of image if image_dim is larger then a grid"""
    w = pygame_image.get_width()
    h = pygame_image.get_height()
    return calcAlignPos(center, (w, h))


# Frame func
def calc_offset(self_offset, item_ref):
    return calc_abs_pos(item_ref, self_offset)


def calc_abs_pos(rel_pos, offset):
    return rel_pos[0]+offset[0], rel_pos[1]+offset[1]


def calc_rel_pos(abs_pos, offset):
    return abs_pos[0]-offset[0], abs_pos[1]-offset[1]


def find_point_loc(point, layout):
    """return the corresponding row and col
    always return right bottom in the case of boundary
    """
    if layout:
        x, y = point
        col = x // GRID_WIDTH
        row = y // GRID_HEIGHT
        if row < len(layout) and col < len(layout[0]):
            return row, col
        else:
            raise Exception("{0} is not in the layout {1}".format(point, layout))
    else:
        x, y = point
        col = x // GRID_WIDTH
        row = y // GRID_HEIGHT
        return row, col


def find_grid_pos(location, layout):
    """

    :param location: row, col
    :param layout:
    :return: top-left pos of the corresponding grid
    """
    row, col = location
    assert row < len(layout), "Invalid location: {0}".format(location)
    assert col < len(layout[0]), "Invalid location: {0}".format(location)
    return col * GRID_WIDTH, row * GRID_HEIGHT





