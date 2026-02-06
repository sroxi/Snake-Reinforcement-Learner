import pygame
import numpy as np
from enum import Enum
from collections import namedtuple
import random

pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN1 = (0, 200, 0)
GREEN2 = (0, 255, 0)
BLUE = (0, 0, 255)

# Direction enum
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# Game settings
BLOCK_SIZE = 20
SPEED = 60

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # Initialize display (visible window size in pixels)
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake RL - Click Quit to stop')
        self.clock = pygame.time.Clock()
        self.quit_requested = False
        self.quit_button_rect = pygame.Rect(self.w - 90, 10, 80, 32)  # set properly in _update_ui
        self.reset()
        
    def reset(self):
        # Initialize game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w // 2, self.h // 2)
        # Align head to grid
        self.head = Point(
            (self.head.x // BLOCK_SIZE) * BLOCK_SIZE,
            (self.head.y // BLOCK_SIZE) * BLOCK_SIZE
        )
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        
    def _place_food(self):
        # Ensure at least 1 cell per axis (avoid empty randint range if w or h < BLOCK_SIZE)
        ncols = max(1, (self.w - BLOCK_SIZE) // BLOCK_SIZE)
        nrows = max(1, (self.h - BLOCK_SIZE) // BLOCK_SIZE)
        x = random.randint(0, ncols) * BLOCK_SIZE
        y = random.randint(0, nrows) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
    
    def play_step(self, action, game_num=0, record=0, mean_score=0.0):
        self.frame_iteration += 1
        # 1. Collect user input (quit button and window close)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.quit_button_rect.collidepoint(event.pos):
                    self.quit_requested = True
        
        if self.quit_requested:
            return -10, True, self.score, True  # reward, game_over, score, user_quit
        
        # 2. Move
        self._move(action)  # Update the head
        self.snake.insert(0, self.head)
        
        # 3. Check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score, False
        
        # 4. Place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. Update ui and clock
        self._update_ui(game_num, record, mean_score)
        self.clock.tick(SPEED)
        
        # 6. Return game over and score
        return reward, game_over, self.score, False
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # Hits itself
        if pt in self.snake[1:]:
            return True
        
        return False
    
    def _update_ui(self, game_num=0, record=0, mean_score=0.0):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Display multiple lines of information
        font = pygame.font.SysFont('arial', 20)
        font_small = pygame.font.SysFont('arial', 16)
        
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        length_text = font_small.render(f"Length: {len(self.snake)}", True, WHITE)
        
        self.display.blit(score_text, [10, 5])
        self.display.blit(length_text, [10, 30])
        
        if game_num > 0:
            game_text = font_small.render(f"Game: {game_num}", True, WHITE)
            record_text = font_small.render(f"Record: {record}", True, (255, 215, 0))  # Gold color
            mean_text = font_small.render(f"Mean: {mean_score:.1f}", True, WHITE)
            
            self.display.blit(game_text, [10, 50])
            self.display.blit(record_text, [10, 70])
            self.display.blit(mean_text, [10, 90])
        
        # Quit button (top-right, always visible)
        btn_w, btn_h = 80, 32
        margin = 10
        self.quit_button_rect = pygame.Rect(self.w - btn_w - margin, margin, btn_w, btn_h)
        pygame.draw.rect(self.display, (180, 50, 50), self.quit_button_rect)
        pygame.draw.rect(self.display, WHITE, self.quit_button_rect, 2)
        quit_label = font_small.render("Quit", True, WHITE)
        label_rect = quit_label.get_rect(center=self.quit_button_rect.center)
        self.display.blit(quit_label, label_rect)
        
        pygame.display.flip()
    
    def _move(self, action):
        # [straight, right turn, left turn]
        
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d
        
        self.direction = new_dir
        
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)

