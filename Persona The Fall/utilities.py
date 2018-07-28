import pygame
from pygame.locals import *

def goodload(thing):
    '''Because the default load function is long and I'm lazy'''
    return pygame.image.load("images/" + thing).convert()