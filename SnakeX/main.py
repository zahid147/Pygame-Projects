import pygame, sys, random, os
from pygame.math import Vector2

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = pygame.transform.scale(
            pygame.image.load(resource_path('images/head_up.png')).convert_alpha(),
            (block_size, block_size)
        )
        self.head_down = pygame.transform.scale(
            pygame.image.load(resource_path('images/head_down.png')).convert_alpha(),
            (block_size, block_size)
        )
        self.head_right = pygame.transform.scale(
            pygame.image.load(resource_path('images/head_right.png')).convert_alpha(),
            (block_size, block_size)
        )
        self.head_left = pygame.transform.scale(
            pygame.image.load(resource_path('images/head_left.png')).convert_alpha(),
            (block_size, block_size)
        )

        self.tail_up = pygame.transform.scale(
            pygame.image.load(resource_path('images/tail_up.png')).convert_alpha(),
            (block_size, block_size)
        )
        self.tail_down = pygame.transform.scale(
            pygame.image.load(resource_path('images/tail_down.png')).convert_alpha(),
            (block_size, block_size)
        )
        self.tail_right = pygame.transform.scale(
            pygame.image.load(resource_path('images/tail_right.png')).convert_alpha(),
            (block_size, block_size)
        )
        self.tail_left = pygame.transform.scale(
            pygame.image.load(resource_path('images/tail_left.png')).convert_alpha(),
            (block_size, block_size)
        )

        self.body_vertical = pygame.transform.scale(
            pygame.image.load(resource_path('images/body_vertical.png')).convert_alpha(),
            (block_size, block_size)
        )
        self.body_horizontal = pygame.transform.scale(
            pygame.image.load(resource_path('images/body_horizontal.png')).convert_alpha(),
            (block_size, block_size)
        )

        self.body_tr = pygame.transform.scale(
            pygame.image.load(resource_path('images/body_tr.png')).convert_alpha(),
            (block_size, block_size)
        )
        self.body_tl = pygame.transform.scale(
            pygame.image.load(resource_path('images/body_tl.png')).convert_alpha(),
            (block_size, block_size)
        )
        self.body_br = pygame.transform.scale(
            pygame.image.load(resource_path('images/body_br.png')).convert_alpha(),
            (block_size, block_size)
        )
        self.body_bl = pygame.transform.scale(
            pygame.image.load(resource_path('images/body_bl.png')).convert_alpha(),
            (block_size, block_size)
        )
        self.crunch_sound = pygame.mixer.Sound(resource_path('sounds/crunch.wav'))

    def draw_snake(self):
        self.update_head_images()
        self.update_tail_images()
        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(block.x * block_size, block.y * block_size, block_size, block_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_images(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_images(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
        self.play_crunch_sound()

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

class FRUIT:
    def __init__(self):
        self.rand()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * block_size, self.pos.y * block_size, block_size, block_size)
        screen.blit(fruit, fruit_rect)

    def rand(self):
        self.x = random.randint(0,block_count - 1)
        self.y = random.randint(0,block_count - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        if running:
            self.snake.move_snake()
            self.check_eat()
            self.check_over()
        else:
            self.start_screen()

    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def check_eat(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.rand()
            self.snake.add_block()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.rand()

    def check_over(self):
        global running
        if not ((0 <= self.snake.body[0].x < block_count) and (0 <= self.snake.body[0].y < block_count)):
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()
        self.start_screen()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for col in range(block_count):
            for row in range(block_count):
                if (col & 1 and row & 1) or (not col & 1 and not row & 1):
                    grass_rect = pygame.Rect(col * block_size, row * block_size, block_size, block_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_plain = font.render(score_text, True, (56, 74, 12))
        scoreX = int(block_size * block_count - 50)
        scoreY = int(block_size * block_count - 40)
        score_rect = score_plain.get_rect(center = (scoreX, scoreY))
        fruit_rect = fruit.get_rect(midright = (score_rect.left, score_rect.centery))
        screen.blit(score_plain, score_rect)
        screen.blit(fruit, fruit_rect)

    def start_screen(self):
        global fruit, running
        if not running:
            screen.fill((50, 50, 50))
            title_font = pygame.font.Font(resource_path('font/PoetsenOne-Regular.ttf'), 40)
            small_font = pygame.font.Font(resource_path('font/PoetsenOne-Regular.ttf'), 25)
            title_text = title_font.render("Choose Your Character", True, (255, 255, 255))
            boy_text = small_font.render("Press B for Boy", True, (100, 200, 255))
            girl_text = small_font.render("Press G for Girl", True, (255, 100, 200))
            screen.blit(title_text, title_text.get_rect(center=(block_size * block_count // 2, 200)))
            screen.blit(boy_text, boy_text.get_rect(center=(block_size * block_count // 2, 300)))
            screen.blit(girl_text, girl_text.get_rect(center=(block_size * block_count // 2, 350)))
            key = pygame.key.get_pressed()
            if key[pygame.K_b]:
                fruit = peach
                running = True
            if key[pygame.K_g]:
                fruit = eggplant
                running = True

pygame.init()
clock = pygame.time.Clock()

block_size = 30
block_count = 20
screen = pygame.display.set_mode((block_size * block_count, block_size * block_count))
pygame.display.set_caption("SnakeX")
pygame.mixer.music.load(resource_path('sounds/bg-music.mp3'))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
running = False

peach = pygame.image.load(resource_path('images/fruit-1.png')).convert_alpha()
peach = pygame.transform.scale(peach, (block_size, block_size))
eggplant = pygame.image.load(resource_path('images/fruit-2.png')).convert_alpha()
eggplant = pygame.transform.scale(eggplant, (block_size, block_size))
font = pygame.font.Font(resource_path('font/PoetsenOne-Regular.ttf'), 25)
fruit = peach

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()
run = True

while run:
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            run = False
        if running:
            screen.fill((175, 215, 70))
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if key[pygame.K_UP]:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if key[pygame.K_DOWN]:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if key[pygame.K_LEFT]:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if key[pygame.K_RIGHT]:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            main_game.draw_elements()
        else:
            main_game.start_screen()

    pygame.display.flip()
    clock.tick(60)
