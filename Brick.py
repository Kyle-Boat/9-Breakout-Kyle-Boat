import pygame

import random


class Bricks:
    def __init__(self, screen, brick_width, brick_height):
        self.screen = screen
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.random_colors = ['blue', 'yellow', 'red', 'green', 'orange']
        self.bricks = []
        self.brick_colors = []
        
        
        self.set_values()

    def set_values(self):
        y_values = [int(y) for y in range(100, 200, 25)]
        x_values = [int(x) for x in range(10, 550, 42)]
        y_index = 0
        self.loop(x_values, y_values, y_index)

    def loop(self, x_values, y_values, y_index):
        for n in x_values:
        
            if n == x_values[-1]:
                
                if y_index < len(y_values) - 1:
                    y_index += 1
                    
                    self.loop(x_values, y_values, y_index)
            
            else:
                x = n
                y = y_values[y_index]
                brick = pygame.Rect(x, y, self.brick_width, self.brick_height)
                self.bricks.append(brick)
                self.brick_colors.append(random.choice(self.random_colors))

    def show_bricks(self):
        for i in range(len(self.bricks)):
            brick = self.bricks[i]
            color = self.brick_colors[i]
            pygame.draw.rect(self.screen, color, brick)