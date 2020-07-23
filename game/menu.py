"""
Implementation of Menus

Developer note
done 1) button implementation
done 2) setting
done 3) license
4) tutorial
done 5) hover checking duplicates here / may put it to the game run

"""
from game.functions import isInside, calcVertices
from game.functions import calc_rel_pos, find_point_loc, calc_offset
import math
import game.button as bt
import pygame
from game.config import *



class Menu(object):
    """Menu instance should never be created directly
    command: commands that get done by this abstraction
    request: command that get done by the higher level of abstraction

    a menu is by default contains one layer of static objects
    """

    def __init__(self):
        # content is a dictionary where {object_type(key): object(value), object(top-left pos corresponding to Menu)
        #                                                                   , object dimension}
        self.mouse_is_on = None
        self.hover = False
        self.request_list = []
        self.command_list = []

    # init function
    def build_layout(self):
        # internal static object cannot fall out of the layer
        # otherwise the code will crash
        col = math.ceil(self.width/GRID_WIDTH)
        row = math.ceil(self.height/GRID_HEIGHT)
        layout = [[None for c in range(col)] for r in range(row)]

        if hasattr(self, "contents"):
            for key, (obj, pos, dim) in self.contents.items():  # O(A)
                if dim == (0, 0):
                    continue
                row_tl, col_tl = find_point_loc(pos, layout)
                dim = dim[0] - GRID_WIDTH, dim[1] - GRID_HEIGHT
                row_br, col_br = find_point_loc(calc_offset(pos, dim), layout)
                assert row_tl <= row_br, "Building layout problem{0}{1}".format(row_tl, row_br)
                assert col_tl <= col_tl, "Building layout problem{0}{1}".format(col_tl, col_br)
                for r in range(row_tl, row_br + 1):
                    for c in range(col_tl, col_br + 1):
                        layout[r][c] = key

            self.layout = layout
        else:
            raise Exception("contents should be created before build_layout method is called, {0}".format(self))

        return None

    # game function
    def run(self, click_command, mouse_pos, offset):  # mouse_pos => abs_mouse_pos
        # handle background commands
        for command in self.get_commands():
            self.handle_command(command)

        # run the static game if self.hover
        rel_mouse_pos = calc_rel_pos(mouse_pos, offset)
        # check hover
        for key, (obj, ref, dim) in self.contents.items():
            if isInside(rel_mouse_pos, calcVertices(ref[0], ref[1], dim[0], dim[1])):
                if self.mouse_is_on != key:
                    if self.mouse_is_on is not None and hasattr(self.contents[self.mouse_is_on][0], "un_hover"):
                        self.contents[self.mouse_is_on][0].un_hover()
                    if hasattr(obj, "do_hover"):
                        obj.do_hover()
                    self.mouse_is_on = key
                break
        else:
            if self.mouse_is_on is not None and hasattr(self.contents[self.mouse_is_on][0], "un_hover"):
                self.contents[self.mouse_is_on][0].un_hover()
            self.mouse_is_on = None

        if click_command == 1:
            if not isInside(rel_mouse_pos, calcVertices(0, 0, self.width, self.height)):
                # return OFF_FOCUS, self
                return RETURN, None
            else:  # otherwise call content button
                if self.mouse_is_on is not None and hasattr(self.contents[self.mouse_is_on][0], "onclick"):
                    obj, ref, dim = self.contents[self.mouse_is_on]
                    new_offset = calc_offset(offset, ref)
                    # when onclick, reset the button to its initial state
                    self.contents[self.mouse_is_on][0].un_hover()  # assert a clickable object must be hoverable
                    self.mouse_is_on = None
                    return obj.onclick(click_command, mouse_pos, new_offset)
        return None, None

    def post_request(self, request):
        self.request_list.append(request)

    def get_requests(self):
        """use a yield generator for scalability"""
        while len(self.request_list) > 0:
            yield self.request_list.pop(0)

    def post_commands(self, commands):
        """can handle either one command or a list of commands"""
        if isinstance(commands, tuple):
            self.command_list.append(commands)
        elif isinstance(commands, list):
            for command in commands:
                self.command_list.append(command)
        else:
            raise Exception("Invalid commands: {0}".format(commands))
        return None

    def get_commands(self):
        """use a yield generator for scalability"""
        for _ in range(len(self.command_list[:])):
            yield self.command_list.pop(0)

    def do_hover(self):
        self.hover = True

    def un_hover(self):
        self.hover = False

    # draw_function
    def draw(self, surface, offset):  # O(n)
        """
        :param surface: pygame.surface
        :param offset: menu's abs top-left pos
        :return: None
        """
        self.draw_bg(surface, offset)
        if hasattr(self, "contents"):
            for name, (obj, rel_pos, dim) in self.contents.items():
                new_offset = calc_offset(offset, rel_pos)
                obj.draw(surface, new_offset)

        if hasattr(self, "objects"):
            for key, objs in self.objects.items():
                for obj in objs:
                    obj.draw(surface, offset)

    def draw_box(self, surface, offset):  # O(n)
        self.draw_box_bg(surface, offset)
        if hasattr(self, "contents"):
            for name, (obj, rel_pos, dim) in self.contents.items():
                new_offset = calc_offset(offset, rel_pos)
                obj.draw_box(surface, new_offset)

        if hasattr(self, "objects"):
            for key, objs in self.objects.items():
                for obj in objs:
                    obj.draw_box(surface, offset)

    def draw_bg(self, surface, offset):
        # fill the layer with theme colored box
        border = 10
        pygame.draw.rect(surface, COLOR_8B4513, (offset[0], offset[1], self.width, self.height), 0)
        pygame.draw.rect(surface, COLOR_FFDEAD, (offset[0]+border, offset[1]+border, self.width-2*border, self.height-2*border), 0)

        return

    def draw_box_bg(self, surface, offset):
        # fill the layer with back bg blue border box
        rect = pygame.Rect(offset, self.dim)
        pygame.draw.rect(surface, BLACK, rect, 0)
        pygame.draw.rect(surface, BLUE, rect, 1)

    # repr function
    def __str__(self):
        out = ""
        for row in self.layout:
            for item in row:
                if item is None:
                    out += '-'
                else:
                    out += item.__str__()[0]
            out += "\n"
        return out
    __repr__ = __str__


class MainMenu(Menu):
    BUTTON_DIM = BUTTON_WIDTH, BUTTON_HEIGHT = MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT
    BUTTON_DISTANCE = MAIN_MENU_BUTTON_DISTANCE
    BUTTON_GAP = MAIN_MENU_BUTTON_GAP
    BUTTON_CUT = BUTTON_X_CUT, BUTTON_Y_CUT = MAIN_MENU_BUTTON_CUT  # How much area not gonna use
    COMMAND_DICT = MAIN_MENU_COMMAND_DICT

    def __init__(self, dim=MAIN_MENU_DIM):
        super(MainMenu, self).__init__()
        self.dim = self.width, self.height = dim
        self.contents = {
            "title": (bt.Text(50, "Main Menu", bold=True, italic=True), (200, 200), (0, 0)),
            "New Game": (bt.NewGame(self.BUTTON_DIM, "New Game",
                                    (LOAD, (LAYER_GAME_PANEL, NEW_GAME_FILE, GAME_PANEL_POS, GAME_PANEL_DIM))),
                         (self.BUTTON_X_CUT + self.BUTTON_DISTANCE, self.BUTTON_Y_CUT + self.BUTTON_GAP),
                         self.BUTTON_DIM),

            "Load Game": (bt.LoadGame(self.BUTTON_DIM, "Load Game",
                                      (LOAD, (LAYER_GAME_PANEL, LOAD_GAME_FILE, GAME_PANEL_POS, GAME_PANEL_DIM))),
                          (self.BUTTON_X_CUT + self.BUTTON_DISTANCE,
                           self.BUTTON_Y_CUT + 2 * self.BUTTON_GAP + self.BUTTON_HEIGHT), self.BUTTON_DIM),

            "Tutorial": (bt.Tutorial(self.BUTTON_DIM, "Tutorial",
                                     (NEW_LAYER, (LAYER_TUTORIAL, LAYER_TUTORIAL, TUTORIAL_POS, TUTORIAL_DIM))),
                         (self.BUTTON_X_CUT + self.BUTTON_DISTANCE,
                          self.BUTTON_Y_CUT + 3 * self.BUTTON_GAP + 2 * self.BUTTON_HEIGHT), self.BUTTON_DIM),

            "Setting": (bt.Setting(self.BUTTON_DIM, "Setting",
                                   (NEW_LAYER, (LAYER_SETTING_MENU, LAYER_SETTING_MENU, SETTING_MENU_POS, SETTING_MENU_DIM))),
                        (self.BUTTON_X_CUT + self.BUTTON_DISTANCE,
                         self.BUTTON_Y_CUT + 4 * self.BUTTON_GAP + 3 * self.BUTTON_HEIGHT), self.BUTTON_DIM),

            "License": (bt.License(self.BUTTON_DIM, "License",
                                   (NEW_LAYER, (LAYER_LICENSE, LAYER_LICENSE, LICENSE_MENU_POS, LICENSE_MENU_DIM))), \
                        (self.BUTTON_X_CUT + self.BUTTON_DISTANCE,
                         self.BUTTON_Y_CUT + 5 * self.BUTTON_GAP + 4 * self.BUTTON_HEIGHT), self.BUTTON_DIM),
        }
        self.build_layout()

    def _main_menu_commands(self, c):
        """No commands is handled here"""
        raise Exception("No commands should falls into this layer: {0}".format(c))

    handle_command = _main_menu_commands


class SettingMenu(Menu):
    """
    key_config: a tuple of the current game setting. i.e (pause_key, newwave_key, return_key, sound_on)
    """
    BUTTON_X_CUT, BUTTON_Y_CUT = 0, 100
    BUTTON_DIM = BUTTON_WIDTH, BUTTON_HEIGHT = 75, 30

    def __init__(self, key_config, dim=SETTING_MENU_DIM):
        super().__init__()
        pause, newwave, retrn, sound_on = key_config
        self.dim = self.width, self.height = dim
        self.contents = {
            "title": (bt.Text(40, "Setting", bold=True, italic=True), (20, 20), (0,0)),
            "PAUSE": (bt.Pause(self.BUTTON_DIM, "Pause",""), (20, 20+self.BUTTON_Y_CUT), self.BUTTON_DIM),
            "pause inp": (bt.SetPause(self.BUTTON_DIM, FULL_REVERSED_KEYBOARD.get(pause, ""), (SET_KEY, PAUSE)),
                          (105, 20+self.BUTTON_Y_CUT), self.BUTTON_DIM),
            "NEW WAVE": (bt.NewWave(self.BUTTON_DIM, "New Wave",""), (220, 20+self.BUTTON_Y_CUT), self.BUTTON_DIM),
            "next wave inp": (bt.SetNewWave(self.BUTTON_DIM, FULL_REVERSED_KEYBOARD.get(newwave, ""), (SET_KEY, NEXT_WAVE)),
                              (305, 20+self.BUTTON_Y_CUT), self.BUTTON_DIM),
            "RETURN": (bt.Return(self.BUTTON_DIM, "Return", ""), (20, 70+self.BUTTON_Y_CUT), self.BUTTON_DIM),
            "return inp": (bt.SetReturn(self.BUTTON_DIM, FULL_REVERSED_KEYBOARD.get(retrn, ""), (SET_KEY, RETURN)),
                           (105, 70+self.BUTTON_Y_CUT), self.BUTTON_DIM),
            "volume": (bt.Volume(self.BUTTON_DIM, "Volume",""), (20, 120+self.BUTTON_Y_CUT), self.BUTTON_DIM),
            "volume inp": (bt.SetVolume((275, 30), sound_on, (SET_VOLUME, None)),
                           (105, 120+self.BUTTON_Y_CUT), (275, 30)),
            "exit": (bt.Exit((100, 40), "Return", (RETURN, None)), (280, 160+self.BUTTON_Y_CUT), (100, 40)),
        }
        self._tem_command_dict = {}
        # self.build_layout()

    def get_set_key(self):
        return self._set_command

    def _in_setting_run(self, click_command, mouse_pos, offset):
        return None, None
    run = Menu.run

    def _setting_menu_commands(self, c):
        # import ver setter
        from game.game import set_var as game_set_var
        from game.inp_devices import set_var as inp_set_var

        command, target = c
        # one cycle
        if command == SET_KEY:
            self._set_command = target
            # initialize keyboard
            self._tem_command_dict = KEYBOARD_COMMAND_DICT
            inp_set_var("KEYBOARD",  FULL_KEY_BOARD)
            game_set_var("KEYBOARD_COMMAND_DICT", {})
            self.run = self._in_setting_run

        # one cycle
        elif command == DONE_SET_KEY:
            new_key = target

            # pop unwanted keys
            for key, command in self._tem_command_dict.items():
                if command == self._set_command:
                    old_key = key
            if locals().get("old_key", False):
                self._tem_command_dict.pop(old_key)
            if new_key in self._tem_command_dict:
                self._tem_command_dict.pop(new_key)

            # update new key/commands
            self._tem_command_dict[new_key] = self._set_command
            inp_set_var("KEYBOARD", self._tem_command_dict.keys())
            game_set_var("KEYBOARD_COMMAND_DICT", self._tem_command_dict)

            # change button display
            reverse_dict = {}
            for key, c in self._tem_command_dict.items():
                reverse_dict[c] = FULL_REVERSED_KEYBOARD[key]
            self.contents["pause inp"][0].change_key(reverse_dict.get(PAUSE, ""))
            self.contents["next wave inp"][0].change_key(reverse_dict.get(NEXT_WAVE, ""))
            self.contents["return inp"][0].change_key(reverse_dict.get(RETURN, ""))
            self.run = super().run

        # one cycle
        elif command == SET_VOLUME:
            self.contents["volume inp"][0].change_key()

        else:
            raise Exception("Invalid command: {0}".format(c))

    handle_command = _setting_menu_commands


class LicenseMenu(Menu):
    # License claim
    line1 = "The MIT License"
    # line2 = "OSI Approved License Logo"
    line3 = "License Copyright: Falcon Lin."
    line4 = "License License: Unknown."
    line5 = "License Contact: falcon.lin.development@gmail.com."
    line6 = "SPDX short identifier: MIT"

    l8 = "Begin license text."
    l9 = "Copyright <2019> <Falcon Lin>"
    l10 = "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and"
    l11 = "associated documentation files (the \"Software\"), to deal in the Software without restriction,"
    l12 = "including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,"
    l13 = "and/or sell copiesof the Software, and to permit persons to whom the Software is furnished to do so,"
    l14 = "subject to the following conditions: The above copyright notice and this permission notice"
    l15 = "shall be included in all copies or substantial portions of the Software."

    l16 = "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,"
    l17 = "INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, "
    l18 = "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. "
    l19 = "IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,"
    l20 = "DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,"
    l21 = " ARISING FROM, OUT OF OR IN CONNECTION WITH "
    l22 = "THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."

    l23 = "End license text."
    TEXT_X_CUT, TEXT_Y_CUT = LICENSE_MENU_POS

    def __init__(self, dim=LICENSE_MENU_DIM):
        super().__init__()
        self.dim = self.width, self.height = dim
        self.contents = {
            "exit": (bt.Exit((100, 40), "Return",(RETURN, None)), (570, 740), (100, 40)),
        }
        self._make_texts()

    def _make_texts(self):
        font40 = pygame.font.SysFont("calibri", 40)
        font30 = pygame.font.SysFont("calibri", 30)
        font20 = pygame.font.SysFont("calibri", 20)
        self.contents[1] = font40.render(self.line1, True, BLUE, None), (20+self.TEXT_X_CUT, 20+self.TEXT_Y_CUT), (0, 0)
        self.contents[3] = font30.render(self.line3, True, BLUE, None), (60+self.TEXT_X_CUT, 60+self.TEXT_Y_CUT), (0, 0)
        self.contents[4] = font30.render(self.line4, True, BLUE, None), (60+self.TEXT_X_CUT, 100+self.TEXT_Y_CUT), (0, 0)
        self.contents[5] = font30.render(self.line5, True, BLUE, None), (60+self.TEXT_X_CUT, 140+self.TEXT_Y_CUT), (0, 0)
        self.contents[6] = font30.render(self.line6, True, BLUE, None), (60+self.TEXT_X_CUT, 180+self.TEXT_Y_CUT), (0, 0)

        self.contents[8] = font20.render(self.l8, True, BLUE, None), (40+self.TEXT_X_CUT, 220+self.TEXT_Y_CUT), (0,0)
        self.contents[9] = font20.render(self.l9, True, BLUE, None), (40+self.TEXT_X_CUT, 250+self.TEXT_Y_CUT), (0, 0)
        self.contents[10] = font20.render(self.l10, True, BLUE, None), (40+self.TEXT_X_CUT, 280+self.TEXT_Y_CUT), (0, 0)
        self.contents[11] = font20.render(self.l11, True, BLUE, None), (40+self.TEXT_X_CUT, 310+self.TEXT_Y_CUT), (0, 0)
        self.contents[12] = font20.render(self.l12, True, BLUE, None), (40+self.TEXT_X_CUT, 340+self.TEXT_Y_CUT), (0, 0)
        self.contents[13] = font20.render(self.l13, True, BLUE, None), (40+self.TEXT_X_CUT, 370+self.TEXT_Y_CUT), (0, 0)
        self.contents[14] = font20.render(self.l14, True, BLUE, None), (40+self.TEXT_X_CUT, 400+self.TEXT_Y_CUT), (0, 0)
        self.contents[15] = font20.render(self.l15, True, BLUE, None), (40+self.TEXT_X_CUT, 430+self.TEXT_Y_CUT), (0, 0)
        self.contents[16] = font20.render(self.l16, True, BLUE, None), (40+self.TEXT_X_CUT, 480+self.TEXT_Y_CUT), (0, 0)
        self.contents[17] = font20.render(self.l17, True, BLUE, None), (40+self.TEXT_X_CUT, 510+self.TEXT_Y_CUT), (0, 0)
        self.contents[18] = font20.render(self.l18, True, BLUE, None), (40+self.TEXT_X_CUT, 540+self.TEXT_Y_CUT), (0, 0)
        self.contents[19] = font20.render(self.l19, True, BLUE, None), (40+self.TEXT_X_CUT, 570+self.TEXT_Y_CUT), (0, 0)
        self.contents[20] = font20.render(self.l20, True, BLUE, None), (40+self.TEXT_X_CUT, 600+self.TEXT_Y_CUT), (0, 0)
        self.contents[21] = font20.render(self.l21, True, BLUE, None), (40+self.TEXT_X_CUT, 630+self.TEXT_Y_CUT), (0, 0)
        self.contents[22] = font20.render(self.l22, True, BLUE, None), (40+self.TEXT_X_CUT, 660+self.TEXT_Y_CUT), (0, 0)
        self.contents[23] = font20.render(self.l23, True, BLUE, None), (560+self.TEXT_X_CUT, 690+self.TEXT_Y_CUT), (0, 0)

    def draw(self, surface, offset):
        super().draw_bg(surface, offset)
        for key, (obj, pos, dim) in self.contents.items():
            if key == "exit":
                new_offset = calc_offset(offset, pos)
                obj.draw(surface, new_offset)
            else:
                surface.blit(obj, pos)

    def draw_box(self, surface, offset):
        super().draw_box_bg(surface, offset)
        for key, (obj, pos, dim) in self.contents.items():
            if key == "exit":
                new_offset = calc_offset(offset, pos)
                obj.draw_box(surface, new_offset)
            else:
                surface.blit(obj, pos)


class TutorialMenu(Menu):
    def __init__(self, dim=TUTORIAL_DIM):
        super().__init__()
        self.dim = self.width, self.height = dim
        self.contents = {
            "exit": (bt.Exit((100, 40), "Return",(RETURN, None)), (580, 740), (100, 40)),
        }


# In game menus
class GameMenu(Menu):
    """
    data: health, money, wave_num
    """
    COMMAND_DICT = IN_GAME_MENU_COMMAND_DICT
    RIGHT_BUTTON_DIM = RIGHT_BUTTON_WIDTH, RIGHT_BUTTON_HEIGHT = 160, 25
    RIGHT_CUT = RIGHT_X_CUT, RIGHT_Y_CUT = IN_GAME_MENU_RIGHT_CUT
    RIGHT_BUTTON_DISTANCE = 20
    RIGHT_BUTTON_GAP = 20

    def __init__(self, data, dim=IN_GAME_MENU_DIM):
        """item has not been well implemented yet"""
        health, money, wave = data
        super(GameMenu, self).__init__()
        self.dim = self.width, self.height = dim
        self.contents = {
            "health bar": (
                bt.HealthBar(IN_GAME_MENU_LEFT_HEALTH_DIM, "Live", health), (20, 820), IN_GAME_MENU_LEFT_HEALTH_DIM),
            "money bar": (bt.MoneyBar(IN_GAME_MENU_LEFT_MONEY_DIM, "Gold", money), (210, 820), IN_GAME_MENU_LEFT_MONEY_DIM),
            "wave bar": (bt.WaveBar(IN_GAME_MENU_LEFT_WAVE_DIM, "Wave", wave), (400, 820), IN_GAME_MENU_LEFT_WAVE_DIM),

            "purchase": (bt.Purchase(IN_GAME_MENU_LEFT_PURCHASE_DIM, "Shop",
                                     (CHANGE_MENU, (LAYER_PURCHASE_MENU, None))),
                         (20, 910), IN_GAME_MENU_LEFT_PURCHASE_DIM),
            "items": (bt.Items(IN_GAME_MENU_LEFT_ITEMS_DIM, "Items", None), (220, 910), IN_GAME_MENU_LEFT_ITEMS_DIM),

            "next wave": (bt.NextWave(self.RIGHT_BUTTON_DIM, "Next Wave", (NEXT_WAVE, None)),
                          (self.RIGHT_X_CUT + self.RIGHT_BUTTON_DISTANCE,
                           self.RIGHT_Y_CUT + self.RIGHT_BUTTON_GAP + 800), self.RIGHT_BUTTON_DIM),
            "save": (bt.SaveGame(self.RIGHT_BUTTON_DIM, "Save Game", (SAVE, None)),
                     (self.RIGHT_X_CUT + self.RIGHT_BUTTON_DISTANCE,
                      self.RIGHT_Y_CUT + 2 * self.RIGHT_BUTTON_GAP + 1 * self.RIGHT_BUTTON_HEIGHT + 800),
                     self.RIGHT_BUTTON_DIM),
            "setting": (bt.Setting(self.RIGHT_BUTTON_DIM, "Setting",
                                   (NEW_LAYER, (LAYER_SETTING_MENU, LAYER_SETTING_MENU, SETTING_MENU_POS, SETTING_MENU_DIM))),
                        (self.RIGHT_X_CUT + self.RIGHT_BUTTON_DISTANCE,
                         self.RIGHT_Y_CUT + 3 * self.RIGHT_BUTTON_GAP + 2 * self.RIGHT_BUTTON_HEIGHT + 800),
                        self.RIGHT_BUTTON_DIM),
            "exit": (bt.Exit(self.RIGHT_BUTTON_DIM, "Return", (RETURN_FROM_GAME, None)),
                     (self.RIGHT_X_CUT + self.RIGHT_BUTTON_DISTANCE,
                      self.RIGHT_Y_CUT + 4 * self.RIGHT_BUTTON_GAP + 3 * self.RIGHT_BUTTON_HEIGHT + 800),
                     self.RIGHT_BUTTON_DIM),
        }


class PurchaseMenu(Menu):
    BUTTON_DIM = BUTTON_WIDTH, BUTTON_HEIGHT = 136, 60
    BUTTON_DISTANCE = 20
    BUTTON_GAP = 20
    BUTTON_X_CUT, BUTTON_Y_CUT = 0, 800
    COMMAND_DICT = PURCHASE_COMMAND_DICT

    def __init__(self, dim=PURCHASE_MENU_DIM):
        super().__init__()
        self.dim = self.width, self.height = dim
        self.contents = {
            "DMG Tower Lv1": (bt.DMGTower(self.BUTTON_DIM, "DMG Tower Lv1", (PURCHASE, DMG_TOWER)), \
                              (self.BUTTON_X_CUT + self.BUTTON_DISTANCE, self.BUTTON_Y_CUT + self.BUTTON_GAP),
                              self.BUTTON_DIM),
            "CC Tower Lv1": (bt.CCTower(self.BUTTON_DIM, "Ranged Tower Lv1", (PURCHASE, CC_TOWER)), \
                             (self.BUTTON_X_CUT + 2 * self.BUTTON_DISTANCE + self.BUTTON_WIDTH,
                              self.BUTTON_Y_CUT + self.BUTTON_GAP), self.BUTTON_DIM),
            "exit": (bt.Exit((100, 40), "Return",(CHANGE_MENU, (LAYER_IN_GAME_MENU, None))), (680, 940), (100, 40)),
        }


class TowerMenu(Menu):
    """resizable frame will be implemented
    data: image, display_name, lv, cost, dmg, acckfreq, tower_range, level_up_cost, loc
    """
    COMMAND_DICT = TOWER_MENU_COMMAND_DICT
    BUTTON_GAP = 10
    BUTTON_DISTANCE = 10

    def __init__(self, data, dim=TOWER_MENU_DIM):
        super().__init__()
        self.dim = self.width, self.height = dim
        image, display_name, lv, cost, dmg, acckfreq, tower_range, level_up_cost, loc = data
        self.contents = {
            "icon": (bt.TowerIcon((160, 160), "Tower_img", image)
                     , (20, 820), (160, 160)),
            "name": (bt.TowerName((380, 50), "name", display_name),
                     (210, 810), (280, 50)),
            "LV": (bt.TowerLV((185, 33), "LV", lv),
                   (210, 870), (185, 33)),
            "cost": (bt.TowerCost((185, 33), "Tower Cost", cost),
                     (405, 870), (185, 33)),
            "dmg": (bt.TowerDmg((185, 33), "Tower Dmg", dmg),
                    (210, 913), (185, 33)),
            "acckfreq": (bt.TowerAcckFreq((185, 33), "Tower attk freq", acckfreq),
                         (405, 913), (185, 33)),
            "item": (bt.TowerItems((185, 33),"Tower items", None),
                     (210, 956), (185, 33)),
            "range": (bt.TowerRange((185, 33), "Range", tower_range),
                      (405, 956), (185, 33)),
            "level up cost": (bt.TowerLevelUp((160, 120), level_up_cost, (LEVEL_UP, (level_up_cost, loc))),
                              (620, 820), (160, 120)),
            "exit": (bt.Exit((100, 40),"return", (CHANGE_MENU, (LAYER_IN_GAME_MENU, None))),
                     (680, 940), (100, 40)),
        }

class ItemCommandMenu(Menu):
    def __init__(self):
        pass








