#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 19:57:35 2019

@author: Falcon
main 
"""
import pygame
pygame.init()
import config as c
#import world as w
#import gameobject as g
#import game
import controlpanel
import time

win = pygame.display.set_mode(c.SCREEN_DIM)
pygame.display.set_caption(c.NAME)
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(c.FRAME)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    
    keys = pygame.key.get_pressed()
    pause = False
    if keys[pygame.K_SPACE]:
        pause = True
        time.sleep(0.2)
#    if keys[pygame.K_c]:
#        controlpanel.a.game.createCreep()
    
    mouses = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if mouses[0]:
        onclick = True
    else:
        onclick = False
    
    
    
    
    
    win.fill((0,0,0))
    controlpanel.a.run((win, pos, onclick, pause))# info = win, mousePos, pause
    pygame.display.update()
    
    
pygame.quit()
