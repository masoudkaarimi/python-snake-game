from datetime import datetime, timedelta
from random import choice, random
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
        self.surf_normal = pygame.image.load(join('..', 'graphics', 'apple-normal.png')).convert_alpha()
        self.surf_special = pygame.image.load(join('..', 'graphics', 'apple-special.png')).convert_alpha()
        self.scaled_surf = self.surf_normal.copy()
        self.scaled_rect = self.scaled_surf.get_rect(center=(self.pos.x * CELL_SIZE + CELL_SIZE / 2, self.pos.y * CELL_SIZE + CELL_SIZE / 2))

        self.is_special = False
        self.spawn_time = None
        self.lifetime_normal = timedelta(seconds=LIFETIME_NORMAL)
        self.lifetime_special = timedelta(seconds=LIFETIME_SPECIAL)
        self.lifetime = self.lifetime_normal

    def set_pos(self):
        available_pos = [
            pygame.Vector2(x, y) for x in range(COLS) for y in range(ROWS)
            if pygame.Vector2(x, y) not in self.snake.body
        ]
        # print(len(available_pos))
        special_chance = 0.2
        if random() < special_chance:
            self.is_special = True
        else:
            self.is_special = False

        self.pos = choice(available_pos)
        self.spawn_time = datetime.now()

    def draw(self):
        # rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        # pygame.draw.rect(self.display_surface, 'blue', rect)
        # self.display_surface.blit(self.surf, rect)

        scale = 1 + sin(pygame.time.get_ticks() / 600) / 3
        # print(scale)
        self.scaled_surf = pygame.transform.smoothscale_by(
            self.surf_special if self.is_special else self.surf_normal,
            scale
        )
        self.scaled_rect = self.scaled_surf.get_rect(center=(self.pos.x * CELL_SIZE + CELL_SIZE / 2, self.pos.y * CELL_SIZE + CELL_SIZE / 2))
        self.lifetime = self.lifetime_special if self.is_special else self.lifetime_normal
        self.display_surface.blit(self.scaled_surf, self.scaled_rect)

    def update(self):
        if self.spawn_time is not None and datetime.now() - self.spawn_time >= self.lifetime:
            self.set_pos()
