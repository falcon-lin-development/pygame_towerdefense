"""item class
these classes should not be created directly
"""
from functions import isInside


class StaticItem(object):
    """a static object has no idea where itself is
    this class should never be created directly
    """
    def __init__(self, **kwargs):
        raise Exception("Root class should be be created directly: {0}".format(self.__class__.__name__))


class DynamicItem(object):
    """a dynamic item know its rel_pos
        this class should never be created directly
    """

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def isInside(self, v, vertices):
        return isInside(v, vertices)

    def step(self, inp):
        s, o = self.getNextValues(self.state, inp)
        self.state = s
        return o

    def start(self):
        self.state = self.startState
