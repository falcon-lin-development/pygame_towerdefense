#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 17:33:37 2019

@author: Falcon
Buttons(dim, command_target)

developer Note:
on it    1) can further abstract away all buttons
"""
from item import StaticItem
import pygame
from config import *
from functions import save_load_image


class Bar(StaticItem):
    def __init__(self, dim, value=None):
        self.dim = self.width, self.height = dim
        self.v = value
        self.image = save_load_image(self, "")

    def get_value(self):
        return self.v

    # init func
    def make_image(self):
        font_size = 40
        font = pygame.font.SysFont("calibri", font_size)
        # while font.get_height() > self.height - 10 or font.get_width > self.width - 10:
        #     font = pygame.font.SysFont("calibri", font_size - 1)
        text = font.render(self.__class__.__name__, True, BLUE, None)
        return text

    # draw function
    def draw(self, surface, offset):
        self.draw_box(surface, offset)

    def draw_box(self, surface, offset):
        # blit rect, blit text
        pygame.draw.rect(surface, BLUE, (offset[0], offset[1], self.width, self.height), 1)
        surface.blit(self.image, offset)


class Button(Bar):  # static item # SM
    """a button class will have
    onclick
    hover
    image
    draw
    draw_box

    make_image
    """

    def __init__(self, dim, c):
        super().__init__(dim, c)
        self.hover = False

    # init function
    def make_hover_image(self):
        font_size = 40
        font = pygame.font.SysFont("calibri", font_size)
        # while font.get_height() > self.height - 10 or font.get_width > self.width - 10:
        #     font = pygame.font.SysFont("calibri", font_size - 1)
        text = font.render(str(self.v), True, BLUE, None)
        return text

    # game function
    def do_onclick(self, click_command, mouse_pos, new_offset):
        return self.v
    onclick = do_onclick

    def do_hover(self):
        self.hover = True

    def un_hover(self):
        self.hover = False

    # draw function
    def draw_box(self, surface, offset):
        if self.hover:
            pygame.draw.rect(surface, BLUE, (offset[0], offset[1], self.width, self.height), 1)
            # blit hover image
            surface.blit(self.make_hover_image(), offset)
        else:
            super().draw_box(surface, offset)


# main menu
class NewGame(Button):
    def __init__(self, dim, c):
        super(NewGame, self).__init__(dim, c)
        self.image = save_load_image(self, NEW_GAME_BUTTON_IMG)


class LoadGame(Button):
    def __init__(self, dim, ct):
        super(LoadGame, self).__init__(dim, ct)
        self.image = save_load_image(self, LOAD_GAME_BUTTON_IMG)


class Tutorial(Button):
    def __init__(self, dim, ct):
        super(Tutorial, self).__init__(dim, ct)
        self.image = save_load_image(self, TUTORIAL_BUTTON_IMG)


class Setting(Button):
    def __init__(self, dim, ct):
        super(Setting, self).__init__(dim, ct)
        self.image = save_load_image(self, SETTING_BUTTON_IMG)


class License(Button):
    def __init__(self, dim, ct):
        super(License, self).__init__(dim, ct)
        self.image = save_load_image(self, LICENSE_BUTTON_IMG)


class Resume(Button):
    def __init__(self, dim, ct):
        super(Resume, self).__init__(dim, ct)
        self.image = save_load_image(self, RESUME_BUTTON_IMG)


# in game menu
class Purchase(Button):
    def __init__(self, dim, ct):
        super().__init__(dim, ct)
        self.image = save_load_image(self, PURCHASE_BUTTON_IMG)


class Items(Button):
    def __init__(self, dim, ct):
        super().__init__(dim, ct)
        self.image = save_load_image(self, ITEMS_BUTTON_IMG)


class NextWave(Button):
    def __init__(self, dim, ct):
        super().__init__(dim, ct)
        self.image = save_load_image(self, NEXT_WAVE_BUTTON_IMG)


class Pause(Button):
    def __init__(self, dim, ct):
        super().__init__(dim, ct)
        self.image = save_load_image(self, PAUSE_BUTTON_IMG)


class SaveGame(Button):
    def __init__(self, dim, ct):
        super().__init__(dim, ct)
        self.image = save_load_image(self, SAVE_GAME_BUTTON_IMG)


class Exit(Button):
    def __init__(self, dim, ct):
        super().__init__(dim, ct)
        self.image = save_load_image(self, EXIT_BUTTON_IMG)


class HealthBar(Bar):
    def hit(self):
        self.v -= 1


class MoneyBar(Bar):
    def pay(self, price):
        self.v -= price


class WaveBar(Bar):
    pass


# purchase menu
class Dmg_tower_b(Button):
    def __init__(self, dim, ct):
        super().__init__(dim, ct)
        self.image = save_load_image(self, DMG_TOWER_BUTTON_IMG)


class Cc_tower_b(Button):
    def __init__(self, dim, ct):
        super().__init__(dim, ct)
        self.image = save_load_image(self, CC_TOWER_BUTTON_IMG)


# Tower menu
class TowerItems(Button):
    pass


class TowerLevelUp(Button):
    def __init__(self, dim, display_name, c):
        super().__init__(dim, c)
        self.__class__.__name__ = str(display_name)


class TowerIcon(Bar):
    pass


class TowerName(Bar):
    pass


class TowerLV(Bar):
    pass


class TowerCost(Bar):
    pass


class TowerDmg(Bar):
    pass


class TowerAcckFreq(Bar):
    pass


class TowerRange(Bar):
    pass













































































