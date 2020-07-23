"""
implementation of creep and creep constructor

developer Note:

"""
from game.item import DynamicItem
from game.functions import save_load_image, calcAlignPos, isInside, calcNextPos, calcAlignCenter, calcVertices
from game.functions import calc_abs_pos, calcAlignImgPos
from game.config import *
import pygame


def construct_creep(creep_type, creepPath, level):
    """constructor for a new creep

    creep_type: int indicating different creep_types which difined in the config file, e.g. WARRIOR == 1
    creepPath: a list of tuple of xy-coordinates for the creep's destinations, e.g. [(x1,y1), (x2,y2), ...]
    level: an integer of the creep's level
    """
    return Creep(creepPath, creep_type, level)


class Creep(DynamicItem):
    def __init__(self, creepPath, creep_type, level=1):
        # fixed info
        self.path = creepPath

        self.type = creep_type
        self._type_construction(creep_type)

        self.level = level
        self._levelize()

        # health: the upper limit of creep's health ｜ hp: the current creep's health
        self.hp = self.health

        # game info
        # creep spawn correspond to the first xy-coordinates in its path
        cx, cy = self.path[0]
        x, y = calcAlignPos((cx, cy), self.dim)
        self.startState = (x, y), self.path[1:]  # dim,  remaining_path
        self.start()

    # init function
    def _type_construction(self, creep_type):
        self.dim = self.width, self.height = CREEP_DIM
        if creep_type == WARRIOR:
            info = WARRIOR_LV1_INFO
        elif creep_type == KNIGHT:
            info = KNIGHT_LV1_INFO
        elif creep_type == DRAGON_KNIGHT:
            info = DRAGON_KNIGHT_LV1_INFO
        elif creep_type == BOSS:
            info = BOSS_LV1_INFO
        else:
            raise Exception("Invalid creep type: {0}".format(creep_type))

        self.prize, self.armor, self.vel, self.cc, self.health, self.name = info[:-1]
        self.image = save_load_image(info[-1])

    def _levelize(self):
        self.prize *= self.level
        self.armor *= self.level
        self.health *= self.level

    def _make_image(self):
        font = pygame.font.SysFont('calibri', 30)
        text = font.render(self.name[0], 1, (0, 255, 0))
        return text

    # game function
    def hit(self, dmg):
        self.hp -= int((dmg * 100) / (100 + self.armor))

    def done(self):
        return self.hp <= 0

    def getNextValues(self, state, inp):
        (x, y), p = state
        t = p[0]
        if not self.done():
            if isInside(t, self.getVertices()):
                if len(p) == 1:
                    return ((x, y), p), 'damn'
                else:
                    return ((x, y), p[1:]), True
            else:
                cx, cy = self.get_relCenter()
                tx, ty = t
                cxNew, cyNew = calcNextPos((cx, cy), (tx, ty), self.vel)
                posNew = calcAlignPos(
                    (cxNew, cyNew), (self.width, self.height))
                return (posNew, p), True

        else:
            return ((x, y), p), False

    def run(self):
        return super().step(None)

    # helper function
    def get_relCenter(self):
        return calcAlignCenter(self.state[0], self.dim)

    def getVertices(self):
        """off by one error is fine here XD very cool"""
        x, y, w, h = self.getDimBox()
        return calcVertices(x, y, w, h)

    def getDimBox(self):
        x, y = self.state[0]
        return x, y, self.width, self.height

    # draw function
    def draw(self, win, offset):
        """offset is dynamic offset"""
        abs_pos = calc_abs_pos(calcAlignImgPos(
            self.get_relCenter(), self.image), offset)
        win.blit(self.image, abs_pos)
        self.drawHP(win, offset)

    def draw_box(self, win, offset):
        # buggy without offsets
        if not hasattr(self, "box_image"):
            self.box_image = self._make_image()
        x, y, w, h = self.getDimBox()
        x, y = calc_abs_pos((x, y), offset)
        pygame.draw.rect(win, BLUE, (x, y, w, h), 1)
        win.blit(self.box_image, (x, y))
        self.drawHP(win, offset)

    def drawHP(self, win, offset):
        x, y, w, h = self.getDimBox()
        k = int(1 / 5 * h)
        bx, by = calc_abs_pos((x, y - k), offset)
        bw, bh = w, k
        gbw = int(self.hp / self.health * bw)
        pygame.draw.rect(win, RED, (bx, by, bw, bh))
        pygame.draw.rect(win, GREEN, (bx, by, gbw, bh))

    # representation function
    def __str__(self):
        return "Creep_LV{0}: at{1} type{2}".format(self.level, self.get_relCenter(), self.type)
    __repr__ = __str__
