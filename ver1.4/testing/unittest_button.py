import sys
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense')
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.4')
import os
os.chdir("/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.4")
from button import *
import unittest
import pygame
pygame.init()



class TestBar(unittest.TestCase):
    test = Bar((123, 321), "testing_display", value="testing_value")


    def test_init(self):
        self.assertTrue(self.test.dim == (123, 321))
        self.assertTrue(self.test.width == 123)
        self.assertTrue(self.test.height == 321)

    def test_get_value(self):
        self.assertTrue(self.test.get_value() == "testing_value")

    def test_make_image(self):
        pass

    def test_draw(self):
        win = pygame.display.set_mode(SCREEN_DIM,
                                      flags=pygame.DOUBLEBUF | pygame.RESIZABLE)
        pygame.display.set_caption(NAME)
        clock = pygame.time.Clock()
        for i in range(100):
            clock.tick(30)

            win.fill(BLACK)
            self.test.draw(win, (20, 20))

            pygame.display.update()


    def test_draw_box(self):
        win = pygame.display.set_mode(SCREEN_DIM,
                                      flags=pygame.DOUBLEBUF | pygame.RESIZABLE)
        pygame.display.set_caption(NAME)
        clock = pygame.time.Clock()
        time = 90
        while time > 0:
            clock.tick(30)

            win.fill(BLACK)
            self.test.draw_box(win, (20, 20))

            pygame.display.update()
            time -= 1

    def test_draw_bg(self):
        pass

class TestText(unittest.TestCase):
    test = Text(20, "testing", (0,0,0))

    def test_init(self):
        self.assertTrue(bool(self.test.image))

    def draw(self):
        win = pygame.display.set_mode(SCREEN_DIM,
                                      flags=pygame.DOUBLEBUF | pygame.RESIZABLE)
        pygame.display.set_caption(NAME)
        clock = pygame.time.Clock()
        time = 90
        while time > 0:
            clock.tick(30)

            win.fill(BLACK)
            self.test.draw_box(win, (20, 20))

            pygame.display.update()
            time -= 1

class TestButton(unittest.TestCase):
    test = Button((123, 321), "testing_name", (None, None))

    def test_init(self):
        self.assertTrue(isinstance(self.test, Button))

    def test_onlick(self):
        self.assertTrue(self.test.onclick(0,0,0), (None, None))

class Test_special_buttons(unittest.TestCase):
    def test_NewWave(self):
        a = NewWave((123,321), "NewWave", None)
        self.assertTrue(isinstance(a, Bar))

    def testSets(self):
        a = SetReturn((123,321), "a", None)
        b = SetPause((123,321), "b", None)
        c = SetNewWave((123,321), "c", None)
        d = SetVolume((123,321), "d", None)

        self.assertTrue(a.onclick(1, None, None) == None)
        self.assertTrue(b.onclick(1, None, None) == None)
        self.assertTrue(c.onclick(1, None, None) == None)
        self.assertTrue(d.onclick(1, None, None) == None)

    def testIngameMenuButton(self):
        pass

    def testTowerMenuButton(self):
        pass












if __name__ == "__main__":
    unittest.main()