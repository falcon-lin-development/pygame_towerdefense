"""define all Menu here
including MainMenu, GameMenu and Purchasing Menu

## possibly putting the game things onto this menu abstraction

Developer note
done 1) button implementation
2) setting
3) license
4) tutorial
5) hover checking duplicates here / may put it to the game run

"""
from functions import isInside, calcVertices, save_load_image
from functions import calc_rel_pos, find_point_loc, calc_offset
import math
import button as bt
import pygame
import queue
from config import *


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
        # inside static object cannot fo out of the layer
        # otherwise the code will crash
        col = math.ceil(self.width/GRID_WIDTH)
        row = math.ceil(self.height/GRID_HEIGHT)
        layout = [[None for c in range(col)] for r in range(row)]

        if hasattr(self, "contents"):
            for key, (obj, pos, dim) in self.contents.items():  # O(A)
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
    def onclick(self, click_command, mouse_pos, offset): # mouse_pos => abs_mouse_pos
        # process mouse_pos
        # assert dynamic object will not have click option
        rel_mouse_pos = calc_rel_pos(mouse_pos, offset)
        if click_command == 2:
            return None, None
        elif rel_mouse_pos[0] < 0 or rel_mouse_pos[1] < 0 or rel_mouse_pos[0] > self.width or rel_mouse_pos[1] > self.height:
            # return OFF_FOCUS, self
            return RETURN, None
        else:  # otherwise call content button
            row, col = find_point_loc(rel_mouse_pos, self.layout)
            # return one command/ one list of commands
            # recursive call until we see a button
            if self.layout[row][col] in self.contents:
                obj, ref, dim = self.contents[self.layout[row][col]]
                if hasattr(obj, "onclick"):
                    new_offset = calc_offset(offset, ref)
                    return obj.onclick(click_command, mouse_pos, new_offset)

        return None, None

    def run(self, mouse_pos, offset):
        # handle background commands
        for command in self.get_commands():
            self.handle_command(command)

        # run the static game if self.hover
        rel_mouse_pos = calc_rel_pos(mouse_pos, offset)
        # check hover
        if isInside(rel_mouse_pos, calcVertices(0, 0, self.width, self.height)):
            self.do_hover()
        else:
            self.un_hover()

        if self.hover:
            row, col = find_point_loc(rel_mouse_pos, self.layout)
            key = self.layout[row][col]
            if key:
                target, ref, dim = self.contents[key]
            else:
                target = key
            if target is not self.mouse_is_on:
                # swap mouse is on and change hover states
                if hasattr(self.mouse_is_on, "un_hover"):
                    self.mouse_is_on.un_hover()
                self.mouse_is_on = target
                if hasattr(self.mouse_is_on, "do_hover"):
                    self.mouse_is_on.do_hover()

        return True

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
        while len(self.command_list) > 0:
            yield self.command_list.pop(0)

    def do_hover(self):
        self.hover = True

    def un_hover(self):
        self.hover = False

    # draw_function
    def draw(self, surface, offset):  # O(n)
        """
        :param surface: pygame.surface
        :param offset: menu_abs_pos/ rel_pos = objs pos relative to the menu
        :return:
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
        """all self make image will have a reference point"""
        if hasattr(self, "image"):
            if isinstance(self.image, tuple):
                # fill the layer with back color
                rect = pygame.Rect(offset, self.dim)
                pygame.draw.rect(surface, BLACK, rect, 0)
                #  blit the blue text
                img, rel_pos = self.image
                ofs = calc_offset(offset, rel_pos)
                surface.blit(img, ofs)
            else:
                surface.blit(self.image, offset)
        else:
            # fill the layer with back color
            rect = pygame.Rect(offset, self.dim)
            pygame.draw.rect(surface, BLACK, rect, 0)
        return

    def draw_box_bg(self, surface, offset):
        self.draw_bg(surface, offset)

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
            "New Game": (bt.NewGame(self.BUTTON_DIM,
                                    (LOAD, (LAYER_GAME_PANEL, NEW_GAME_FILE, GAME_PANEL_POS, GAME_PANEL_DIM))),
                         (self.BUTTON_X_CUT + self.BUTTON_DISTANCE, self.BUTTON_Y_CUT + self.BUTTON_GAP),
                         self.BUTTON_DIM),

            "Load Game": (bt.LoadGame(self.BUTTON_DIM,
                                      (LOAD, (LAYER_GAME_PANEL, LOAD_GAME_FILE, GAME_PANEL_POS, GAME_PANEL_DIM))),
                          (self.BUTTON_X_CUT + self.BUTTON_DISTANCE,
                           self.BUTTON_Y_CUT + 2 * self.BUTTON_GAP + self.BUTTON_HEIGHT), self.BUTTON_DIM),

            "Tutorial": (bt.Tutorial(self.BUTTON_DIM,
                                     (LOAD, (LAYER_TUTORIAL, TUTORIAL_GAME_FILE, TUTORIAL_POS, TUTORIAL_DIM))),
                         (self.BUTTON_X_CUT + self.BUTTON_DISTANCE,
                          self.BUTTON_Y_CUT + 3 * self.BUTTON_GAP + 2 * self.BUTTON_HEIGHT), self.BUTTON_DIM),

            "Setting": (bt.Setting(self.BUTTON_DIM,
                                   (LOAD, (LAYER_SETTING_MENU, SETTING_FILE, SETTING_MENU_POS, SETTING_MENU_DIM))),
                        (self.BUTTON_X_CUT + self.BUTTON_DISTANCE,
                         self.BUTTON_Y_CUT + 4 * self.BUTTON_GAP + 3 * self.BUTTON_HEIGHT), self.BUTTON_DIM),

            "License": (bt.License(self.BUTTON_DIM,
                                   (LOAD, (LAYER_LICENSE, LICENSE_FILE, LICENSE_MENU_POS, LICENSE_MENU_DIM))), \
                        (self.BUTTON_X_CUT + self.BUTTON_DISTANCE,
                         self.BUTTON_Y_CUT + 5 * self.BUTTON_GAP + 4 * self.BUTTON_HEIGHT), self.BUTTON_DIM),
        }
        self.build_layout()
        self.image = save_load_image(self, MAIN_MENU_BG_IMG)

    def _main_menu_commands(self, c):
        """
        NEW_GAME = 99
LOAD_GAME = 98
TUTORIAL = 97
SETTING = 96
LICENSE = 95
        :param c:
        :return:
        """
        command, target = c
        if command == NEW_GAME:
            self.post_request((LOAD, target))
        elif command == LOAD_GAME:
            self.post_request((LOAD, target))
        elif command == TUTORIAL:
            self.post_request((LOAD, target))
        elif command == SETTING:
            self.post_request((LOAD, target))
        elif command == LICENSE:
            self.post_request((LOAD, target))
        else:
            raise Exception("Invalid main_menu_command: {0}".format(command))
        return None

    handle_command = _main_menu_commands

    def make_image(self):
        font = pygame.font.SysFont("calibri", 40, True, True)
        return font.render("Main Menu", True, (0, 0, 255), None), (40, 20)


class PurchaseMenu(Menu):
    BUTTON_DIM = BUTTON_WIDTH, BUTTON_HEIGHT = PURCHASE_MENU_BUTTON_WIDTH, PURCHASE_MENU_BUTTON_HEIGHT
    BUTTON_DISTANCE = PURCHASE_MENU_BUTTON_DISTANCE
    BUTTON_GAP = PURCHASE_MENU_BUTTON_GAP
    BUTTON_X_CUT, BUTTON_Y_CUT = PURCHASE_MENU_BUTTON_CUT
    COMMAND_DICT = PURCHASE_COMMAND_DICT

    def __init__(self, dim=PURCHASE_MENU_DIM):
        super().__init__()
        self.dim = self.width, self.height = dim
        self.contents = {
            "DMG Tower Lv1": (bt.Dmg_tower_b(self.BUTTON_DIM, (PURCHASE, DMG_TOWER)), \
                              (self.BUTTON_X_CUT + self.BUTTON_DISTANCE, self.BUTTON_Y_CUT + self.BUTTON_GAP),
                              self.BUTTON_DIM),
            "CC Tower Lv1": (bt.Cc_tower_b(self.BUTTON_DIM, (PURCHASE, CC_TOWER)), \
                             (self.BUTTON_X_CUT + 2 * self.BUTTON_DISTANCE + self.BUTTON_WIDTH,
                              self.BUTTON_Y_CUT), self.BUTTON_DIM),
        }
        self.build_layout()

    # command handler
    def _purchase_menu_commands(self, c):
        """Do not handle any commands here but to the game panel layer"""
        # need clear testing
        self.post_request((RETURN, None))
        self.post_request(c)
        return None

    handle_command = _purchase_menu_commands


class TowerMenu(Menu):
    """resizable frame will be implemented"""
    COMMAND_DICT = TOWER_MENU_COMMAND_DICT
    BUTTON_GAP = 10
    BUTTON_DISTANCE = 10

    def __init__(self, data, dim=TOWER_MENU_DIM):
        super().__init__()
        self.dim = self.width, self.width = dim
        image, display_name, lv, cost, dmg, acckfreq, tower_range, level_up_cost, loc = data
        self.contents = {
            "icon": (bt.TowerIcon((40, 40), image), (10, 10), (40, 40)),
            "name": (bt.TowerName((130, 40), display_name), (60, 10), (130, 40)),
            "LV": (bt.TowerLV((80, 20), lv), (10, 60), (80, 20)),
            "cost": (bt.TowerCost((80, 20), cost), (110, 60), (80, 20)),
            "dmg": (bt.TowerDmg((80, 20), dmg), (10, 90), (80, 20)),
            "acckfreq": (bt.TowerAcckFreq((80, 20), acckfreq), (10, 90), (80, 20)),
            "item": (bt.TowerItems((80, 20), None), (10, 120), (80, 20)),
            "range": (bt.TowerRange((80, 20), tower_range), (110, 120), (80, 20)),
            "level up cost": (bt.TowerLevelUp((180, 40), level_up_cost, (LEVEL_UP, (level_up_cost, loc))),
                              (10, 150), (180, 40)),
        }

    # command handler
    def _tower_menu_commands(self, c):
        """Do not handle any commands here but to the game panel layer"""
        # need clear testing
        self.post_request((RETURN, None))
        self.post_request(c)
        return None

    handle_command = _tower_menu_commands


class ItemInfoMenu(Menu):
    def __init__(self):
        pass


class ItemCommandMenu(Menu):
    def __init__(self):
        pass


class TutorialMenu(Menu):
    def __init__(self, dim):
        pass


class SettingMenu(Menu):
    def __init__(self, dim):
        pass


class LicenseMenu(Menu):
    def __init__(self, dim):
        pass


# class GameMenu(Menu):
#     COMMAND_DICT = IN_GAME_MENU_COMMAND_DICT
#     RIGHT_BUTTON_DIM = RIGHT_BUTTON_WIDTH, RIGHT_BUTTON_HEIGHT = 160, 25
#     RIGHT_CUT = RIGHT_X_CUT, RIGHT_Y_CUT = IN_GAME_MENU_RIGHT_CUT
#     RIGHT_BUTTON_DISTANCE = 20
#     RIGHT_BUTTON_GAP = 20
#
#     def __init__(self, data, dim=IN_GAME_MENU_DIM):
#         """item has not been well implemented yet"""
#         health, money, wave = data
#         super(GameMenu, self).__init__()
#         self.dim = self.width, self.height = dim
#         self.contents = {
#             "health bar": (bt.HealthBar(IN_GAME_MENU_LEFT_HEALTH_DIM, health), (20, 20), IN_GAME_MENU_LEFT_HEALTH_DIM),
#             "money bar": (bt.MoneyBar(IN_GAME_MENU_LEFT_MONEY_DIM, money), (210, 20), IN_GAME_MENU_LEFT_MONEY_DIM),
#             "wave bar": (bt.WaveBar(IN_GAME_MENU_LEFT_WAVE_DIM, wave), (400, 20), IN_GAME_MENU_LEFT_WAVE_DIM),
#
#             "purchase": (bt.Purchase(IN_GAME_MENU_LEFT_PURCHASE_DIM,
#                                      (PURCHASE_MENU, (LAYER_PURCHASE_MENU, PURCHASE_MENU_ABS_POS, PURCHASE_MENU_DIM))),
#                          (20, 110), IN_GAME_MENU_LEFT_PURCHASE_DIM),
#             "items": (bt.Items(IN_GAME_MENU_LEFT_ITEMS_DIM, None), (220, 110), IN_GAME_MENU_LEFT_ITEMS_DIM),
#
#
#             "next wave": (bt.NextWave(self.RIGHT_BUTTON_DIM, (NEXT_WAVE, None)),
#                           (self.RIGHT_X_CUT + self.RIGHT_BUTTON_DISTANCE,
#                            self.RIGHT_Y_CUT + self.RIGHT_BUTTON_GAP), self.RIGHT_BUTTON_DIM),
#             "save": (bt.SaveGame(self.RIGHT_BUTTON_DIM, (SAVE, None)),
#                      (self.RIGHT_X_CUT + self.RIGHT_BUTTON_DISTANCE,
#                       self.RIGHT_Y_CUT + 2 * self.RIGHT_BUTTON_GAP + 1 * self.RIGHT_BUTTON_HEIGHT),
#                      self.RIGHT_BUTTON_DIM),
#             "setting": (bt.Setting(self.RIGHT_BUTTON_DIM,
#                                    (LOAD, (LAYER_SETTING_MENU, SETTING_FILE, SETTING_MENU_POS, SETTING_MENU_DIM))),
#                         (self.RIGHT_X_CUT + self.RIGHT_BUTTON_DISTANCE,
#                          self.RIGHT_Y_CUT + 3 * self.RIGHT_BUTTON_GAP + 2 * self.RIGHT_BUTTON_HEIGHT),
#                         self.RIGHT_BUTTON_DIM),
#             "exit": (bt.Exit(self.RIGHT_BUTTON_DIM, (RETURN, None)),
#                      (self.RIGHT_X_CUT + self.RIGHT_BUTTON_DISTANCE,
#                       self.RIGHT_Y_CUT + 4 * self.RIGHT_BUTTON_GAP + 3 * self.RIGHT_BUTTON_HEIGHT),
#                      self.RIGHT_BUTTON_DIM),
#         }
#         self.build_layout()
#
#     # initialization
#     def get_data(self):
#         return [self.get_health(), self.get_money(), self.get_wave_num()]
#
#     def get_health(self):
#         return self.contents["health bar"][0].get_value()
#
#     def get_money(self):
#         return self.contents["money bar"][0].get_value()
#
#     def get_wave_num(self):
#         return self.contents["wave bar"][0].get_value()
#
#     # game function
#     def done(self):
#         return self.get_health() <= 0
#
#     def hit(self):
#         self.contents["health bar"][0].hit()
#         if self.done():
#             return False
#         else:
#             return True
#
#     def can_and_buy(self, price):
#         if self.get_money() >= price:
#             self.contents["money bar"][0].pay(price)
#             return True
#         return False