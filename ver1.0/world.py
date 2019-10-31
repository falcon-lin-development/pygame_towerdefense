#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 19:45:12 2019

@author: Falcon

all world class
"""
import item
import pygame
import config as c

class Tile(item.RectItem):
    def __init__(self, x=0, y=0, width=c.TILE_WIDTH, height=c.TILE_HEIGHT, image=None):
        item.RectItem.__init__(self, x, y, width, height)
        self.image = pygame.image.load(image)
        self.occupied = True
    def draw(self, win):
        if self.visible:
            win.blit(self.image, self.getPos())
        else:
            print('{0} is covered'.format(self.getPos()))
    def drawBox(self, win, w):
        pygame.draw.rect(win, (255,255,255), self.getDimBox(), w)
 
    def __str__(self):
        return self.__class__.__name__ + '(' + str(self.x) + ',' +\
                str(self.y) + ')'
    __repr__ = __str__
    

class PathTile(Tile):
    def __init__(self, x=0, y=0, width=c.TILE_WIDTH, height=c.TILE_HEIGHT, image = c.PATH_IMAGE):
        Tile.__init__(self, x, y, width, height,image)
        self.visible = True
        self.hover = False
    def drawBox(self, win, w):
        pygame.draw.rect(win, (105,105,105), self.getDimBox(), w)

class TurnTile(Tile):
    #visually same as path, but creep will see it different
    def __init__(self, x=0, y=0, width=c.TILE_WIDTH, height=c.TILE_HEIGHT, image = c.TURN_IMAGE):
        Tile.__init__(self, x, y, width, height,image)
        self.visible = True
        self.hover = False
    def drawBox(self, win, w):
        pygame.draw.rect(win, (200,200,200), self.getDimBox(), w)
        
class BornTile(Tile):
    #visually same as path, but creep will see it different
    def __init__(self, x=0, y=0, width=c.TILE_WIDTH, height=c.TILE_HEIGHT, image = c.BORN_IMAGE):
        Tile.__init__(self, x, y, width, height,image)
        self.visible = True
        self.hover = False
    def drawBox(self, win, w):
        pygame.draw.rect(win, (50,50,50), self.getDimBox(), w)
        
class GoalTile(Tile):
    #visually same as path, but creep will see it different
    def __init__(self, x=0, y=0, width=c.TILE_WIDTH, height=c.TILE_HEIGHT, image = c.GOAL_IMAGE):
        Tile.__init__(self, x, y, width, height,image)
        self.visible = True
        self.hover = False
    def drawBox(self, win, w):
        pygame.draw.rect(win, (40,89,205), self.getDimBox(), w)
            
class GrassTile(Tile):
    def __init__(self, x=0, y=0, width=c.TILE_WIDTH, height=c.TILE_HEIGHT, image = c.GRASS_IMAGE):
        Tile.__init__(self, x, y, width, height,image)
        self.visible = True
        self.hover = False
        self.occupied = False
    def drawBox(self, win, w):
        pygame.draw.rect(win, (0,100,0), self.getDimBox(), w)
        

class World(item.RectItem):
    '''
    a combinator for different tiles: grass / path
    by default it is a square
    '''
    def __init__(self, listOfTiles,  x=0, y=0, screenWidth=c.WORLD_WIDTH, screenHeight=c.WORLD_HEIGHT):
        item.RectItem.__init__(self, x, y, screenWidth, screenHeight) # pixel dim
        self.wWidth = self.wHeight = self.safeExpo(len(listOfTiles), 0.5) # tile dim
        self.listOfTiles = listOfTiles
        self.wTiles = [[tile for tile in listOfTiles[self.wHeight*i:self.wHeight*(i+1)]]for i in range(self.wHeight)]
        self.creepPath = self.calcCreepPath()
        self.fixImg()
#        for j in range(self.wHeight):
#            tem = []
#            for i in range(self.wWidth):
#                tem.append(listOfTiles.pop(0))
#            self.tiles.append(tem)
    def fixImg(self):
        for tile in self.listOfTiles:
            if self.isPath(tile):
                if tile.__class__.__name__ == 'TurnTile':
                    tile.image = pygame.transform.rotate(tile.image, self.turnTileRotate(tile))
                else:
                    if not self.isVer(tile):
                        tile.image = pygame.transform.rotate(tile.image, 90)
            else:
                if self.isNearPath(tile):
                    tile.image = pygame.image.load(self.findNearPathImg(tile))
                
    
            
                        

    def saveFind(self, row, col):
        try:
            if row == -1 or col == -1:
                return None
            return self.wTiles[row][col]
        except:
            return None
    def findNearTiles(self, tile):
        row, col = self.findTile(tile)
        leftTile = self.saveFind(row, col-1)
        rightTile = self.saveFind(row, col+1)
        topTile = self.saveFind(row-1, col)
        botTile = self.saveFind(row+1, col)
        return [leftTile, rightTile, topTile, botTile]
    def isVer(self, tile):
        nearTiles = self.findNearTiles(tile)
        for i, tile in enumerate(nearTiles):
            if tile != None:
                if self.isPath(tile):
                    if i < 2:
                        return False
                    else:
                        return True
    def isPath(self, tile):
        pathName = ['BornTile','GoalTile','PathTile','TurnTile']
        return tile.__class__.__name__ in pathName
    def isNearPath(self, tile):
        for tile in self.findNearTiles(tile):
            if self.isPath(tile):
                return True
        return False
    def findNearPathImg(self, tile):
        isPaths = [self.isPath(t) for t in self.findNearTiles(tile)]
        if isPaths.count(True) == 1:
            i = isPaths.index(True)
            if i == 0:
                return c.GRASS_ROAD_R
            elif i == 1:
                return c.GRASS_ROAD_L
            elif i == 2:
                return c.GRASS_ROAD_B
            else:
                return c.GRASS_ROAD_T
        else:
            i1, i2 = [i for i, x in enumerate(isPaths) if x == True]
            if i1 == 0 and i2 == 2:
                return c.GRASS_ROAD_RB
            elif i1 == 1 and i2 == 2:
                return c.GRASS_ROAD_LB
            elif i1 == 0 and i2 == 3:
                return c.GRASS_ROAD_RT
            else:
                return c.GRASS_ROAD_LT
            
    def turnTileRotate(self, tile):
        l, r, t, b = self.findNearTiles(tile)
        if self.isPath(l) and self.isPath(t):
            return 90
        elif self.isPath(l) and self.isPath(b):
            return 180
        elif self.isPath(r) and self.isPath(t):
            return 0
        elif self.isPath(r) and self.isPath(b):
            return 270
        else:
            raise Exception
        
        
    def isNextTo(self, t1, t2):
        j1, i1 = self.findTile(t1)
        j2, i2 = self.findTile(t2)
        if j1 == j2 and abs(i1-i2)==1:
            return True
        elif i1 == i2 and abs(j1-j2)==1:
            return True
        else:
            return False    
    def findTile(self, tile):
        # return index of the tile
        x, y = tile.getPos()
        if self.wTiles[y//tile.height][x//tile.width] == tile:
            return y//tile.height, x//tile.width
        else:
            raise Exception('somethings wrong')
    def calcCreepPath(self):
        out = []
        path = []
        for tile in self.listOfTiles:
            if tile.__class__.__name__ == 'BornTile':
                start = tile
                out.append(start)
            elif tile.__class__.__name__ == 'GoalTile':
                goal = tile
            elif tile.__class__.__name__ == 'PathTile':
                path.append(tile)
            elif tile.__class__.__name__ == 'TurnTile':
                path.append(tile)
        
        while path:
            for t in path[:]:
                if self.isNextTo(out[-1], t):
                    out.append(path.pop(path.index(t)))
                    break
                
        out.append(goal)
        for i, t in enumerate(out[:]):
            if tile.__class__.__name__ == 'PathTile':
                out.pop(i)
        return out    
    
    def pointIsIn(self, point):
        # return the corresponding tile
        x, y = point
        tw = th = self.width // self.wWidth
        col = x // tw
        row = y //th
        return self.wTiles[row][col]
        
            
    def creepIsIn(self, creep):
        return self.pointIsIn(creep.getCenter())
    def calcTileCenter(self, pos = (0,0)):
        return self.pointIsIn(pos).getCenter()
    def calcTilePos(self, pos = (0,0)):
        return self.pointIsIn(pos).getPos()
    
# presentation function    
    def __str__(self):
        out = ''
        for rows in self.wTiles:
            for t in rows:
                if t.__class__.__name__ == 'PathTile':
                    out += '1'
                elif t.__class__.__name__ == 'TurnTile':
                    out += '2'
                elif t.__class__.__name__ == 'BornTile':
                    out += '3'
                elif t.__class__.__name__ == 'GoalTile':
                    out += '4'
                else:
                    out += '0'
            out += '\n'
        return out
    __repr__ = __str__        
    def draw(self, win):
        re = self.listOfTiles[:]
        re.reverse()
        for tile in re:
#            tile.drawBox(win, 1)
            tile.draw(win)
    def drawBox(self, win):
        re = self.listOfTiles[:]
        re.reverse()
        for tile in re:
            tile.drawBox(win, 1)
            




            
            



        
        
        

