"""
carefully handle mouse command
https://www.pygame.org/docs/ref/mouse.html
"""
from config import *
from item import DynamicItem


class KeyboardCommand(DynamicItem):
    startState = None  # state

    def getNextValues(self, state, inp):
        for k in KEYBOARD:
            if inp[k]:
                if state == k:
                    return state, None
                else:
                    return k, state
        else:
            return None, state


class MouseCommand(DynamicItem):
    startState = None  # state

    command_d = {
        "left_clicked": 1,
        "right_clicked": 2,
    }

    def getNextValues(self, state, inp):  # Less efficient way in memory
        if inp[:-1].count(1) >= 2:
            return None, None
        else:
            for i, b in enumerate(inp[:-1]):  # 2 ops.
                if b:
                    if state == i:
                        return state, None
                    else:
                        return i + 1, None
            else:
                return None, state



