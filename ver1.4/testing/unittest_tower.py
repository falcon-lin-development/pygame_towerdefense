import sys
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense')
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.4')
import os
os.chdir("/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.4")
from tower import *
from creep import construct_creep
import unittest
import pygame
pygame.init()


class Test_tower(unittest.TestCase):
    t1 = construct_tower(DMG_TOWER, (20, 20), 1)
    t2 = construct_tower(CC_TOWER, (20, 20), 1)

    def test_init_(self):
        """
        class Tower(DynamicItem):
    def __init__(self, tower_type, rel_pos, level, dim=TOWER_DIM):
        # fixed info
        self.level = 0
        self.type = tower_type
        self.rel_pos = self.x, self.y = rel_pos
        self.dim = self.width, self.height = dim

        # build tower
        self._type_construction(tower_type)
        for _ in range(level - self.level):
            self.levelUp()

        # dynamic info
        self.startState = 0  # dim, CDcount
        self.start()

        # static info
        self.hover = False

    # initialization
    def _type_construction(self, tower_type):
        if tower_type == CC_TOWER:
            self.cost, bullet, self.attkFreq, self.attk_range, self.name, img = list(CC_TOWER_LV1)
            self.bullet = list(bullet)
            self.image = save_load_image(img)
        elif tower_type == DMG_TOWER:
            self.cost, bullet, self.attkFreq, self.attk_range, self.name, img = list(DMG_TOWER_LV1)
            self.bullet = list(bullet)
            self.image = save_load_image(img)
        else:
            raise Exception("Invalid Tower type: {0}".format(tower_type))
        self.range = self._calc_range(self.attk_range)
        self.CD = self._calcCD(self.attkFreq)  # f/movement
        :return:
        """
        self.assertTrue(self.t1.type == DMG_TOWER)
        self.assertTrue(self.t1.rel_pos == (20,20))
        self.assertTrue(self.t1.dim == TOWER_DIM)
        self.assertTrue(self.t1.cost == 10)
        self.assertTrue(self.t1.upgrade_cost == 50)
        self.assertTrue(self.t1.bullet == list(DMG_BULLET_LV1))
        self.assertTrue(self.t1.attkFreq == 0.4)
        self.assertTrue(self.t1.attk_range == 2)
        self.assertTrue(self.t1.name == "Tower Lv1")

        self.assertTrue(self.t2.type == CC_TOWER)
        self.assertTrue(self.t2.rel_pos == (20, 20))
        self.assertTrue(self.t2.dim == TOWER_DIM)
        self.assertTrue(self.t2.cost == 30)
        self.assertTrue(self.t2.upgrade_cost == 150)
        self.assertTrue(self.t2.bullet == list(CC_BULLET_LV1))
        self.assertTrue(self.t2.attkFreq == 0.3)
        self.assertTrue(self.t2.attk_range == 3)
        self.assertTrue(self.t2.name == "Long Range Tower Lv1")

    def test_lv_up(self):
        self.t1.levelUp()
        self.assertTrue(self.t1.level == 2)
        self.assertTrue(self.t1.cost == 50)
        self.assertTrue(self.t1.upgrade_cost == 250)
        self.assertTrue(self.t1.bullet == [30, 20, None, (4, 4), DMG_BULLET_LV1_IMG])
        self.assertTrue(self.t1.attkFreq == 0.4/1.25)
        self.assertTrue(self.t1.name == "Tower Lv2")

        self.t2.levelUp()
        self.assertTrue(self.t2.level == 2)
        self.assertTrue(self.t2.cost == 150)
        self.assertTrue(self.t2.upgrade_cost == 750)
        self.assertTrue(self.t2.bullet == [24, 25, None, (4, 4), CC_BULLET_LV1_IMG], str(self.t2.bullet))
        self.assertTrue(self.t2.attkFreq == 0.3/1.25)
        self.assertTrue(self.t2.name == "Long Range Tower Lv2")

        # test_getupgradecost
        self.assertTrue(self.t1.level == 2)
        self.assertTrue(self.t1.getUpgradeCost() == 250, "Expected 250, Result: {0}".format(self.t1.getUpgradeCost()))
        self.assertTrue(self.t2.getUpgradeCost() == 750, "Expected 750, Result: {0}".format(self.t2.getUpgradeCost()))

    def get_relCenter(self):
        self.assertTrue(self.t1.get_relCenter() == (30, 30))
        self.assertTrue(self.t2.get_relCenter() == (30, 30))

    def test_run(self):
        foo = construct_creep(WARRIOR, [(1,2), (3, 4), (5,6)], 1)
        foo1 = construct_creep(WARRIOR, [(20, 10), (20, 15), (20, 10)], 1)
        foo2 = construct_creep(WARRIOR, [(1, 2), (3, 4), (5, 6)], 1)
        creeps = [foo, foo1, foo2]

        self.assertTrue(self.t1.state == 0)
        bullet = self.t1.run(creeps)
        self.assertTrue(self.t1.state > 0)
        self.assertTrue(isinstance(bullet, Projectile))
        self.assertTrue(bullet.state[1] is foo1)

        self.assertTrue(self.t2.state == 0)
        bullet = self.t2.run(creeps)
        self.assertTrue(self.t2.state > 0)
        self.assertTrue(isinstance(bullet, Projectile))
        self.assertTrue(bullet.state[1] is foo1)

    def test_onclick(self):
        Expected = self.t1.onclick(1, None, None)
        Result = CHANGE_MENU, (LAYER_TOWER_MENU, (self.t1.image, self.t1.name, 2, 50, 30, round(1/self.t1.attkFreq, 2), self.t1.attk_range, 250, (1,1)))
        self.assertTrue(Expected == Result, "{0}\n{1}".format(Expected, Result))

        Expected = self.t2.onclick(1, None, None)
        Result = CHANGE_MENU, (LAYER_TOWER_MENU, (
        self.t2.image, self.t2.name, 2, 150, 24, round(1 / self.t2.attkFreq, 2), self.t2.attk_range, 750, (1, 1)))
        self.assertTrue(Expected == Result, "{0}\n{1}".format(Expected, Result))

    def test_hover_and_draw(self):
        """in game real time testing will do"""
        pass

class Test_Bullet(unittest.TestCase):
    foo = construct_tower(DMG_TOWER, (20, 20), 1)
    foo1 = construct_creep(WARRIOR, [(20, 10), (20, 15), (20, 10)], 1)
    test = foo.attk(foo1)

    def test_init(self):
        """
            def __init__(self, fr, to, info):
        # fixed info
        self.dmg, self.vel, self.cc, self.dim = info[:-1]
        self.width, self.height = self.dim
        self.image = save_load_image(info[-1])
        self.target = to

        # game info
        self.startState = fr, to  # (fx, fy), target
        self.start()
        self.hover = False

        :return:
        """
        self.assertTrue(self.test.dmg == 10)
        self.assertTrue(self.test.vel == 20)
        self.assertTrue(self.test.state == (self.foo.get_relCenter(), self.foo1))
        self.assertTrue(self.test.dim == (4,4))
        self.assertTrue(self.test.target is self.foo1)

    def test_run(self):
        Expected = None
        result = self.test.run()
        self.assertTrue(Expected == result)



if __name__ == "__main__":
    unittest.main()