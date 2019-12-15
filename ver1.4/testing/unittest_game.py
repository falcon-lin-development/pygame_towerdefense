import sys
sys.path.append('/Users/Falcon/Downloads/Game/Pygame_towerdefense')
sys.path.append('/Users/Falcon/Downloads/Game/Pygame_towerdefense/ver1.4')
import os
os.chdir("/Users/Falcon/Downloads/Game/Pygame_towerdefense/ver1.4")
from game import *
from menu import MainMenu, SettingMenu
from gamepanel import GamePanel
import unittest
from pygame import K_ESCAPE
import pygame
pygame.init()


class TestGame(unittest.TestCase):
    test = Game()

    def test_init_(self):
        self.assertTrue(self.test.focus, MainMenu)
        self.assertTrue(self.test.focus == self.test.layers[0][1])
        self.assertTrue(self.test._volume == 1)
        self.assertTrue(isinstance(self.test.command_list, list))

    def test_run(self):
        """
        self, key_command, click_command, mouse_pos, verbose=False
        :return:
        """

        # test do nothing
        key_command, click_command, mouse_pos = None, None, (0,0)
        result = self.test.run(key_command, click_command, mouse_pos)
        self.assertTrue(result)

        # test return key_board command
        key_command, click_command, mouse_pos = K_ESCAPE, None, (0, 0)
        self.test.run(key_command, click_command, mouse_pos)
        result = len(pygame.event.get())
        expect = 1
        self.assertTrue(expect is result, "{0}\n{1}".format(expect, result))

        # anything else run in menu/gamepanel layer
        pass

    def test_hand_commands(self):
        """
        QUIT = 0
SAVE = 1
LOAD = 2
NEW_LAYER = 3
RETURN = 4
RUN_BY_LAYER = 5
SET_VOLUME = 6
"""
        test = Game()
        c1 = (QUIT, None)
        c2 = (SAVE, None)
        c3 = (LOAD, (LAYER_GAME_PANEL, NEW_GAME_FILE, GAME_PANEL_POS, GAME_PANEL_DIM))
        c4 = (NEW_LAYER, (LAYER_SETTING_MENU, LAYER_SETTING_MENU, SETTING_MENU_POS, SETTING_MENU_DIM))
        c5 = (RETURN, None)
        c6 = RUN_BY_LAYER, None
        c7 = SET_VOLUME, None

        # quit
        test.handle_command(c1)
        expect = type(pygame.event.Event(pygame.QUIT, {}))
        result = type(pygame.event.get()[0])
        self.assertTrue(expect == result, "{0}\n{1}".format(expect, result))

        # load game
        test.handle_command(c3)
        expect = len(test.command_list)
        result = 1
        self.assertTrue(expect == result, "{0}\n{1}".format(expect, result))

        # save game
        key_command, click_command, mouse_pos = None, None, (0,0)
        self.assertTrue(test.run(key_command, click_command, mouse_pos))

        path = "/Users/Falcon/Downloads/Game/Pygame_towerdefense/ver1.4/data/saved_game.txt"
        if os.path.isfile(path):
            os.remove(path)
        test.handle_command(c2)
        expect = True
        result = os.path.isfile("/Users/Falcon/Downloads/Game/Pygame_towerdefense/ver1.4/data/saved_game.txt")
        self.assertTrue(expect == result, "{0}\n{1}".format(expect, result))

        # test new layer
        test.handle_command(c4)
        expect = SettingMenu
        result = type(test.focus)
        self.assertTrue(expect == result, "{0}\n{1}".format(expect, result))

        # test run by layer
        pass

        # test set volume
        self.assertTrue(test._find_layer_by_name(LAYER_GAME_PANEL)[1].sound.vol_state)
        test.handle_command(c7)
        expect = False
        result = test._find_layer_by_name(LAYER_GAME_PANEL)[1].sound.vol_state
        self.assertTrue(expect == result, "{0}\n{1}".format(expect, result))

        # test return
        test.handle_command(c5)
        expect = GamePanel
        result = type(test.focus)
        self.assertTrue(expect == result, "{0}\n{1}".format(expect, result))


if __name__ == "__main__":
    unittest.main()
