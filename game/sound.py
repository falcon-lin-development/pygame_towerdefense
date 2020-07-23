"""
pyfame.mixer.Sound handler
"""

from game.config import *
import pygame

if __name__ == "__main__":
    pygame.mixer.init()


class Py_Sound(object):
    def __init__(self):
        self.bg_music = pygame.mixer.Sound(BG_MUSIC)
        self.hit_sound = pygame.mixer.Sound(HIT_SOUND)
        self.vol_state = True

    # setting
    def sound_on(self):
        self.bg_music.set_volume(1)
        self.hit_sound.set_volume(1)
        self.vol_state = True

    def sound_off(self):
        self.bg_music.set_volume(0)
        self.hit_sound.set_volume(0)
        self.vol_state = False

    def set_vol(self, vol):
        self.bg_music.set_volume(vol)
        self.hit_sound.set_volume(vol)
        self.vol_state = bool(vol)

    # playing
    def play_bg(self):
        self.bg_music.play(-1)

    def stop_bg(self):
        self.bg_music.stop()

    def play_hit(self):
        self.hit_sound.play(0)