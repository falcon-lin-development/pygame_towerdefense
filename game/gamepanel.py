"""
Implementation of a game Loader and the Gamepanel
the playable game logic and contents is here


Developer Note:
done 1) towers can be overlapping/ placable checking
done 2) simplify structure


further simplify everything
done 1) selection mode
"""
from game.config import *
from game.menu import Menu, PurchaseMenu, TowerMenu, MainMenu, GameMenu
from game.tower import construct_tower
from game.creep import construct_creep
from game.functions import calc_offset, calc_rel_pos, find_point_loc, isInside, calcVertices, calcAlignCenter, find_grid_pos, calc_abs_pos
from game.sound import Py_Sound
import os
import pygame


def loader(file):
    if not os.path.isfile(file):
        file = "data/new_game.txt"
    game_panel = GamePanel()
    game_panel.load_game(file)
    return game_panel


class GamePanel(Menu):
    """
    dim: a tuple of (width, height)
    map_file: a file that contains (map + creepPath) information
    wave_file: creep wave
    load_file: player data
    """
    COMMAND_DICT = {**GAME_PANEL_COMMAND_DICT, **IN_GAME_MENU_COMMAND_DICT,
                    **PURCHASE_COMMAND_DICT, **TOWER_MENU_COMMAND_DICT}
    tower_ID = 1

    def __init__(self, dim=(800, 1000), map_file=GAME_MAP, wave_file=GAME_WAVE):
        # build basic
        print("Initializing game")
        super().__init__()
        self.dim = self.width, self.height = dim
        self.contents = {}
        self.buttons = []
        self.objects = {
            "creeps": [],
            "bullets": [],
            "towers": []
        }
        self.pause = False
        # load data
        self._load_map(map_file)
        self._load_wave(wave_file)
        self._load_image()
        self._load_sounds()
        self.build_layout()
        self.sound.play_bg()
        print("game initialized")

    # initialization
    def load_game(self, file):
        print("loading game data...")
        map_data = []
        menu_data = []
        with open(file) as f:
            for i, line in enumerate(f.readlines()):
                if i <= 2:
                    menu_data.append(int(line.strip()))
                else:
                    tower_name, tower_type, x, y, level = line.strip(
                        " ").split(" ")
                    map_data.append(
                        (tower_name, int(tower_type), (int(x), int(y)), int(level)))

        self._tem_health, self._tem_money, self._tem_wave_num = menu_data
        self.handle_command((CHANGE_MENU, (LAYER_IN_GAME_MENU, None)))

        for t_name, t_type, t_pos, t_lv in map_data:
            self._make_tower(t_type, t_pos, t_lv)
        print("game_data load")

        return True

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
                neighbors = [(t_row, t_col), (r_row, r_col),
                             (b_row, b_col), (l_row, l_col)]
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
            assert creepPath[-1] == end, "creep path is not correctly calculated: {0}|{1}".format(
                creepPath, end)

            # calc rel centers
            for index, (row, col) in enumerate(creepPath[:]):
                creepPath[index] = calcAlignCenter(
                    find_grid_pos((row, col), _map), GRID_DIM)

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

    def _load_image(self):
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
        :param paths:
        :return:
        """
        try:
            self.grid_images = {
                GRASS: pygame.image.load(GRASS_IMG),
                PATH_H: pygame.image.load(PATH_H_IMG),
                PATH_V: pygame.image.load(PATH_V_IMG),
                TURN_TL: pygame.image.load(TURN_TL_IMG),
                TURN_TR: pygame.image.load(TURN_TR_IMG),
                TURN_BL: pygame.image.load(TURN_BL_IMG),
                TURN_BR: pygame.image.load(TURN_BR_IMG),
                SPAWN: pygame.image.load(SPAWN_IMG),
                GOAL: pygame.image.load(GOAL_IMG),
                PATH_SIDE: pygame.image.load(PATH_SIDE_IMG),
                BOARDER: pygame.image.load(BOARDER_IMG),
            }
        except Exception as e:
            print(e)
            font = pygame.font.SysFont("calibri", 20, False, True)
            self.grid_images = {
                GRASS: font.render(GRASS, True, BLUE, None),
                PATH_H: font.render(PATH_H, True, BLUE, None),
                PATH_V: font.render(PATH_V, True, BLUE, None),
                TURN_TL: font.render(TURN_TL, True, BLUE, None),
                TURN_TR: font.render(TURN_TR, True, BLUE, None),
                TURN_BL: font.render(TURN_BL, True, BLUE, None),
                TURN_BR: font.render(TURN_BR, True, BLUE, None),
                SPAWN: font.render(SPAWN, True, BLUE, None),
                GOAL: font.render(GOAL, True, BLUE, None),
                PATH_SIDE: font.render(PATH_SIDE, True, BLUE, None),
                BOARDER: font.render(BOARDER, True, BLUE, None),
            }

    def _load_sounds(self):
        print("loading sounds...")
        self.sound = Py_Sound()
        print("sound loaded")

    def save_game(self):
        towers, info = self.get_data()
        assert isinstance(towers, list)
        assert isinstance(info, tuple)
        with open("game/data/saved_game.txt", "w+") as f:
            # could be buggy
            for n in info:
                f.write("{0}\n".format(n))
            for name, tower_type, pos, level in towers:
                f.write("{0} {1} {2} {3} {4}\n".format(
                    name, tower_type, pos[0], pos[1], level))
        return True

    # game function
    def done(self):
        return self.get_health() <= 0

    def do_pause(self):
        self.pause = not self.pause

    def set_vol(self, vol):
        self.sound.set_vol(vol)

    def pay(self, price):
        if "money bar" in self.contents:
            self.contents["money bar"][0].pay(price)
        else:
            self._tem_money -= price

    def earn(self, money):
        if "money bar" in self.contents:
            self.contents["money bar"][0].earn(money)
        else:
            self._tem_money += money

    def hit(self):
        if "health bar" in self.contents:
            self.contents["health bar"][0].hit()
        else:
            self._tem_health -= 1

    def next_wave(self, wave_num):
        """Increment wave num here ***"""
        # Increment wave num
        if "wave bar" in self.contents:
            self.contents["wave bar"][0].incre_wave()
        else:
            self._tem_wave_num += 1
        # spawn creeps
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

    def _normal_run(self, click_command, mouse_pos, offset):
        """default game run logic"""
        # run dynamic game if not pause
        if not self.pause:
            for bullet in self.objects["bullets"][:]:
                creep_hit = bullet.run()
                if creep_hit:
                    creep_hit.hit(bullet.dmg)
                    # sound effect
                    self.sound.play_hit()
                    self.objects["bullets"].remove(bullet)

            for creep in self.objects["creeps"][:]:
                goal = creep.run()
                if goal == "damn":
                    self.hit()
                    if self.done():
                        self.post_commands((LOST, None))
                    self.objects["creeps"].remove(creep)
                    self.earn(creep.prize)
                elif not goal:
                    self.objects["creeps"].remove(creep)
                    self.earn(creep.prize)

            for tower in self.objects["towers"]:
                bullet = tower.run(self.objects["creeps"])
                if bullet:
                    self.objects["bullets"].append(bullet)

        # handle all requests && run static hovers
        return super().run(click_command, mouse_pos, offset)

    run = _normal_run

    def _selection_run(self, click_command, mouse_pos, offset):
        """how the game_logic run when selecting location for tower placement"""
        if click_command == 1:
            rel_mouse_pos = calc_rel_pos(mouse_pos, offset)
            if isInside(rel_mouse_pos, calcVertices(0, 0, 800, 800)):
                if self._can_place_tower(rel_mouse_pos):
                    self.handle_command(
                        (SELECTED, (self._selected, rel_mouse_pos)))
                    return self._normal_run(None, mouse_pos, offset)
            else:
                # return OFF_FOCUS, self
                self.handle_command((SELECTED, (0, rel_mouse_pos)))
                return self._normal_run(None, mouse_pos, offset)

        return None, None

    # query/ helper function
    def get_data(self):
        data = []
        for t in self.objects["towers"]:
            data.append(("1", t.type, t.rel_pos, t.level))
        return data, (self.get_health(), self.get_money(), self.get_wave_num())

    def get_health(self):
        if "health bar" in self.contents:
            return self.contents["health bar"][0].get_value()
        else:
            return self._tem_health

    def get_money(self):
        if "money bar" in self.contents:
            return self.contents["money bar"][0].get_value()
        else:
            return self._tem_money

    def get_wave_num(self):
        if "wave bar" in self.contents:
            return self.contents["wave bar"][0].get_value()
        else:
            return self._tem_wave_num

    def can_buy(self, price):
        try:
            if self.get_money() >= price:
                return True
            return False
        except TypeError:
            return False

    def _can_place_tower(self, rel_mouse_pos):
        loc = find_point_loc(rel_mouse_pos, self.layout)
        if self.layout[loc[0]][loc[1]] is None and self.map[loc[0]][loc[1]] == "0":
            return True
        return False

    # command handler
    def _game_panel_commands(self, c: tuple) -> None:
        """
WIN = 99
LOST = 98
RETURN_FROM_GAME = 97
CHANGE_MENU = 96
MAKE_CREEP = 95
SET_VOLUME = 94

NEXT_WAVE = 89
ITEMS = 88

PURCHASE = 79
SELECTED = 79

LEVEL_UP = 69
        :return:
        """
        command, target = c
        # game panel
        # 1 cycle
        if command == WIN:
            pass

        # 1 cycle
        elif command == LOST:
            self.do_pause()
            print("gg well played")

        # 2 cycles
        elif command == RETURN_FROM_GAME:
            self.save_game()
            self.post_request((RETURN, None))
            self.sound.stop_bg()
            layer = MainMenu()
            self.post_request(
                (NEW_LAYER, (LAYER_MAIN_MENU, layer, (0, 0), MAIN_MENU_DIM)))

        # 1 cycle
        elif command == CHANGE_MENU:
            layer_name, data = target
            if layer_name == LAYER_IN_GAME_MENU:
                tem = GameMenu(
                    (self._tem_health, self._tem_money, self._tem_wave_num))
            else:
                towers, (self._tem_health, self._tem_money,
                         self._tem_wave_num) = self.get_data()
                if layer_name == LAYER_PURCHASE_MENU:
                    tem = PurchaseMenu()
                elif layer_name == LAYER_TOWER_MENU:
                    tem = TowerMenu(data)
                else:
                    raise Exception("Invalid menu")
            # pop old bt
            for key in self.buttons:
                self.contents.pop(key)
            self.buttons = []
            # add new bts
            for key, (obj, ref, dim) in tem.contents.items():
                self.contents[key] = obj, ref, dim
                self.buttons.append(key)

        # n cycles
        elif command == MAKE_CREEP:
            wave, i, lv = target
            if self.make_creep_CD <= 0:
                self.make_creep_CD = 15
                self.objects["creeps"].append(
                    self._make_creep(wave[i], self.creepPath, lv))
                i += 1
            else:
                self.make_creep_CD -= 1

            if i < len(wave):
                self.post_commands((MAKE_CREEP, (wave, i, lv)))

        # 1 cycle
        elif command == SET_VOLUME:
            if self.sound.vol_state:
                self.sound.sound_off()
            else:
                self.sound.sound_on()

        # in game menu
        # 2 cycles
        elif command == NEXT_WAVE:
            wave_num = self.get_wave_num()
            self.next_wave(wave_num)
        elif command == ITEMS:
            pass

        # purchasing go to select mode
        # 1 cycle
        elif command == PURCHASE:
            if target == CC_TOWER:
                price = CC_TOWER_LV1[0]
            elif target == DMG_TOWER:
                price = DMG_TOWER_LV1[0]
            else:
                raise Exception("Invalid tower type: {0}".format(target))
            if self.can_buy(price):
                self._selected = target
                self.run = self._selection_run

        # 1 cycle
        elif command == SELECTED:
            tower_type, ref = target
            if tower_type == 0:
                pass
            else:
                if tower_type == CC_TOWER:
                    price = CC_TOWER_LV1[0]
                else:
                    price = DMG_TOWER_LV1[0]
                self.pay(price)
                self.create_tower(tower_type, find_grid_pos(
                    find_point_loc(ref, None), None))
            self._selected = None
            self.run = self._normal_run

        # tower menu
        # 1 cycle
        elif command == LEVEL_UP:
            upgrade_cost, loc = target
            if self.can_buy(upgrade_cost):
                tower_ID = self.layout[loc[0]][loc[1]]
                self.pay(upgrade_cost)
                self.contents[tower_ID][0].levelUp()
                self.post_commands(
                    self.contents[tower_ID][0].do_onclick(1, None, None))
        elif command is None:
            pass
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
        self.draw_bg(surface, offset)
        if hasattr(self, "contents"):
            for name, (obj, rel_pos, dim) in self.contents.items():
                new_offset = calc_offset(offset, rel_pos)
                obj.draw(surface, new_offset)

        if hasattr(self, "objects"):
            for key, objs in self.objects.items():
                if key == "towers":
                    continue
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
                if key == "towers":
                    continue
                for obj in objs:
                    obj.draw_box(surface, offset)

    def draw_bg(self, surface, offset):
        for row, r in enumerate(self.map):
            for col, grid in enumerate(r):
                # calc blit pos
                rel_pos = find_grid_pos((row, col), self.map)
                blit_pos = calc_abs_pos(rel_pos, offset)
                # blit rect, blit text
                surface.blit(self.grid_images[grid], blit_pos)

        border = 5
        pygame.draw.rect(surface, COLOR_8B4513, (0, 800, 800, 200), 0)
        pygame.draw.rect(surface, COLOR_FFDEAD, (5, 805, 790, 190), 0)

    def draw_box_bg(self, surface, offset):
        for row, r in enumerate(self.map):
            for col, grid in enumerate(r):
                # calc blit pos
                rel_pos = find_grid_pos((row, col), self.map)
                blit_pos = calc_abs_pos(rel_pos, offset)
                # blit rect, blit text
                pygame.draw.rect(
                    surface, BLUE, (blit_pos[0], blit_pos[1], 20, 20), 1)
                surface.blit(self.grid_images[grid], blit_pos)

    # representation function
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
