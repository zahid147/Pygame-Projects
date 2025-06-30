import pygame
import random
import os
import sys

# 🛡️ Resource path for frozen (PyInstaller) and dev mode
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Initialize the game
pygame.init()
clock = pygame.time.Clock()

# Set display
screen = pygame.display.set_mode((400, 650))

# Background
bg = pygame.image.load(resource_path('images/bg1.jpg'))
bg = pygame.transform.scale(bg, (870, 650))
pygame.mixer.music.load(resource_path('sounds/bg-music.mp3'))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# Icon and caption
pygame.display.set_caption("Go Alien Go")
icon = pygame.image.load(resource_path('images/icon.png'))
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load(resource_path('images/player.png'))
playerImg = pygame.transform.scale(playerImg, (64, 64))
def player(x, y):
    screen.blit(playerImg, (x, y))

# Pillar
pillarImg = pygame.image.load(resource_path('images/pillar.png'))
pillarImg = pygame.transform.scale(pillarImg, (250, 600))
def pillar(x, y):
    screen.blit(pillarImg, (x, y))
    screen.blit(pillarImg, (x, y + 725))

def reset_game():
    global playerX, playerY, px1, px2, py1, py2
    global x1, x2, score_value, running

    playerX = 30
    playerY = 450
    px1, px2 = 200, 600
    py1, py2 = random.randint(-500, -150), random.randint(-500, -150)
    x1, x2 = 0, 870
    score_value = 0
    running = True

font = pygame.font.Font("freesansbold.ttf", 32)

def showScore():
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (10, 10))

def show_gameOver(x, y):
    text = font.render("Game over!", True, (255, 255, 0))
    screen.blit(text, (x, y))
    small_text = font.render("Press spacebar!", True, (255 , 255, 0)) 
    screen.blit(small_text, (x - 30, y + 50))

reset_game()
run = True

while run:
    key = pygame.key.get_pressed()
    scroll_speed = 3 + score_value / 50
    screen.fill((0, 0, 0))

    # Scroll background
    if running:
        x1 -= scroll_speed
        x2 -= scroll_speed
    if x1 <= -870: x1 = x2 + 870
    if x2 <= -870: x2 = x1 + 870
    screen.blit(bg, (x1, 0))
    screen.blit(bg, (x2, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            run = False
        if not running and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game()

    # Player movement
    player(playerX, playerY)
    if running:
        playerY += 4
        if key[pygame.K_SPACE] or key[pygame.K_UP] or key[pygame.K_w]:
            playerY -= 10

    # Pillars movement
    if running:
        px1 -= scroll_speed
        px2 -= scroll_speed

    pillar(px1, py1)
    if px1 <= -190:
        px1 = px2 + 400
        py1 = random.randint(-500, -150)
        if running: score_value += 1

    pillar(px2, py2)
    if px2 <= -190:
        px2 = px1 + 400
        py2 = random.randint(-500, -150)
        if running: score_value += 1

    # Collision detection
    player_rect = pygame.Rect(playerX, playerY, 55, 45)
    player_rect.y += 10
    player_rect.x += 5
    pillar1_top = pygame.Rect(px1+60, py1, 130, 590)
    pillar1_bottom = pygame.Rect(px1+60, py1 + 700, 130, 600)
    pillar1_bottom.y += 35
    pillar2_top = pygame.Rect(px2+60, py2, 130, 590)
    pillar2_bottom = pygame.Rect(px2+60, py2 + 700, 130, 600)
    pillar2_bottom.y += 35

    if player_rect.colliderect(pillar1_top) or player_rect.colliderect(pillar1_bottom) or \
       player_rect.colliderect(pillar2_top) or player_rect.colliderect(pillar2_bottom) or \
       not (0 <= playerY <= 600):
        if running:
            pygame.mixer.Sound(resource_path('sounds/explosion.wav')).play()
        running = False
        show_gameOver(100, 300)

    showScore()
    pygame.display.flip()
    clock.tick(60)
