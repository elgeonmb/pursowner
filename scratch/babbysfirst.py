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
#	for event in pygame.event.get():
#		if event.type == QUIT:	
#			quit()
#		elif event.type == KEYDOWN:
#			if event.key == K_UP:
				
