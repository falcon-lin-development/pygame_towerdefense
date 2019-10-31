"""
carefully handle mouse command and keyboard commands
https://www.pygame.org/docs/ref/mouse.html
"""
from config import *
from item import DynamicItem


class KeyboardCommand(DynamicItem):
    """
    Only accept the keyboard inputs specified in the KEYBOARD. [K_space, K_w, K_escape] by default

    Acts similar to a delay/R state machine, return the k-command when a pressed key is released.
    If two key is pressed together, no guarantee of which key is considered
    """
    startState = None  # state

    def getNextValues(self, state, inp):
        """
        :param state: an integer indicates the current saved key
        :param inp: list return from pygame.key.get_pressed()
        :return: next_state, output
        """
        for k in KEYBOARD:
            if inp[k]:
                if state == k:
                    return state, None
                else:
                    return k, state
        else:
            return None, state


class MouseCommand(DynamicItem):
    """
    Acts similar to a delay/R state machine, return the click when the mouse button is released.
    only support for mouse left button currently.

    Developer note:
    1) multiple mouse button supports
        i) If two buttons is pressed together, the original internal mouse pressed state will be cancelled
    """
    startState = None  # state

    LEFT_CLICK = 1
    RIGHT_CLICK = 2
    PRESS = 3

    def getNextValues(self, state, inp):
        """
        :param state: an integer indicates the current button pressed
        :param inp: list return from pygame.mouse.get_pressed()
        :return: next_state, output
        """
        if inp[:-1].count(1) >= 2:
            return None, None
        else:
            b = inp[0]
            if b:
                if state == b:
                    return state, None
                else:
                    return b, None
            else:
                return None, state


def set_var(var, v):
    globals()[var] = v





