
import pygame
import random
import math
from pygame import mixer

pygame.init()

#pencere yaratır
screen=pygame.display.set_mode((800,600))

background=pygame.image.load("arka1.jpg")

#Arkaplan Ses
mixer.music.load("background.wav")
mixer.music.play(-1)

running=True

#Başlık ve icon
pygame.display.set_caption("Space Game")
icon=pygame.image.load("ufo.jpg")
pygame.display.set_icon(icon)

#Player
playerImg=pygame.image.load("arac.png")
playerX=370
playerY=480
playerX_change=0

#Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0,700))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)



#Bullet
#Ready - ekranda mermi görünmez
#Fire - mermi hareket halinde olur
bulletImg=pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=1
bullet_state="ready"

#Score
score_value=0
font=pygame.font.Font("freesansbold.ttf",32)

textX=10
textY=10

#Game Over Text
over_font=pygame.font.Font("freesansbold.ttf",64)


def show_score(x,y):
    score=font.render("Score : "+str(score_value), True,(0,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text=over_font.render("GAME OVER",True,(0,255,255))
    screen.blit(over_text,(200,250))



def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))


def isCollision(enemyX,enemyY,bulletX,bulleyY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulleyY,2) )
    if distance <27:
        return  True
    else:
        return False



while running:

    screen.fill((0, 0, 0))

    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        #klavye ile hareket ettirme
        if event.type ==pygame.KEYDOWN:
            #print("Bir tuşa basıldı")

            if event.key == pygame.K_LEFT:
                #print("sol tuşa basıldı")
                playerX_change=-0.3

            if event.key == pygame.K_RIGHT:
                #print("sağ tuşa basıldı")
                playerX_change=0.3

            #Boşluğa basınca mermi çıkar
            if event.key == pygame.K_SPACE:
                if bullet_state=="ready":
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #print("hareket durduruldu")
                playerX_change=0



    playerX += playerX_change

    if playerX <=0:
        playerX=0
    elif playerX >=736:
        playerX=736


    enemyX += enemyX_change
    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break

        enemyX[i]+=enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i]=0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i]=-0.3
            enemyY[i] += enemyY_change[i]

        collison = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison:
            explosion_Sound=mixer.Sound("explosion.wav")
            explosion_Sound.play()

            bulletY = 480
            bullet_state = "ready"
            score_value +=1
            enemyX[i] = random.randint(0, 730)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i],i)

    #Mermi hareketi

    if bulletY <=0:
        bulletY=480
        bullet_state="ready"

    if bullet_state=="fire":
        fire_bullet(playerX,bulletY)
        bulletY -= bulletY_change




    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()

