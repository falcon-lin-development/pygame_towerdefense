import sys
import os
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense')
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.2')
from gamepanel import *
import unittest
pygame.init()



class Testing(unittest.TestCase):
    verbose = True
    test_obj = GamePanel()
    def test_init(self):
        test = self.test_obj
        self.assertTrue(isinstance(test, GamePanel))
        self.assertTrue(len(self.test_obj.contents) == 9)
        if self.verbose: print(test)

    def test_load_map(self):
        pass

    def test_load_wave(self):
        self.assertTrue(len(self.test_obj.waves) == 5)
        self.assertTrue(len(self.test_obj.waves[0]) == 5)
        if self.verbose: print(self.test_obj.waves)

    def test_load_game(self):
        self.test_obj.load_game(NEW_GAME_FILE)
        self.assertTrue(len(self.test_obj.objects["towers"]) == 1)
        self.assertTrue(len(self.test_obj.contents) == 10)
        if self.verbose: print(self.test_obj)

    def test_save_game(self):
        if os.path.isfile("./data/saved_game.txt"):
            os.remove("./data/saved_game.txt")
        self.assertTrue(not os.path.isfile("./data/saved_game.txt"))
        self.test_obj.save_game()
        self.assertTrue(os.path.isfile("./data/saved_game.txt"), os.getcwd())
        if self.verbose: print(self.test_obj.get_data())

    def test_get_data(self):
        pass

    def test_done(self):
        pass

    def test_can_buy(self):
        pass

    def test_do_pause(self):
        pass

    def test_next_wave(self):
        pass

    def test_make_creep(self):
        pass

    def test_make_tower(self):
        pass

    def test_run(self):
        pass

    def test_3gets(self):
        pass

    def test_command_handling(self):
        pass

if __name__ == "__main__":
    unittest.main()
