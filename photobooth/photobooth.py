
import pygame
import sys

pygame.init()
width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
size = width, height

class PhotoBooth(object):
    def __init__(self):
        speed = [2,2]
        black = 0,0,0
        screen = pygame.display.set_mode(size)
        font = pygame.font.SysFont("monospace",24)
        text = font.render("something",True,(255,255,255))
       

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            textrect = text.get_rect()
            textrect.centerx = screen.get_rect().centerx
            textrect.centery = screen.get_rect().centery
 
            screen.blit(text,textrect)
            pygame.display.flip()

