import pygame
import random
import math
from pygame import mixer

#initilise the pygame

pygame.init()
#Create a screen
screen = pygame.display.set_mode((800,600))


#Background
background = pygame.image.load("F:/Game_Project/SpaceInvader/background.png")

# Background sound

mixer.music.load("F:/Game_Project/SpaceInvader/background.wav")
mixer.music.play(-1)
#Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("F:/Game_Project/SpaceInvader/ufo.png")
pygame.display.set_icon(icon)

#Player 

playerImg = pygame.image.load("F:/Game_Project/SpaceInvader/player.png")
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = [] 
EnemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load("F:/Game_Project/SpaceInvader/enemy.png"))
    EnemyX.append(random.randint(0,735))
    EnemyY.append(random.randint(50,150))
    EnemyX_change.append(4)
    EnemyY_change.append(40)

#Bullet
bulletImg = pygame.image.load("F:/Game_Project/SpaceInvader/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready" #You can't see the bullet on the screen  
 
# Font

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY =10

# Game over text

over_font = pygame.font.Font("freesansbold.ttf", 64)


def player(x,y):
    screen.blit(playerImg ,(x , y))


def Enemy(x,y,i):
    screen.blit(EnemyImg[i] ,(x , y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16 , y + 10))


def isCollision(EnemyX, EnemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(EnemyX - bulletX,2)) + (math.pow(EnemyY - bulletY,2)))
    if distance < 27:
        return True
    else: 
        return False

def show_score(x,y):
    score = font.render("Score : "+ str(score_value), True , (255, 255 ,255))
    screen.blit(score ,(x , y))


def game_over_text(x,y):
    over_text = over_font.render("GAME OVER ", True , (255, 255 ,255))
    screen.blit(over_text ,(200 , 250))




#Game Loop

running = True
while running:
    screen.fill((0,0,0))
    #background image
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            
            if event.key == pygame.K_RIGHT:
                 playerX_change = 5
            if event.key == pygame.K_SPACE:
                bullet_Sound = mixer.Sound("F:/Game_Project/SpaceInvader/laser.wav")
                bullet_Sound.play()
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, playerX)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                 playerX_change = 0
 # Checking for boundries of spaceship and enemy  
    playerX+= playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX= 736
# Enemy movement

    for i in range(num_of_enemies):

        # SOUND GAME OVER
        if EnemyY[i] > 440:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            game_over_text(200,250)
            break
        
        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <=0:
            EnemyX_change[i] = 4
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >=736:
            EnemyX_change[i] = -4
            EnemyY[i] += EnemyY_change[i]
        
        #Collision

        collision = isCollision(EnemyX[i], EnemyY[i], bulletX , bulletY)
        if collision:
            explosion_Sound = mixer.Sound("F:/Game_Project/SpaceInvader/explosion.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            
            EnemyX[i] = random.randint(0,735)
            EnemyY[i] = random.randint(50,150)
        
        Enemy(EnemyX[i] , EnemyY[i] ,i)


# Bullet movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is 'fire':
        fire_bullet(bulletX , bulletY)
        bulletY -= bulletY_change

    


    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()