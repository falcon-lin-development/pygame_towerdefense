import sys
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense')
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.2')
from game import Game
import gamepanel
import menu
from config import *
import pygame
pygame.init()
import unittest

class Test_Game(unittest.TestCase):
    def test_init(self):
        test = Game(None)
        result = test.layers[-1]
        expected = test.focus, (0,0), (800, 1000)
        self.assertTrue(result == expected, "Expected:{0}|Result:{1}".format(expected, result))

    def test_run(self):
        test = Game(None)

        # test do nothing
        key_command, click_command, mouse_pos = None, None, (0, 0)

        result = test.run(key_command, click_command, mouse_pos)
        expected = True
        self.assertTrue(result == expected, "Expected:{0}|Result:{1}".format(expected, result))

        # test button hover
        key_command, click_command, mouse_pos = None, None, (320, 440)
        test.run(key_command, click_command, mouse_pos)

        for key, (obj, ref, dim) in test.focus.contents.items():
            if key == "New Game":
                result = obj.hover
                expected = True
                self.assertTrue(result == expected, "Expected:{0}|Result:{1} \n{2}".format(expected, result, key))
            else:
                result = obj.hover
                expected = False
                self.assertTrue(result == expected, "Expected:{0}|Result:{1} \n{2}".format(expected, result, key))

        # test button onclick
        key_command, click_command, mouse_pos = None, 1, (320, 440)
        test.run(key_command, click_command, mouse_pos)

        for key, (obj, ref, dim) in test.focus.contents.items():
            if key == "map":
                result = obj.hover
                expected = True
                self.assertTrue(result == expected, "Expected:{0}|Result:{1} \n{2}".format(expected, result, key))
            else:
                result = obj.hover
                expected = False
                self.assertTrue(result == expected, "Expected:{0}|Result:{1} \n{2}".format(expected, result, key))

        result = test.layers[-1][0]
        expected = gamepanel.GamePanel
        self.assertTrue(isinstance(result, expected), "Expected:{0}|Result:{1} \n{2}".format(expected, result, None))

        result = len(test.layers)
        expected = 2
        self.assertTrue(result == expected, "Expected:{0}|Result:{1} \n{2}".format(expected, result, None))

        # test keyboard command
        key_command, click_command, mouse_pos = K_SPACE, None, (320, 440)
        test.run(key_command, click_command, mouse_pos)

        result = test.focus.contents['map'][0].pause
        expected = True
        self.assertTrue(result == expected, "Expected:{0}|Result:{1}".format(expected, result))

    def test_handle_command(self):
        """
QUIT = 0
SAVE = 1
LOAD = 2
NEW_LAYER = 3
RETURN = 4
PUT_FRONT_LAYER = 5
        :return:
        """
        test = Game(None)
        # test Not command
        test.post_commands((None, None))
        for c in test.get_commands():
            test.handle_command(c, test.focus)

        result = test.focus.command_list.qsize()
        expected = 1
        self.assertTrue(result == expected, "Expected:{0}|Result:{1}".format(expected, result))

        # test Quit
        test.post_commands((QUIT, None))
        for c in test.get_commands():
            test.handle_command(c, test.focus)

        result =len(pygame.event.get())
        expected = 1
        self.assertTrue(result == expected, "Expected:{0}|Result:{1}".format(expected, result))

        # test SAVE
        test.post_commands((SAVE, None))
        result = False
        try:
            for c in test.get_commands():
                test.handle_command(c, test.focus)
        except AttributeError:
            result = True

        expected = True
        self.assertTrue(result == expected, "Expected:{0}|Result:{1}".format(expected, result))

        # test LOAD
        pass

        # test NEW_LAYER
        test.post_commands((NEW_LAYER, ("test layer", None, (0,0), (0,0))))
        for c in test.get_commands():
            test.handle_command(c, test.focus)

        result = test.focus
        expected = None
        self.assertTrue(result is expected, "Expected:{0}|Result:{1}".format(expected, result))

        # test return
        test.post_commands((RETURN, None))
        for c in test.get_commands():
            test.handle_command(c, test.focus)

        result = test.focus
        expected = menu.MainMenu
        self.assertTrue(isinstance(result, expected), "Expected:{0}|Result:{1}".format(expected, result))

        # test PUT FRONT LAYER
        test.post_commands((NEW_LAYER, ("test layer", None, (0,0), (0,0))))
        test.post_commands((PUT_FRONT_LAYER, "main menu"))
        for c in test.get_commands():
            test.handle_command(c, test.focus)

        result = test.focus
        expected = menu.MainMenu
        self.assertTrue(isinstance(result, expected), "Expected:{0}|Result:{1}".format(expected, result))

    def test_keyboard_command(self):
        test = Game(None)
        key_command, click_command, mouse_pos = None, 1, (320, 440)
        test.run(key_command, click_command, mouse_pos)

        test.handle_keyboard(KEYBOARD_COMMAND_DICT[K_SPACE])
        result = test.focus.command_list.qsize()
        expected = 1
        self.assertTrue(result == expected, "Expected:{0}|Result:{1} \n{2}".format(expected, result, None))

        test.handle_keyboard(KEYBOARD_COMMAND_DICT[K_ESCAPE])
        result = test.command_list.qsize()
        expected = 1
        self.assertTrue(result == expected, "Expected:{0}|Result:{1} \n{2}".format(expected, result, None))

        test.handle_keyboard(KEYBOARD_COMMAND_DICT[K_w])
        result = None
        expected = None
        self.assertTrue(result == expected, "Expected:{0}|Result:{1} \n{2}".format(expected, result, None))


if __name__ == "__main__":
    unittest.main()
