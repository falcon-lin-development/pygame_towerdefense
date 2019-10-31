#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 19:57:35 2019

@author: Falcon

"""
import pygame
from game import Game
from config import *
import os
assert os.getcwd()[-27:] == "/Pygame_towerdefense/ver1.2", \
    "Invalid location: {0}\nExpected: {1}".format(os.getcwd(), "./Pygame_towerdefense/ver1.2")

pygame.init()

win = pygame.display.set_mode(SCREEN_DIM,
                              flags=pygame.DOUBLEBUF|pygame.RESIZABLE)
pygame.display.set_caption(NAME)
clock = pygame.time.Clock()
# input device handler
keyboard = None
mouse = None


def key_step(state, inp):
    for k in KEYBOARD:
        if inp[k]:
            if state == k:
                return state, None
            else:
                return k, state
    else:
        return None, state


def mouse_step(state, inp):
    if inp[:-1].count(1) >= 2:
        return None, None
    else:
        for i, b in enumerate(inp[:-1]):  # 2 ops.
            if b:
                if state == i:
                    return state, None
                else:
                    return i + 1, None
        else:
            return None, state


# new game
new_game = Game(win)
playing = True
while playing:
    clock.tick(FRAME)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            break

    keyboard, key_command = key_step(keyboard, pygame.key.get_pressed())
    mouse, click_command = mouse_step(mouse, pygame.mouse.get_pressed())
    mouse_pos = pygame.mouse.get_pos()

    if not new_game.run(key_command, click_command, mouse_pos, verbose=0):
        # game_run will return the value whether the game
        # should keep going
        break

    win.fill(BLACK)
    # new_game.draw()
    new_game.draw_box()

    pygame.display.update()

pygame.quit()
