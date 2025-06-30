import pygame
import random
import os
import sys

# Setup resource path for PyInstaller or normal run
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((900, 600))

# Background
background = pygame.image.load(resource_path('images/bg-space.jpg'))
background = pygame.transform.scale(background, (900, 600))
pygame.mixer.music.load(resource_path('sounds/bg-music.mp3'))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Alien Strike")
icon = pygame.image.load(resource_path('images/ufo.png'))
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load(resource_path('images/player.png'))
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 418
playerY = 530

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyCount = 6
enemyImgList = []
enemyX = []
enemyY = []
change = [0.75] * enemyCount
for i in range(enemyCount):
    enemyImgList.append(pygame.image.load(resource_path('images/enemy.png')))
    enemyImgList[i] = pygame.transform.scale(enemyImgList[i], (56, 56))
    enemyX.append(random.randint(11, 799))
    enemyY.append((random.randint(20, 200) // 50) * 50)

def enemy(x, y, i):
    screen.blit(enemyImgList[i], (x, y))

# Bullet
bulletImg = pygame.image.load(resource_path('images/bullet.png'))
bulletImg = pygame.transform.scale(bulletImg, (50, 50))
bulletX = 0
bulletY = 530
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 7, y))

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

def showScore(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game over screen
def show_gameOver(x, y):
    text = font.render("Game over!", True, (255, 255, 255))
    screen.blit(text, (x, y))
    small_text = font.render("Press r key to restart!", True, (255, 255, 255))
    screen.blit(small_text, (x-70, y+50))

# Game loop
run = True
while run:
    key = pygame.key.get_pressed()
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            run = False

    # Player movement
    player(playerX, playerY)

    if key[pygame.K_LEFT] or key[pygame.K_a]:
        playerX -= (1 if playerX > 1 else 0)
    if key[pygame.K_RIGHT] or key[pygame.K_d]:
        playerX += (1 if playerX < 835 else 0)
    if key[pygame.K_SPACE]:
        if bullet_state == "ready":
            fire_bullet(playerX, playerY)
            bulletX = playerX
            pygame.mixer.Sound(resource_path('sounds/laser.wav')).play()

    # Enemy movement and collision
    for i in range(enemyCount):
        enemy(enemyX[i], enemyY[i], i)
        enemyX[i] += change[i]
        if enemyX[i] > 840 or enemyX[i] < 10:
            change[i] *= -1
            enemyY[i] = round((enemyY[i] + 50) / 10) * 10

        # Collision detection
        if (enemyY[i] <= bulletY <= enemyY[i] + 55) and (enemyX[i] - 28 <= bulletX <= enemyX[i] + 28):
            score_value += 1
            enemyX[i] = random.randint(11, 799)
            enemyY[i] = (random.randint(20, 200) // 50) * 50
            bullet_state = "ready"
            bulletY = 530
            pygame.mixer.Sound(resource_path('sounds/explosion.wav')).play()

        # Game Over
        if enemyY[i] > 475:
            for j in range(enemyCount):
                enemyX[j] = 1000
                enemyY[j] = 1000
            show_gameOver(350, 250)
            

        # Restart (reset only one enemy? Bugfix below)
        if key[pygame.K_r]:
            playerX, playerY = 414, 530
            for i in range(enemyCount):
                enemyX[i] = random.randint(11, 799)
                enemyY[i] = (random.randint(20, 200) // 50) * 50
            score_value = 0
            bullet_state = "ready"
            bulletY = 530

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= 1.5
    if bulletY < 0:
        bullet_state = "ready"
        bulletY = 530

    showScore(textX, textY)
    pygame.display.flip()

pygame.quit()
