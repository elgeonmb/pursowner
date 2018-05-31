import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
player = pygame.image.load("images/H.png").convert()
background = pygame.image.load("images/1.png").convert()
screen.blit(background, (0,0))
position = player.get_rect()
screen.blit(player, position)
pygame.display.update()
while True:
    for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                quit()
    screen.blit(background, position, position)
    position = position.move(2,0)
    screen.blit(player, position)
    pygame.display.update()
    pygame.time.delay(100)
