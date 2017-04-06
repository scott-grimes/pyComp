import pygame
from pygame.locals import *
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
class KEYBOARD():
    def __init__(self):
        self.keys_pressed = []
        
    def fetch(self,event):
        if event.type == pygame.KEYDOWN:
                k = self.getKeyVal(event)
                if k is not None:
                    self.keys_pressed.append(k)
                    
        if event.type == pygame.KEYUP:
            k = self.getKeyVal(event)
            if k is not None:
                self.keys_pressed.remove(k)
                
        if(len(self.keys_pressed)>0):
            return self.keys_pressed[0]
        
        return 0
        
    def getKeyVal(self,event):
        shifted=False
        if event.key == K_BACKSPACE: 
            return 129
        elif event.key == K_LSHIFT or event.key == K_RSHIFT: 
            shifted = True
        elif event.key == K_SPACE: 
            return 32
        if not shifted:
            if event.key == K_a : return ord('a')
            elif event.key == K_b : return ord('b')
            elif event.key == K_c : return ord('c')
            elif event.key == K_d : return ord('d')
            elif event.key == K_e : return ord('e')
            elif event.key == K_f : return ord('f')
            elif event.key == K_g : return ord('g')
            elif event.key == K_h : return ord('h')
            elif event.key == K_i : return ord('i')
            elif event.key == K_j : return ord('j')
            elif event.key == K_k : return ord('k')
            elif event.key == K_l : return ord('l')
            elif event.key == K_m : return ord('m')
            elif event.key == K_n : return ord('n')
            elif event.key == K_o : return ord('o')
            elif event.key == K_p : return ord('p')
            elif event.key == K_q : return ord('q')
            elif event.key == K_r : return ord('r')
            elif event.key == K_s : return ord('s')
            elif event.key == K_t : return ord('t')
            elif event.key == K_u : return ord('u')
            elif event.key == K_v : return ord('v')
            elif event.key == K_w : return ord('w')
            elif event.key == K_x : return ord('x')
            elif event.key == K_y : return ord('y')
            elif event.key == K_z : return ord('z')
            elif event.key == K_0 : return ord('0')
            elif event.key == K_1 : return ord('1')
            elif event.key == K_2 : return ord('2')
            elif event.key == K_3 : return ord('3')
            elif event.key == K_4 : return ord('4')
            elif event.key == K_5 : return ord('5')
            elif event.key == K_6 : return ord('6')
            elif event.key == K_7 : return ord('7')
            elif event.key == K_8 : return ord('8')
            elif event.key == K_9 : return ord('9')
            elif event.key == K_BACKQUOTE : return ord('`')
            elif event.key == K_MINUS : return ord('-')
            elif event.key == K_EQUALS : return ord('=')
            elif event.key == K_LEFTBRACKET : return ord('[')
            elif event.key == K_RIGHTBRACKET : return ord(']')
            elif event.key == K_BACKSLASH and '\\' in self.restricted: return ord('\\')
            elif event.key == K_SEMICOLON : return ord(';')
            elif event.key == K_QUOTE and '\'' in self.restricted: return ord('\'')
            elif event.key == K_COMMA : return ord(',')
            elif event.key == K_PERIOD : return ord('.')
            elif event.key == K_SLASH : return ord('/')
        elif self.shifted:
            if event.key == K_a : return ord('A')
            elif event.key == K_b : return ord('B')
            elif event.key == K_c : return ord('C')
            elif event.key == K_d : return ord('D')
            elif event.key == K_e : return ord('E')
            elif event.key == K_f : return ord('F')
            elif event.key == K_g : return ord('G')
            elif event.key == K_h : return ord('H')
            elif event.key == K_i : return ord('I')
            elif event.key == K_j : return ord('J')
            elif event.key == K_k : return ord('K')
            elif event.key == K_l : return ord('L')
            elif event.key == K_m : return ord('M')
            elif event.key == K_n : return ord('N')
            elif event.key == K_o : return ord('O')
            elif event.key == K_p : return ord('P')
            elif event.key == K_q : return ord('Q')
            elif event.key == K_r : return ord('R')
            elif event.key == K_s : return ord('S')
            elif event.key == K_t : return ord('T')
            elif event.key == K_u : return ord('U')
            elif event.key == K_v : return ord('V')
            elif event.key == K_w : return ord('W')
            elif event.key == K_x : return ord('X')
            elif event.key == K_y : return ord('Y')
            elif event.key == K_z : return ord('Z')
            elif event.key == K_0 : return ord(')')
            elif event.key == K_1 : return ord('!')
            elif event.key == K_2 : return ord('@')
            elif event.key == K_3 : return ord('#')
            elif event.key == K_4 : return ord('$')
            elif event.key == K_5 : return ord('%')
            elif event.key == K_6 : return ord('^')
            elif event.key == K_7 : return ord('&')
            elif event.key == K_8 : return ord('*')
            elif event.key == K_9 : return ord('(')
            elif event.key == K_BACKQUOTE : return ord('~')
            elif event.key == K_MINUS : return ord('_')
            elif event.key == K_EQUALS : return ord('+')
            elif event.key == K_LEFTBRACKET : return ord('{')
            elif event.key == K_RIGHTBRACKET : return ord('}')
            elif event.key == K_BACKSLASH : return ord('|')
            elif event.key == K_SEMICOLON : return ord(':')
            elif event.key == K_QUOTE : return ord('"')
            elif event.key == K_COMMA : return ord('<')
            elif event.key == K_PERIOD : return ord('>')
            elif event.key == K_SLASH : return ord('?')
