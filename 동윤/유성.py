import pygame
from pygame.rect import *
import random

def restart():
    global isGameOver, score
    isGameOver = False
    score = 0
    for i in range(len(star)):
        recStar[i].y = -1
    for i in range(len(missile)):
        recMissile[i].y = -1

def eventProcess():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            if event.key == pygame.K_LEFT:
                move.x = -1
            if event.key == pygame.K_RIGHT:
                move.x = 1
            if event.key == pygame.K_UP:
                move.y = -1
            if event.key == pygame.K_DOWN:
                move.y = 1
            if event.key == pygame.K_r:
                restart()
            if event.key == pygame.K_SPACE:
                makeMissile()

def movePlayer():
    if not isGameOver:
        recPlayer.x += move.x
        recPlayer.y += move.y
    if recPlayer.x < 0:
        recPlayer.x = 0
    if recPlayer.x > SCREEN_WIDTH-recPlayer.width:
        recPlayer.x = SCREEN_WIDTH-recPlayer.width
    if recPlayer.y < 0:
        recPlayer.y = 0
    if recPlayer.y > SCREEN_HEIGHT-recPlayer.height:
        recPlayer.y = SCREEN_HEIGHT-recPlayer.height        
    SCREEN.blit(player, recPlayer)

def timeDelay500ms():
    global time_delay_500ms
    if time_delay_500ms > 5:
        time_delay_500ms = 0
        return True    
    time_delay_500ms += 1
    return False

def makeStar():
    if isGameOver:
        return
    if timeDelay500ms():
        idex = random.randint(0, len(star)-1)
        if recStar[idex].y == -1:
            recStar[idex].x = random.randint(0, SCREEN_WIDTH)
            recStar[idex].y = 0

def moveStar():
    makeStar()
    for i in range(len(star)):
        if recStar[i].y == -1:
            continue
        if not isGameOver:
            recStar[i].y += 1
        if recStar[i].y > SCREEN_HEIGHT:
            recStar[i].y = 0
        SCREEN.blit(star[i], recStar[i])

def CheckCollisionMissile():
    global score, isGameOver
    if isGameOver:
        return
    for rec in recStar:
        if rec.y == -1:
            continue
        for recM in recMissile:
            if recM.y == -1:
                continue
            if rec.top < recM.bottom \
                    and recM.top < rec.bottom \
                    and rec.left < recM.right \
                    and recM.left < rec.right:
                rec.y = -1
                recM.y = -1
                score += 10
                # print(rec, recM)
                break            

def makeMissile():
    if isGameOver:
        return
    for i in range(len(missile)):
        if recMissile[i].y == -1:
            recMissile[i].x = recPlayer.x
            recMissile[i].y = recPlayer.y
            break

def moveMissile():
    # makeMissile()
    for i in range(len(missile)):
        if recMissile[i].y == -1:
            continue
        if not isGameOver:
            recMissile[i].y -= 1
        if recMissile[i].y < 0:
            recMissile[i].y = -1
        SCREEN.blit(missile[i], recMissile[i])

def CheckCollision():   
    global score, isGameOver
    if isGameOver:
        return
    for rec in recStar:
        if rec.y == -1:
            continue
        if rec.top < recPlayer.bottom \
            and recPlayer.top < rec.bottom \
            and rec.left < recPlayer.right \
            and recPlayer.left < rec.right:
            print('??????')
            isGameOver = True
            break
    score += 1

def blinking():
    global time_dealy_4sec, toggle
    time_dealy_4sec += 1
    if time_dealy_4sec > 40:
        time_dealy_4sec = 0
        toggle = ~toggle    
    return toggle

def setText():
    mFont = pygame.font.SysFont("arial",20, True, False)
    SCREEN.blit(mFont.render(
        f'score : {score}', True, 'green'), (10, 10, 0, 0))

    if isGameOver and blinking():
        SCREEN.blit(mFont.render(
            'Game Over!!', True, 'red'), (150, 300, 0, 0))
        SCREEN.blit(mFont.render(
            'press R - Restart', True, 'red'), (140, 320, 0, 0))

isActive = True
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
move = Rect(0,0,0,0)
time_delay_500ms = 0
time_dealy_4sec = 0
toggle = False
score = 0
isGameOver = False

pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('???????????????!!')

player = pygame.image.load('player.png')
player = pygame.transform.scale(player,(20,30))
recPlayer = player.get_rect()
recPlayer.centerx = (SCREEN_WIDTH/2)
recPlayer.centery = (SCREEN_HEIGHT/2)

star = [pygame.image.load('star.png') for i in range(40)]
recStar = [None for i in range(len(star))]
for i in range(len(star)):
    star[i] = pygame.transform.scale(star[i], (20, 20))
    recStar[i] = star[i].get_rect()
    recStar[i].y = -1

missile = [pygame.image.load('player.png') for i in range(40)]
recMissile = [None for i in range(len(missile))]
for i in range(len(missile)):
    missile[i] = pygame.transform.scale(missile[i], (20, 20))
    recMissile[i] = missile[i].get_rect()
    recMissile[i].y = -1

clock = pygame.time.Clock()

while isActive:
    SCREEN.fill((0,0,0))
    eventProcess()
    movePlayer()
    moveStar()
    moveMissile()
    CheckCollisionMissile()
    CheckCollision()
    setText() 
    pygame.display.flip()
    clock.tick(100)
