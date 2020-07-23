"""
Implementation of all Bar(a Textbox), Text, Button classes


developer Note:
on it    1) can further abstract away all buttons
    2) message box feature
"""
from game.item import StaticItem
import pygame
from game.config import *
from game.functions import calcAlignImgPos, calc_abs_pos


class Bar(StaticItem):
    """
    Bar object is a box with designed display_text and information(value)

    dim: a tuple (width, height)
    display_name: str or integer that will be displayed On the bar
    value(optional): the value contain inside the object
    """

    def __init__(self, dim, display_name, value=None):
        self.dim = self.width, self.height = dim
        self.display_name = display_name
        self.v = value
        self.image = self.make_image()

    def get_value(self):
        return self.v

    # init func
    def make_image(self):
        font_size = 20
        font = pygame.font.SysFont("calibri", font_size)
        text = font.render(str(self.display_name) + " : " +
                           str(self.v), True, BLUE, None)
        return text

    # draw function
    def draw(self, surface, offset):
        self.draw_bg(surface, offset)
        abs_pos = calc_abs_pos(calcAlignImgPos(
            (self.width//2, self.height//2), self.image), offset)
        surface.blit(self.image, abs_pos)

    def draw_box(self, surface, offset):
        # blit rect, blit text
        pygame.draw.rect(
            surface, BLUE, (offset[0], offset[1], self.width, self.height), 1)
        abs_pos = calc_abs_pos(calcAlignImgPos(
            (self.width // 2, self.height // 2), self.image), offset)
        surface.blit(self.image, abs_pos)

    def draw_bg(self, surface, offset):
        border = 5
        pygame.draw.rect(surface, COLOR_8B4513,
                         (offset[0], offset[1], self.width, self.height), 0)
        pygame.draw.rect(surface, COLOR_FFDEAD, (
            offset[0]+border, offset[1]+border, self.width-2*border, self.height-2*border), 0)


class Text(Bar):
    """
    Create a pure text object

    font_size: the size of text
    color: RBG code for text color , e.g. (0,0,0) for black
    bold(optional): bool value for bold text
    italic(optional): bool value for italic text
    """

    def __init__(self, font_size, text, color=BLUE, bold=False, italic=False):
        font = pygame.font.SysFont("calibri", font_size, bold, italic)
        self.image = font.render(str(text), True, color, None)

    # draw function
    def draw(self, surface, offset):
        self.draw_box(surface, offset)

    def draw_box(self, surface, offset):
        # blit rect, blit text
        surface.blit(self.image, offset)


class Button(Bar):
    """
    Button object is a Bar object with hover and onclick response

    value: a command tuple (COMMAND, INFO) for the onclick function to return
    """

    def __init__(self, dim, display_name, value):
        super().__init__(dim, display_name, value)
        self.hover_image = self._make_hover_image()
        self.hover = False

    # init function
    def make_image(self):
        font_size = 20
        font = pygame.font.SysFont("calibri", font_size)
        text = font.render(str(self.display_name), True, BLUE, None)
        return text

    def _make_hover_image(self):
        font_size = 20
        font = pygame.font.SysFont("calibri", font_size)
        # text = font.render(str(self.v), True, BLUE, None)
        text = font.render("hover", True, BLUE, None)
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
    def draw(self, surface, offset):
        if self.hover:
            super().draw_bg(surface, offset)
            # blit hover image
            abs_pos = calc_abs_pos(calcAlignImgPos(
                (self.width // 2, self.height // 2), self.hover_image), offset)
            surface.blit(self.hover_image, abs_pos)
        else:
            super().draw(surface, offset)

    def draw_box(self, surface, offset):
        if self.hover:
            pygame.draw.rect(
                surface, BLUE, (offset[0], offset[1], self.width, self.height), 1)
            # blit hover image
            abs_pos = calc_abs_pos(calcAlignImgPos(
                (self.width // 2, self.height // 2), self.hover_image), offset)
            surface.blit(self.hover_image, abs_pos)
        else:
            super().draw_box(surface, offset)


# main menu
class NewGame(Button):
    pass


class LoadGame(Button):
    pass


class Tutorial(Button):
    pass


class Setting(Button):
    pass


class License(Button):
    pass


class Resume(Button):
    pass


# Setting Menu
class Pause(Bar):
    pass


class NewWave(Bar):
    def make_image(self):
        font_size = 20
        font = pygame.font.SysFont("calibri", font_size)
        text = font.render(str(self.display_name), True, BLUE, None)
        return text


class Return(Bar):
    pass


class Volume(Bar):
    pass


class SetPause(Button):
    def change_key(self, key):
        self.display_name = key
        self.image = self.make_image()


class SetNewWave(Button):
    def change_key(self, key):
        self.display_name = key
        self.image = self.make_image()


class SetReturn(Button):
    def change_key(self, key):
        self.display_name = key
        self.image = self.make_image()


class SetVolume(Button):
    def __init__(self,  dim, display_name, value=None):
        self.state = display_name
        super().__init__(dim, display_name, value)

    def make_image(self):
        if self.state:
            display = "On"
        else:
            display = "Off"

        font_size = 20
        font = pygame.font.SysFont("calibri", font_size)
        text = font.render(display, True, BLUE, None)
        return text

    def change_key(self, state=None):
        if state:
            self.state = state
            self.image = self.make_image()
        else:
            self.state = not self.state
            self.image = self.make_image()

# in game menu


class Purchase(Button):
    pass


class Items(Button):
    pass


class NextWave(Button):
    pass


class SaveGame(Button):
    pass


class Exit(Button):
    pass


class HealthBar(Bar):
    def hit(self):
        self.v -= 1
        self.image = self.make_image()


class MoneyBar(Bar):
    def pay(self, price):
        self.v -= price
        self.image = self.make_image()

    def earn(self, money):
        self.v += money
        self.image = self.make_image()


class WaveBar(Bar):
    def incre_wave(self):
        self.v += 1
        self.image = self.make_image()


# purchase menu
class DMGTower(Button):
    pass


class CCTower(Button):
    pass


# Tower menu
class TowerItems(Button):
    pass


class TowerLevelUp(Button):
    def make_image(self):
        font_size = 20
        font = pygame.font.SysFont("calibri", font_size)
        text = font.render(str("Level_up cost") + " : " +
                           str(self.display_name), True, BLUE, None)
        return text


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
