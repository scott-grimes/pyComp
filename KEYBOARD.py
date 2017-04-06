import pygame
import sys
pygame.init()

pygame.display.set_mode((100, 100))
"""
newline     128
backspace   129
left arrow  130
up arrow    131
right arrow 132
down arrow  133
home        134
end         135
page up     136
page down   137
insert      138
delete      139
esc         140
f1-f12      141-152
"""
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print('Forward')
            elif event.key == pygame.K_s:
                print('Backward')