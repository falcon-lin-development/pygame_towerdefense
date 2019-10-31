"""
The game logic happens here

developer Note
1) simplify structure
"""
from config import *
from queue import Queue
from gamepanel import loader
from menu import MainMenu
import pygame


class Game(object):
    def __init__(self, surface):
        # drawings
        self.win = surface

        # game panels
        self.focus = loader(NEW_GAME_FILE) # everything starts here
        self.layers = [(LAYER_MAIN_MENU, self.focus, (0, 0), MAIN_MENU_DIM)]  # name:

        # commands and requests
        self.command_list = []

    # game func
    def run(self, key_command, click_command, mouse_pos, verbose=False):
        # get keyboard command
        if key_command: self.handle_keyboard(KEYBOARD_COMMAND_DICT[key_command])

        if bool(self.focus):
            # run the game and get mouse click command
            layer_name, layer, offset, dim = self.layers[-1]
            # filter out all None
            c = layer.run(click_command, mouse_pos, offset)  # self.focus is by default hover
            if c is not None and c[0] is not None:
                self.post_commands(c)

            # get requests from layer
            if hasattr(self.focus, "get_requests"):
                for request in self.focus.get_requests():
                    self.post_commands(request)

        # process commands
        for command in self.get_commands():
            self.handle_command(command, self.focus)

        # verbose
        if verbose: print(self.focus)

        return True

    # draw func
    def draw(self):
        """
        self.ref == (0,0)
        thus, background at (0,0)
        calc_new_offset == old_off_set
        :return:
        """
        self._draw_bg((0,0))
        for layer_name, layer, ref, dim in self.layers:
            layer.draw(self.win, ref)

    def draw_box(self):
        self._draw_box_bg((0, 0))
        for layer_name, layer, ref, dim in self.layers:
            layer.draw_box(self.win, ref)

    def _draw_bg(self, self_ref):
        pass

    def _draw_box_bg(self, self_ref):
        pass

    # command handler
    def _GM_commands(self, c, layer):
        """
        I might in fact post the command to the target instead of self.focus
QUIT = 0
SAVE = 1
LOAD = 2
NEW_LAYER = 3
RETURN = 4
PUT_FRONT_LAYER = 5
        """

        command, target = c
        if command not in GM_COMMAND_DICT:
            layer.post_commands(c)
        else:
            if command == QUIT:
                event = pygame.event.Event(pygame.QUIT, {})
                pygame.event.post(event)
            elif command == SAVE:
                self.focus.save_game()  # save game
            elif command == LOAD:  # load game will also make the game new layer.
                if DEBUG: assert len(target) == 4, "invalid load format: {0}".format(target)
                if DEBUG: assert isinstance(target, tuple), "load  format: {0}".format(target)
                self.layers.pop()
                self.focus = None
                name, file, ref, dim = target
                focus = loader(file)  # load game
                self.post_commands((NEW_LAYER, (name, focus, ref, dim)))
            elif command == NEW_LAYER:
                # we don't know what layer it is
                if DEBUG: assert len(target) == 4, "invalid layer format: {0}".format(target)
                if DEBUG: assert isinstance(target, tuple), "invalid layer format: {0}".format(target)
                name, self.focus, ref, dim = target
                self.layers.append((name, self.focus, ref, dim))
            elif command == RETURN:
                """we may lost information due to this design"""
                # we don't know what that layer is
                self.layers.pop()
                try:
                    self.focus = self.layers[-1][1]
                except IndexError:
                    self.focus = None
            elif command == PUT_FRONT_LAYER:
                # assume one layer can only exist once in the focus list
                for name, layer, ref, dim in self.layers[:]:
                    if name == target:
                        self.layers.remove((name, layer, ref, dim))
                        self.layers.append((name, layer, ref, dim))
                        self.focus = layer
            else:
                raise Exception("Invalid command: {0}".format(command))
        return None

    handle_command = _GM_commands

    def _special_commands(self, command):
        if command == PAUSE:
            if hasattr(self.focus, "do_pause"): self.focus.do_pause()
        elif command == RETURN:
            if len(self.layers) > 1:
                self.post_commands((RETURN, None))
            else:
                self.post_commands((QUIT, None))
        elif command == NEXT_WAVE:
            if hasattr(self.focus, "next_wave"): self.focus.next_wave(self.focus.get_wave_num())
        else:
            raise Exception("Invalid Keyboard Input: {0}".format(command))

    handle_keyboard = _special_commands

    def post_commands(self, commands):
        if isinstance(commands, tuple):
            self.command_list.append(commands)
        elif isinstance(commands, list):
            for command in commands:
                self.command_list.append(command)
        else:
            raise Exception("Invalid commands: {0}".format(commands))
        return None

    def get_commands(self):
        """might use a yield generator for scalability"""
        while len(self.command_list) > 0:
            yield self.command_list.pop(0)


