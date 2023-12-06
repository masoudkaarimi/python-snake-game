import pygame.mixer

from settings import *
from snake import Snake
from apple import Apple


# Docs
# pygame.Rect(left,top,width,height)
# pygame.draw.rect(surf,color,rect)


class Main:
    def __init__(self):
        # General
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake')

        # Game objects
        self.bg_rects = [
            pygame.Rect((col + int(row % 2 == 0)) * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            for col in range(0, COLS, 2) for row in range(ROWS)
        ]
        self.snake = Snake()
        self.apple = Apple(self.snake)

        # Timer
        self.update_event = pygame.event.custom_type()
        pygame.time.set_timer(self.update_event, 200)
        self.game_active = False
        self.snake_died = False

        # Audio
        self.crunch_sound = pygame.mixer.Sound(join('..', 'audio', 'crunch.wav'))
        self.bg_music = pygame.mixer.Sound(join('..', 'audio', 'arcade.ogg'))
        self.bg_music.set_volume(0.5)
        self.bg_music.play(-1)

        # Statusbar
        self.eaten_apples = 0
        self.score = 0
        self.start_time = pygame.time.get_ticks()

    def draw_bg(self):
        self.display_surface.fill(LIGHT_GREEN)
        for rect in self.bg_rects:
            pygame.draw.rect(self.display_surface, DARK_GREEN, rect)

    def draw_status_bar(self):
        label_font = pygame.font.Font(None, 30)
        value_font = pygame.font.Font(None, 24)

        status_bar_surface = pygame.Surface((WINDOW_WIDTH, STATUS_BAR_HEIGHT), pygame.SRCALPHA)
        status_bar_surface.fill((0, 0, 0, 128))

        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)

        timer_text = f'{hours:02}:{minutes:02}:{seconds:02}'
        apples_text = f'{self.eaten_apples}'
        score_text = f'{self.score}'

        status_bar_surface.blit(label_font.render('Time: ', True, (255, 255, 255)), (10, 15))
        status_bar_surface.blit(value_font.render(timer_text, True, (255, 255, 255)), (70, 18))
        status_bar_surface.blit(label_font.render('Apples: ', True, (255, 255, 255)), (160, 15))
        status_bar_surface.blit(value_font.render(apples_text, True, (255, 255, 255)), (250, 18))
        status_bar_surface.blit(label_font.render('Score: ', True, (255, 255, 255)), (290, 15))
        status_bar_surface.blit(value_font.render(score_text, True, (255, 255, 255)), (360, 18))

        # Blit the status bar surface to the main display surface at the top
        self.display_surface.blit(status_bar_surface, (0, 0))

    def draw_3d_button(self, text, center_pos, bg_color, text_color=(255, 255, 255), font_size=40, depth=5):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=center_pos)

        button_rect = text_rect.inflate(30, 15)
        shadow_rect = button_rect.copy().move(depth, depth)

        # Draw button shadow
        pygame.draw.rect(self.display_surface, (0, 0, 0, 100), shadow_rect)

        # Draw button top layer
        pygame.draw.rect(self.display_surface, bg_color, button_rect)

        self.display_surface.blit(text_surface, text_rect)

        return button_rect

    def draw_shadow(self):
        shadow_surf = pygame.Surface(self.display_surface.get_size())
        shadow_surf.fill((0, 255, 0))
        shadow_surf.set_colorkey((0, 255, 0))

        # surf
        shadow_surf.blit(self.apple.scaled_surf, self.apple.scaled_rect.topleft + SHADOW_SIZE)
        for surf, rect in self.snake.draw_data:
            shadow_surf.blit(surf, rect.topleft + SHADOW_SIZE)

        mask = pygame.mask.from_surface(shadow_surf)
        mask.invert()
        shadow_surf = mask.to_surface()
        shadow_surf.set_colorkey((255, 255, 255))
        shadow_surf.set_alpha(SHADOW_OPACITY)

        self.display_surface.blit(shadow_surf, (0, 0))

    def reset_game(self):
        self.snake.reset()
        self.apple.set_pos()
        self.eaten_apples = 0
        self.score = 0
        self.game_active = True
        self.start_time = pygame.time.get_ticks()

    def show_game_over_screen(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 208))
        self.display_surface.blit(overlay, (0, 0))

        # Central message position
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2

        # Game Over text
        font = pygame.font.Font(None, 100)
        text_surface = font.render('Game Over', True, (255, 0, 0))  # Red color
        text_rect = text_surface.get_rect(center=(center_x, center_y - 100))
        self.display_surface.blit(text_surface, text_rect)

        # Score, apples, and time
        small_font = pygame.font.Font(None, 40)
        score_text = f'Score: {self.score}'
        apples_text = f'Apples: {self.eaten_apples}'
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        time_text = f'Time: {int(elapsed_time // 60):02}:{int(elapsed_time % 60):02}'

        # Calculate positions for score, apples, and time to center them
        score_surface = small_font.render(score_text, True, (255, 255, 255))
        apples_surface = small_font.render(apples_text, True, (255, 255, 255))
        time_surface = small_font.render(time_text, True, (255, 255, 255))

        self.display_surface.blit(score_surface, score_surface.get_rect(center=(center_x, center_y)))
        self.display_surface.blit(apples_surface, apples_surface.get_rect(center=(center_x, center_y + 40)))
        self.display_surface.blit(time_surface, time_surface.get_rect(center=(center_x, center_y + 80)))

        # Buttons
        self.play_again_rect = self.draw_3d_button('Play Again', (center_x, center_y + 160), (0, 128, 0))  # Dark green
        self.exit_rect = self.draw_3d_button('Exit', (center_x, center_y + 230), (128, 0, 0))  # Dark red

        pygame.display.update()

        # Wait for user interaction
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.play_again_rect.collidepoint(mouse_pos):
                        self.reset_game()
                        waiting_for_input = False
                    elif self.exit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.snake.direction = pygame.Vector2(1, 0) if self.snake.direction.x != -1 else self.snake.direction
        if keys[pygame.K_LEFT]:
            self.snake.direction = pygame.Vector2(-1, 0) if self.snake.direction.x != 1 else self.snake.direction
        if keys[pygame.K_UP]:
            self.snake.direction = pygame.Vector2(0, -1) if self.snake.direction.y != 1 else self.snake.direction
        if keys[pygame.K_DOWN]:
            self.snake.direction = pygame.Vector2(0, 1) if self.snake.direction.y != -1 else self.snake.direction

    def collision(self):
        # Apple
        if self.snake.body[0] == self.apple.pos:
            # print('Matched')
            self.snake.has_eaten = True
            self.apple.set_pos()
            self.crunch_sound.play()
            self.eaten_apples += 1
            self.score = self.calculate_score()

        # Game over
        if self.snake.body[0] in self.snake.body[1:] or \
                not 0 <= self.snake.body[0].x < COLS or \
                not 0 <= self.snake.body[0].y < ROWS:
            # print('Death')
            self.snake.reset()
            self.game_active = False
            self.snake_died = True

    def calculate_score(self):
        return self.eaten_apples * 5

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == self.update_event and self.game_active:
                    self.snake.update()

                if event.type == pygame.KEYDOWN and not self.game_active and not self.snake_died:
                    self.game_active = True

            # Updates
            self.input()
            self.collision()

            # Game over condition
            if not self.game_active and self.snake_died:
                self.show_game_over_screen()
                self.snake_died = False  # Reset the flag

            # Drawing
            self.draw_bg()
            self.draw_shadow()
            self.snake.draw()
            self.apple.draw()
            self.draw_status_bar()
            # if self.apple.check_last_pos():
            #     pass

            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()
