import pygame
from pygame.locals import *

def goodload(thing):
	return pygame.image.load("images/" + thing).convert()

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Purse Owner Free: FPS")
bg = goodload("bg.png")
screen.blit(bg, (0,0))
pygame.display.update()