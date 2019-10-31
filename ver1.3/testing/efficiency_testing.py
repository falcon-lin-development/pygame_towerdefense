import sys
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense')
sys.path.append('/Users/alohahawk/Downloads/Game/Pygame_towerdefense/ver1.2')
from game import Game
from config import *
import pygame
pygame.init()


a = Game(None)
a.handle_command((LOAD, (LAYER_GAME_PANEL, NEW_GAME_FILE, GAME_PANEL_POS, GAME_PANEL_DIM)), None)
