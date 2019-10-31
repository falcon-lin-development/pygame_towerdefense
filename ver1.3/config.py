"""
configuration

Developer Notes:
done    2) keyboard command is buggy due to it's not layer dependent.
done    4) need careful testing of the command&request system
done    5) next_wave
done    6) draw function
done    7) creepPath in the map

Coming soon
done    1) command communication design
done    2) dynamic object implementation
    4) resizable frame
    5) dynamic motion feature
    6) items
    7) resume feature
    8) setting license
    9) mouse cursor when hover on clickable object


"""
from pygame import K_SPACE, K_w, K_ESCAPE

################################################################################
# general
DEBUG = True
SCREEN_DIM = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 1000
SCREEN_VERTICES = (0, 0), (SCREEN_WIDTH, 0), (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT)
STANDARD_DIM = STANDARD_WIDTH, STANDARD_HEIGHT = 20, 20
GRID_DIM = GRID_WIDTH, GRID_HEIGHT = 20, 20
FRAME = 60
NAME = "Falcon's Tower Defense ver 1.2"

# color
BLACK = 0,0,0
WHITE = 255,255,255
BLUE = 0, 0, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

#################################################################################
# files
GAME_MAP = 'map/map.txt'
GAME_WAVE = 'map/wave.txt'


NEW_GAME_FILE = "data/new_game.txt"
LOAD_GAME_FILE = "data/saved_game.txt"
TUTORIAL_GAME_FILE = "tutorial"
SETTING_FILE = "setting"
LICENSE_FILE = "license"

# IMG
# Main Menu Img
IMG_FILE = "./image/"
MAIN_MENU_BG_IMG = IMG_FILE + ""
NEW_GAME_BUTTON_IMG = IMG_FILE + ""
LOAD_GAME_BUTTON_IMG = IMG_FILE + ""
TUTORIAL_BUTTON_IMG = IMG_FILE + ""
SETTING_BUTTON_IMG = IMG_FILE + ""
LICENSE_BUTTON_IMG = IMG_FILE + ""

# Towers and bullet
DMG_BULLET_LV1_IMG = IMG_FILE + ""
DMG_TOWER_IMG = IMG_FILE + ""
CC_BULLET_LV1_IMG = IMG_FILE + ""
CC_TOWER_IMG = IMG_FILE + ""

# Creeps
WARRIOR_LV1_IMG = IMG_FILE + ""
KNIGHT_LV1_IMG = IMG_FILE + ""
DRAGON_KNIGHT_LV1_IMG = IMG_FILE + ""
TITAN_LV1_IMG = IMG_FILE + ""

# In game menu img
PURCHASE_BUTTON_IMG = ""
ITEMS_BUTTON_IMG = ""
NEXT_WAVE_BUTTON_IMG = ""
PAUSE_BUTTON_IMG = ""
SAVE_GAME_BUTTON_IMG = ""
EXIT_BUTTON_IMG = ""

# purchase menu img
DMG_TOWER_BUTTON_IMG = ""
CC_TOWER_BUTTON_IMG  = ""
###################################################################################
# GM command
GM_COMMAND_DICT = {  # only for debug purpose
    0: "quit",
    1: "save",
    2: "load",
    3: "new layer",
    4: "return",
    5: "put front layer"
}
QUIT = 0
SAVE = 1
LOAD = 2
NEW_LAYER = 3
RETURN = 4
PUT_FRONT_LAYER = 5

# MAIN MENU command
MAIN_MENU_COMMAND_DICT = {  # only for debug purpose
    99: "new game",
    98: "load game",
    97: "tutorial game",
    96: "setting",
    95: "license",
}
NEW_GAME = 99
LOAD_GAME = 98
TUTORIAL = 97
SETTING = 96
LICENSE = 95

# GAME_PANEL command
GAME_PANEL_COMMAND_DICT = {  # also implemented inside class
    100: "victory",
    101: "lose",
    102: "selected",
    103: "return from game",
}
WIN = 100
LOST = 101
SELECTED = 102
RETURN_FROM_GAME = 103

# In game Menu command
IN_GAME_MENU_COMMAND_DICT = {  # only for debug purpose
    99: "new wave",
    98: "In game save",
    97: "pause game",
    96: "setting",
    95: "exit",
    94: "purchase menu",
    93: "items"

}
NEXT_WAVE = 99
# SAVE_GAME = 98
PAUSE = 97
SETTING = 96
EXIT = 95
PURCHASE_MENU = 94
ITEMS = 93

# In game Map command
MAP_COMMAND_DICT = {
    89: "player get hit",
    88: "making creep"
}
GET_HIT = 89  # called when a creep reached goal tile
MAKE_CREEP = 88  # this one is specially handled in layer

# Purchase Menu command
PURCHASE_COMMAND_DICT = {
    79: "Try purchasing",
}

PURCHASE = 79

# Tower & Tower Menu
TOWER_MENU_COMMAND_DICT = {
    69: "tower menu",
    68: "tower level up"
}
TOWER_MENU = 69
LEVEL_UP = 68

################################################################################
# Layer
LAYER_MAIN_MENU = "main menu"
LAYER_GAME_PANEL = "game"
LAYER_TUTORIAL = "tutorial"
LAYER_SETTING_MENU = "setting menu"
LAYER_LICENSE = "license menu"

LAYER_PURCHASE_MENU = "purchase menu"
LAYER_SELECTION = "selection mode"

LAYER_TOWER_MENU = "tower menu"


#################################################################################
"""Need to change keyboard to follow this layered command design"""
# input devices
KEYBOARD = [K_SPACE, K_w, K_ESCAPE]  # what do you have in your virtual keyboard
KEYBOARD_COMMAND_DICT = {
    K_SPACE: PAUSE,
    K_w: NEXT_WAVE,
    K_ESCAPE: RETURN
}

#############################      Menus             #############################
##################################################################################
# MAIN MENU
MAIN_MENU_DIM = MAIN_MENU_WIDTH, MAIN_MENU_HEIGHT = SCREEN_DIM

MAIN_MENU_BUTTON_DIM = MAIN_MENU_BUTTON_WIDTH, MAIN_MENU_BUTTON_HEIGHT = 200, 96
MAIN_MENU_BUTTON_CUT = MAIN_MENU_BUTTON_X_CUT, MAIN_MENU_BUTTON_Y_CUT = 0, 400
MAIN_MENU_BUTTON_GAP = 20  # 20 by default
MAIN_MENU_BUTTON_DISTANCE = 300  # 300 by default

##################################################################################
# GAME PANEL
GAME_PANEL_POS = 0,0
GAME_PANEL_DIM = GAME_PANEL_WIDTH, GAME_PANEL_HEIGHT = SCREEN_DIM

GAME_PANEL_IN_GAME_MENU_CUT = GAME_PANEL_IN_GAME_MENU_X_CUT, GAME_PANEL_IN_GAME_MENU_Y_CUT = 0, 800

##################################################################################
# TUTORIAL
TUTORIAL_POS = 0, 0
TUTORIAL_DIM = TUTORIAL_WIDTH, TUTORIAL_HEIGHT = SCREEN_DIM

# SETTING_MENU_DIM
SETTING_MENU_POS = 0, 0
SETTING_MENU_DIM = SETTING_MENU_WIDTH, SETTING_MENU_HEIGHT = SCREEN_DIM

# LICENSE_MENU_DIM
LICENSE_MENU_POS = 0, 0
LICENSE_MENU_DIM = LICENSE_MENU_WIDTH, LICENSE_MENU_HEIGHT = SCREEN_DIM














#################################################################################
# Map
MAP_REF = MPA_POS = 0, 0  # by default
MAP_DIM = MAP_WIDTH, MAP_HEIGHT = 800, 800  # by default

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

##################################################################################
# IN GAME MENU
IN_GAME_MENU_DIM = IN_GAME_MENU_WIDTH, IN_GAME_MENU_HEIGHT = GAME_PANEL_WIDTH - GAME_PANEL_IN_GAME_MENU_X_CUT, \
                                                             GAME_PANEL_HEIGHT - GAME_PANEL_IN_GAME_MENU_Y_CUT

IN_GAME_MENU_GAP = 20  # by default
IN_GAME_MENU_DISTANCE = 20  # by default

IN_GAME_MENU_LEFT_DIM = IN_GAME_MENU_LEFT_WIDTH, IN_GAME_MENU_LEFT_HEIGHT = 600, 200
IN_GAME_MENU_LEFT_BUTTON_GAP = 20
IN_GAME_MENU_LEFT_BUTTON_DISTANCE = 20
IN_GAME_MENU_LEFT_HEALTH_DIM = 170, 70
IN_GAME_MENU_LEFT_MONEY_DIM = 170, 70
IN_GAME_MENU_LEFT_WAVE_DIM = 170, 70
IN_GAME_MENU_LEFT_PURCHASE_DIM = 180, 70
IN_GAME_MENU_LEFT_ITEMS_DIM = 360, 70

IN_GAME_MENU_RIGHT_CUT = 600, 0
IN_GAME_MENU_RIGHT_DIM = IN_GAME_MENU_RIGHT_WIDTH, IN_GAME_MENU_RIGHT_HEIGHT = 200, 200
IN_GAME_MENU_RIGHT_BUTTON_GAP = 10  # by default
IN_GAME_MENU_RIGHT_BUTTON_DISTANCE = 10  # by default
IN_GAME_MENU_RIGHT_BUTTON_DIM = IN_GAME_MENU_RIGHT_BUTTON_WIDTH, IN_GAME_MENU_RIGHT_BUTTON_HEIGHT = 180, 28

################################################################################
# Purchase menu
PURCHASE_MENU_ABS_POS = 0, 800
PURCHASE_MENU_DIM = PURCHASE_MENU_WIDTH, PURCHASE_MENU_HEIGHT = IN_GAME_MENU_DIM

PURCHASE_MENU_BUTTON_WIDTH, PURCHASE_MENU_BUTTON_HEIGHT = 100, 80  # by default
PURCHASE_MENU_BUTTON_CUT = 20, 20
PURCHASE_MENU_BUTTON_GAP = 0
PURCHASE_MENU_BUTTON_DISTANCE = 0




# TOWER_MENU_DIM

TOWER_MENU_DIM = 200, 200




#############################      Objects        #############################
###############################################################################
# Tower
TOWER_DIM = 20, 20  # by default

DMG_TOWER = 1
CC_TOWER = 2

DMG_BULLET_LV1 = [10, 20, None, (8, 8), DMG_BULLET_LV1_IMG]  # dmg, vel, cc, dim, image
DMG_TOWER_LV1 = [10, DMG_BULLET_LV1, 0.8, 2, "Tower Lv1", DMG_TOWER_IMG]  # cost, bullet, attkFreq(sec), range, name, img

CC_BULLET_LV1 = [8, 25, None, (8, 8), CC_BULLET_LV1_IMG]
CC_TOWER_LV1 = [30, CC_BULLET_LV1, 0.65, 3, "Long Range Tower Lv1", CC_TOWER_IMG]

#################################################################################
# Creep
CREEP_DIM = 20, 20  # by default

WARRIOR = "1"
KNIGHT = "2"
DRAGON_KNIGHT = "3"
BOSS = "4"

WARRIOR_LV1_INFO = [1, 20, 5, None, 100, "Warrior LV1", WARRIOR_LV1_IMG]  # prize, armor, vel, cc, health, name, img
KNIGHT_LV1_INFO = [2, 25, 7, None, 80, "Knight LV1", KNIGHT_LV1_IMG]
DRAGON_KNIGHT_LV1_INFO = [3, 50, 8, None, 120, "Dragon Knight LV1", DRAGON_KNIGHT_LV1_IMG]

BOSS_LV1_INFO = [10, 70, 3, None, 400, "TITAN LV1", TITAN_LV1_IMG]
