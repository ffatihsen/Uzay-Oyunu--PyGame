import pygame
import random #Düşmanın rastgele hareket etmesi için gerekli kütüphane
import math
from pygame import mixer


#Initialize the pygame
pygame.init()


#create the screen
screen=pygame.display.set_mode((800,600))

#Arkaplan
background=pygame.image.load("arka1.jpg")

#Arkaplan Ses
mixer.music.load("background.wav")
mixer.music.play(-1)

#Caption and icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("ufo.jpg")
pygame.display.set_icon(icon)

#Player
playerImg=pygame.image.load("arac.png")
playerX=370
playerY=480
playerX_change=0


#Enemy

#Burda liste şeklinde tanım yapıyoruz
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    #Düşmanın rastgele hareket etmesi için
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#Bullet
#Ready - ekran da mermiyi göremezsiniz
#fire - mermi muhtemelen hareket ediyor
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
    score=font.render("Score : "+str(score_value),True,(0,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x,y):
    screen.blit(playerImg,(x,y))


#Burda da i değişkenini parametre olarak ekledik
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10)) #Burdaki 16 ve 10 merminin tam ortadan çıkmasını sağlıyor



#Bu fonkssiyon da mermi  düşmana çarpıyorsa geriye true değerini dönderiyor
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt( (math.pow(enemyX-bulletX,2) )+ (math.pow(enemyY-bulletY,2)) ) #Burda yaptığımız işlem matematik de iki noktanın birbirine olan uzaklığını bulma formülü integral alınarak hesaplanıyor
    if distance<27:
        return True
    else:
        return False



#Game loop
running=True
while running:
    # RGB - Red,Green,Blue
    screen.fill((0, 0, 0))
    #playerX+=0.1 Burda sağa doğru hafif kaymasını sağlıyoruz

    #Arkaplan değişme
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        #klavyeden basılan tuşlara göre oyuncuyu hareket ettirme
        if event.type == pygame.KEYDOWN:
            #print("A keystoke is pressed ")
            if event.key == pygame.K_LEFT:
                #print("left arrow is pressed")
                playerX_change=-0.3
            if event.key == pygame.K_RIGHT:
                #print("right arrow is pressed")
                playerX_change = 0.3

            #Boşluğa basınca mermi oluşuyor fakat hareket etmiyor
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready": #Bu if de mermiyi ateşledikten sonra tekrardan space ye basınca merminin konumunun değişmemesini sağlıyor
                    bullet_Sound=mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    bulletX=playerX #Bu mermiyi nerde attıysak oraya götürecek mermi sağa sola kaymayacak
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               # print("keystoke has been relased")
               #playerX_change = 0.1
               playerX_change = 0



    playerX +=playerX_change

    #Bu if koşulu oyuncunun dışarı çıkmasını önlüyor
    if playerX <=0:
        playerX=0
    elif playerX >=736:
        playerX=736

    enemyX += enemyX_change

    # Bu if koşulu düşmanın dışarı çıkmasını önlüyor ve sağa sola doğru hareket etmesini sağlıyoruz
    #Bu for döngüsü sayesinde birden fazşa düşman hareket ediyor
    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i] >= 500:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break

        enemyX[i] +=enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        # Burda da fonksiyon çalıştırılıyor ve eğer düşman vuruldu ise yeni düşman yaratıyor
        #Bu kod sayesinde hangi düşmanı vurduğumuzu biliyoruz
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i],i)
    #Mermi hareketi
    #Mermi yi birden fazla kez atmamızı sağlayacak
    if bulletY <=0:
        bulletY=480
        bullet_state="ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change



    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()







