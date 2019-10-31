#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 17:23:58 2019

@author: Falcon
Message Box
"""
import item
import pygame

class MessageBox(item.RectItem):
    def __init__(self, msgs, referenceCoord):
        self.msgs = self.makeMsg(msgs) # msg list
        self.ref = referenceCoord
        self.border = 10
    def makeMsg(self, msgs):
        out = []
        for i, msg in enumerate(msgs):
            out.append(Msg((0, i*30), msg))
        return out
    def calcTrueDimBox(self, pos = (0,0)):
        x, y = pos
        rx, ry = self.ref
        w = max([msg.image.get_width() for msg in self.msgs]) + 4 * self.border
        h = self.msgs[-1].getBottom() + 4 * self.border
        return x + rx, y+ry, w, h
    def calcDimBox2(self, pos = (0,0)):
        x, y, w, h = self.calcTrueDimBox(pos)
        return x+self.border, y+self.border, w - 2*self.border, h-2*self.border
    def calContentDimBox(self, pos = (0,0)):
        x, y, w, h = self.calcDimBox2(pos)
        return x+self.border, y+self.border, w - 2*self.border, h-2*self.border
    def draw(self, win):
        pygame.draw.rect(win, (139,69,19), self.calcTrueDimBox())
        pygame.draw.rect(win, (255,222,173), self.calcDimBox2())
        for msg in self.msgs:
            msg.draw(win, self.calContentDimBox(msg.getPos()))
    drawBox = draw
    
class Msg(item.RectItem):
    def __init__(self, pos = (0,0), msg = ''):
        self.msg = msg
        self.x, self.y = pos
        self.image = self.getSurface(self.msg)
    def getSurface(self, msg, color = (0, 0, 0), size = 30):
        font = pygame.font.SysFont('calibri', size)
        return font.render('{0}'.format(msg), 1, color) 
    def getBottom(self):
        return self.y + self.image.get_height()
    def draw(self, win, pos):
        win.blit(self.image, pos)
        
        
