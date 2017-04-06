import pygame
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
        
        for index,pixel in enumerate(memory):
            if(pixel==1):
                color = (0,0,0)
            else:
                color = (255,255,255)
            row = index//col_width
            col = (index-row)%col_width
            rect = (col,
                    row,
                    1,1)
            pygame.draw.rect(image,color,rect)
        return image
    