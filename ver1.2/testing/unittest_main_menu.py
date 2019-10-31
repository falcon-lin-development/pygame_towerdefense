import sys
import os
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense')
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.2')
from screen_object import TwoDLayer
from menu import Menu, MainMenu, PurchaseMenu
import unittest
from config import *


class Test_Menus(unittest.TestCase):
    def test_main_menu(self):
        test, pos, dim = MainMenu(), (0,0), MAIN_MENU_DIM

        # test menu layout
        count = 0
        for row in test.layout:
            for grid in row:
                if grid is not None:
                    count += 1
        result = count
        expected = 240
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))

        # test do nothing
        mouse_pos, offset = (0,0), (0,0)
        test.run(mouse_pos, offset)

        for key, (b, ref, dim) in test.contents.items():
            result = b.hover
            expected = False
            self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))
        result = test.command_list.qsize()
        expected = 0
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))

        result = test.request_list.qsize()
        expected = 0
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))

        # test button hover
        mouse_pos, offset = (320, 440), (0, 0)
        test.run(mouse_pos, offset)

        for key, (b, ref, dim) in test.contents.items():
            if key != "New Game":
                result = b.hover
                expected = False
                self.assertTrue(result == expected,
                                "Expected: {0}| Result: {1}\n{2}".format(expected, result, key))
            else:
                result = b.hover
                expected = True
                self.assertTrue(result == expected,
                                "Expected: {0}| Result: {1}\n{2}".format(expected, result, key))

        result = test.mouse_is_on
        expected = test.contents["New Game"][0]
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, None))

        # change hover to None
        mouse_pos, offset = (330, 740), (0, 0)
        test.run(mouse_pos, offset)

        result = test.mouse_is_on
        expected = None
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, None))

        for key, (b, ref, dim) in test.contents.items():
            if key != "None":
                result = b.hover
                expected = False
                self.assertTrue(result == expected,
                                "Expected: {0}| Result: {1}\n{2}".format(expected, result, key))
            else:
                result = b.hover
                expected = True
                self.assertTrue(result == expected,
                                "Expected: {0}| Result: {1}\n{2}".format(expected, result, key))

        # change hover to other button
        mouse_pos, offset = (330, 540), (0, 0)
        test.run(mouse_pos, offset)

        result = test.mouse_is_on
        expected = test.contents["Load Game"][0]
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, None))

        for key, (b, ref, dim) in test.contents.items():
            if key != "Load Game":
                result = b.hover
                expected = False
                self.assertTrue(result == expected,
                                "Expected: {0}| Result: {1}\n{2}".format(expected, result, key))
            else:
                result = b.hover
                expected = True
                self.assertTrue(result == expected,
                                "Expected: {0}| Result: {1}\n{2}".format(expected, result, key))

        # test post request
        test.post_request((None, None))
        result = test.request_list.qsize()
        expected = 1
        self.assertTrue(result == expected,
                        "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.request_list))

        # test get request
        for request in test.get_requests():
            result = request
            expected = (None, None)
            self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, None))

        # test post command
        test.post_commands((None, None))
        result = test.command_list.qsize()
        expected = 1
        self.assertTrue(result == expected,
                        "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.command_list))

        test.post_commands([(None, None), (None, None)])
        result = test.command_list.qsize()
        expected = 3
        self.assertTrue(result == expected,
                        "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.command_list))

        # test get command
        for c in test.get_commands():
            result = c
            expected = (None, None)
            self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, None))

        # test handling commands
        test.post_commands((NEW_GAME, None))
        test.post_commands((LOAD_GAME, None))
        test.post_commands((TUTORIAL, None))
        test.post_commands((SETTING, None))
        test.post_commands((LICENSE, None))
        test.run((0,0), (0,0))

        result = test.request_list.qsize()
        expected = 5
        self.assertTrue(result == expected,
                        "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.request_list))

        for request in test.get_requests():
            result = request
            expected = LOAD, None
            self.assertTrue(result == expected,
                            "Expected: {0}| Result: {1}\n{2}".format(expected, result, request))

    def test_build_layout(self):
        class a(TwoDLayer):
            def __init__(self):
                self.width, self.height = 800, 1000
                self.contents = {}
        test = a()
        test.build_layout()
        self.assertTrue(hasattr(test, "layout"))
        self.assertTrue(len(test.layout) == 50)
        self.assertTrue(len(test.layout[0]) == 40)
        for row in test.layout:
            for grid in row:
                self.assertTrue(grid is None)

        # try button
        test.contents = {
            "test button 1": (None, (20, 20), (200, 200)),
        }
        test.build_layout()

        count = 0
        for row in test.layout:
            for grid in row:
                if grid == "test button 1":
                    count += 1

        result = count
        expected = 100
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test))

        # multi buttons
        test.contents = {
            "1": (None, (20, 20), (180, 180)),
            "2": (None, (20, 220), (180, 180)),
            "3": (None, (20, 420), (180, 180)),
            "4": (None, (20, 620), (180, 180)),
            "5": (None, (20, 820), (180, 180))
        }
        test.build_layout()

        count = 0
        for row in test.layout:
            for grid in row:
                if grid is not None:
                    count += 1

        result = count
        expected = 405
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))


        # test boarder
        test.contents = {
            "1": (None, (0, 0), (800, 20)),
            "2": (None, (0, 20), (20, 980)),
            "3": (None, (20, 980), (780, 20)),
            "4": (None, (780, 20), (20, 960)),
        }
        test.build_layout()

        count = 0
        for row in test.layout:
            for grid in row:
                if grid is not None:
                    count += 1

        result = count
        expected = 176
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))

    def test_onclick(self):
        class a(TwoDLayer):
            def __init__(self):
                self.width, self.height = 800, 1000
                self.contents = {}
        test = a()

        class b(object):
            def __init__(self, v):
                self.v = v

            def onclick(self, command, pos, offset):
                return self.v, command, pos, offset

        test.contents = {
            "1": (b(1), (20, 20), (180, 180)),
            "2": (b(2), (20, 220), (180, 180)),
            "3": (b(3), (20, 420), (180, 180)),
            "4": (b(4), (20, 620), (180, 180)),
            "5": (b(5), (20, 820), (180, 180))
        }
        test.build_layout()

        # test right click
        command = test.onclick(2, (88, 898), (0,0))
        result = command
        expected = None, None
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))

        # test out focus
        command = test.onclick(1, (-1, 20), (0, 0))
        result = command
        expected = RETURN, None
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))

        command = test.onclick(1, (1, -20), (0, 0))
        result = command
        expected = RETURN, None
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))

        command = test.onclick(1, (801, 20), (0, 0))
        result = command
        expected = RETURN, None
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))

        command = test.onclick(1, (1, 1020), (0, 0))
        result = command
        expected = RETURN, None
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))

        # test miss hit button
        command = test.onclick(1, (300, 40), (0, 0))
        result = command
        expected = None, None
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))

        # test hit button
        command = test.onclick(1, (20, 40), (0, 0))[0]
        result = command
        expected = 1
        self.assertTrue(result == expected, "Expected: {0}| Result: {1}\n{2}".format(expected, result, test.__str__()))




if __name__ == "__main__":
    unittest.main()


