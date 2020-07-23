import sys
sys.path.append('/Users/Falcon/Downloads/Game/Pygame_towerdefense')
sys.path.append('/Users/Falcon/Downloads/Game/Pygame_towerdefense/ver1.4')
import os
os.chdir("/Users/Falcon/Downloads/Game/Pygame_towerdefense/ver1.4")
from creep import *
import unittest
import pygame
pygame.init()


class Test_creep(unittest.TestCase):
    test = construct_creep(WARRIOR, [(30,70),(730,70),(730,190),(70,190),(70,530),(610,530),(610,410),(190,410),(190,310),(730,310),(730,650),(70,650),(70,730),(770,730)], 1)

    def test_init(self):
        self.assertTrue(self.test.type == WARRIOR)
        self.assertTrue(self.test.level == 1)
        self.assertTrue(self.test.dim == CREEP_DIM)
        self.assertTrue((self.test.prize, self.test.armor, self.test.vel, self.test.cc, self.test.health, self.test.name) == tuple(WARRIOR_LV1_INFO[:-1]))

    def test_run(self):
        s1 = self.test.state[0]
        self.assertTrue(self.test.run())
        s2 = self.test.state[0]
        self.assertTrue(s1 != s2)

    def test_draw(self):
        """In game test"""
        pass


if __name__ == "__main__":
    unittest.main()