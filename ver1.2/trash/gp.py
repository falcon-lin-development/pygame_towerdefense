"""
Loader
Gamepanel

Developer Note:
1) towers can be overlapping
"""
from config import *
from menu import GameMenu, SettingMenu, LicenseMenu, Menu, PurchaseMenu, TutorialMenu, TowerMenu
from functions import calc_offset, calc_rel_pos
from world import Map
import pygame


def loader(file):
    if file == "setting":
        return SettingMenu(SETTING_MENU_DIM)
    elif file == "license":
        return LicenseMenu(LICENSE_MENU_DIM)
    elif file == "tutorial":
        return Tutorial(TUTORIAL_DIM)
    else:
        game_panel = GamePanel()
        game_panel.load_game(file)
        return game_panel


class GamePanel(Menu):
    """
    Game Panel will be a general version of Menu which can contains multi-layers
    and dynamic objects
    """
    MENU_CUT = MENU_X_CUT, MENU_Y_CUT = GAME_PANEL_IN_GAME_MENU_CUT  # How much area not gonna use
    MENU_REF = MENU_CUT
    COMMAND_DICT = {**GAME_PANEL_COMMAND_DICT, **IN_GAME_MENU_COMMAND_DICT, **MAP_COMMAND_DICT,
                    **PURCHASE_COMMAND_DICT, **TOWER_MENU_COMMAND_DICT}

    def __init__(self):
        super().__init__()

    # initialization
    def load_game(self, data_file, dim=GAME_PANEL_DIM):
        map_data, menu_data = self._process(data_file)
        print("initializing...")
        super(GamePanel, self).__init__()
        self.dim = self.width, self.height = dim
        self.contents = {
            "map": (Map(map_data, MAP_DIM), MAP_REF, MAP_DIM),
            "game menu": (GameMenu(menu_data, IN_GAME_MENU_DIM), self.MENU_REF, IN_GAME_MENU_DIM),
        }
        self.build_layout()
        print("game initialized.")

    def _process(self, file):
        towers = []
        menu = []
        with open(file) as f:
            for i, line in enumerate(f.readlines()):
                if i <= 2:
                    menu.append(int(line.strip()))
                else:
                    tower_name, tower_type, x, y, level = line.strip(" ").split(" ")
                    towers.append((tower_name, int(tower_type), (int(x), int(y)), int(level)))

        return towers, menu

    def save_game(self):
        towers = self.contents["map"][0].get_data()
        info = health, money, wave_num = self.contents["game menu"][0].get_data()
        assert isinstance(health, int)
        assert isinstance(money, int)
        assert isinstance(wave_num, int)
        assert isinstance(towers, list)
        with open("./data/saved_game.txt", "w+") as f:
            # could be buggy
            for n in info:
                f.write("{0}\n".format(n))
            for name, tower_type, pos, level in towers:
                f.write("{0} {1} {2} {3} {4}".format(name, tower_type, pos[0], pos[1], level))
        return True

    # game function
    def run(self, mouse_pos, offset):
        # get request from children
        for key, (obj, ref, dim) in self.contents.items():
            for request in obj.get_requests():
                self.post_commands(request)

        # handle all requests && run static hovers
        super(GamePanel, self).run(mouse_pos, offset)

        # Menu runs only if is hovered
        obj, ref, dim = self.contents["game menu"]
        if hasattr(obj, "hover") and obj.hover:
            new_offset = calc_offset(offset, ref)
            obj.run(mouse_pos, new_offset)

        # Map runs anyway
        obj, ref, dim = self.contents["map"]
        new_offset = calc_offset(offset, ref)
        obj.run(mouse_pos, new_offset)
        return True

    # command handler
    def _game_panel_commands(self, c: tuple) -> None:
        """
WIN = 100
LOST = 101
SELECTED = 102

NEXT_WAVE = 99
# SAVE_GAME = 98
PAUSE = 97
SETTING = 96
EXIT = 95
PURCHASE_MENU = 94
ITEMS = 93

GET_HIT = 89  # called when a creep reached goal tile
MAKE_CREEP = 88  # this one is specially handled in layer

PURCHASE = 79

TOWER_MENU = 69
LEVEL_UP = 68
        :return:
        """
        command, target = c
        # game panel
        if command == WIN:
            pass
        elif command == LOST:
            self.do_pause()
            print("gg well played")
        elif command == SELECTED:
            tower_type, ref = target
            if tower_type == CC_TOWER:
                price = CC_TOWER_LV1[0]
            else:
                price = DMG_TOWER_LV1[0]
            self.contents["game menu"][0].can_and_buy(price)
            self.contents["map"][0].create_tower(tower_type, ref)
        # in game menu
        elif command == NEXT_WAVE:
            self.contents["game menu"][0].contents["wave bar"][0].v += 1
            wave_num = self.contents["game menu"][0].get_wave_num()
            self.contents["map"][0].next_wave(wave_num)
        # elif command == SAVE_GAME:
        #     pass
        elif command == PAUSE:
            self.contents["map"][0].do_pause()
        elif command == SETTING:
            self.post_request((LOAD, target))
        elif command == EXIT:
            self.post_request((RETURN, target))
        elif command == PURCHASE_MENU:
            name, ref, dim = target
            layer = PurchaseMenu(dim)
            self.post_request((NEW_LAYER, (name, layer, ref, dim)))
        elif command == ITEMS:
            pass
        # map
        elif command == GET_HIT:
            still_alive = self.contents["game menu"][0].hit()
            if not still_alive:
                self.post_commands((LOST, None))
        # purchasing go to select mode
        elif command == PURCHASE:
            if target == CC_TOWER:
                price = CC_TOWER_LV1[0]
            elif target == DMG_TOWER:
                price = DMG_TOWER_LV1[0]
            else:
                raise Exception("Invalid tower type: {0}".format(target))
            if self.contents["game menu"][0].get_money() >= price:
                self.post_request((NEW_LAYER, (LAYER_SELECTION, Select_mode(target), MAP_REF, MAP_DIM)))
        # tower
        elif command == TOWER_MENU:
            # could be buggy once the frame changed
            mouse_pos, offset, tower_data = target
            # calculating how will the layer present
            x, y = mouse_pos
            if x <= SCREEN_WIDTH//2 and y <= SCREEN_HEIGHT//2:  # TL
                mouse_pos = x, y
            elif x <= SCREEN_WIDTH//2 and y >= SCREEN_HEIGHT//2:  # BL
                mouse_pos = x, y - TOWER_MENU_DIM[1]
            elif x >= SCREEN_WIDTH//2 and y <= SCREEN_HEIGHT//2:  # TR
                mouse_pos = x - TOWER_MENU_DIM[0], y
            elif x >= SCREEN_WIDTH // 2 and y >= SCREEN_HEIGHT // 2:  # BR
                mouse_pos = x - TOWER_MENU_DIM[0], y - TOWER_MENU_DIM[1]
            else:
                raise Exception("Invalid pos: {0}".format(mouse_pos))
            self.post_request((NEW_LAYER, (LAYER_TOWER_MENU, TowerMenu(tower_data), mouse_pos, TOWER_MENU_DIM)))
        # tower menu
        elif command == LEVEL_UP:
            upgrade_cost, loc = target
            if self.contents["game menu"][0].can_and_buy(upgrade_cost):
                game_map = self.contents["map"][0]
                tower_ID = game_map.layout[loc[0]][loc[1]]
                game_map.contents[tower_ID][0].levelUp()

        else:
            raise Exception("Invalid command: {0}".format(c))

    handle_command = _game_panel_commands

    def do_pause(self):
        self.post_commands((PAUSE, None))

    def next_wave(self):
        self.post_commands((NEXT_WAVE, None))

    # representation funciton
    def __str__(self):
        out = ""
        for key, (obj, ref, dim) in self.contents.items():
            for row in obj.layout:
                for c in row:
                    if c is None:
                        out += "-"
                    else:
                        out += c.__str__()[0]
                out += "\n"
        return out
    __repr__ = __str__


class Select_mode(GamePanel):
    def __init__(self, target):
        super().__init__()
        self.selected = target

    def run(self, mouse_pos, offset):
        pass

    def do_onclick(self, click_command, mouse_pos, offset):
        """just to return the last click then done of the layer"""
        rel_mouse_pos = calc_rel_pos(mouse_pos, offset)
        return [(RETURN, None), (SELECTED, (self.selected, rel_mouse_pos))]
    onclick = do_onclick

    def draw(self, surface, offset):
        pass

    def draw_box(self, surface, offset):
        pass

    def draw_bg(self, surface, offset):
        pass

    def draw_box_bg(self, surface, offset):
        pass


Tutorial = TutorialMenu

