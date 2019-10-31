#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 19:45:12 2019

@author: Falcon

all world class
Map

developer Note
done 1) abstract tile object away
done 2) embed them into the layout of map
"""
from menu import Menu
from tower import construct_tower, Tower
from creep import construct_creep
from functions import find_grid_pos, calcAlignCenter, find_point_loc, calc_abs_pos, calc_offset
import pygame
from config import *


class Map(Menu):
    """
    a combinator for different tiles: grass / path / tower
    by default it is a square
    """
    tower_ID = 1

    def __init__(self, map_data, dim=MAP_DIM, map_file=GAME_MAP, wave_file=GAME_WAVE,):
        # build basic
        super(Map, self).__init__()
        self.dim = self.width, self.height = dim
        self.contents = {}
        self.objects = {
            "creeps": [],
            "bullets": [],
            "towers": []
        }
        self.pause = False

        # load data
        print("Loading data...")
        self._load_map(map_file)
        self._load_wave(wave_file)
        self.build_layout()
        self._load_data(map_data)
        print("Finished loading data.")

    # initiate functions
    def _load_data(self, map_data):
        print("Initializing data...")
        assert isinstance(map_data, list), "Invalid map_data: {0}".format(map_data)
        for tower in map_data:
            tower_name, tower_type, rel_pos, level = tower
            self._make_tower(tower_type, rel_pos, level)
        print("data initialized.")
        return

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
                    raise Exception("Invalid map configuration: current{0}, \ncreepPath{1}".format(current, creepPath))
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
        return

    def get_data(self):
        data = []
        for key, (t, ref, dim) in self.contents.items():
            if isinstance(t, Tower):
                data.append((key, t.type, ref, t.level))
        return data

# game function
    def run(self, mouse_pos, offset):
        """contents do not have requests"""
        # get requests from contents
        for key, (obj, ref, dim) in self.contents.items():
            if hasattr(obj, "get_requests"):
                for request in obj.get_requests():
                    self.post_commands(request)

        # get request from objects
        for key, obj_list in self.objects.items():
            if key == "towers":
                continue
            for obj in obj_list:
                if hasattr(obj, "get_requests"):
                    for request in obj.get_requests():
                        self.post_commands(request)

        # handle all requests && run static hovers
        super(Map, self).run(mouse_pos, offset)

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
                    self.post_request((GET_HIT, None))
                    self.objects["creeps"].remove(creep)
                elif not goal:
                    self.objects["creeps"].remove(creep)

            for tower in self.objects["towers"]:
                bullet = tower.run(self.objects["creeps"])
                if bullet:
                    self.objects["bullets"].append(bullet)

        return True

    # command handler
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

    def next_wave(self, wave_num):
        wave_index = (wave_num - 1) % 5
        level = (wave_num - 1) // 5 + 1
        self.post_commands((MAKE_CREEP, (self.waves[wave_index], 0, level)))
        self.make_creep_CD = 15

    def _make_creep(self, creep_type, creepPath, level):
        return construct_creep(creep_type, creepPath, level)

    def _map_commands(self, c):
        command, target = c
        if command == MAKE_CREEP:
            wave, i, lv = target
            if self.make_creep_CD <= 0:
                self.make_creep_CD = 15
                self.objects["creeps"].append(self._make_creep(wave[i], self.creepPath, lv))
                i += 1
            else:
                self.make_creep_CD -= 1

            if i < len(wave):
                self.post_commands((MAKE_CREEP, (wave, i, lv)))

    handle_command = _map_commands

    def do_pause(self):
        self.pause = not self.pause
        return None

# draw functions
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








            




            
            



        
        
        

