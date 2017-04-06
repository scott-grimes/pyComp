import pygame
class SCREEN:
    def __init__(self,display_size,pixel_size):
        self.display_size = display_size
        self.pixel_size = pixel_size
    def fetch(self,memory):
        #given a single array of bits from our memory, 
        #breaks up the memory into rows and and 
        col_width = self.display_size[0]
        row_count = self.display_size[1]
        image = pygame.Surface((col_width*self.pixel_size,
                                row_count*self.pixel_size))
        
        for index,pixel in enumerate(memory):
            if(pixel==1):
                color = (0,0,0)
            else:
                color = (255,255,255)
            row = index//col_width
            col = (index-row)%col_width
            rect = (col*self.pixel_size,
                    row*self.pixel_size,
                    self.pixel_size,
                    self.pixel_size)
            pygame.draw.rect(image,color,rect)
        return image
    