import pygame
from pygame.locals import *

def goodload(thing):
    '''Because the default load function is long and I'm lazy'''
    return pygame.image.load("images/" + thing).convert()
	
def makesound(thing):
	'''It's like goodload, but for sound.'''
	return pygame.mixer.Sound("sounds/" + thing)

def makemusic(thing):
	'''I love snowflake code.'''
	return pygame.mixer.Sound("music/" + thing)