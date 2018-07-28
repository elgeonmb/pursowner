import pygame
from pygame.locals import *
from collections import deque

pygame.init()

#constant assignments
screensize = (640, 480)
topleft = (0,0)
topmid = (screensize[0]/2, 0)
topright = (screensize[0], 0)
midleft = (0, screensize[1]/2)
midmid = (screensize[0]/2, screensize[1]/2)
midright = (screensize[0], screensize[1]/2)
botleft = (0, screensize[1])
botmid = (screensize[0]/2, screensize[1])
botright = screensize

#getting access to fun fun pygame tools
screen = pygame.display.set_mode(screensize)
clock = pygame.time.Clock()

def goodload(thing):
    '''Because the default load function is long and I'm lazy'''
    return pygame.image.load("images/" + thing).convert()

class Vsprite:
    '''Contains a position (can be a constant or a 2-tuple) and an apperance (must be a string pointing to a file name)'''
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
                

test1 = Vsprite("A.png", topleft)
test2 = Vsprite("ana.png", midmid)
test3 = Vsprite("bg.png", topleft)
draw = Vdraw()
draw.draw(test1, 2)
draw.draw(test2, 2)
draw.draw(test3, 1)
pressed = pygame.key.get_pressed()


while True:
    clock.tick(60)
    pygame.event.pump()
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            quit()
    if pressed[pygame.K_w]:
        test2.moveup(1)
    if pressed[pygame.K_s]:
        test2.movedown(1)
    if pressed[pygame.K_a]:
        test2.moveleft(1)
    if pressed[pygame.K_d]:
        test2.moveright(1)
    draw.render()
    pygame.display.update()

##
##
##print(screensize)
##
##
##
##pygame.init()
##screen = pygame.display.set_mode((640, 480))
##pygame.display.set_caption("Purse Owner Free: FPS")
##bg = goodload("bg.png")
##screen.blit(bg, (0,0))
##atk = goodload("atk.png")
##skil = goodload("skil.png")
##tac = goodload("tac.png")
##gun = goodload("gun.png")
##ana = goodload("ana.png")
##per = goodload("per.png")
##menu = [atk, skil, tac, gun, ana, per]
##
##def drawmenu():
##        for count, x in enumerate(menu):
##                screen.blit(x, (0, 60*count + 1))
##
##drawmenu()
##cursor = goodload("cursor.png")
##cursor.set_colorkey((255,255,255))
##screen.blit(cursor, (0,0))
##pygame.display.update()
##cursor_pos = (0,0)
##def cursor_up():
##        global cursor_pos
##        oldcursor = cursor_pos
##        if cursor_pos == (0,0):
##                cursor_pos = (0, 60 * len(menu))
##        else:
##                cursor_pos = [oldcursor[0], oldcursor[1] - 60]
##        drawmenu()
##        screen.blit(cursor, cursor_pos)
##        pygame.display.update()
##
##while True:
##        pygame.time.delay(100)
##        cursor_up()
##        pygame.time.delay(10)
###while True:
###   for event in pygame.event.get():
###       if event.type == QUIT:
###           quit()
###       elif event.type == KEYDOWN:
###           if event.key == K_UP:
##
