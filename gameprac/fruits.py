
import math
import random

import pygame
from pygame import mixer

pygame.init()


screen = pygame.display.set_mode((800,600))
background = pygame.image.load('background-gradient-lights.jpg')
mixer.music.load("26876617_MotionElements_sparks-of-edm_preview.mp3")
mixer.music.play(-1)


pygame.display.set_caption("Fruit Ninja")
icon = pygame.image.load('ninja.png')
pygame.display.set_icon(icon)


player = pygame.image.load('ninja.png')
pX = 370
pY = 480
pXchange = 0

fruit = []
fX = []
fY = []
fXchange = []
fYchange = []
num = 6

for i in range(num):
    fruit.append(pygame.image.load('watermelon.png'))
    fX.append(random.randint(0,736))
    fY.append(random.randint(50,150))
    fXchange.append(4)
    fYchange.append(40)

sword = pygame.image.load('ninja (1).png')
sX = 0
sY = 480
sXchange = 0
sYchange = 10
s_state = "ready"

score = 0

font = pygame.font.Font('freesansbold.ttf',32)

tx = 10
ty = 10

ov = pygame.font.Font('freesansbold.ttf',64)

def scores(x,y):
    s = font.render("Score: " + str(score), True,(255,255,255))
    screen.blit(s,(x,y))
    
def gameover():
    over = ov.render("Gameover bro", True,(255,255,255))    
    screen.blit(over,(200,250))

def play(x,y):
    screen.blit(player, (x,y))
    
def cut(x,y,i):
    screen.blit(fruit[i], (x,y))    
    
def slice(x,y):
    global s_state
    s_state = "fire"
    screen.blit(sword,(x+16, y+10))

def collision(fX,fY,sX,sY):
    d = math.sqrt(math.pow(fX-sX,2) + math.pow(fY-sY,2))
    if d<27:
        return True
    else:
        return False

run = True
while run:
    
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pXchange = -5
            if event.key == pygame.K_RIGHT:
                pXchange = 5
            if event.key == pygame.K_SPACE:
                if s_state is "ready":
                  sX = pX
                  slice(sX,sY)    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pXchange = 0
                              
    pX += pXchange
    
    if pX <= 0:
        pX = 0
    elif pX >= 736:
        pX = 736             
    
    for i in range(num):
        
        if fY[i] > 440:
            for j in range(num):
                fY[j] = 2000
            gameover()
            break    
        
        fX[i] += fXchange[i]
    
        if fX[i] <= 0:
           fXchange[i] = 1
           fY[i] += fYchange[i]
        elif fX[i] >= 736:
           fXchange[i] = -1     
           fY[i] += fYchange[i] 
    
        col = collision(fX[i],fY[i],sX,sY)   
        if col:
           explosion = mixer.Sound("knife-slice-41231.mp3")
           explosion.play()
           sY = 480
           s_state = "ready"
           score += 1
           fX[i] = random.randint(0,736)
           fY[i] = random.randint(50,150) 
        
        cut(fX[i], fY[i], i)          
        
    if sY <= 0:
        sY = 480
        s_state = "ready"
                                  
            
    if s_state == "fire":
        slice(sX,sY)
        sY -= sYchange
        
    
 
    play(pX,pY)
    scores(tx,ty)
    
    
    pygame.display.update()        