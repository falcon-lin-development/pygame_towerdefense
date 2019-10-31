"""
Loader
Gamepanel

Developer Note:
1) towers can be overlapping
done 2) simplify structure
"""
from config import *
from menu import SettingMenu, LicenseMenu, Menu, PurchaseMenu, TutorialMenu, TowerMenu, MainMenu
from tower import construct_tower
from creep import construct_creep
from functions import calc_offset, calc_rel_pos, find_point_loc, isInside, calcVertices, save_load_image
from functions import calcAlignCenter, find_grid_pos, calc_abs_pos
import button as bt
import pygame
import queue


def loader(file):
    if file == "setting":
        return SettingMenu(SETTING_MENU_DIM)
    elif file == "license":
        return LicenseMenu(LICENSE_MENU_DIM)
    elif file == "tutorial":
        return TutorialMenu(TUTORIAL_DIM)
    else:
        game_panel = GamePanel()
        game_panel.load_game(file)
        return game_panel


class GamePanel(Menu):
    """
    map_data:
    dim:
    map_file: map + creepPath
    wave_file: creep wave
    load_file: player data
    """
    MENU_CUT = MENU_X_CUT, MENU_Y_CUT = GAME_PANEL_IN_GAME_MENU_CUT  # How much area not gonna use
    MENU_REF = MENU_CUT
    COMMAND_DICT = {**GAME_PANEL_COMMAND_DICT, **IN_GAME_MENU_COMMAND_DICT, **MAP_COMMAND_DICT,
                    **PURCHASE_COMMAND_DICT, **TOWER_MENU_COMMAND_DICT}

    RIGHT_BUTTON_DIM = RIGHT_BUTTON_WIDTH, RIGHT_BUTTON_HEIGHT = 160, 25
    RIGHT_CUT = RIGHT_X_CUT, RIGHT_Y_CUT = IN_GAME_MENU_RIGHT_CUT
    RIGHT_BUTTON_DISTANCE = 20
    RIGHT_BUTTON_GAP = 20
    tower_ID = 1

    def __init__(self, dim=(800, 1000), map_file=GAME_MAP, wave_file=GAME_WAVE):
        # build basic
        print("Initializing game")
        super().__init__()
        self.dim = self.width, self.height = dim
        self.contents = {
            "health bar": (
                bt.HealthBar(IN_GAME_MENU_LEFT_HEALTH_DIM, 0), (20, 820), IN_GAME_MENU_LEFT_HEALTH_DIM),
            "money bar": (bt.MoneyBar(IN_GAME_MENU_LEFT_MONEY_DIM, 0), (210, 820), IN_GAME_MENU_LEFT_MONEY_DIM),
            "wave bar": (bt.WaveBar(IN_GAME_MENU_LEFT_WAVE_DIM, 0), (400, 820), IN_GAME_MENU_LEFT_WAVE_DIM),

            "purchase": (bt.Purchase(IN_GAME_MENU_LEFT_PURCHASE_DIM,
                                     (PURCHASE_MENU,
                                      (LAYER_PURCHASE_MENU, PURCHASE_MENU_ABS_POS, PURCHASE_MENU_DIM))),
                         (20, 910), IN_GAME_MENU_LEFT_PURCHASE_DIM),
            "items": (bt.Items(IN_GAME_MENU_LEFT_ITEMS_DIM, None), (220, 910), IN_GAME_MENU_LEFT_ITEMS_DIM),

            "next wave": (bt.NextWave(self.RIGHT_BUTTON_DIM, (NEXT_WAVE, None)),
                          (self.RIGHT_X_CUT + self.RIGHT_BUTTON_DISTANCE,
                           self.RIGHT_Y_CUT + self.RIGHT_BUTTON_GAP + 800), self.RIGHT_BUTTON_DIM),
            "save": (bt.SaveGame(self.RIGHT_BUTTON_DIM, (SAVE, None)),
                     (self.RIGHT_X_CUT + self.RIGHT_BUTTON_DISTANCE,
                      self.RIGHT_Y_CUT + 2 * self.RIGHT_BUTTON_GAP + 1 * self.RIGHT_BUTTON_HEIGHT + 800),
                     self.RIGHT_BUTTON_DIM),
            "setting": (bt.Setting(self.RIGHT_BUTTON_DIM,
                                   (LOAD, (LAYER_SETTING_MENU, SETTING_FILE, SETTING_MENU_POS, SETTING_MENU_DIM))),
                        (self.RIGHT_X_CUT + self.RIGHT_BUTTON_DISTANCE,
                         self.RIGHT_Y_CUT + 3 * self.RIGHT_BUTTON_GAP + 2 * self.RIGHT_BUTTON_HEIGHT + 800),
                        self.RIGHT_BUTTON_DIM),
            "exit": (bt.Exit(self.RIGHT_BUTTON_DIM, (RETURN_FROM_GAME, None)),
                     (self.RIGHT_X_CUT + self.RIGHT_BUTTON_DISTANCE,
                      self.RIGHT_Y_CUT + 4 * self.RIGHT_BUTTON_GAP + 3 * self.RIGHT_BUTTON_HEIGHT + 800),
                     self.RIGHT_BUTTON_DIM),
        }
        self.objects = {
            "creeps": [],
            "bullets": [],
            "towers": []
        }
        self.pause = False
        # load data
        self._load_map(map_file)
        self._load_wave(wave_file)
        self.build_layout()
        print("game initialized")

    # initialization
    def _load_map(self, file):
        """
GRASS = '0'
PATH_H = '1'
PATH_V = '2'
TURN_TL = '3'
TURN_TR = '4'
TURN_BL = '5'
TURN_BR = '6'

SPAWN = 's'
GOAL = 'g'
PATH_SIDE = '-'
BOARDER = 'x'
        :param map: txt
        :return: [(x0, y0), (x1, y1), ...] xi, yi is rel_center
        """
        print("initializing map...")
        _map = []
        row = []
        path = 0

        # draw map
        with open(file) as f:  # O(A)
            data = f.read().split("##########\n")
            if len(data) == 1:
                map_info, creepPath_info = data[0], None
            elif len(data) == 2:
                map_info, creepPath_info = data
            else:
                raise Exception("Invalid Map file: {0}".format(file))

            for c in map_info:
                if c == '\n':
                    _map.append(row)
                    row = []
                else:
                    if c == SPAWN:
                        row_num = len(_map)
                        col_num = len(row)
                        start = row_num, col_num
                        path += 1
                    elif c == GOAL:
                        end = len(_map), len(row)
                        path += 1
                    elif c in [TURN_TL, TURN_TR, TURN_BL, TURN_BR]:
                        path += 1
                    row.append(c)

        # find creepPath (trace algorithm)
        if creepPath_info:
            cp = creepPath_info.strip().split("\n")
            creepPath = []
            for x in cp:
                cen_x, cen_y = x.split()
                creepPath.append((int(cen_x), int(cen_y)))
            assert find_point_loc(creepPath[0], None) == start
            assert find_point_loc(creepPath[-1], None) == end

        else:  # (trace algorithm)
            creepPath = [start]
            pathway = [start]
            current = start
            while len(creepPath) < path:  # O(l)
                row, col = current
                t_row, t_col = row - 1, col
                r_row, r_col = row, col + 1
                b_row, b_col = row + 1, col
                l_row, l_col = row, col - 1
                neighbors = [(t_row, t_col), (r_row, r_col), (b_row, b_col), (l_row, l_col)]
                for grid_row, grid_col in neighbors:
                    if (grid_row, grid_col) not in pathway:
                        grid = _map[grid_row][grid_col]
                        if grid in [PATH_H, PATH_V]:
                            current = grid_row, grid_col
                            pathway.append(current)
                            break
                        elif grid in [TURN_TL, TURN_TR, TURN_BL, TURN_BR, GOAL]:
                            current = grid_row, grid_col
                            creepPath.append(current)
                            pathway.append(current)
                            break
                else:
                    raise Exception(
                        "Invalid map configuration: current{0}, \ncreepPath{1}".format(current, creepPath))
            assert creepPath[-1] == end, "creep path is not correctly calculated: {0}|{1}".format(creepPath, end)

            # calc rel centers
            for index, (row, col) in enumerate(creepPath[:]):
                creepPath[index] = calcAlignCenter(find_grid_pos((row, col), _map), GRID_DIM)

            # write the result back to the file
            with open(file, "a") as f:
                f.write("##########\n")
                for cen_x, cen_y in creepPath:
                    f.write("{0} {1}\n".format(cen_x, cen_y))

        print("map initialized.")

        self.map = _map
        self.creepPath = creepPath
        return

    def _load_wave(self, file):
        print("Initializing creeps...")
        waves = []
        with open(file, "r") as f:
            wave = []
            for char in f.read():
                if char == "\n":
                    waves.append(wave)
                    wave = []
                else:
                    wave.append(char)
        self.waves = waves
        print("creep initialized")
        return

    def load_game(self, file):
        print("loading game data...")
        map_data = []
        menu_data = []
        with open(file) as f:
            for i, line in enumerate(f.readlines()):
                if i <= 2:
                    menu_data.append(int(line.strip()))
                else:
                    tower_name, tower_type, x, y, level = line.strip(" ").split(" ")
                    map_data.append((tower_name, int(tower_type), (int(x), int(y)), int(level)))

        health, money, wave = menu_data
        self.contents["health bar"][0].v = health
        self.contents["money bar"][0].v = money
        self.contents["wave bar"][0].v = wave

        for t_name, t_type, t_pos, t_lv in map_data:
            self._make_tower(t_type, t_pos, t_lv)
        print("game_data load")
        return True

    def save_game(self):
        towers, info = self.get_data()
        assert isinstance(towers, list)
        assert isinstance(info, tuple)
        with open("./data/saved_game.txt", "w+") as f:
            # could be buggy
            for n in info:
                f.write("{0}\n".format(n))
            for name, tower_type, pos, level in towers:
                f.write("{0} {1} {2} {3} {4}".format(name, tower_type, pos[0], pos[1], level))
        return True

    def get_data(self):
        data = []
        for t in self.objects["towers"]:
            data.append(("1", t.type, t.rel_pos, t.level))
        return (data, (self.get_health(), self.get_money(), self.get_wave_num()))

    # game function
    def done(self):
        return self.get_health() <= 0

    def can_buy(self, price):
        if self.get_money() >= price:
            return True
        return False

    def do_pause(self):
        self.pause = not self.pause

    def next_wave(self, wave_num):
        wave_index = (wave_num - 1) % 5
        level = (wave_num - 1) // 5 + 1
        self.post_commands((MAKE_CREEP, (self.waves[wave_index], 0, level)))
        self.make_creep_CD = 15

    def _make_creep(self, creep_type, creepPath, level):
        return construct_creep(creep_type, creepPath, level)

    def _make_tower(self, tower_type, tower_rel_pos, level=1):
        # create tower
        tower = construct_tower(tower_type, tower_rel_pos, level)
        # add to contents
        self.contents[self.tower_ID] = tower, tower_rel_pos, TOWER_DIM
        # add to object
        self.objects["towers"].append(tower)
        # update layout
        row, col = find_point_loc(tower_rel_pos, self.layout)
        self.layout[row][col] = self.tower_ID
        # Increment tower_ID
        self.tower_ID += 1
        return tower

    create_tower = _make_tower

    def run(self, click_command, mouse_pos, offset):
        """contents do not have requests"""
        # run dynamic game if not pause
        if not self.pause:
            for bullet in self.objects["bullets"][:]:
                creep_hit = bullet.run()
                if creep_hit:
                    creep_hit.hit(bullet.dmg)
                    self.objects["bullets"].remove(bullet)

            for creep in self.objects["creeps"][:]:
                goal = creep.run()
                if goal == "damn":
                    self.contents["health bar"][0].hit()
                    if self.done():
                        self.post_commands((LOST, None))
                    self.objects["creeps"].remove(creep)
                elif not goal:
                    self.objects["creeps"].remove(creep)

            for tower in self.objects["towers"]:
                bullet = tower.run(self.objects["creeps"])
                if bullet:
                    self.objects["bullets"].append(bullet)

        # handle all requests && run static hovers
        return super().run(click_command, mouse_pos, offset)

    # helper function
    def get_health(self):
        return self.contents["health bar"][0].get_value()

    def get_money(self):
        return self.contents["money bar"][0].get_value()

    def get_wave_num(self):
        return self.contents["wave bar"][0].get_value()

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
            self.contents["money bar"][0].pay(price)
            self.create_tower(tower_type, ref)
        # in game menu
        elif command == NEXT_WAVE:
            self.contents["wave bar"][0].v += 1
            wave_num = self.get_wave_num()
            self.next_wave(wave_num)
        # elif command == SAVE_GAME:
        #     pass
        # elif command == PAUSE:
        #     self.do_pause()
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
        elif command == MAKE_CREEP:
            wave, i, lv = target
            if self.make_creep_CD <= 0:
                self.make_creep_CD = 15
                self.objects["creeps"].append(self._make_creep(wave[i], self.creepPath, lv))
                i += 1
            else:
                self.make_creep_CD -= 1

            if i < len(wave):
                self.post_commands((MAKE_CREEP, (wave, i, lv)))
        elif command == RETURN_FROM_GAME:
            self.post_request((RETURN, None))
            layer = MainMenu()
            self.post_request((NEW_LAYER, (LAYER_MAIN_MENU, layer, (0,0), MAIN_MENU_DIM)))
        # purchasing go to select mode
        elif command == PURCHASE:
            if target == CC_TOWER:
                price = CC_TOWER_LV1[0]
            elif target == DMG_TOWER:
                price = DMG_TOWER_LV1[0]
            else:
                raise Exception("Invalid tower type: {0}".format(target))
            if self.can_buy(price):
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
            if self.can_buy(upgrade_cost):
                tower_ID = self.layout[loc[0]][loc[1]]
                self.contents["money bar"][0].pay(upgrade_cost)
                self.contents[tower_ID][0].levelUp()
        else:
            raise Exception("Invalid command: {0}".format(c))

    handle_command = _game_panel_commands

    # draw_function
    def draw(self, surface, offset):  # O(n)
        """
        :param surface: pygame.surface
        :param offset: menu_abs_pos/ rel_pos = objs pos relative to the menu
        :return:
        """
        self.draw_box(surface, offset)

    def draw_box(self, surface, offset):  # O(n)
        self.draw_box_bg(surface, offset)
        if hasattr(self, "contents"):
            for name, (obj, rel_pos, dim) in self.contents.items():
                new_offset = calc_offset(offset, rel_pos)
                obj.draw_box(surface, new_offset)

        if hasattr(self, "objects"):
            for key, objs in self.objects.items():
                if key == "towers":
                    continue
                for obj in objs:
                    obj.draw(surface, offset)

    def draw_bg(self, surface, offset):
        """No image available now"""
        self.draw_box_bg(surface, offset)

    def draw_box_bg(self, surface, offset):
        for row, r in enumerate(self.map):
            for col, grid in enumerate(r):
                # create a text
                font = pygame.font.SysFont("calibri", 20, False, True)
                text = font.render(grid, True, BLUE, None)
                # calc blit pos
                rel_pos = find_grid_pos((row, col), self.map)
                blit_pos = calc_abs_pos(rel_pos, offset)
                # blit rect, blit text
                pygame.draw.rect(surface, BLUE, (blit_pos[0], blit_pos[1], 20, 20), 1)
                surface.blit(text, blit_pos)

    # representation funciton
    def __str__(self):
        out = ""
        for row in self.layout:
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

    def run(self, click_command, mouse_pos, offset):
        """just to return the last click then done of the layer"""
        if click_command == 1:
            rel_mouse_pos = calc_rel_pos(mouse_pos, offset)
            if not isInside(rel_mouse_pos, calcVertices(0, 0, self.width, self.height)):
                # return OFF_FOCUS, self
                pass
            else:
                return [(RETURN, None), (SELECTED, (self.selected, rel_mouse_pos))]
        else:
            return None, None

    def draw(self, surface, offset):
        pass

    def draw_box(self, surface, offset):
        pass

    def draw_bg(self, surface, offset):
        pass

    def draw_box_bg(self, surface, offset):
        pass


