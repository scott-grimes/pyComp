import pygame,random
import sys
from SCREEN import *

pygame.init()
PIXEL_SIZE = 1
DISPLAY_SIZE = (512,256)
screen = SCREEN(DISPLAY_SIZE,PIXEL_SIZE)
DISPLAY_SURF = pygame.display.set_mode((DISPLAY_SIZE[0]*PIXEL_SIZE,DISPLAY_SIZE[1]*PIXEL_SIZE))
keys_pressed = {}


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = event.unicode
        if event.type == pygame.KEYUP:
            del keys_pressed[event.key]
    if(len(keys_pressed)>0):
        print([ord(i.encode('ascii')) for i in keys_pressed.values()])
    
    memory = [random.choice([0,1])for w in range(DISPLAY_SIZE[0]*DISPLAY_SIZE[1])]
    image = screen.fetch(memory)
    DISPLAY_SURF.blit(image,(0,0))
    pygame.display.update()
    