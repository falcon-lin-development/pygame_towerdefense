"""
configuration
This file contain all the static variables in the whole program

Developer Notes:
done    2) keyboard command is buggy due to it's not layer dependent.
done    4) need careful testing of the command&request system
done    5) next_wave
done    6) draw function
done    7) creepPath in the map
done    8) images
        8a) creeps are too small, may be do it 25x25, 36, 36, 42x42
    9) tutorial
done    10) sounds
done    11) testing
done    12) distinguish between one cycle and two cycles commands
done    13) rewrite all doc and comment block

Coming soon
done    1) command communication design
done    2) dynamic object implementation
    4) resizable frame
    5) dynamic motion feature
    6) items
    7) resume feature
done    8) setting license
    9) mouse cursor when hover on clickable object
    10) deepen the story line
    11) range dmg
    12) img pixel
    13) right click cancel
    14) continuous purchasing
    15) select cursor figure


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
NAME = "Falcon's Tower Defense ver 1.4"


# color
BLACK = 0,0,0
WHITE = 255,255,255
BLUE = 0, 0, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
COLOR_8B4513 = 139, 69, 19
COLOR_FFDEAD = 255, 222, 173

#################################################################################
# files

GAME_MAP = 'map/map.txt'
GAME_WAVE = 'map/wave.txt'

NEW_GAME_FILE = "data/new_game.txt"
LOAD_GAME_FILE = "data/saved_game.txt"

BG_MUSIC = "data/bg_music.wav"
HIT_SOUND = "data/hit.wav"

# IMG
IMG_FILE = "../ps/"
NO_IMG = IMG_FILE + "display/no_image.png"

# Main Menu Img

MAIN_MENU_BG_IMG = IMG_FILE + ""
NEW_GAME_BUTTON_IMG = IMG_FILE + ""
LOAD_GAME_BUTTON_IMG = IMG_FILE + ""
TUTORIAL_BUTTON_IMG = IMG_FILE + ""
SETTING_BUTTON_IMG = IMG_FILE + ""
LICENSE_BUTTON_IMG = IMG_FILE + ""

# Towers and bullet
DMG_BULLET_LV1_IMG = IMG_FILE + "bullets/dbullet.png"
DMG_TOWER_IMG = IMG_FILE + "towers/dmg_t_lv1.png"
CC_BULLET_LV1_IMG = IMG_FILE + "bullets/Bullet.png"
CC_TOWER_IMG = IMG_FILE + "towers/cc_t_lv1.png"

# Creeps
WARRIOR_LV1_IMG = IMG_FILE + "creep/warrior_lv1.png"
KNIGHT_LV1_IMG = IMG_FILE + "creep/knight_lv1.png"
DRAGON_KNIGHT_LV1_IMG = IMG_FILE + "creep/dragon_knight_lv1.png"
TITAN_LV1_IMG = IMG_FILE + "creep/Titan_lv1.png"

# In game menu img
PURCHASE_BUTTON_IMG = ""
ITEMS_BUTTON_IMG = ""
NEXT_WAVE_BUTTON_IMG = ""
PAUSE_BUTTON_IMG = ""
SAVE_GAME_BUTTON_IMG = ""
EXIT_BUTTON_IMG = ""

# purchase menu img
DMG_TOWER_BUTTON_IMG = ""
CC_TOWER_BUTTON_IMG = ""

# Map img
GRASS_IMG = IMG_FILE + "tiles/Grass.png"
PATH_H_IMG = IMG_FILE + "tiles/road_H.png"
PATH_V_IMG = IMG_FILE + "tiles/road_V.png"
TURN_TL_IMG = IMG_FILE + "tiles/road_TL.png"
TURN_TR_IMG = IMG_FILE + "tiles/road_TR.png"
TURN_BL_IMG = IMG_FILE + "tiles/road_BL.png"
TURN_BR_IMG = IMG_FILE + "tiles/road_BR.png"

SPAWN_IMG = IMG_FILE + "tiles/spawn.png"
GOAL_IMG = IMG_FILE + "tiles/goal.png"
PATH_SIDE_IMG = IMG_FILE + "tiles/rock.png"
BOARDER_IMG = IMG_FILE + "tiles/rock.png"
###################################################################################
# GM command
GM_COMMAND_DICT = {  # only for debug purpose
    0: "quit",
    1: "save",
    2: "load",
    3: "new layer",
    4: "return",
    5: "run by layer",
    6: "set volume"
}
QUIT = 0
SAVE = 1
LOAD = 2
NEW_LAYER = 3
RETURN = 4
RUN_BY_LAYER = 5
SET_VOLUME = 6

# MAIN MENU command
MAIN_MENU_COMMAND_DICT = {  # only for debug purpose
    99: "new game",
    98: "load game",
    97: "tutorial game",
    96: "setting",
    95: "license",
}

# GAME_PANEL command
GAME_PANEL_COMMAND_DICT = {  # also implemented inside class
    99: "victory",
    98: "lose",
    97: "selected",
    96: "return from game",
    95: "making creep",
    # 94: "set volume"
}
WIN = 99
LOST = 98
RETURN_FROM_GAME = 97
CHANGE_MENU = 96
MAKE_CREEP = 95
# SET_VOLUME = 94

# In game Menu command
IN_GAME_MENU_COMMAND_DICT = {  # only for debug purpose
    89: "new wave",
    88: "items",
}
NEXT_WAVE = 89
ITEMS = 88
# Purchase Menu command
PURCHASE_COMMAND_DICT = {
    79: "Try purchasing",
    78: "selection made",
}
PURCHASE = 79
SELECTED = 78
# Tower & Tower Menu
TOWER_MENU_COMMAND_DICT = {
    69: "tower level up"
}
LEVEL_UP = 69

# Setting Menu Command
SET_KEY = 99
DONE_SET_KEY = 98


# Tutorial Menu Command
NEXT_PAGE = 99
LAST_PAGE = 98

#################################################################################
"""Need to change keyboard to follow this layered command design"""
# input devices
PAUSE = 999
# SET_KEY = 998

FULL_PYGAME_KEYBOARD = {'K_BACKSPACE': 8, 'K_TAB': 9, 'K_CLEAR': 12, 'K_RETURN': 13, 'K_PAUSE': 19, 'K_ESCAPE': 27, 'K_SPACE': 32, 'K_EXCLAIM': 33, 'K_QUOTEDBL': 34, 'K_HASH': 35, 'K_DOLLAR': 36, 'K_AMPERSAND': 38, 'K_QUOTE': 39, 'K_LEFTPAREN': 40, 'K_RIGHTPAREN': 41, 'K_ASTERISK': 42, 'K_PLUS': 43, 'K_COMMA': 44, 'K_MINUS': 45, 'K_PERIOD': 46, 'K_SLASH': 47, 'K_0': 48, 'K_1': 49, 'K_2': 50, 'K_3': 51, 'K_4': 52, 'K_5': 53, 'K_6': 54, 'K_7': 55, 'K_8': 56, 'K_9': 57, 'K_COLON': 58, 'K_SEMICOLON': 59, 'K_LESS': 60, 'K_EQUALS': 61, 'K_GREATER': 62, 'K_QUESTION': 63, 'K_AT': 64, 'K_LEFTBRACKET': 91, 'K_BACKSLASH': 92, 'K_RIGHTBRACKET': 93, 'K_CARET': 94, 'K_UNDERSCORE': 95, 'K_BACKQUOTE': 96, 'K_a': 97, 'K_b': 98, 'K_c': 99, 'K_d': 100, 'K_e': 101, 'K_f': 102, 'K_g': 103, 'K_h': 104, 'K_i': 105, 'K_j': 106, 'K_k': 107, 'K_l': 108, 'K_m': 109, 'K_n': 110, 'K_o': 111, 'K_p': 112, 'K_q': 113, 'K_r': 114, 'K_s': 115, 'K_t': 116, 'K_u': 117, 'K_v': 118, 'K_w': 119, 'K_x': 120, 'K_y': 121, 'K_z': 122, 'K_DELETE': 127, 'K_KP0': 256, 'K_KP1': 257, 'K_KP2': 258, 'K_KP3': 259, 'K_KP4': 260, 'K_KP5': 261, 'K_KP6': 262, 'K_KP7': 263, 'K_KP8': 264, 'K_KP9': 265, 'K_KP_PERIOD': 266, 'K_KP_DIVIDE': 267, 'K_KP_MULTIPLY': 268, 'K_KP_MINUS': 269, 'K_KP_PLUS': 270, 'K_KP_ENTER': 271, 'K_KP_EQUALS': 272, 'K_UP': 273, 'K_DOWN': 274, 'K_RIGHT': 275, 'K_LEFT': 276, 'K_INSERT': 277, 'K_HOME': 278, 'K_END': 279, 'K_PAGEUP': 280, 'K_PAGEDOWN': 281, 'K_F1': 282, 'K_F2': 283, 'K_F3': 284, 'K_F4': 285, 'K_F5': 286, 'K_F6': 287, 'K_F7': 288, 'K_F8': 289, 'K_F9': 290, 'K_F10': 291, 'K_F11': 292, 'K_F12': 293, 'K_F13': 294, 'K_F14': 295, 'K_F15': 296, 'K_NUMLOCK': 300, 'K_CAPSLOCK': 301, 'K_SCROLLOCK': 302, 'K_RSHIFT': 303, 'K_LSHIFT': 304, 'K_RCTRL': 305, 'K_LCTRL': 306, 'K_RALT': 307, 'K_LALT': 308, 'K_RMETA': 309, 'K_LMETA': 310, 'K_LSUPER': 311, 'K_RSUPER': 312, 'K_MODE': 313, 'K_HELP': 315, 'K_PRINT': 316, 'K_SYSREQ': 317, 'K_BREAK': 318, 'K_MENU': 319, 'K_POWER': 320, 'K_EURO': 321}
FULL_REVERSED_KEYBOARD = {8: 'K_BACKSPACE', 9: 'K_TAB', 12: 'K_CLEAR', 13: 'K_RETURN', 19: 'K_PAUSE', 27: 'K_ESCAPE', 32: 'K_SPACE', 33: 'K_EXCLAIM', 34: 'K_QUOTEDBL', 35: 'K_HASH', 36: 'K_DOLLAR', 38: 'K_AMPERSAND', 39: 'K_QUOTE', 40: 'K_LEFTPAREN', 41: 'K_RIGHTPAREN', 42: 'K_ASTERISK', 43: 'K_PLUS', 44: 'K_COMMA', 45: 'K_MINUS', 46: 'K_PERIOD', 47: 'K_SLASH', 48: 'K_0', 49: 'K_1', 50: 'K_2', 51: 'K_3', 52: 'K_4', 53: 'K_5', 54: 'K_6', 55: 'K_7', 56: 'K_8', 57: 'K_9', 58: 'K_COLON', 59: 'K_SEMICOLON', 60: 'K_LESS', 61: 'K_EQUALS', 62: 'K_GREATER', 63: 'K_QUESTION', 64: 'K_AT', 91: 'K_LEFTBRACKET', 92: 'K_BACKSLASH', 93: 'K_RIGHTBRACKET', 94: 'K_CARET', 95: 'K_UNDERSCORE', 96: 'K_BACKQUOTE', 97: 'K_a', 98: 'K_b', 99: 'K_c', 100: 'K_d', 101: 'K_e', 102: 'K_f', 103: 'K_g', 104: 'K_h', 105: 'K_i', 106: 'K_j', 107: 'K_k', 108: 'K_l', 109: 'K_m', 110: 'K_n', 111: 'K_o', 112: 'K_p', 113: 'K_q', 114: 'K_r', 115: 'K_s', 116: 'K_t', 117: 'K_u', 118: 'K_v', 119: 'K_w', 120: 'K_x', 121: 'K_y', 122: 'K_z', 127: 'K_DELETE', 256: 'K_KP0', 257: 'K_KP1', 258: 'K_KP2', 259: 'K_KP3', 260: 'K_KP4', 261: 'K_KP5', 262: 'K_KP6', 263: 'K_KP7', 264: 'K_KP8', 265: 'K_KP9', 266: 'K_KP_PERIOD', 267: 'K_KP_DIVIDE', 268: 'K_KP_MULTIPLY', 269: 'K_KP_MINUS', 270: 'K_KP_PLUS', 271: 'K_KP_ENTER', 272: 'K_KP_EQUALS', 273: 'K_UP', 274: 'K_DOWN', 275: 'K_RIGHT', 276: 'K_LEFT', 277: 'K_INSERT', 278: 'K_HOME', 279: 'K_END', 280: 'K_PAGEUP', 281: 'K_PAGEDOWN', 282: 'K_F1', 283: 'K_F2', 284: 'K_F3', 285: 'K_F4', 286: 'K_F5', 287: 'K_F6', 288: 'K_F7', 289: 'K_F8', 290: 'K_F9', 291: 'K_F10', 292: 'K_F11', 293: 'K_F12', 294: 'K_F13', 295: 'K_F14', 296: 'K_F15', 300: 'K_NUMLOCK', 301: 'K_CAPSLOCK', 302: 'K_SCROLLOCK', 303: 'K_RSHIFT', 304: 'K_LSHIFT', 305: 'K_RCTRL', 306: 'K_LCTRL', 307: 'K_RALT', 308: 'K_LALT', 309: 'K_RMETA', 310: 'K_LMETA', 311: 'K_LSUPER', 312: 'K_RSUPER', 313: 'K_MODE', 315: 'K_HELP', 316: 'K_PRINT', 317: 'K_SYSREQ', 318: 'K_BREAK', 319: 'K_MENU', 320: 'K_POWER', 321: 'K_EURO'}
FULL_KEY_BOARD = [8, 9, 12, 13, 19, 27, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52,
                  53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102,
                  103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122,
                  127, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274,
                  275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294,
                  295, 296, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 315, 316, 317, 318,
                  319, 320, 321]

KEYBOARD = [K_SPACE, K_w, K_ESCAPE]  # what do you have in your virtual keyboard
KEYBOARD_COMMAND_DICT = {
    K_SPACE: PAUSE,
    K_w: NEXT_WAVE,
    K_ESCAPE: RETURN
}

################################################################################
# Layer
LAYER_MAIN_MENU = "main menu"
LAYER_GAME_PANEL = "game"
LAYER_TUTORIAL = "tutorial"
LAYER_SETTING_MENU = "setting menu"
LAYER_LICENSE = "license menu"

LAYER_IN_GAME_MENU = "in game menu"
LAYER_PURCHASE_MENU = "purchase menu"
LAYER_SELECTION = "selection mode"
LAYER_TOWER_MENU = "tower menu"

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
GAME_PANEL_POS = 0, 0
GAME_PANEL_DIM = GAME_PANEL_WIDTH, GAME_PANEL_HEIGHT = SCREEN_DIM

GAME_PANEL_IN_GAME_MENU_CUT = GAME_PANEL_IN_GAME_MENU_X_CUT, GAME_PANEL_IN_GAME_MENU_Y_CUT = 0, 800

##################################################################################
# TUTORIAL
TUTORIAL_POS = 50, 100
TUTORIAL_DIM = TUTORIAL_WIDTH, TUTORIAL_HEIGHT = 700, 800

# SETTING_MENU
SETTING_MENU_POS = 200, 250
SETTING_MENU_DIM = SETTING_MENU_WIDTH, SETTING_MENU_HEIGHT = 400, 310

# LICENSE_MENU_DIM
LICENSE_MENU_POS = 50, 100
LICENSE_MENU_DIM = LICENSE_MENU_WIDTH, LICENSE_MENU_HEIGHT = 700, 800

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
TOWER_MENU_DIM = 0, 0


#############################      Objects        #############################
###############################################################################
# Tower
TOWER_DIM = 20, 20  # by default

DMG_TOWER = 1
CC_TOWER = 2

DMG_BULLET_LV1 = 10, 20, None, (4, 4), DMG_BULLET_LV1_IMG  # dmg, vel, cc, dim, image
DMG_TOWER_LV1 = 10, DMG_BULLET_LV1, 0.4, 2, "Tower Lv1", DMG_TOWER_IMG  # cost, bullet, attkFreq(sec), range, name, img

CC_BULLET_LV1 = 8, 25, None, (4, 4), CC_BULLET_LV1_IMG
CC_TOWER_LV1 = 30, CC_BULLET_LV1, 0.3, 3, "Long Range Tower Lv1", CC_TOWER_IMG

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

##################################################################################


















