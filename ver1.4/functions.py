"""
implementation of all universal helper functions
"""
import pygame
from config import *


# Item function
def calcVertices(x, y, w, h):
    """
    given a rectangular object's dimbox, return the vertices of the object
    :param x: x-coordinate of top-left corner
    :param y: y-coordinate of top-left corner
    :param w: object width
    :param h: object height
    :return: a tuple of vertices of the object
    """
    return (x, y), (x + w, y), (x, y + h), (x + w, y + h)


def isInside(v, vertices):
    """
    given a point and an object vertices, return bool(the point lies on the the object)
    :param v: a tuple of xy-coordinates of a point. e.g. (x1, y1)
    :param vertices: a tuple of four xy-coordinates. e.g. ((x1,y1), (x2,y2), (x3,y3),(x4,y4))
    :return: bool of whether the point is inside/lies in the object
    """
    x, y = v
    if vertices[0][0] <= x <= vertices[3][0]:
        if vertices[0][1] <= y <= vertices[3][1]:
            return True
    return False


def isCollide(vertices1, vertices2):
    """
    given two sets of vertices, return whether two objects collide
    :param vertices1: a tuple of four xy-coordinates. e.g. ((x1,y1), (x2,y2), (x3,y3),(x4,y4))
    :param vertices2: a tuple of four xy-coordinates. e.g. ((x1,y1), (x2,y2), (x3,y3),(x4,y4))
    :return: boolean of which two objects collide
    """
    # rect to rect
    for v in vertices1:
        if isInside(v, vertices2):
            return True
    for v in vertices2:
        if isInside(v, vertices1):
            return True
    return False


def calcDistance(p1, p2):
    """
    given two points, return the pythagoras distance
    :param p1: a tuple of xy-coordinates of a point. e.g. (x1, y1)
    :param p2: a tuple of xy-coordinates of a point. e.g. (x1, y1)
    :return: float value of straight line distance
    """
    x1, y1 = p1
    x2, y2 = p2
    return ((x1-x2)**2 + (y1-y2)**2)**0.5


def calcNextPos(c1, c2, vel):
    """
    given the current position, destination and the velocity(pixel/frame), return the next position
    :param c1: a tuple of xy-coordinates of the current position. e.g. (x1, y1)
    :param c2: a tuple of xy-coordinates of the destination. e.g. (x1, y1)
    :param vel: int/float indicating the velocity (unit: pixel/frame)
    :return: a tuple of xy-coordinates. e.g.(x, y) -> tuple(int, int)
    """
    x1, y1 = c1
    x2, y2 = c2
    disTravel = vel
    disTotal = calcDistance((x1, y1),(x2, y2))
    disLeft = disTotal - disTravel
    xNew, yNew = int((x1*disLeft + x2*disTravel)/disTotal), int((y1*disLeft + y2*disTravel)/disTotal)
    return xNew, yNew


def calcAlignPos(center, dim):
    """
    given an center and object dimension, return the top-left corner point position
    :param center: a tuple of xy-coordinates of the center position. e.g. (cx1, cy1)
    :param dim: a tuple of (width, height) of the object. e.g. (w1, h1)
    :return: a tuple of xy-coordinates of the top-left corner position. e.g. (x1, y1)
    """
    cx, cy = center
    w, h = dim
    return cx - w // 2, cy - h // 2


def calcAlignCenter(pos, dim):
    """
    given a top-left corner point position and object dimension, return the center point position
    :param pos: a tuple of xy-coordinates of the top-left point position. e.g. (x1, y1)
    :param dim: a tuple of (width, height) of the object. e.g. (w1, h1)
    :return: a tuple of xy-coordinates of the object center point position. e.g. (cx1, cy1)
    """
    x, y = pos
    w, h = dim
    return x + w//2, y + h//2


# image func
def save_load_image(path):
    """
    given a file, return a pygame image.
    :param path: a file path
    :return: if the path is valid, return the corresponding image, else return a NO_IMAGE image
    """
    try:
        return pygame.image.load(path)
    except pygame.error:
        return pygame.image.load(NO_IMG)


def calcAlignImgPos(center, pygame_image):
    """
    given a object center and a pygame image, return a top-left point for centralized drawing property
    :param center: a tuple of xy-coordinates of the center position. e.g. (cx1, cy1)
    :param pygame_image: a pygame.image instance
    :return: a tuple of xy-coordinates of the top-left corner position. e.g. (x1, y1)
    """
    w = pygame_image.get_width()
    h = pygame_image.get_height()
    return calcAlignPos(center, (w, h))


# Frame func
def calc_offset(self_offset, item_ref):
    """
    given a layer offset and one of its content reference, return the absolute offset for that content
    :param self_offset: a tuple of xy-values of the layer's offset. e.g. (offset_x, offset_y)
    :param item_ref: a tuple of xy-values of the layer's offset. e.g. (offset_x, offset_y)
    :return: a tuple of xy-values of the content's absolute offset. e.g. (offset_x, offset_y)
    """
    return calc_abs_pos(item_ref, self_offset)


def calc_abs_pos(rel_pos, offset):
    """
    given a layer offset and one of its content relative top-left, return the absolute top-left position for that content
    :param rel_pos: a tuple of xy-coordinates of the content object. e.g. (x1, y1)
    :param offset: a tuple of xy-values of the layer's offset. e.g. (offset_x, offset_y)
    :return: a tuple of xy-coordinates of the content's absolute top-left position. e.g. (x, y)
    """
    return rel_pos[0]+offset[0], rel_pos[1]+offset[1]


def calc_rel_pos(abs_pos, offset):
    """
    given a layer's offset and objects absolute point position, return the relative
    point position of the object in that layer
    :param abs_pos: a tuple of xy-coordinates of the object. e.g. (x1, y1)
    :param offset:  a tuple of xy-values of the layer's offset. e.g. (offset_x, offset_y)
    :return: a tuple of xy-coordinates of the content's relative top-left position. e.g. (x, y)
    """
    return abs_pos[0]-offset[0], abs_pos[1]-offset[1]


def find_point_loc(point, layout=None):
    """
    given a point, return the location of the point
    :param point: a tuple of xy-coordinates of a object. e.g. (x1, y1)
    :param layout(optional): a nested list representing a layer's layout
    :return: a tuple of location (row, col) for the layout
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


def find_grid_pos(location, layout=None):
    """
    given a location, return the top-left point position of that location
    :param location: a tuple of (row, col) of a specific grid
    :param layout(optional): a nested list of a layer's layout
    :return: top-left pos of the corresponding grid
    """
    row, col = location
    if layout:
        assert row < len(layout), "Invalid location: {0}".format(location)
        assert col < len(layout[0]), "Invalid location: {0}".format(location)
    return col * GRID_WIDTH, row * GRID_HEIGHT





