"""
Implementation of the game holder class
the game logic happens in the Game class

developer Note
done    1) simplify structure
    2) add a waiting command_list for optimization purpose (RUN_BY_LAYER)
"""
from config import *
from sound import Py_Sound
from gamepanel import loader
from menu import MainMenu, SettingMenu, LicenseMenu, TutorialMenu
import pygame


class Game(object):
    """
    surface: a pygame surface for the whole game to display on

    game_logic: implemented in the run function
    display_logic: implemented in draw functions
    """
    def __init__(self, surface=None):
        # drawings
        self.win = surface

        # initialization
        self.focus = MainMenu() # everything starts here
        self.layers = [(LAYER_MAIN_MENU, self.focus, (0, 0), MAIN_MENU_DIM)]  # name:
        self._volume = 1

        # commands and requests
        self.command_list = []

    # game func
    def run(self, key_command, click_command, mouse_pos, verbose=False):
        # get keyboard command
        if key_command:
            if key_command in KEYBOARD_COMMAND_DICT:
                self.handle_keyboard(KEYBOARD_COMMAND_DICT[key_command])
            else:
                self.handle_keyboard(SET_KEY, key_command)

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
    
    # helper function
    def _get_setting_configs(self):
        reversed_dict = {}
        for key, value in globals()["KEYBOARD_COMMAND_DICT"].items():
            reversed_dict[value] = key
        
        out = []
        for c in [PAUSE, NEXT_WAVE, RETURN]:
            if c in reversed_dict:
                out.append(reversed_dict[c])
            else:
                out.append(None)
        
        if self._has_layer(LAYER_GAME_PANEL):
            layer = self._find_layer_by_name(LAYER_GAME_PANEL)[1]
            out.append(layer.sound.vol_state)
        else:
            out.append(bool(self._volume))

        return out
        
    def _has_layer(self, layer_name):
        for name, layer, ref, dim in self.layers:
            if layer_name == name:
                return True
        else:
            return False
    
    def _find_layer_by_name(self, layer_name):
        for name, layer, ref, dim in self.layers:
            if layer_name == name:
                return name, layer, ref, dim
        else:
            raise Exception("Layer not found Error: {0}".format(layer_name))
        
    
    # draw func
    def draw(self):
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
    def _GM_commands(self, c, layer=None):
        """
GM_COMMAND_DICT = {  # only for debug purpose
    0: "quit",
    1: "save",
    2: "load",
    3: "new layer",
    4: "return",
    5: "run by layer",
    6: "set volume"
}
QUIT = 0
SAVE = 1
LOAD = 2
NEW_LAYER = 3
RETURN = 4
RUN_BY_LAYER = 5
SET_VOLUME = 6
        """
        command, target = c
        if command not in GM_COMMAND_DICT and bool(layer):
            layer.post_commands(c)
        else:
            # two cycles
            if command == QUIT:
                event = pygame.event.Event(pygame.QUIT, {})
                pygame.event.post(event)

            # one cycle
            elif command == SAVE:
                self.focus.save_game()  # save game

            # two cycle
            elif command == LOAD:  # load game will also make the game new layer.
                if DEBUG: assert len(target) == 4, "invalid load format: {0}".format(target)
                if DEBUG: assert isinstance(target, tuple), "load  format: {0}".format(target)
                if len(self.layers) > 0: self.layers.pop()
                self.focus = None
                name, file, ref, dim = target
                focus = loader(file)  # load game
                focus.set_vol(self._volume)
                self.post_commands((NEW_LAYER, (name, focus, ref, dim)))

            # one cycle
            elif command == NEW_LAYER:
                # we don't know what layer it is
                if DEBUG: assert len(target) == 4, "invalid layer format: {0}".format(target)
                if DEBUG: assert isinstance(target, tuple), "invalid layer format: {0}".format(target)
                if isinstance(target[1], str):
                    name, name, ref, dim = target
                    if name == LAYER_SETTING_MENU:
                        setting_configs = self._get_setting_configs()
                        self.focus = SettingMenu(setting_configs)
                        self.layers.append((name, self.focus, ref, dim))
                    elif name == LAYER_LICENSE:
                        self.focus = LicenseMenu()
                        self.layers.append((name, self.focus, ref, dim))
                    elif name == LAYER_TUTORIAL:
                        self.focus = TutorialMenu()
                        self.layers.append((name, self.focus, ref, dim))
                    else:
                        raise Exception("Invalid layer: {0}".format(c))
                else:
                    name, self.focus, ref, dim = target
                    self.layers.append((name, self.focus, ref, dim))

            # one cycle
            elif command == RETURN:
                """we may lost information due to this design"""
                # we don't know what that layer is
                self.layers.pop()
                try:
                    self.focus = self.layers[-1][1]
                except IndexError:
                    self.focus = None

            # one cycle
            elif command == SET_VOLUME:
                if self._has_layer(LAYER_GAME_PANEL):
                    name, layer, ref, dim = self._find_layer_by_name(LAYER_GAME_PANEL)
                    layer.handle_command((SET_VOLUME, None))
                    self.focus.handle_command((SET_VOLUME, None))
                else:
                    self._volume = float((self._volume + 1) % 2)
                    self.focus.handle_command((SET_VOLUME, None))
            else:
                raise Exception("Invalid command: {0}".format(command))

    handle_command = _GM_commands

    def _special_commands(self, command, target=None):
        # one cycle
        if command == PAUSE:
            if hasattr(self.focus, "do_pause"): self.focus.do_pause()
        elif command == RETURN:
            if len(self.layers) > 1:
                self.post_commands((RETURN, None))
            else:
                self.post_commands((QUIT, None))
        elif command == NEXT_WAVE:
            if hasattr(self.focus, "next_wave"): self.focus.next_wave(self.focus.get_wave_num())
        elif command == SET_KEY:
            assert target is not None, "Invalid Key: {0}|{1}".format(command, target)
            # target == key to be use on that command
            self.focus.handle_command((DONE_SET_KEY, target))
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
        for _ in range(len(self.command_list[:])):
            yield self.command_list.pop(0)


def set_var(var, v):
    globals()[var] = v


