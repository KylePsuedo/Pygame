#always start with Import.
import random
import pygame
import time
#import paddle
from Paddle import paddle
from Paddle2 import paddle2
from ball import Ball
from brick import Brick
import sys, os
from pygame import K_q, mixer

pygame.init()

scary = ("background.png")

#getting some colors in.
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)
PINK = (255, 192, 203)
DARKBLUE = (36,90,190)
SILVER = (192,192,192)
DARKPINK = (220, 182, 193)

score = 0
lives = 5

#background music

mixer.music.load("BACKGROUND.wav")
mixer.music.play()


#game window
size = (800,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Kyle Breakout!!!")

#all the sprites
all_sprites_list = pygame.sprite.Group()

#creates paddle
paddle = paddle(BLACK, 100, 10)
paddle2 = paddle2(BLACK, 100, 10)
paddle2.rect.x = 550
paddle2.rect.y = 560
paddle.rect.x = 150
paddle.rect.y = 560

#creates ball
ball = Ball(WHITE,10,10)
ball.rect.x = 345
ball.rect.y = 195

all_bricks = pygame.sprite.Group()


for i in range(7):
    brick = Brick(YELLOW,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(YELLOW,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(YELLOW,80,30)
    brick.rect.x = 60 + i* 100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)


#adding paddle to list of sprites
all_sprites_list.add(paddle)
all_sprites_list.add(paddle2)
all_sprites_list.add(ball)

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
bigfont = pygame.font.SysFont("comicsansms", 80)


def text_objects(text, color,shape):
    if shape == "small":
        textSurface = smallfont.render(text, True, color)
    elif shape == "medium":
        textSurface = medfont.render(text, True, color)
    elif shape == "big":
        textSurface = bigfont.render(text, True, color)
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

screen_height = 800
screen_width = 600
def message_to_screen (msg,color, y_displaced=0, shape ="small"):
    textSurf, textRect = text_objects(msg, color, shape)
    textRect.center = (screen_height / 2), (screen_width / 2) + y_displaced
    screen.blit(textSurf, textRect)
music = mixer.Sound("PAUSE.wav")

def pause():

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    music.stop()
                    mixer.music.play()
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
            screen.fill(PINK)
            message_to_screen("Paused", BLACK, -100, shape = "med")

        message_to_screen("Press C to continue or Q to quit.", BLACK, 25)
        message_to_screen("Please don't copyright strike me :(", BLACK, 200)
        pygame.display.update()
        clock.tick(60)

carryOn = True 
clock = pygame.time.Clock()

#Main Program Stuff
while carryOn:
    for event in pygame.event.get():    
        if event.type == pygame.QUIT: #if player closes game
            carryOn = False
                
                    
    #Key control for Paddle(s)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        #sprite.
        paddle.moveLeft (5)
    if keys[pygame.K_d]:
        paddle.moveRight(5)
    if keys[pygame.K_LEFT]:
        paddle2.moveLeft2 (5)
    if keys[pygame.K_RIGHT]:
        paddle2.moveRight2(5)
    if keys[pygame.K_q]:
                carryOn = False
    if keys[pygame.K_ESCAPE]:
        mixer.music.stop()
        music.play()
        pause()




    all_sprites_list.update()

    if ball.rect.x>=790:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=0:
        ball.velocity[0] = -ball.velocity[0]    
    if ball.rect.y>=590:
        ball.velocity[1] = -ball.velocity[1]
        lives -= 1
        if lives == 0:
            #Display Game Over Message for 3 seconds
            over = mixer.Sound("FAIL.wav")
            mixer.music.stop()
            font = pygame.font.Font(None, 74)
            image = pygame.image.load("download.png")
            image = pygame.transform.scale(image, (500,400))
            screen.blit(image, (150, 100))
            text = font.render("GAME OVER", 1, RED)
            screen.blit(text, (250,300))
            over.play()
            pygame.display.flip()
            pygame.time.wait(3000)
 
            #Stop the Game
            carryOn=False

    if ball.rect.y<=40:
        ball.velocity[1] = -ball.velocity[1]
    
    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddle):
      ball.rect.x -= ball.velocity[0]
      ball.rect.y -= ball.velocity[1]
      ball.bounce()
    if pygame.sprite.collide_mask(ball, paddle2):
      ball.rect.x -= ball.velocity[0]
      ball.rect.y -= ball.velocity[1]
      ball.bounce()

    #Plays noise once ball touches any Brick
    if pygame.sprite.spritecollideany(ball,all_bricks):
        #screen.fill(RED)
        impact = mixer.Sound("DING.wav")
        impact.play()
        screen.fill(RED, ball)
        pygame.display.update()
        pygame.time.wait(60)

        
      #Check if there is the ball collides with any of bricks
        
    brick_collision_list = pygame.sprite.spritecollide(ball,all_bricks,False)
    for brick in brick_collision_list:
        ball.bounce()
        score += 1
        brick.kill()
        


        if len(all_bricks)==0:
           #Display Level Complete Message for 3 seconds
            #giving VICTORY a variable
            win = mixer.Sound("VICTORY.wav")
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL COMPLETE", 1, WHITE)
            mixer.music.stop()
            #play win song!
            win.play()
            screen.blit(text, (200,300))
            pygame.display.flip()
            pygame.time.wait(4000)

            #Stop the Game
            carryOn=False

    
    screen.fill(PINK)
    pygame.draw.line(screen, WHITE, [0,38], [800, 38], 2)

#Score, Lives, and Title!
    font = pygame.font.Font(None, 34)
    text = font.render("Score: " + str(score), 1, BLACK)
    screen.blit(text, (20, 10))
    text =  font.render("Lives: " + str(lives), 1 , BLACK)
    screen.blit(text, (650,10))
    text =  font.render("Q = Quit." , 1 , BLACK)
    screen.blit(text, (185,10))
    text =  font.render("ESC = Pause." , 1 , BLACK)
    screen.blit(text, (385,10))

#draws all sprites
    all_sprites_list.draw(screen)

#displays name
    pygame.display.flip()

#limiting fps
    clock.tick(60)
#stops game engine
pygame.quit()