'''
This is something that I really want to work on. Space arcade-y sort of game with spaceships and stuff
Work in progress.
'''
import pygame
from sys import exit

pygame.init()
screen=pygame.display.set_mode((1000,500))
pygame.display.set_caption('Cyberia')
clock=pygame.time.Clock()
test_font=pygame.font.SysFont('couriernew',36)
game_active = True

screen.fill('Black')
ship_surface=pygame.image.load('graphics/ship.png').convert_alpha()
ship_rect=ship_surface.get_rect(midbottom=(-100,410))

while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            exit()
pygame.display.update()
clock.tick(60)