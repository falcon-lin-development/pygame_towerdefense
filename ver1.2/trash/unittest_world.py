import sys

sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense')
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.2')
from world import *
import creep
import unittest
import pygame
pygame.init()


class test_world(unittest.TestCase):
    def test_init(self):
        test = Map([])

    def test_load_data(self):
        test = Map([(1, 1, (20, 20), 1), (1, 1, (40, 40), 1), (1, 1, (60, 60), 1), (1, 1, (80, 80), 1)])
        self.assertTrue(len(test.contents) == 4)

    def test_load_map(self):
        pass

    def test_load_wave(self):
        test = Map([])
        self.assertTrue(len(test.waves) == 5, test.waves)
        self.assertTrue(isinstance(test.waves[0], list))

    def test_get_data(self):
        test = Map([(1, 1, (20, 20), 1), (1, 1, (40, 40), 1), (1, 1, (60, 60), 1), (1, 1, (80, 80), 1)])
        self.assertTrue(
            test.get_data() == [(1, 1, (20, 20), 1), (2, 1, (40, 40), 1), (3, 1, (60, 60), 1), (4, 1, (80, 80), 1)],
            test.get_data())

    def test_run(self):
        test = Map([(1, 1, (20, 20), 1)])
        self.assertTrue(test.run((0, 0), (0, 0)) is True)
        test.objects["creeps"].append(test._make_creep('1', test.creepPath, 1))

        for i in range(60):
            self.assertTrue(test.run((0,0), (0,0)))

    def test_make_tower(self):
        test = Map([])
        test._make_tower(1, (20, 20), 1)
        self.assertTrue(len(test.contents) == 1)

    def test_next_wave(self):
        test = Map([])
        test.next_wave(1)
        self.assertTrue(test.command_list.qsize()==1)

    def test_make_creep(self):
        test = Map([])
        c = test._make_creep("1", test.creepPath, 1)
        self.assertTrue(isinstance(c, creep.Creep))

    def test_map_command(self):
        test = Map([])
        test.make_creep_CD = 15
        test.handle_command((MAKE_CREEP, (test.waves[0], 0, 1)))

        self.assertTrue(test.make_creep_CD == 14)

    def do_pause(self):
        test = Map([])
        test.do_pause()
        self.assertTrue(test.pause is True)

if __name__ == "__main__":
    unittest.main()
