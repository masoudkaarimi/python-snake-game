from random import choice
from math import sin

from settings import *


# Docs
# self.display_surface.blit(surf,pos/rect)
# pygame.transform.smoothscale_by(surf,factor)

class Apple:
    def __init__(self, snake):
        self.display_surface = pygame.display.get_surface()
        self.pos = pygame.Vector2()
        self.snake = snake
        self.set_pos()
        self.surf = pygame.image.load(join('..', 'graphics', 'apple.png')).convert_alpha()
        self.scaled_surf = self.surf.copy()
        self.scaled_rect = self.scaled_surf.get_rect(center=(self.pos.x * CELL_SIZE + CELL_SIZE / 2, self.pos.y * CELL_SIZE + CELL_SIZE / 2))

    def set_pos(self):
        available_pos = [
            pygame.Vector2(x, y) for x in range(COLS) for y in range(ROWS)
            if pygame.Vector2(x, y) not in self.snake.body
        ]
        # print(len(available_pos))
        self.pos = choice(available_pos)

    def draw(self):
        # rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        # pygame.draw.rect(self.display_surface, 'blue', rect)
        # self.display_surface.blit(self.surf, rect)
        scale = 1 + sin(pygame.time.get_ticks() / 600) / 3
        # print(scale)
        self.scaled_surf = pygame.transform.smoothscale_by(self.surf, scale)
        self.scaled_rect = self.scaled_surf.get_rect(center=(self.pos.x * CELL_SIZE + CELL_SIZE / 2, self.pos.y * CELL_SIZE + CELL_SIZE / 2))
        self.display_surface.blit(self.scaled_surf, self.scaled_rect)
