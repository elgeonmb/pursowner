import pygame
from pygame.locals import *
from collections import deque

import utilities
import vdraw
import constants
pygame.init()

drawer = vdraw.Vdraw()
clock = pygame.time.Clock()
pygame.mixer.init()


class State:
    '''Base class for states. Take the previous state as an argument (except for MainMenuState)'''
    def init(self, before = None):
        self.prevstate = before
    def on_enter(self):
        pass
    def on_exit(self):
        pass
    def perframe(self):
        pass
        
class MainMenuState(State):
    '''State used only for the main menu (the new/load/options screen)'''
    def __init__(self, before = None):
        super().__init__()
        self.cursor_on_load = False
        self.clickdelay = 0
    def on_enter(self):
        self.bg = vdraw.Vsprite ("bg.png", constants.topleft)
        self.menu = vdraw.Vsprite("menusplash.png", constants.midmid)
        self.menu.moveup(100)
        self.newgame = vdraw.Vsprite("newgame.png", constants.midmid)
        self.loadgame = vdraw.Vsprite("loadgame.png", constants.midmid)
        self.cursor = vdraw.Vsprite("tinyarrow.png", constants.midmid)
        self.cursor.moveleft(5)
        self.loadgame.movedown(100)
        drawer.draw(self.bg, 1)
        drawer.draw(self.menu, 2)
        drawer.draw(self.newgame, 3)
        drawer.draw(self.loadgame, 3)
        drawer.draw(self.cursor, 5)
    def on_exit(self):
        pass
    def perframe(self):
        clock.tick(30)
        drawer.render()
        if self.clickdelay > 0:
            self.clickdelay -= 1
            return
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                quit()
        pygame.event.pump()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w] or pressed[pygame.K_s] or pressed[pygame.K_UP] or pressed[pygame.K_DOWN]:
            self.clickdelay = 4
            print("THIS PART IS WORKIGN")
            if self.cursor_on_load:
                self.cursor_on_load = False
                self.cursor.moveup(100)
            else:
                self.cursor_on_load = True
                self.cursor.movedown(100)
        if pressed[pygame.K_SPACE] or pressed[pygame.K_RETURN]:
            if self.cursor_on_load:
                print("LOADED!")
            else:
                print("NEW GAME!")

menu = MainMenuState()
menu.on_enter()
while True:
    menu.perframe()
            
print("aw fuck")
        
