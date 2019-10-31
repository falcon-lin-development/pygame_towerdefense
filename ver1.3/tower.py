"""
tower and tower constructor
bullet

developer Note:
handled    1) different types of bullet will come up sooner or later
    2) Tower special effect will be implemented
fixed    3) activate implementation is weird
"""
from item import DynamicItem
from functions import save_load_image, calcDistance, calcAlignPos, find_point_loc
from functions import calcNextPos, isCollide, calcAlignCenter, calcVertices, calc_abs_pos
from config import *
import pygame
import math


def construct_tower(tower_type, pos, level):
    return Tower(tower_type, pos, level)


class Tower(DynamicItem):
    def __init__(self, tower_type, rel_pos, level, dim=TOWER_DIM):
        # fixed info
        self.level = level
        self.type = tower_type
        self.rel_pos = self.x, self.y = rel_pos
        self.dim = self.width, self.height = dim

        # build tower
        self._type_construction(tower_type)
        self._levelize(level)

        # dynamic info
        self.startState = 0  # dim, CDcount
        self.start()

        # static info
        self.hover = False

    # button function
    def do_onclick(self, click_command, abs_mouse_pos, offset):
        """create new tower menu

        data = image, display_name, lv, cost, dmg, acckfreq, tower_range, level_up_cost, loc
        return command, (mousepos, offset, data)
        """
        if click_command == 2:
            raise Exception("Invalid onclick")
        elif self.level >= 3:
            pass
        else:
            image = self.image
            display_name = self.name
            lv = self.level
            cost = self.cost
            dmg = self.bullet[0]
            acckfreq = round(1/self.attkFreq, 2)
            tower_range = self.range
            level_up_cost = self.upgrade_cost
            loc = find_point_loc(self.getCenter(), None)
            data = image, display_name, lv, cost, dmg, acckfreq, tower_range, level_up_cost, loc
            return TOWER_MENU, (abs_mouse_pos, offset, data)

    onclick = do_onclick

    def do_hover(self):
        self.hover = True

    def un_hover(self):
        self.hover = False

    # initialization
    def _type_construction(self, tower_type):
        if tower_type == CC_TOWER:
            self.cost, self.bullet, self.attkFreq, self.attk_range, self.name = CC_TOWER_LV1[:-1]
            self.image = save_load_image(self, CC_TOWER_LV1[-1])
        elif tower_type == DMG_TOWER:
            self.cost, self.bullet, self.attkFreq, self.attk_range, self.name = DMG_TOWER_LV1[:-1]
            self.image = save_load_image(self, DMG_TOWER_LV1[-1])
        else:
            raise Exception("Invalid Tower type: {0}".format(tower_type))
        self.range = self._calc_range(self.attk_range)
        self.CD = self._calcCD(self.attkFreq)  # f/movement

    def _levelize(self, level):
        if level == 1:
            self.upgrade_cost = self.cost * 5
        elif level == 2:
            self.cost = self.upgrade_cost
            self.upgrade_cost = self.cost * 5
            self.bullet[0] *= 3  # dmg
            self.attkFreq /= 1.25
            self.CD = self._calcCD(self.attkFreq)
            self.name = self.name[:-3] + "LV2"
        elif level == 3:
            self.cost = self.upgrade_cost
            self.upgrade_cost = "Highest LV"
            self.bullet[0] *= 5
            self.attkFreq /= 1.25
            self.CD = self._calcCD(self.attkFreq)
            self.attk_range += 1
            self.range = self._calc_range(self.attk_range)
            self.name = self.name[:-3] + "LV3"
        else:
            raise Exception("illegal level up: {0}".format(level))

    def _calcCD(self, freq, frame=FRAME): # in terms of frames/movement
        '''
        1s = 1000ms = 30f
        input: s/num
        return: f/num
        '''
        return round(freq * frame, 2)

    def _calc_range(self, grid_num):
        return grid_num * math.ceil(math.sqrt(GRID_HEIGHT**2 + GRID_WIDTH**2))

    def make_image(self):
        font = pygame.font.SysFont("calibri", 20)
        text = font.render(str(self.name[0]), True, BLUE, None)
        return text

    # helper function
    def levelUp(self):
        if self.level < 3:
            self.level += 1
            self._levelize(self.level)
            return True
        else:
            raise Exception("illegal level up: {0}".format(self.level))

    def getUpgradeCost(self):
        return self.upgrade_cost

    def getCenter(self):
        x, y = self.rel_pos
        w, h = self.dim
        return x + w//2, y + h//2

    # game function
    def attk(self, target):
        return Projectile(self.getCenter(), target, self.bullet)

    def findTarget(self, targets):
        inRange = {}
        for t in targets:
            d = calcDistance(self.getCenter(), t.getCenter())
            if d <= self.range:
                inRange[t] = d

        if len(inRange) == 0:
            return None
        else:
            return min(inRange.keys(), key=(lambda k: inRange[k]))

    def getNextValues(self, state, inp):
        # output bullets
        cd = state
        target = self.findTarget(inp)
        if target is None:
            return cd - 1, None
        elif cd <= 0:
            cdNew = self.CD - 1
            return cdNew, self.attk(target)
        else:
            return cd - 1, None

    def run(self, creeps):
        bullet = super(Tower, self).step(creeps)
        return bullet

    # draw function
    def draw(self, win, offset):
        """
        :param win:
        :param offset: static offset, i.e new offset
        :return:
        """
        self.draw_box(win, offset)

    def draw_box(self, win, offset):
        if self.hover:
            pass
        rect = pygame.Rect(offset, (20, 20))
        pygame.draw.rect(win, BLACK, rect, 0)
        win.blit(self.image, offset)


    # representation function
    def __str__(self):
        return "Tower_LV{0}: at{1} type{2}".format(self.level, self.getCenter(), self.type)
    __repr__ = __str__


####################################################################################
# Bullet


class Projectile(DynamicItem):
    def __init__(self, fr, to, info):
        # fixed info
        self.dmg, self.vel, self.cc, self.dim = info[:-1]
        self.width, self.height = self.dim
        self.image = save_load_image(self, info[-1])
        self.target = to

        # game info
        self.startState = fr, to  # (fx, fy), target
        self.start()
        self.hover = False

# game func
    def done(self):
        return isCollide(self.getVertices(), self.target.getVertices())

    def getNextValues(self, state, inp):
        if self.done():
            return None, True
        else:
            (fx, fy), (tx, ty) = state[0], state[1].getCenter(),
            cx, cy = calcAlignCenter((fx, fy), (self.width, self.height))
            cxNew, cyNew = calcNextPos((cx, cy), (tx, ty), self.vel)
            posNew = calcAlignPos((cxNew, cyNew), (self.width, self.height))
            return (posNew, state[1]), None

    def run(self):
        # simple implementation will do
        if super(Projectile, self).step(None):
            return self.target
        else:
            return None

    # helper function
    def getVertices(self):
        x, y, w, h = self.getDimBox()
        return calcVertices(x, y, w, h)

    def getDimBox(self):
        x, y = self.state[0]
        return x, y, self.width, self.height

# init func
    def make_image(self):
        pass

# draw func
    def draw(self, win, offset):
        """dynamic offset"""
        self.draw_box(win, offset)
        # win.blit(self.image, calcAlignImgPos(self.getCenter(), self.image))

    def draw_box(self, win, offset):
        x, y, w, h = self.getDimBox()
        x, y = calc_abs_pos((x, y), offset)
        pygame.draw.rect(win, WHITE, (x, y, w, h))

    # representation function
    def __str__(self):
        return "Bullet: fr: {0}|to: {1}".format(self.state[0], self.target.getCenter())
    __repr__ = __str__




