import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("images/background.png")

# Background game music
mixer.music.load("soundEffects/02_Objective.mp3")
# adding -1 play the music in loop
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('images/spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('images/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/alien.png'))
    enemyX.append(random.randint(0, 765))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(30)

# missile

# Ready - You can't see the missile on the screen
# Fire - The missile is currently moving
missileImg = pygame.image.load('images/missile.png')
missileX = 0
missileY = 480
missileX_change = 4
missileY_change = 10
missile_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 42)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 72)


def showScore(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render(f"Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = 'fire'
    screen.blit(missileImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt((math.pow(enemyX - missileX, 2)) + (math.pow(enemyY - missileY, 2)))
    if distance < 33:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # Background color
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        # KEYDOWN is pressing up any key in keyboard and KEYUP is releasing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if missile_state == 'ready':
                    missile_sound = mixer.Sound("soundEffects/missileSound.wav")
                    missile_sound.play()
                    # Get the current x coordinate of the spaceship
                    missileX = playerX
                    fire_missile(missileX, missileY)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 767:
        playerX = 767

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 430:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            mixer.music.stop()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 727:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], missileX, missileY)
        if collision:
            explosion_sound = mixer.Sound("soundEffects/Explosion.wav")
            explosion_sound.play()
            missileY = 480
            missile_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 765)
            enemyY[i] = random.randint(20, 50)

        enemy(enemyX[i], enemyY[i], i)

    # missile movement
    if missileY <= 0:
        missileY = 480
        missile_state = 'ready'

    if missile_state == 'fire':
        fire_missile(missileX, missileY)
        missileY -= missileY_change

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
