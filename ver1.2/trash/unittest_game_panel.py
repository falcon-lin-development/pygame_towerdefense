"""
Developer Notes
    1) cannot test yet until finish writing the whole game

"""

import sys
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense')
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.2')
from gamepanel import *
from menu import TutorialMenu, SettingMenu, LicenseMenu
import pygame
pygame.init()
import unittest
import os


class Test_Game(unittest.TestCase):
    def test_loader(self):
        # test New Game
        result = type(loader(NEW_GAME_FILE))
        expected = GamePanel
        self.assertTrue(result is expected)

        # test Load Game
        pass

        # test tutorial
        result = type(loader('tutorial'))
        expected = TutorialMenu
        self.assertTrue(result is expected)

        # test setting
        result = type(loader('setting'))
        expected = SettingMenu
        self.assertTrue(result is expected)

        # test license
        result = type(loader('license'))
        expected = LicenseMenu
        self.assertTrue(result is expected)

    def test_init(self):
        pass

    def test_load_game(self):
        test = GamePanel()
        test.load_game(NEW_GAME_FILE)

        expected = hasattr(test, "objects")
        result = False
        self.assertTrue(expected == result, "Expected:{0}\nResult:{1}\n".format(expected, result))

        expected = len(test.contents)
        result = 2
        self.assertTrue(expected == result, "Expected:{0}\nResult:{1}\n".format(expected, result))

    def test_process(self):
        test = GamePanel()
        towers, menu = test._process(NEW_GAME_FILE)
        self.assertTrue(menu == [5, 10, 1])
        expected = [('1', 1, (20,20), 1)]
        result = towers
        self.assertTrue(towers == [('1', 1, (20,20), 1)], "Expected:{0}\nResult:{1}\n".format(expected, result))

    def test_save_game(self):
        test = GamePanel()
        test.load_game(NEW_GAME_FILE)

        # create tower and save
        test.save_game()
        self.assertTrue(os.path.isfile("./data/saved_game.txt"))

    def test_run(self):
        test = GamePanel()
        test.load_game(NEW_GAME_FILE)

        # test do nothing
        mouse_pos, offset = (0,0), (0,0)
        result = test.run(mouse_pos, offset)
        expected = True
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test hover on button/tower
        result = test.contents["map"][0].objects["towers"][0].hover
        expected = False
        self.assertTrue(result == expected,
                        "Expected: {0}\nResult: {1}\n{2}".format(expected, result, test.contents["map"][0]))

        mouse_pos, offset = (21, 21), (0, 0)
        test.run(mouse_pos, offset)

        result = test.contents["map"][0].hover
        expected = True
        self.assertTrue(result == expected,
                        "Expected: {0}\nResult: {1}\n{2}".format(expected, result, test))

        result = test.contents["map"][0].objects["towers"][0].hover
        expected = True
        self.assertTrue(result == expected,
                        "Expected: {0}\nResult: {1}\n{2}".format(expected, result, test.contents["map"][0]))

        # test change hover
        mouse_pos, offset = (90, 21), (0, 0)
        test.run(mouse_pos, offset)

        result = test.contents["map"][0].objects["towers"][0].hover
        expected = False
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

    def test_handle_command(self):
        """
WIN = 100
LOST = 101
SELECTED = 102

NEXT_WAVE = 99
# SAVE_GAME = 98
PAUSE = 97
SETTING = 96
EXIT = 95
PURCHASE_MENU = 94
ITEMS = 93

GET_HIT = 89  # called when a creep reached goal tile
MAKE_CREEP = 88  # this one is specially handled in layer

PURCHASE = 79

TOWER_MENU = 69
LEVEL_UP = 68
        :return:
        """
        test = GamePanel()
        test.load_game(NEW_GAME_FILE)
        self.assertTrue(test.contents["game menu"][0].get_money() == 10)
        # mouse_pos, offset = (0, 0), (0, 0)

        # test win
        pass

        # test lose
        test.handle_command((LOST, None))

        expected = 1
        result = test.command_list.qsize()
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test selected
        test.handle_command((SELECTED, (DMG_TOWER, (41, 41))))

        expected = True
        result = bool(test.contents["map"][0].layout[2][2])
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test new wave
        test.handle_command((NEXT_WAVE, None))

        expected = 1
        result = test.contents["map"][0].command_list.qsize()
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test Pause
        test.handle_command((PAUSE, None))

        expected = True
        result = test.contents["map"][0].pause
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test setting
        test.handle_command((SETTING, ('name', 'layer', "ref", "dim")))

        expected = 1
        result = test.request_list.qsize()
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test exit
        test.handle_command((EXIT, None))

        expected = 2
        result = test.request_list.qsize()
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test purchase menu
        test.handle_command((PURCHASE_MENU, ("name", (0,0), (800,200))))

        expected = 3
        result = test.request_list.qsize()
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test Items
        pass

        # test get hit
        test.handle_command((GET_HIT, None))

        expected = 4
        result = test.contents["game menu"][0].get_health()
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test Purchase
        test.contents["game menu"][0].contents["money bar"][0].v += 10
        test.handle_command((PURCHASE, DMG_TOWER))
        self.assertTrue(test.contents["game menu"][0].get_money() == 10)
        self.assertTrue(DMG_TOWER_LV1[0] == 10)

        expected = 4
        result = test.request_list.qsize()
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test tower menu
        test.handle_command((TOWER_MENU, ((0,0), (0,0), ("", "", 1, 10, 10, 1, 1, 1, (1,1)))))

        expected = 5
        result = test.request_list.qsize()
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

        # test levelUP
        test.handle_command((LEVEL_UP, (0, (1,1))))

        expected = 2
        result = test.contents["map"][0].contents[1][0].level
        self.assertTrue(result == expected, "Expected: {0}\nResult: {1}".format(expected, result))

    def test_select_mode(self):
        """detailed tests will be tested in integrated tests"""
        layer = Select_mode(CC_TOWER)
        result = layer.onclick(1,(21,21),(0,0))
        self.assertTrue(isinstance(result, list))
        self.assertTrue(result[0][0]==RETURN)
        self.assertTrue(result[1][0]==SELECTED)


if __name__ == "__main__":
    unittest.main()
