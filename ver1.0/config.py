#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 19:34:43 2019

@author: Falcon
all game constant stays here
"""
#unit quatity
#[velocity] = pixels / frame
#[freq] = num of actions / frame
#
# Todo- simplify code using rect.move**
# surf = pygame.transform.rotate(image_surf, angle)

################################################################################
# general
SCREEN_DIM = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 1000
SCREEN_VERTICES = (0,0), (SCREEN_WIDTH, 0), (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT)
STANDARD_DIM = STANDARD_WIDTH, STANDARD_HEIGHT = 20,20
FRAME = 30
NAME = "Falcon's Tower Defense ver 1.0"
TEST_MAP = 'map.txt'
TEST_WAVE = 'wave.txt'

################################################################################
#World
WORLD_DIM = WORLD_WIDTH, WORLD_HEIGHT = 800,800
WORLD_VERTICES = (0,0), (WORLD_WIDTH,0), (0, WORLD_HEIGHT), (WORLD_WIDTH, WORLD_HEIGHT)
#Tiles
TILE_DIM = TILE_WIDTH, TILE_HEIGHT = STANDARD_DIM
PATH_IMAGE = 'road_vertical.png'

GRASS_IMAGE = 'Grass.png'
GRASS_ROAD_L = 'Grass_and_road_4.png'
GRASS_ROAD_R = 'Grass_and_road_3.png'
GRASS_ROAD_T = 'Grass_and_road_2.png'
GRASS_ROAD_B = 'Grass.png'
GRASS_ROAD_LT = 'Grass.png'
GRASS_ROAD_RT = 'Grass.png'
GRASS_ROAD_LB = 'Grass.png'
GRASS_ROAD_RB = 'Grass.png'
GRASS_ROAD_OLT = 'Grass.png'
GRASS_ROAD_ORT = 'Grass.png'
GRASS_ROAD_OLB = 'Grass.png'
GRASS_ROAD_ORB = 'Grass.png'

TURN_IMAGE = 'Road_L.png'
GOAL_IMAGE = 'road_vertical.png'
BORN_IMAGE = 'road_vertical.png'
GRASS = '0'
TILE = '1'
TURN_TILE = '2'
BORN_TILE = '3'
GOAL_TILE = '4'

################################################################################
#bullet
DEFAULT_BULLET = (10, 10, None, 8, 8, 'Iron_man.png')#dmg, vel, special effect/cc,width, height img
DMG_BULLET = (10, 10, None, 4, 4, 'dbullet.png')
DMG_BULLET_2 = (15, 10, None, 4, 4, 'dbullet.png')
DMG_BULLET_3 = (20, 12, None, 4, 4, 'dbullet.png')
CC_BULLET = (7, 10, None, 4, 4, 'dbullet.png')
CC_BULLET_2 = (9, 15, None, 4, 4, 'dbullet.png')
CC_BULLET_3 = (15, 20, None, 4, 4, 'dbullet.png')
#Towers
DEFAULT_TOWER_DIM = DEFAULT_TOWER_WIDTH, DEFAULT_TOWER_HEIGHT = TILE_DIM
DEFAULT_TOWER_INFO = [(10, DEFAULT_BULLET, 3, None, 100, 'defaut-tower','dTower'), 'lv2','lv3'] # cost, bullet_type, attkfreq, special effect,range, img

DMG_TOWER_2 = (20, DMG_BULLET_2,  4, None, 100, 'DMG_TOWER_2','Thor.png')
DMG_TOWER_3 = (60, DMG_BULLET_3,  5, None, 150, 'DMG_TOWER_3','Thor.png')
DMG_TOWER = [(10, DMG_BULLET,  4, None, 100, 'DMG_TOWER','Thor.png'), DMG_TOWER_2, DMG_TOWER_3]

CC_TOWER_2 = (20, CC_BULLET_2,  3, None, 200, 'CC_TOWER_2','Vision.png')
CC_TOWER_3 = (60, CC_BULLET_3,  4, None, 300, 'CC_TOWER_3','Vision.png')
CC_TOWER = [(10, CC_BULLET,  3, None, 200, 'CC_TOWER','Vision.png'), CC_TOWER_2, CC_TOWER_3]


#Creeps
DEFAULT_CREEP_DIM = DEFAULT_CREEP_WIDTH, DEFAULT_CREEP_HEIGHT = TILE_DIM
DEFAULT_CREEP_INFO = (2, 1, 5, None, 100, 'creep', 'creep.jpeg') # prize, armor, velocity, special effect, health, name ,img
BRAWLER = '0'
BRAWLER_INFO = (1, 0, 5, None, 20, 'brawler','Iron_spider.png')
SOLDIER = '1'
SOLDIER_INFO = (2, 1, 5, None, 20, 'soldier','Cap.png')
TANK = '2'
TANK_INFO = (3, 5, 3, None, 40, 'tank', 'Hulk.png')
NINJA = '3'
NINJA_INFO = (3, 0, 10, None, 15, 'ninja', 'Vision.png')
KNIGHT = '4'
KNIGHT_INFO = (5, 3, 8, None, 30, 'knight', 'knight')
DRAGON = '5'
DRAGON_INFO = (10, 5, 10, None, 30, 'dragon', 'Iron_man.png')

################################################################################
#Menu
MENU_POS = MENU_X, MENU_Y = 0, WORLD_HEIGHT
MENU_DIM = MENU_WIDTH, MENU_HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT - WORLD_HEIGHT
MENU_DIMBOX = MENU_X, MENU_Y, MENU_WIDTH, MENU_HEIGHT


MAIN_MENU_DIMBOX = ()
MAIN_MENU = ()

GAME_MENU_DIMBOX = MENU_DIMBOX
GAME_MENU = ('GAME_MENU',('Purchase', 'Sell', 'NextWave', 'Exit'), 'GAME_MENU') # 1::=game_menu, listofbuttons, img

PURCHASE_MENU_DIM = (200, 300)
PURCHASE_MENU = ('PURCHASE_MENU',('CCTower', 'DMGTower'), 'PURCHASE_MENU')

TOWER_MENU_DIM = (150, 200)
TOWER_MENU = ('TOWER_MENU',('UpGrade', 'Sell'), 'TOWER_MENU')
#Buttons
DEFAULT_BUTTON_DIM = DEFAULT_BUTTON_WIDTH, DEFAULT_BUTTON_HEIGHT = 50, 100
DEFAULT_BUTTON_IMAGE = ''
#Purchse
DEFAULT_PURCHASE_INFO = ('',)
#Sell
DEFAULT_SELL_INFO = ('',)
#Setting
DEFAULT_SETTING_INFO = ('',)
#Exit
DEFAULT_EXIT_INFO = ('',)

################################################################################
# Message Box
DEFAULT_MESSAGE_BOX_INFO = ()

#################################################################################
# Button Commands
PRESSED = 0
ONCLICK = 1
CANCEL= 2
HOVER = 3
























