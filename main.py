import pygame
import time
import random
import os

pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Set up the game window
DIS_WIDTH = 800
DIS_HEIGHT = 600
DIS = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game by OpenAI GPT')

# Set up the snake and food
SNAKE_BLOCK = 20
SNAKE_SPEED = 15

font_style = pygame.font.SysFont(None, 50)

# Load sound effects
try:
    EAT_SOUND = pygame.mixer.Sound("eat_sound.wav")
except FileNotFoundError:
    print("Sound file 'eat_sound.wav' not found.")
    EAT_SOUND = None

class SnakeGame:
    def __init__(self):
        self.game_over = False
        self.game_close = False

        self.snake_block = SNAKE_BLOCK
        self.snake_speed = SNAKE_SPEED

        self.x1 = DIS_WIDTH / 2
        self.y1 = DIS_HEIGHT / 2

        self.x1_change = 0
        self.y1_change = 0

        self.snake_list = []
        self.length_of_snake = 1

        self.foodx = round(random.randrange(0, DIS_WIDTH - self.snake_block) / 20.0) * 20.0
        self.foody = round(random.randrange(0, DIS_HEIGHT - self.snake_block) / 20.0) * 20.0

    def draw_snake(self):
        for x in self.snake_list:
            pygame.draw.rect(DIS, WHITE, [x[0], x[1], self.snake_block, self.snake_block])

    def draw_food(self):
        pygame.draw.rect(DIS, RED, [self.foodx, self.foody, self.snake_block, self.snake_block])

    def message(self, msg, color, y_displace=0):
        mesg = font_style.render(msg, True, color)
        dis_width_center = DIS_WIDTH / 2 - mesg.get_width() / 2
        DIS.blit(mesg, [dis_width_center, DIS_HEIGHT / 2 + y_displace])

    def game_loop(self):
        while not self.game_over:
            while self.game_close:
                DIS.fill(BLUE)
                self.message("You Lost! Press Q-Quit or C-Play Again", RED, y_displace=-50)
                self.message("Your Score: {}".format(self.length_of_snake - 1), WHITE, y_displace=50)
                self.draw_snake()
                self.draw_food()
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_over = True
                            self.game_close = False
                        elif event.key == pygame.K_c:
                            self.__init__()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x1_change = -self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        self.x1_change = self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_UP:
                        self.y1_change = -self.snake_block
                        self.x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        self.y1_change = self.snake_block
                        self.x1_change = 0

            if (
                self.x1 >= DIS_WIDTH
                or self.x1 < 0
                or self.y1 >= DIS_HEIGHT
                or self.y1 < 0
            ):
                self.game_close = True

            self.x1 += self.x1_change
            self.y1 += self.y1_change
            DIS.fill(BLACK)
            self.draw_food()
            snake_head = [self.x1, self.y1]
            self.snake_list.append(snake_head)
            if len(self.snake_list) > self.length_of_snake:
                del self.snake_list[0]

            for x in self.snake_list[:-1]:
                if x == snake_head:
                    self.game_close = True

            self.draw_snake()
            pygame.display.update()

            if self.x1 == self.foodx and self.y1 == self.foody:
                self.foodx = round(random.randrange(0, DIS_WIDTH - self.snake_block) / 20.0) * 20.0
                self.foody = round(random.randrange(0, DIS_HEIGHT - self.snake_block) / 20.0) * 20.0
                self.length_of_snake += 1
                if EAT_SOUND:
                    EAT_SOUND.play()

            pygame.time.Clock().tick(self.snake_speed)

        pygame.quit()
        quit()


if __name__ == "__main__":
    snake_game = SnakeGame()
    snake_game.game_loop()
