#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 12:24:40 2019

@author: Falcon
Control Panel
Control the game flow
"""
#import gameobject 
import pygame
import config 
#import world
import time
import button
import sys
import constructor as const
pygame.init()

#def waitNextInstruction(instruction):

class ControlPanel(object):
    """
    special class with methods to deal with different game situation
    """
    def __init__(self, mp = config.TEST_MAP, level = config.TEST_WAVE):
        self.constructor = const.Constructor(mp = mp , level = level)
        self.world = WorldHandler(self.constructor)
        self.game = GameObjectHandler(self.constructor)
        self.menu = MenuHandler()  

    def run(self, info = None):
        if info != None:
            win, mousePos, onClick, pause = info
            menuInfo = self.menu.run(mousePos, onClick) 
            gameTemInfo, towers = self.game.run(menuInfo, mousePos, onClick, pause)
            money, hit = gameTemInfo
            self.menu.money += money
            self.menu.setTowers(towers)
            if hit: self.menu.hit()
        else:
            menuInfo = self.menu.run() 
            money, hit, ing = self.game.run()
            self.menu.money += money
            if hit: self.menu.hit()
        
        if __name__ != '__main__':
            self.draw(win)
        return self.__str__(), 
    
    
    def __str__(self):
        return self.world.__str__() + '\n' + self.game.__str__() + '\n' + self.menu.__str__()
    __repr__ = __str__
    def draw(self, win):
        self.world.draw(win)
        self.game.draw(win)
        self.menu.drawBox(win)
    def drawBox(self, win):
        self.world.drawBox(win)
        self.game.drawBox(win)
        self.menu.drawBox(win)




        
        
        
class WorldHandler:
    def __init__(self, constructor, m=config.TEST_MAP):
        self.constructor = constructor
        self.world = self.constructor.worldConstruction()
#        self.creepPath = self.world.creepPath
        self.constructor.creepPath = self.world.creepPath
    def pointIsInWorld(self, pos):
        return self.world.isInside(pos, self.world.getVertices())
    def draw(self, win):
        self.world.draw(win)
    def drawBox(self, win):
        self.world.drawBox(win)
    def __str__(self):
        return ''
    __repr__ = __str__
        
class GameObjectHandler:
    def __init__(self, constructor):
        self.towers = []
        self.creeps = [] 
        self.bullets = []
        self.constructor = constructor
        self.items = [self.towers, self.creeps, self.bullets]
        self.wave = []
        self.waveCount = 0
        self.gamePause = False
        self.state = 'game'
        self.stateCD = 0

    def createTower(self, pos = (0,0), towerDim = config.DEFAULT_TOWER_DIM, order = 'defaultTower'):
        x,y = pos
        w,h = towerDim
        return self.constructor.towerConstruction(cDimBox = (x,y,w,h), order = order)
    def createCreep(self, wave = None):
        self.creeps.append(self.constructor.creepConstruction(wave))
        return self.creeps
    
    def run(self, orders = None, mousePos = None, onClick = None, pause = False):
        if pause:
            self.gamePause = not(self.gamePause)
        
        self.stateCD -= 1
        temInfo = [0, False] #coins, isHit
        if orders != None and mousePos != None and onClick != None:
# =============================================================================
#            Goes to menu
#             # check hover
#             for t in self.towers:
#                 if t.isInside(mousePos, t.getVertices()):
#                     t.hover = True
#                 else:
#                     t.hover = False
# =============================================================================
                    
            # check order  
            if self.state == 'game':
                temInfo = self.orderRun(orders, mousePos, onClick)
            elif self.state == 'ccTowerPurchase' or self.state == 'dmgTowerPurchase':
                temInfo = self.purchaseRun(orders, mousePos, onClick)
            

        if self.gamePause == False:
            temInfo1 = self.gameRun()
            return [temInfo[0] + temInfo1[0], temInfo[1] or temInfo1[1]], self.towers
        return (temInfo, self.towers)
    
    def purchaseRun(self, orders, mousePos, onClick):
        temInfo = [0, False]
        if onClick:
            if self.state == 'ccTowerPurchase':
                t = self.createTower(pos = mousePos,order = self.state)
                if t != None: self.towers.append(t)
            elif self.state == 'dmgTowerPurchase':
                t = self.createTower(pos = mousePos,order = self.state)
                if t != None: self.towers.append(t)
            self.state = 'game'
        return temInfo
    
    def sellRun(orders, mousePos, onClick):
        pass
    def orderRun(self, orders, mousePos, onClick):
        temInfo = [0, False]
        for order in set(orders):
            if order == 'ccTowerPurchase':
                if self.checkStateCD(): 
                    self.state = order
                    time.sleep(0.1)
            elif order == 'dmgTowerPurchase':
                if self.checkStateCD(): 
                    self.state = order
                    time.sleep(0.1)
            elif order == 'towerSell':
                pygame.event.set_blocked(None)
                pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                pygame.event.wait()
                time.sleep(0.1)
                x, y = pygame.mouse.get_pos()
                for t in self.towers[:]:
                    if t.isInside((x,y), t.getVertices()):
                        self.towers.remove(t)
                        temInfo[0] += self.constructor.towerDestruction(t)
            elif order == 'nextWave':
                if len(self.wave) == 0:
                    self.wave += self.constructor.nextWave()
            elif order == 'Exit':
                sys.exit()      
            elif order == None:
                pass
            elif order[0] == 'sellThisTower':
                self.towers.remove(order[1])
                pass
        return temInfo
    
    def gameRun(self):
        temInfo = [0, False] #coins, isHit
        # wave count        
        if self.waveCount <= 0 and len(self.wave) > 0:
            self.creeps.append(self.wave.pop(0))
            self.waveCount = 5
        elif self.waveCount > 0:
            self.waveCount -= 1
        else:
            self.waveCount = 0
        # game run
        for t in self.towers:
            b = t.step(self.creeps)
            if b != None:
                self.bullets.append(b)
                
        for c in self.creeps[:]:
            hit = c.step(None)
            if hit == 'damn':
                temInfo[1] = True
#            print(self.world.creepIsIn(c))
#            print(c.hp)
            if c.done():
                temInfo[0] += c.prize
                tem = self.creeps.pop(self.creeps.index(c))
            
        for b in self.bullets[:]:
            b.step(None)
            if b.done():
                tem = self.bullets.pop(self.bullets.index(b))
                tem.state[1].hit(tem.dmg)
        return temInfo
    
    def checkStateCD(self):
        if self.stateCD <= 0:
            self.stateCD = 10
            return True
        else:
            return False
    def pause(self):
        self.gamePause = True
    def unPause(self):
        self.gamePause = False           
    def draw(self, win):
        for i in self.items:
            for item in i:
                item.draw(win)
    def drawBox(self, win):
        for i in self.items:
            for item in i:
                item.drawBox(win)
                
    def __str__(self):
        out = ''
        for item in self.items:
            for i in item:
                out += i.__str__ + ', '
        return '[{0}]'.format(out)
    __repr__ = __str__
    
    
class MenuHandler:
    def __init__(self):
        self.gameMenu = button.GameMenu(info = config.GAME_MENU)
#        self.purchaseMenu = button.PurchaseMenu(info = config.PURCHASE_MENU)
        self.buttons = self.gameMenu.buttons
        self.state = 'game'
        self.stateCD = 0
        self.inPurchase = []
        self.towers = []
        self.inTowers = []
        self.live = 5
        self.money = 100
    def hit(self):
        self.live -= 1
    def lose(self):
        return self.live <= 0
    def __str__(self):
        return ''
    __repr__ = __str__
    def setTowers(self, towers):
        self.towers = towers
                  
        
    def run(self, mousePos = None, onClick = None):
        if self.lose():
            pass
        # check for data game
        if mousePos == onClick == None:
            return None
        
        # visual game
        self.stateCD -= 1
        menuOrders = []
        
        if self.state == 'game':
            menuOrders += self.gameMenuRun(mousePos, onClick)
        elif self.state == 'purchase':
            menuOrders += self.purchaseMenuRun(mousePos, onClick)   
        elif self.state == 'tower':
            menuOrders += self.towerMenuRun(mousePos, onClick)
        return menuOrders
    
    def gameMenuRun(self, mousePos = None, onClick = None):
        orders = []
        for b in self.buttons + self.towers:
            b.decbCD()
            if b.isInside(mousePos, b.getVertices()):
                b.hover = True
            else:
                b.hover = False
        if onClick:
            for b in self.buttons + self.towers:
                if b.hover and b.checkCD():
                    order = self.firstProcessOrder(b.onClick(self.money), mousePos, b)
                    orders.append(order)  
                    b.unClick()
#        return self.removeNone(orders)
        return orders
    
    def purchaseMenuRun(self, mousePos = None, onClick = None):
        orders = []
        for b in self.inPurchase:
            b.decbCD()
            if b.isInside(mousePos, b.getVertices()):
                b.hover = True
            else:
                b.hover = False
        if onClick:
            if not self.purMenu.isInside(mousePos, self.purMenu.getVertices()):
                if self.checkStateCD(): 
                    self.duringPurchase(conf = False)
            for b in self.inPurchase:
                if b.hover and b.checkCD():
                    order = self.firstProcessOrder(b.onClick(self.money), mousePos, b)
                    orders.append(order) 
                    self.duringPurchase(conf = False)
#                    b.unClick()
#        return self.removeNone(orders)
        return orders
    
    def settingMenuRun(self, mousePos = None, onclick = None):
        pass
    
    def towerMenuRun(self, mousePos = None, onClick = None):
        orders = []
        for b in self.inTowers:
            b.decbCD()
            if b.isInside(mousePos, b.getVertices()):
                b.hover = True
            else:
                b.hover = False
        if onClick:
            if not self.towMenu.isInside(mousePos, self.towMenu.getVertices()):
                if self.checkStateCD(): 
                    self.duringTower(conf = False)
            for b in self.inTowers:
                if b.hover and b.checkCD():
                    order = self.firstProcessOrder(b.onClick(self.money), mousePos, b)
                    orders.append(order)
                    self.duringTower(conf = False)
#                    b.unClick()
#        return self.removeNone(orders)
        return orders
    
# helper functions
#    def removeNone(self, l):
#        return [x for x in l if l != None]
    def firstProcessOrder(self, order, mousePos, b = None):
        if order == 'towerPurchase':
            if self.checkStateCD():
                self.duringPurchase(pos = mousePos)
                return None
        elif order == 'ccTowerPurchase' :
            if self.money >= 8:
                self.money -= 8
                return order            
        elif order == 'dmgTowerPurchase':
            if self.money >= 10:
                self.money -= 10
                return order
        elif order == 'TowerMenu':
            if self.checkStateCD():
                self.duringTower(pos = mousePos, tower = b)
                return None
        elif order in ['towerSell', 'nextWave', 'Exit', None]:
            return order
        elif order[0] == 'upgradeThisTower':
            order[1].levelUp()
            order[1].levelize()
            self.money -= order[2]
            return None
        elif order[0] == 'sellThisTower':
            self.money += order[2]
            return order          
        else:
            raise Exception(order)
        
    def checkStateCD(self):
        if self.stateCD <= 0:
            self.stateCD = 10
            return True
        else:
            return False
    def duringPurchase(self, pos = (0,0), conf = True):
        if conf:
            self.purMenu = button.PurchaseMenu(pos = pos, info = config.PURCHASE_MENU)
            self.inPurchase = self.purMenu.buttons
            self.state = 'purchase'
        else:
            del(self.purMenu)
            self.inPurchase = []
            self.state = 'game'
    def duringTower(self, pos = (0,0), conf = True,tower = None):
        if conf:
            self.towMenu = button.TowerMenu(pos = pos, info = config.TOWER_MENU, parent = tower)
            self.inTowers = self.towMenu.buttons
            self.state = 'tower'
        else:
            del(self.towMenu)
            self.inTowers = []
            self.state = 'game'
            






        
#display function        
    def draw(self, win):
        self.gameMenu.draw(win)
        self.gameMenu.drawInfo(win, self.live, self.money)
        if self.inPurchase: self.purMenu.draw(win)
        if self.inTowers: self.towMenu.draw(win)
    def drawBox(self, win):
#        self.gameMenu.draw(win)
        self.gameMenu.drawBox(win)
        self.gameMenu.drawInfo(win, self.live, self.money)
        if self.inPurchase: self.purMenu.drawBox(win)
        if self.inTowers: self.towMenu.drawBox(win)
    
    
    

a = ControlPanel()



#if __name__ == '__main__':  
#    while True:
#        time.sleep(0.1)
#        print(a.run()[0])
        
        
        
        
        
        
        
        
        
        
        
        
        
        
