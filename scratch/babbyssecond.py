import pygame
from pygame.locals import *
from collections import deque

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


class Vsprite:
    '''Contains a position (can be a constant or a 2-tuple) and an apperance (must be a string pointing to a file name)'''
    def __init__(self, appear, position):
        self.appear = appear
        self.position = position
    def moveup(self, quantity):
        self.position = (self.position[0], self.position[1] + quantity)
    def moveright(self, quantity):
        self.position = (self.position[0] + quantity, self.position[1])
    def moveboth(self, quantity):
        self.position = (self.position[0] + quantity[0], self.position[1] + quantity[1])
    def change(self, newapp):
        self.appear = newapp

class Vscreen: 
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
        if layer < 1:
            except ValueError
            layer = 1
            continue
        if layer > 8:
            except ValueError
            layer = 8
            continue
        self.layerlist[layer-1].append(sprite)
    def render(self):
        '''Draws the screen. Should be called 30 times a second, hopefully.'''
        for x in self.layerlist:
            for y in x:
                



print(screensize)

def goodload(thing):
    '''Because the default load function is long and I'm lazy'''
    return pygame.image.load("images/" + thing).convert()

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Purse Owner Free: FPS")
bg = goodload("bg.png")
screen.blit(bg, (0,0))
atk = goodload("atk.png")
skil = goodload("skil.png")
tac = goodload("tac.png")
gun = goodload("gun.png")
ana = goodload("ana.png")
per = goodload("per.png")
menu = [atk, skil, tac, gun, ana, per]

def drawmenu():
        for count, x in enumerate(menu):
                screen.blit(x, (0, 60*count + 1))

drawmenu()
cursor = goodload("cursor.png")
cursor.set_colorkey((255,255,255))
screen.blit(cursor, (0,0))
pygame.display.update()
cursor_pos = (0,0)
def cursor_up():
        global cursor_pos
        oldcursor = cursor_pos
        if cursor_pos == (0,0):
                cursor_pos = (0, 60 * len(menu))
        else:
                cursor_pos = [oldcursor[0], oldcursor[1] - 60]
        drawmenu()
        screen.blit(cursor, cursor_pos)
        pygame.display.update()

while True:
        pygame.time.delay(100)
        cursor_up()
        pygame.time.delay(10)
#while True:
#   for event in pygame.event.get():
#       if event.type == QUIT:
#           quit()
#       elif event.type == KEYDOWN:
#           if event.key == K_UP:

