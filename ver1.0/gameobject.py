#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 22:19:29 2019

@author: Falcon
# try to do multu parent class
"""
import config as c
import item
import pygame
import messagebox
import button

class GameObject(item.RectGameObject):
    def getPos(self):
        return self.state[0]
    def getCenter(self):
        x, y = self.state[0]
        return int(x+self.width//2), int(y+self.height//2)
    def getDimBox(self):
        x, y = self.state[0]
        return x, y, self.width, self.height
    def getVertices(self):
        x, y = self.state[0]
        return (x ,y), (x+self.width, y), (x, y+self.height),(x+self.width, y+self.height)
    def getArea(self):
        return int(self.width * self.height)
    def calcAlignPos(self, center, image):
        cx, cy = center
        w = image.get_width()
        h = image.get_height()
        return cx - w//2, cy - h//2
        
        
    def isInside(self, v, vertices):
        x, y = v
        if x > vertices[0][0] and x < vertices[3][0]:
            if y > vertices[0][1] and y < vertices[3][1]:
                return True
        return False  
    def isCollide(self, other):
        # rect to rect
        a1, a2, a3, a4 = self.getVertices()
        b1, b2, b3 ,b4 = other.getVertices()
        for v in self.getVertices():
            if self.isInside(v, other.getVertices()):
                return True
        for v in other.getVertices():
            if self.isInside(v, self.getVertices()):
                return True
        return False
#    def gameLogic(self):
#        pass
    def calcCD(self, freq, frame = c.FRAME): # in terms of frames/movement
        '''
        1s = 1000ms = 30f
        input: num/s
        return: f/num
        '''
        return round(frame/freq, 2)
    def calcDistance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return ((x1-x2)**2 + (y1-y2)**2)**0.5
    def calcPos(self, dimBox):
        cx, cy, w, h = dimBox
        return cx - w//2, cy - h//2
    def calcCenter(self, dimBox):
        x, y, w, h = dimBox
        return x + w//2, y + h//2
    def calcNextPos(self, c1, c2, vel):
        x1, y1 = c1
        x2, y2 = c2
        disTravel = vel
        disTotal = self.calcDistance((x1, y1),(x2, y2))
        disLeft = disTotal - disTravel
        xNew, yNew = int((x1*disLeft + x2*disTravel)/disTotal), int((y1*disLeft + y2*disTravel)/disTotal)
        return xNew, yNew

    def saveLoadImage(self, path):
        # try load image, return an pygame surface
        try:
            return pygame.image.load(path)
        except:
            font = pygame.font.SysFont('calibri', 30)
            return font.render(path, 1, (0,0,0))
        
    def draw(self, win):
        if self.hover:
            self.drawBox(win)
        else:
            win.blit(self.image, self.calcAlignPos(self.getCenter(), self.image))
    def drawBox(self, win):
        if self.hover:
            font = pygame.font.SysFont('calibri', 30)
            text = font.render('hover', 1, (0,255,0))
            win.blit(text, (self.getCenter()[0]-text.get_width()//2, self.getCenter()[1]-text.get_height()//2))
            pygame.draw.rect(win, (0, 0,255),self.getDimBox(),1)
        else:
            pygame.draw.rect(win, (0, 0,255), self.getDimBox(),1)  
    def __str__(self):
        return self.__class__.__name__ + '(' + str(self.state[0][0]) + ',' +\
                str(self.state[0][1]) + ')'       
    __repr__ = __str__

  


      
#lets try multi parent class   
class Tower(GameObject):
    def __init__(self, x=0, y=0, width=c.DEFAULT_TOWER_WIDTH, \
                 height=c.DEFAULT_TOWER_HEIGHT, info=c.DEFAULT_TOWER_INFO):
        # fixed info
        self.lv1, self.lv2, self.lv3 = info
        self.level = 1
        self.width, self.height = width, height
        self.levelize()        
        
        # game info
        self.startState = (x,y), 0, True # dim, CDcount, activate       
        self.start()
        self.activate = True
        #button info
        self.hover = False
        self.acti = False
        self.buttonCD = 10

# button function
    def onClick(self, info = None):
        self.acti = True
        action = 'TowerMenu'
        return action  
    def unClick(self, info = None):
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


# level up function        
    def levelize(self):
        if self.level == 1:
            self.cost, self.bullet, self.attkFreq, self.cc, self.range, self.name = self.lv1[:-1]
            self.image = self.saveLoadImage(self.lv1[-1])
        elif self.level == 2:
            self.cost, self.bullet, self.attkFreq, self.cc, self.range, self.name = self.lv2[:-1]
            self.image = self.saveLoadImage(self.lv2[-1])
        elif self.level ==3:
            self.cost, self.bullet, self.attkFreq, self.cc, self.range, self.name = self.lv3[:-1]
            self.image = self.saveLoadImage(self.lv3[-1])
        else:
            raise Exception        
        self.CD = self.calcCD(self.attkFreq) #f/movement    
    def levelUp(self):
        if self.level < 3:
            self.level += 1
            return self.level
        else:
            raise Exception
    def getUpgradeCost(self):
        if self.level ==1:
            return 20
        elif self.level ==2:
            return 60
        else:
            return 9999999

# game function        
    def attk(self, target):
        return Projectile(self.getCenter(), target, self.bullet)
    def sell(self):
        self.activate = False
        return 0.5*self.cost
    def done(self):
        return not(self.activate)
    def findTarget(self, targets):
        inRange = {}    
        for t in targets:
            d = self.calcDistance(self.getCenter(), t.getCenter())
            if  d <= self.range:    
                inRange[t] = d 
                
        if len(inRange) == 0:
            return None
        else:
            return min(inRange.keys(), key = (lambda k: inRange[k]))
    def getNextValues(self, state, inp):
        # output bullets
        (x, y,), cd, acti = state
        target = self.findTarget(inp)
        if target == None:
            return ((x,y),cd-1, acti), None
        elif cd <= 0:
            cdNew = self.CD - 1
            return ((x,y),cdNew, acti), self.attk(target)
        else:
            return ((x,y),cd-1, acti), None
        

# draw function        
    def getInfo(self):
        info = ['Name: {0}'.format(self.name), 
                'Cost: {0}'.format(self.cost), 
                'ATKfreq: {0}'.format(self.attkFreq), 
                'Range: {0}'.format(self.range), 
                'Damage: {0}'.format(self.bullet[0]), 
                'Effect: {0}'.format(self.cc)]
        return messagebox.MessageBox(info, self.getCenter())
    def draw(self, win):
        if self.hover:
            self.drawBox(win)
        else:
            win.blit(self.image, self.calcAlignPos(self.getCenter(), self.image))
    def drawBox(self, win):
        if self.hover:
            self.drawInfo(win)
            font = pygame.font.SysFont('calibri', 30)
            text = font.render('hover', 1, (0,255,0))
            win.blit(text, (self.getCenter()[0]-text.get_width()//2, self.getCenter()[1]-text.get_height()//2))
            pygame.draw.rect(win, (0, 0,255),self.getDimBox(),1)
        else:
            pygame.draw.rect(win, (0, 0,255), self.getDimBox(),1)  
    def drawInfo(self, win):
        if self.hover:
            self.getInfo().draw(win)

    
class Creep(GameObject):
    def __init__(self, creepPath, level = 1, width=c.DEFAULT_CREEP_WIDTH, \
                 height=c.DEFAULT_CREEP_HEIGHT, info=c.DEFAULT_CREEP_INFO):
        #fixed info
        self.path = creepPath
        self.width, self.height = width, height
        self.prize, self.armor, self.vel, self.cc, self.health, self.name = info[:-1]
        self.image = self.saveLoadImage(info[-1])
        self.level = level
        self.levelize()
        self.hp = self.health
        cx, cy = self.path[0].getCenter()
        x, y = self.calcPos((cx,cy,width,height))
        
        #gameinfo
        self.startState = [(x, y), self.path[1:], True] # dim,  path, acti
        self.start()
        self.hover = False
    def levelize(self):
        self.prize *= self.level
        self.armor *= self.level
        self.health *= self.level
    def hit(self, dmg):
        self.hp -= int(dmg * (10/(10+self.armor)))
        if self.hp <=0:
            self.state[-1] = False
        else:
            self.state[-1] = True
    def done(self):
        return not(self.state[-1])
    def getNextValues(self, state, inp):
        (x, y), p, acti = state
        t = p[0]
        if acti:
            if self.isInside(t.getCenter(), self.getVertices()):
                if t.__class__.__name__ == 'GoalTile':
                    return [(x, y), p, False], 'damn'
                else:
                    return [(x, y), p[1:], True], None
            else:
                cx, cy = self.getCenter()
                tx, ty = t.getCenter()
                cxNew, cyNew= self.calcNextPos((cx, cy), (tx, ty), self.vel)
                posNew = self.calcPos((cxNew, cyNew, self.width, self.height))
                return [posNew, p, acti], None
                
        else:
            return [(x, y), p, False], None
    def draw(self, win):
        win.blit(self.image, self.calcAlignPos(self.getCenter(), self.image))
        self.drawHP(win)
    def drawBox(self, win):
        if self.hover:
            font = pygame.font.SysFont('calibri', 30)
            text = font.render('hover', 1, (0,255,0))
            win.blit(text, (self.getCenter()[0]-text.get_width()//2, self.getCenter()[1]-text.get_height()//2))
            pygame.draw.rect(win, (0, 0,255),self.getDimBox(),1)
        else:
            pygame.draw.rect(win, (0, 0,255), self.getDimBox(),1)
        self.drawHP(win)
    def drawHP(self, win):
        x,y,w,h = self.getDimBox()
        k = int(1/5*h)
        bx, by = x, y-k
        bw, bh = w, k
        gbw = int(self.hp/self.health * bw)
        pygame.draw.rect(win,(255,0,0),(bx,by,bw,bh))
        pygame.draw.rect(win,(0,255,0),(bx,by,gbw,bh))
        
    def __str__(self):
        return self.name + '(' + str(self.state[0][0]) + ',' +\
                str(self.state[0][1]) + ')'       
    __repr__ = __str__
        
    

class Projectile(GameObject):
    def __init__(self, fr, to, info):
        #fixed info
        self.dmg, self.vel, self.cc, self.width, self.height = info[:-1]
        self.image = pygame.image.load(info[-1])
        
        #game info
        self.startState = fr, to, True# (fx, fy), target, acti
        self.start()
        self.hover = False
    def draw(self, win):
        win.blit(self.image, self.calcAlignPos(self.getCenter(), self.image))
    def drawBox(self, win):
        pygame.draw.rect(win, (255,255,255),(self.getDimBox()))
    def done(self):
        return self.isCollide(self.state[1])
    def getNextValues(self, state, inp):
        (fx, fy),(tx, ty), acti = state[0], state[1].getCenter(), state[2]
        cx, cy = self.calcCenter((fx,fy,self.width,self.height))
        if not acti:
            raise Exception
        cxNew, cyNew= self.calcNextPos((cx, cy), (tx, ty), self.vel)
        posNew = self.calcPos((cxNew, cyNew, self.width, self.height))
        return (posNew, state[1], acti), None
   


    
        
    
    
        
            
        
        