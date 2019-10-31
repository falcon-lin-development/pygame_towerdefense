#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 16:39:58 2019

@author: Falcon
Constuctor
"""
import config as c
import world as w
import gameobject as g
import button as b
import pygame as pg

class Constructor(object):
    def __init__(self, mp = c.TEST_MAP, level = c.TEST_WAVE):
#        self.creepPath = creepPath
        self.mp = mp
        self.level = self.loadLevel(level)
        self.wave = 0
        self.creepPath = None
        self.world = None   
    def loadLevel(self, level):
        f = open(level)
        self.waves = f.read().split('\n')
        f.close
        return 1
    
    def nextWave(self):
        out = []
        for creep in self.waves[self.wave]:
            out.append(self.creepConstruction(creep))
        self.wave += 1
        if self.wave >= len(self.waves): 
            self.wave = 0
            self.level += 0.5
        return out
    def creepConstruction(self, typ = None):
        if typ == c.BRAWLER:
            return g.Creep(self.creepPath,level = self.level, info = c.BRAWLER_INFO)
        elif typ == c.SOLDIER:
            return g.Creep(self.creepPath,level = self.level, info = c.SOLDIER_INFO)
        elif typ == c.TANK:
            return g.Creep(self.creepPath,level = self.level, info = c.TANK_INFO)
        elif typ == c.NINJA:
            return g.Creep(self.creepPath,level = self.level, info = c.NINJA_INFO)
        elif typ == c.KNIGHT:
            return g.Creep(self.creepPath,level = self.level, info = c.KNIGHT_INFO)
        elif typ == c.DRAGON:
            return g.Creep(self.creepPath,level = self.level, info = c.DRAGON_INFO)
        else:
            return g.Creep(self.creepPath)
    def dataTower(self, dimBox, typ = None):
        x, y, w, h = dimBox
        return g.Tower(x,y)
    def towerConstruction(self, cDimBox, order = None):
        cx, cy, w, h = cDimBox
        try:
            tile = self.world.pointIsIn((cx,cy))
        except:
            return None
        
        x, y = tile.getPos()
        if tile.occupied == False:
            tile.occupied = True
            if order == 'ccTowerPurchase':
                return g.Tower(x, y, info = c.CC_TOWER)
            elif order == 'dmgTowerPurchase':
                return g.Tower(x, y, info = c.DMG_TOWER)
            else:
                return g.Tower(x,y)
        else:
            return None
    def towerDestruction(self, tower):
        cx, cy = tower.getCenter()
        tile = self.world.pointIsIn((cx,cy))
        tile.occupied = False
        return tower.cost //2

    def worldConstruction(self):
        f = open(self.mp)
        l = f.read().split('\n')
        f.close
        out = []
        for j, row in enumerate(l):
            for i,tile in enumerate(row):
                if tile == c.GRASS:
                    out.append(w.GrassTile(i*c.TILE_WIDTH,j*c.TILE_HEIGHT))
                elif tile ==c.TILE:
                    out.append(w.PathTile(i*c.TILE_WIDTH,j*c.TILE_HEIGHT))
                elif tile == c.TURN_TILE:
                    out.append(w.TurnTile(i*c.TILE_WIDTH,j*c.TILE_HEIGHT))
                elif tile == c.BORN_TILE:
                    out.append(w.BornTile(i*c.TILE_WIDTH,j*c.TILE_HEIGHT))
                elif tile == c.GOAL_TILE:
                    out.append(w.GoalTile(i*c.TILE_WIDTH,j*c.TILE_HEIGHT))
                else:
                    print('oopss')
        self.world = w.World(out)
        return self.world
    


if __name__ == "__main__":
    a = Constructor()

