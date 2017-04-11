import pygame,random
import sys
from SCREEN import *
from KEYBOARD import *
from Components import Memory

pygame.init()
DISPLAY_SIZE = (512,256)
DISPLAY_SURF = pygame.display.set_mode((DISPLAY_SIZE[0],DISPLAY_SIZE[1]))


screen = SCREEN(DISPLAY_SIZE)
keyboard = KEYBOARD()
memory = Memory()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        k = keyboard.fetch(event)
        print(k)
    
    memory = [random.choice([0,1])for w in range(DISPLAY_SIZE[0]*DISPLAY_SIZE[1])]
    image = screen.fetch(memory)
    DISPLAY_SURF.blit(image,(0,0))
    pygame.display.update()
    