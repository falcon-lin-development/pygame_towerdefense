"""
creep and creep constructor

developer Note:

"""
from item import DynamicItem
from functions import save_load_image, calcAlignPos, isInside, calcNextPos, calcAlignCenter, calcVertices
from functions import calc_abs_pos
from config import *
import pygame


def construct_creep(creep_type, creepPath, level):
    return Creep(creepPath, creep_type, level)


class Creep(DynamicItem):
    def __init__(self, creepPath, creep_type, level):
        # fixed info
        self.path = creepPath
        self.type = creep_type
        self._type_construction(creep_type)
        self.level = level
        self._levelize()
        self.hp = self.health

        cx, cy = self.path[0]
        x, y = calcAlignPos((cx, cy), self.dim)

        # game info
        self.startState = (x, y), self.path[1:]  # dim,  remaining_path
        self.start()

    # initialize
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
        self.image = save_load_image(self, info[-1])

    def _levelize(self):
        self.prize *= self.level
        self.armor *= self.level
        self.health *= self.level

    def make_image(self):
        font = pygame.font.SysFont('calibri', 30)
        text = font.render(self.name, 1, (0, 255, 0))
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
                cx, cy = self.getCenter()
                tx, ty = t
                cxNew, cyNew = calcNextPos((cx, cy), (tx, ty), self.vel)
                posNew = calcAlignPos((cxNew, cyNew), (self.width, self.height))
                return (posNew, p), True

        else:
            return ((x, y), p), False

    def run(self):
        return super().step(None)

    # helper function
    def getCenter(self):
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
        # win.blit(self.image, calcAlignPos(self.getCenter(), self.image))
        # self.drawHP(win)
        self.draw_box(win, offset)

    def draw_box(self, win, offset):
        # buggy without offsets
        x, y, w, h = self.getDimBox()
        x, y = calc_abs_pos((x, y), offset)
        pygame.draw.rect(win, BLUE, (x, y, w, h), 0)
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
        return "Creep_LV{0}: at{1} type{2}".format(self.level, self.getCenter(), self.type)
    __repr__ = __str__