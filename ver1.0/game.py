#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 17:03:19 2019

@author: Falcon
game control panel
"""
import gameobject as go
import time
import world as w
#    w.worldConstruction().draw(win)
#    pygame.draw.rect(win, (255,255,255), (40,40,50,50))
w = w.worldConstruction()
a = go.towerConstruction()
b = go.creepConstruction(w.creepPath)

towers = [a,]
creeps = [b,]
bullets = []
gameObjects = [towers, creeps, bullets]
def run(win = None):
    for t in towers:
        b = t.step(creeps)
        if b != None:
            bullets.append(b)
    
    for b in bullets[:]:
        b.step(None)
        if b.done():
            tem = bullets.pop(bullets.index(b))
            tem.state[1].hit(tem.dmg)
    
    for c in creeps[:]:
        c.step(None)
        print(w.creepIsIn(c))
        print(c.hp)
        if c.done():
            tem = creeps.pop(creeps.index(c))
        

            
    print(gameObjects)
       
    if __name__ != '__main__':  
        w.draw(win)
        for items in gameObjects:
            for i in items:
                if i is not None:
                    i.draw(win)

if __name__ == '__main__':  
    start = time.time()
    while True:
        time.sleep(0.01)
        run()