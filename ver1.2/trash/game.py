"""
The game logic happens here

developer Note
1) simplify structure
"""
from config import *
from queue import Queue
import menu
from data_structure import Layer
from gamepanel import loader
import pygame


class Game(object):
    def __init__(self, surface):
        # drawings
        self.win = surface

        # game panels
        self.main_menu = menu.MainMenu()  # everything starts here
        self.focus = self.main_menu
        self.layers = Layer()  # name:
        self.layers.add_layer(LAYER_MAIN_MENU, self.main_menu, (0, 0), MAIN_MENU_DIM)

        # commands and requests
        self.command_list = Queue()
        # self.request_list = Queue()

    # game func
    def run(self, key_command, click_command, mouse_pos, verbose=False):
        if DEBUG: assert self.focus is self.layers[-1][0], "RI violation: {0}//{1}".format(self.focus, self.layers[-1][0])

        # get keyboard command
        if key_command: self.handle_keyboard(KEYBOARD_COMMAND_DICT[key_command])

        # get mouse click command
        if click_command:
            layer, abs_pos, dim = self.layers[-1]
            # filter out all None
            c = layer.onclick(click_command, mouse_pos, abs_pos)
            if c is not None and c[0] is not None:
                self.post_commands(c)

        # get requests from layer
        if hasattr(self.focus, "get_requests"):
            for request in self.focus.get_requests():
                self.post_commands(request)

        # process commands
        for command in self.get_commands():
            self.handle_command(command, self.focus)

        # run the game
        layer, offset, dim = self.layers[-1]
        layer.run(mouse_pos, offset)  # self.focus is by default hover

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
        for layer, ref, dim in self.layers.layers_to_draw():
            layer.draw(self.win, ref)

    def draw_box(self):
        self._draw_box_bg((0, 0))
        for layer, ref, dim in self.layers.layers_to_draw():
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
                name, file, ref, dim = target
                focus = loader(file)  # load game
                self.post_commands((NEW_LAYER, (name, focus, ref, dim)))
            elif command == NEW_LAYER:
                # we don't know what layer it is
                if DEBUG: assert len(target) == 4, "invalid layer format: {0}".format(target)
                if DEBUG: assert isinstance(target, tuple), "invalid layer format: {0}".format(target)
                name, self.focus, ref, dim = target
                self.layers.append(name, self.focus, ref, dim)
            elif command == RETURN:
                """we may lost information due to this design"""
                # we don't know what that layer is
                self.layers.pop()
                self.focus = self.layers[-1][0]
            elif command == PUT_FRONT_LAYER:
                # assume one layer can only exist once in the focus list
                self.layers.put_top_layer(target)
                self.focus = self.layers[-1][0]
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
            if hasattr(self.focus, "next_wave"): self.focus.next_wave()
        else:
            raise Exception("Invalid Keyboard Input: {0}".format(c))

    handle_keyboard = _special_commands

    def post_commands(self, commands):
        if isinstance(commands, tuple):
            self.command_list.put(commands)
        elif isinstance(commands, list):
            for command in commands:
                self.command_list.put(command)
        else:
            raise Exception("Invalid commands: {0}".format(commands))
        return None

    def get_commands(self):
        """might use a yield generator for scalability"""
        while not self.command_list.empty():
            yield self.command_list.get()


