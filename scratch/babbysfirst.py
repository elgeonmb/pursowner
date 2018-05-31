import pygame
from pygame.locals import *

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
for x in range(len(menu)):
	screen.blit(menu[x], (0, 60*x))
cursor = goodload("cursor.png")
cursor.set_colorkey((0,0,0))
screen.blit(cursor, (0,0))
pygame.display.update()

def cursor_up():
	if cursor.get_rect() == atk.get_rect():
		

while True:
	for event in pygame.event.get():
		if event.type == QUIT:	
			quit()
		elif event.type == KEYDOWN:
			if event.key == K_UP:
				
