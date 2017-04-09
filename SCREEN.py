import pygame, random
class SCREEN:
    def __init__(self,display_size):
        self.display_size = display_size
    def fetch(self,memory):
        #given a single array of bits from our memory, 
        #breaks up the memory into rows and and 
        col_width = self.display_size[0]
        row_count = self.display_size[1]
        image = pygame.Surface((col_width,
                                row_count))
        pygame.draw.rect(image,(255,255,255),(0,0,col_width,row_count))
        
        for index,pixel in enumerate(memory):
            if(pixel==1):
                row = index//col_width
                col = (index-row)%col_width
                rect = (col,
                        row,
                        1,1)
                pygame.draw.rect(image,(0,0,0),rect)
        return image
