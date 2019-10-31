import sys
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense')
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.4')
import os
os.chdir("/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.4")
from gamepanel import *
import unittest
import pygame
pygame.init()


class Test_Game(unittest.TestCase):
    test = loader(NEW_GAME_FILE)

    def test_init(self):
        """
               self.mouse_is_on = None
        self.hover = False
        self.request_list = []
        self.command_list = []
        :return:
        """
        self.assertTrue(hasattr(self.test, "mouse_is_on"))
        self.assertTrue(hasattr(self.test, "hover"))
        self.assertTrue(hasattr(self.test, "request_list"))
        self.assertTrue(hasattr(self.test, "command_list"))



    def test_load_game(self):
        expected = hasattr(self.test, "objects")
        result = True
        self.assertTrue(expected == result, "Expected:{0}\nResult:{1}\n".format(expected, result))

        expected = len(self.test.contents)
        result = 9
        self.assertTrue(expected == result, "Expected:{0}\nResult:{1}\n".format(expected, result))

    def test_save_game(self):

        # create tower and save
        if os.path.isfile("/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.4/data/saved_game.txt"):
            os.remove("/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.4/data/saved_game.txt")
        self.test.save_game()
        self.assertTrue(os.path.isfile("/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.4/data/saved_game.txt"))

    def test_run(self):

        # test do nothing
        mouse_pos, offset = (0, 0), (0, 0)
        result = self.test.run(1, mouse_pos, offset)
        expected = None, None
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test hover on button/tower
        mouse_pos, offset = (60, 920), (0, 0)
        self.test.run(None, mouse_pos, offset)
        result = self.test.contents["purchase"][0].hover
        expected = True
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test onclick
        mouse_pos, offset = (60, 920), (0, 0)
        c = self.test.run(1, mouse_pos, offset)
        result = c[0]
        expected = CHANGE_MENU
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test_selection_run
        self.test.handle_command((CHANGE_MENU, (LAYER_PURCHASE_MENU, None)))
        mouse_pos, offset = (60, 840), (0, 0)
        c = self.test.run(1, mouse_pos, offset)
        result = c[0]
        expected = PURCHASE
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

    def test_handle_command(self):
        """
        WIN = 99
        LOST = 98
        RETURN_FROM_GAME = 97
        CHANGE_MENU = 96
        MAKE_CREEP = 95
        SET_VOLUME = 94

        NEXT_WAVE = 89
        ITEMS = 88

        PURCHASE = 79
        SELECTED = 79

        LEVEL_UP = 69
        """
        t = loader(NEW_GAME_FILE)
        c1 = (WIN, None)
        c2 = (LOST, None)
        c3 = RETURN_FROM_GAME, None
        c4 = CHANGE_MENU, (LAYER_PURCHASE_MENU, None)
        # c5 = MAKE_CREEP, ([1,1,2], 0, 1)
        c6 = SET_VOLUME, None
        c7 = NEXT_WAVE, None
        c8 = PURCHASE, DMG_TOWER
        c9 = SELECTED, (DMG_TOWER, (20, 20))
        c10 = LEVEL_UP, (10, (1,1))

        t.handle_command(c1)
        expected = None
        result = None
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        t.handle_command(c2)
        expected = True
        result = t.pause
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        t.handle_command(c3)
        expected = 2
        result = len(t.request_list)
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        t.handle_command(c4)
        expected = 3
        result = len(t.contents.keys())
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        t.handle_command(c6)
        expected = False
        result = t.sound.vol_state
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        t.handle_command(c7)
        expected = 1
        result = len(t.command_list)
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        t.handle_command(c8)
        expected = t._selection_run
        result = t.run
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        t.handle_command(c9)
        expected = 1
        result = t.layout[1][1]
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        t.handle_command(c10)
        expected = 2
        result = t.contents[1][0].level
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

    def test_draws(self):
        """in game testing"""
        pass



if __name__ == "__main__":
    unittest.main()
