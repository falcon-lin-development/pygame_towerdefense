#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 17:33:37 2019

@author: Falcon
Buttons
"""
import item
import pygame
import config as c


class Button(item.RectItem):
    def __init__(self, x, y, width, height, ref):
        item.RectItem.__init__(self, x, y, width, height)
        self.ref = ref
        self.hover = False
        self.acti = False
        self.fixXY()
        self.buttonCD = 10

    # game function
    def onClick(self):
        pass

    def unClick(self):
        self.acti = False
        self.hover = False

    def checkCD(self):
        if self.buttonCD <= 0:
            self.buttonCD = 10
            return True
        else:
            return False

    def decbCD(self):
        if self.buttonCD >= 0: self.buttonCD -= 1

    # display function
    def draw(self, win):
        if self.hover:
            win.blit(self.image, self.getPos())
        else:
            win.blit(self.image, self.getPos())

    def drawBox(self, win):
        pygame.draw.rect(win, (210, 180, 140), self.getDimBox())
        font = pygame.font.SysFont('calibri', 30)
        if self.hover:
            try:
                text = font.render(str(self.price), 1, (0, 255, 0))
            except:
                text = font.render('hover', 1, (0, 255, 0))
        else:
            text = font.render(self.__class__.__name__, 1, (0, 255, 0))
        cx, cy = self.getCenter()
        win.blit(text, (cx - text.get_width() // 2, cy - text.get_height() // 2))

    def __str__(self):
        return self.__class__.__name__ + ' Button {0}, '.format(self.getPos())

    __repr__ = __str__

    # attribute function
    def safeLoadImage(self, image):
        try:
            return pygame.image.load(image)
        except:
            return None

    def fixXY(self, pos=0):
        if pos:
            rx, ry = self.ref = pos
        else:
            rx, ry = self.ref
        x, y = self.getPos()
        self.x, self.y = x + rx, y + ry

    def getVertices(self):
        x, y, w, h = self.getDimBox()
        return (x, y), (x + w, y), (x, y + h), (x + w, y + h)

    def isInside(self, v, vertices):
        x, y = v
        if x > vertices[0][0] and x < vertices[3][0]:
            if y > vertices[0][1] and y < vertices[3][1]:
                return True
        return False


class Purchase(Button):
    def __init__(self, x, y, width, height, referenceFrame, info=c.DEFAULT_PURCHASE_INFO):
        Button.__init__(self, x, y, width, height, referenceFrame)
        self.image = self.safeLoadImage(info[-1])

    def onClick(self, info=None):
        self.acti = True
        action = 'towerPurchase'
        return action


class Sell(Button):
    def __init__(self, x, y, width, height, ref, info=c.DEFAULT_SELL_INFO, parent=None):
        Button.__init__(self, x, y, width, height, ref)
        if parent:
            self.parent = parent
            self.price = self.parent.cost * 0.5
            self.onClick = self.onClickTarget
        self.image = self.safeLoadImage(info[-1])

    def onClickTarget(self, info=None):
        return 'sellThisTower', self.parent, self.price

    def onClick(self, info=None):
        action = 'towerSell'
        return action


class NextWave(Button):
    def __init__(self, x, y, width, height, ref, info=c.DEFAULT_SETTING_INFO):
        Button.__init__(self, x, y, width, height, ref)
        self.image = self.safeLoadImage(info[-1])

    def onClick(self, info=None):
        action = 'nextWave'
        return action


class Exit(Button):
    def __init__(self, x, y, width, height, ref, info=c.DEFAULT_EXIT_INFO):
        Button.__init__(self, x, y, width, height, ref)
        self.image = self.safeLoadImage(info[-1])

    def onClick(self, info=None):
        action = 'Exit'
        return action


class CCTower(Button):
    def __init__(self, x, y, width, height, ref, info=c.DEFAULT_PURCHASE_INFO):
        Button.__init__(self, x, y, width, height, ref)
        self.image = self.safeLoadImage(info[-1])

    def onClick(self, info=None):
        self.acti = True
        action = 'ccTowerPurchase'
        return action


class DMGTower(Button):
    def __init__(self, x, y, width, height, ref, info=c.DEFAULT_PURCHASE_INFO):
        Button.__init__(self, x, y, width, height, ref)
        self.image = self.safeLoadImage(info[-1])

    def onClick(self, info=None):
        self.acti = True
        action = 'dmgTowerPurchase'
        return action


class UpGrade(Button):
    def __init__(self, x, y, width, height, ref, info=c.DEFAULT_PURCHASE_INFO, parent=None):
        Button.__init__(self, x, y, width, height, ref)
        if parent:
            self.parent = parent
            self.price = parent.getUpgradeCost()
            self.onClick = self.onClickTarget
        self.image = self.safeLoadImage(info[-1])

    def onClickTarget(self, info=None):
        money = info
        if money > self.price:
            return ('upgradeThisTower', self.parent, self.price)
        else:
            return None

    def onClick(self, info=None):
        self.acti = True
        action = 'TowerUpgrade'
        return action


class Menu(item.RectItem):
    def getVertices(self):
        x, y, w, h = self.getDimBox()
        return (x, y), (x + w, y), (x, y + h), (x + w, y + h)

    def isInside(self, v, vertices):
        x, y = v
        if x > vertices[0][0] and x < vertices[3][0]:
            if y > vertices[0][1] and y < vertices[3][1]:
                return True
        return False


class GameMenu(Menu):
    #   this class is made to arrange all button and present them on the screen:
    def __init__(self, dimBox=c.GAME_MENU_DIMBOX, info=c.GAME_MENU):
        # fixed info
        self.x, self.y, self.width, self.height = dimBox
        self.ref = self.x, self.y
        self.border = 15
        self.typ = info[0]
        self.buttons = self.construction(info[1])

    def construction(self, listOfButtons):
        out = []
        for b in listOfButtons:
            x, y, w, h, ref = self.calcButtonDimRef(b)
            out.append(globals()[b](x, y, w, h, ref))
        return out

    def calcTrueDimBox(self, pos=(0, 0)):
        x, y = pos
        rx, ry = self.ref
        w = self.width
        h = self.height
        return x + rx, y + ry, w, h

    def calc1dimBox(self, pos=(0, 0)):
        x, y, w, h = self.calcTrueDimBox(pos)
        w1 = int(w // 3 * 2 - 1.5 * self.border)
        return x + self.border, y + self.border, w1, h - 2 * self.border

    def calc2dimBox(self, pos=(0, 0)):
        x, y, w, h = self.calcTrueDimBox(pos)
        w1 = w // 3 * 2
        x, y, w, h = w1, y, w1 // 2, h
        return int(x + 0.5 * self.border), y + self.border, int(w - 1.5 * self.border), h - 2 * self.border

    def calc1contentDimBox(self, pos=(0, 0)):
        x, y, w, h = self.calc1dimBox(pos)
        return x + self.border, y + self.border, w - 2 * self.border, h - 2 * self.border

    def calc2contentDimBox(self, pos=(0, 0)):
        x, y, w, h = self.calc2dimBox(pos)
        return x + self.border, y + self.border, w - 2 * self.border, h - 2 * self.border

    def calcContentRef(self, frame=1):
        if frame == 1:
            return self.calc1contentDimBox()[0], self.calc1contentDimBox()[1]
        else:
            return self.calc2contentDimBox()[0], self.calc2contentDimBox()[1]

    def calcButtonDimRef(self, buttonType):
        x, y, w, h = self.calc2contentDimBox()
        h2 = (h - 2 * self.border) // 3
        if buttonType == 'Purchase':
            x, y, w, h = self.calc1contentDimBox()
            return 0, h // 2, w, h // 2, self.calcContentRef(1)
        elif buttonType == 'Sell':
            return 0, 0, w, h2, self.calcContentRef(2)
        elif buttonType == 'NextWave':
            return 0, h2 + self.border, w, h2, self.calcContentRef(2)
        elif buttonType == 'Exit':
            return 0, 2 * (h2 + self.border), w, h2, self.calcContentRef(2)
        else:
            raise Exception

    def draw(self, win):
        win.blit(self.image, self.getPos())
        for button in self.buttons:
            button.draw(win)

    def drawBox(self, win):
        pygame.draw.rect(win, (139, 69, 19), self.calcTrueDimBox())
        pygame.draw.rect(win, (255, 222, 173), self.calc1dimBox())
        pygame.draw.rect(win, (255, 222, 173), self.calc2dimBox())
        for button in self.buttons:
            button.drawBox(win)

    def drawInfo(self, win, live, money):
        font = pygame.font.SysFont('calibri', 30)
        text = font.render('live: {0}'.format(live), 1, (100, 255, 0))
        text1 = font.render('money: {0}'.format(money), 1, (100, 255, 0))
        textDim, text1Dim = text.get_rect(), text1.get_rect()
        x, y, w, h = self.calc1contentDimBox()
        textDim.move_ip(x, y)
        text1Dim.move_ip(x, y + text.get_height() + self.border)
        win.blit(text, textDim)
        win.blit(text1, text1Dim)
        pygame.draw.rect(win, (0, 0, 0), textDim, 1)
        pygame.draw.rect(win, (0, 0, 0), text1Dim, 1)

    def __str__(self):
        out = ''
        for b in self.buttons:
            out += b.__str__
        return '[{0}]'.format(out)

    __repr__ = __str__


class PurchaseMenu(Menu):
    def __init__(self, pos=(0, 0), dim=c.PURCHASE_MENU_DIM, info=c.PURCHASE_MENU):
        # fixed info
        self.x, self.y = pos
        self.width, self.height = dim
        self.y -= self.height
        self.ref = self.x, self.y
        self.border = 15
        self.typ = info[0]
        self.buttons = self.construction(info[1])

    def construction(self, listOfButtons):
        out = []
        for b in listOfButtons:
            x, y, w, h, ref = self.calcButtonDimRef(b)
            out.append(globals()[b](x, y, w, h, ref))
        return out

    def calcTrueDimBox(self, pos=(0, 0)):
        x, y = pos
        rx, ry = self.ref
        w = self.width
        h = self.height
        return x + rx, y + ry, w, h

    def calcDimBox2(self, pos=(0, 0)):
        x, y, w, h = self.calcTrueDimBox(pos)
        return x + self.border, y + self.border, w - 2 * self.border, h - 2 * self.border

    def calContentDimBox(self, pos=(0, 0)):
        x, y, w, h = self.calcDimBox2(pos)
        return x + self.border, y + self.border, w - 2 * self.border, h - 2 * self.border

    def calcButtonDimRef(self, buttonType):
        x, y, w, h = self.calContentDimBox()
        if buttonType == 'CCTower':
            return 0, 0, w, 40, (x, y)
        elif buttonType == 'DMGTower':
            return 0, 40 + self.border, w, 40, (x, y)
        else:
            raise Exception

    def draw(self, win):
        win.blit(self.image, self.getPos())
        for button in self.buttons:
            button.draw(win)

    def drawBox(self, win):
        pygame.draw.rect(win, (139, 69, 19), self.calcTrueDimBox())
        pygame.draw.rect(win, (255, 222, 173), self.calcDimBox2())
        for button in self.buttons:
            button.drawBox(win)


class TowerMenu(Menu):
    def __init__(self, pos=(0, 0), dim=c.TOWER_MENU_DIM, info=c.TOWER_MENU, parent=None):
        # fixed info
        self.x, self.y = pos
        self.width, self.height = dim
        self.ref = self.x, self.y
        self.border = 10
        self.typ = info[0]
        self.parent = parent
        self.buttons = self.construction(info[1])

    def construction(self, listOfButtons):
        out = []
        for b in listOfButtons:
            x, y, w, h, ref = self.calcButtonDimRef(b)
            out.append(globals()[b](x, y, w, h, ref, parent=self.parent))
        return out

    def calcTrueDimBox(self, pos=(0, 0)):
        x, y = pos
        rx, ry = self.ref
        w = self.width
        h = self.height
        return x + rx, y + ry, w, h

    def calcDimBox2(self, pos=(0, 0)):
        x, y, w, h = self.calcTrueDimBox(pos)
        return x + self.border, y + self.border, w - 2 * self.border, h - 2 * self.border

    def calContentDimBox(self, pos=(0, 0)):
        x, y, w, h = self.calcDimBox2(pos)
        return x + self.border, y + self.border, w - 2 * self.border, h - 2 * self.border

    def calcButtonDimRef(self, buttonType):
        x, y, w, h = self.calContentDimBox()
        if buttonType == 'UpGrade':
            return 0, 0, w, 30, (x, y)
        elif buttonType == 'Sell':
            return 0, 30 + self.border, w, 30, (x, y)
        else:
            raise Exception

    def draw(self, win):
        win.blit(self.image, self.getPos())
        for button in self.buttons:
            button.draw(win)

    def drawBox(self, win):
        pygame.draw.rect(win, (139, 69, 19), self.calcTrueDimBox())
        pygame.draw.rect(win, (255, 222, 173), self.calcDimBox2())
        for button in self.buttons:
            button.drawBox(win)
