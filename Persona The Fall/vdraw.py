import pygame
from pygame.locals import *
from collections import deque
from utilites import goodload
from constants import *

class Vsprite:
    '''Contains a position (can be a constant or a 2-tuple) and an appearance (must be a string pointing to a file name)'''
    def __init__(self, appear, position):
        self.appear = goodload(appear)
        self.position = position
    def movedown(self, quantity):
        self.position = (self.position[0], self.position[1] + quantity)
    def moveup(self, quantity):
        self.movedown(-1 * quantity)
    def moveright(self, quantity):
        self.position = (self.position[0] + quantity, self.position[1])
    def moveleft(self, quantity):
        self.moveright(-1 * quantity)
    def moveboth(self, quantity):
        self.position = (self.position[0] + quantity[0], self.position[1] + quantity[1])
    def changeapp(self, newapp):
        self.appear = goodload(newapp)
    def changepos(self, newpos):
        self.position = newpos

class Vdraw: 
    '''Handles screen drawing in a way that's stomachable for my dumb ass'''
    def __init__(self):
        self.layer1 = deque()#background, should be one image the size of the screen
        self.layer2 = deque()#just in case
        self.layer3 = deque()#enemies
        self.layer4 = deque()#players
        self.layer5 = deque()#effects
        self.layer6 = deque()#cursors and whatnot
        self.layer7 = deque()#just in case
        self.layer8 = deque()#also just in case
        self.layerlist = [self.layer1, self.layer2, self.layer3, self.layer4, self.layer5, self.layer6, self.layer7, self.layer8]
    def draw(self, sprite, layer):
        '''Adds a given sprite to a layer'''
        #todo: error handling
        if layer < 1:
            layer = 1
        if layer > 8:
            layer = 8
        self.layerlist[layer-1].append(sprite)
    def undraw(self, sprite, layer=None)
        '''Removes a given sprite from Vdraw. Will only operate once.'''
        if layer = None:
            for x in layerlist:
                if sprite in x:
                    x.remove(sprite)
        else:
            if sprite in layerlist[layer]:
                layerlist[layer].remove(sprite)
    def render(self):
        '''Draws the screen. Should be called 30 times a second, hopefully.'''
        for x in self.layerlist:
            for y in x:
                screen.blit(y.appear, y.position)