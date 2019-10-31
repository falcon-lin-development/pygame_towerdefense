#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 19:19:04 2019

@author: Falcon
"""
import config as c
from sm import SM
class RectItem(object):
    def __init__(self, x=0, y=0, width=c.STANDARD_WIDTH, height=c.STANDARD_HEIGHT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def getPos(self):
        return self.x, self.y
    def getCenter(self):
        return int(self.x + self.width//2), int(self.y + self.height//2)
    def getDimBox(self):
        return self.x, self.y, self.width, self.height
    def getVertices(self):
        return (self.x ,self.y), (self.x+self.width, self.y), (self.x, self.y+self.height),(self.x+self.width, self.y+self.height)
    def getArea(self):
        return int(self.width * self.height)
    def safeAdd(self, a, b):
        return int(a+b)
    def safeMul(self, a, b):
        return int(a*b)
    def safeExpo(self, a, b):
        return int(a**b)
    def isInside(self, v, vertices):
        x, y = v
        if x > vertices[0][0] and x < vertices[3][0]:
            if y > vertices[0][1] and y < vertices[3][1]:
                return True
        return False   
    
class RectGameObject(SM, RectItem):
    pass
    
