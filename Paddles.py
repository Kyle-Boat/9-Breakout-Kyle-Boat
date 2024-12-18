import pygame
#from Screen import paddle_width, paddle_height

class Paddle:
   def __init__(self, x, y, width, height, screen_width):
     self.x = x
     self.y = y
     self.width = width
     self.height = height
     self.screen_width = screen_width  # Screen width for boundary checking
     self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
     self.color = pygame.Color("white")
    
   def draw(self, screen):
       pygame.draw.rect(screen, self.color, self.rect)

   def move_right(self):
       if self.rect.x + self.width <= 550:
           self.rect.x += 8

   def move_left(self):
       if self.rect.x >= 0:
           self.rect.x -= 8
