"""
Executable main file

Key components
win: pygame display window
new_game: game object supports game_logic and display_logic

helper objects
clock: pygame inner counter
key: keyboard inputs processor object
mouse: mouse inputs processor object
"""
import pygame
from game import Game
from inp_devices import KeyboardCommand, MouseCommand
from config import *
import os

assert os.getcwd()[-27:] == "/Pygame_towerdefense/ver1.4", \
    "Invalid location: {0}\nExpected: {1}".format(os.getcwd(), "./Pygame_towerdefense/ver1.4")

pygame.init()

win = pygame.display.set_mode(SCREEN_DIM,
                              flags=pygame.DOUBLEBUF|pygame.RESIZABLE)
pygame.display.set_caption(NAME)
clock = pygame.time.Clock()
# input device handler
key = KeyboardCommand()
mouse = MouseCommand()
key.start()
mouse.start()

# new game
new_game = Game(win)
playing = True
while playing:
    clock.tick(FRAME)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            break

    key_command = key.step(pygame.key.get_pressed())
    click_command = mouse.step(pygame.mouse.get_pressed())
    mouse_pos = pygame.mouse.get_pos()

    if not new_game.run(key_command, click_command, mouse_pos, verbose=0):
        # game_run will return the value whether the game
        # should keep going
        break

    win.fill(BLACK)
    new_game.draw()
    # new_game.draw_box()

    pygame.display.update()

pygame.quit()
