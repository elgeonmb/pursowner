 import pygame
from pygame.locals import *
from collections import deque

import random
import utilities
import vdraw
import constants
import events
pygame.init()

drawer = vdraw.Vdraw()
clock = pygame.time.Clock()
pygame.mixer.init()
music = pygame.mixer.Channel(0)
sfx = pygame.mixer.Channel(1)

class StateManager: #incidentally this is an object because I cba to fuck around with global statements
    '''Manages states.'''
    def __init__(self):
        self.state_stack = deque()
        self.demon_list = deque()
        self.party_list = deque()
        self.slinks = deque()
        self.inventory = deque()
        self.money = 0
        self.date = (4, 1)
        self.event_manager = events.EventManager()
        self.prevstate = None
    def render(self):
        clock.tick(30)
        if self.state_stack[-1] != self.prevstate:
            if self.prevstate:
                self.prevstate.on_exit()
                print("Prevstate Exited!")
                print(self.prevstate)
            self.state_stack[-1].on_enter()
            print("New state entered!")
            print(self.state_stack[-1])
            self.prevstate = self.state_stack[-1]
            print("Prevstate assigned!")
            print(self.prevstate)
        self.state_stack[-1].perframe()
        drawer.render()

class State:
    '''Base class for states. Take the previous state as an argument (except for MainMenuState)'''
    def __init__(self, stateman):        
        self.stateman = stateman
    def on_enter(self):
        pass
    def on_exit(self):
        pass
    def perframe(self):
        pass
        
class MainMenuState(State):
    '''State used only for the main menu (the new/load/options screen)'''
    def __init__(self, stateman):
        super().__init__(stateman)
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
        self.dramaturgy = utilities.makemusic("dramaturgy.ogg")
        self.woop = utilities.makesound("woop.ogg")
        music.play(self.dramaturgy)
    def on_exit(self):
            del self.bg
            del self.menu
            del self.newgame
            del self.loadgame
            del self.cursor
            print("Eyyy")
    def perframe(self):
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
            sfx.play(self.woop)
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
                print(self.stateman)
                self.stateman.state_stack.append(JunkState(self.stateman))
                print(self.stateman.state_stack)

class JunkState(State):
    def __init__(self, stateman):
        super().__init__(stateman)
        self.counter = 0
    def on_enter(self):
        print("JunkState Entered")
        drawer.whiteout()
    def perframe(self):
        print("TICK!")
        self.counter += 1
        if self.counter > 100:
            self.stateman.state_stack.remove(self)

class VnState(State):
    pass

man = StateManager()
man.state_stack.append(MainMenuState(man)) #append this and keep it at the root to prevent index errors

while True:
    man.render()

            
print("aw fuck")
        
