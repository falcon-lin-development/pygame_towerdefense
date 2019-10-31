import sys
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense')
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.4')
from inp_devices import KeyboardCommand, MouseCommand
import inp_devices as inpd
from config import KEYBOARD
import unittest


class TestInputDevices(unittest.TestCase):
    def test_keyboard(self):
        keyboard = KeyboardCommand()
        keyboard.start()
        keys = [0 for _ in range(500)]
        # do nothing
        for i in range(10):
            key_command = keyboard.step(keys)
            self.assertTrue(key_command is None)

        # test single key
        for i in range(len(KEYBOARD)):
            keys[KEYBOARD[i]] = 1
            key_command = keyboard.step(keys)
            self.assertTrue(key_command is None)
            keys[KEYBOARD[i]] = 0
            key_command = keyboard.step(keys)
            self.assertTrue(key_command == KEYBOARD[i])

        # test multiple keys
        for i in range(len(KEYBOARD)):
            keys[KEYBOARD[i]] = 1
            keys[KEYBOARD[(i+1) % 3]] = 1
            key_command = keyboard.step(keys)
            self.assertTrue(key_command is None)
            keys[KEYBOARD[i]] = 0
            keys[KEYBOARD[(i+1) % 3]] = 0
            key_command = keyboard.step(keys)
            if i < (i+1) % 3:
                self.assertTrue(key_command == KEYBOARD[i])
            else:
                self.assertTrue(key_command == KEYBOARD[(i+1) % 3])

        # test alternating key
        keys[KEYBOARD[1]] = 1
        keyboard.step(keys)
        for i in range(10):
            keys[KEYBOARD[0]] = 1
            keys[KEYBOARD[1]] = 0
            key_command = keyboard.step(keys)
            self.assertTrue(key_command == KEYBOARD[1], "alternating key: Expected {0} get {1}".format(KEYBOARD[1], key_command))
            keys[KEYBOARD[0]] = 0
            keys[KEYBOARD[1]] = 1
            key_command = keyboard.step(keys)
            self.assertTrue(key_command == KEYBOARD[0])

    def test_mouse(self):
        mouse = MouseCommand()
        mouse.start()
        # do nothing
        for i in range(10):
            inp0 = [0, 0, 0]
            outp0 = mouse.step(inp0)
            self.assertTrue(outp0 is None)

        # tests
        inp0 = [0,0,0]
        outp0 = mouse.step(inp0)
        self.assertTrue(outp0 is None)
        inp1 = [1,0,0]
        outp1 = mouse.step(inp1)
        self.assertTrue(outp1 is None)
        inp2 = [1,0,0]
        outp2 = mouse.step(inp2)
        self.assertTrue(outp2 is None)
        inp3 = [0,0,0]
        outp3 = mouse.step(inp3)
        self.assertTrue(outp3 == 1, "Expected {0} get {1}".format(1, outp3))
        inp4 = [1,1,0]
        outp4 = mouse.step(inp4)
        self.assertTrue(outp4 is None)
        inp5 = [1,1,1]
        outp5 = mouse.step(inp5)
        self.assertTrue(outp5 is None)
        inp6 = [0,1,1]
        outp6 = mouse.step(inp6)
        self.assertTrue(outp6 is None)
        inp7 = [0,0,0]
        outp7 = mouse.step(inp7)
        self.assertTrue(outp7 is None, "Expected {0} get {1}".format(2, outp7))

    def test_set_var(self):
        inpd.set_var("testing", 1)
        from inp_devices import testing
        self.assertTrue(testing == 1)


if __name__ == "__main__":
    unittest.main()
