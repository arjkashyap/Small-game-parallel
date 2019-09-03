#!/usr/bin/python3.6
import sys
import pygame
import time
from pygame.locals import *
import random

pygame.init()

pygame.font.init()
myFont = pygame.font.SysFont('Comic Sans MS', 35)

# some color variables
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Display settings
W, H = 1366, 768
bg_speed = 3
posX, posY = W // 2, H // 2 - 140    # Player co-ordinates
posX2, posY2 = posX, posY * 3 / 2 + 105     # Player 2 co-ordinates

gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Parallel")

# Background Images
bgUp, bgDown = pygame.image.load('sprites/bgUp.jpg').convert(), pygame.image.load('sprites/bgDown.jpg').convert()
bgUp, bgDown = pygame.transform.scale(bgUp, (W, H // 2)), pygame.transform.scale(bgDown, (W, H // 2))

clock = pygame.time.Clock()
run = True
fps = 15
vel = 0         # inital speed of the player

# background image co-ordinates
bg_x = bg_y = 0
bg_x2, bg_y2 = 0, H // 2

# Player Common sprites
idle = [pygame.image.load("sprites/player/Idle/id1-r.png").convert_alpha(),
        pygame.image.load("sprites/player/Idle/id1-l.png").convert_alpha(),
        ]

run_right = [
    pygame.image.load("sprites/player/running/r" + str(x) + ".png").convert_alpha()
    for x in range(0, 7)
]

run_left = [
    pygame.image.load("sprites/player/running/l" + str(x) + ".png").convert_alpha()
    for x in range(0, 7)
]

jump = [
    pygame.image.load("sprites/player/jump/jump-up-l.png").convert_alpha(),
    pygame.image.load("sprites/player/jump/jump-fall-l.png").convert_alpha(),
    pygame.image.load("sprites/player/jump/jump-up-r.png").convert_alpha(),
    pygame.image.load("sprites/player/jump/jump-fall-r.png").convert_alpha(),
]

# Class for player1

knife_img = pygame.image.load("./sprites/knife/knife.png").convert_alpha()


class PlayerUP(object):

    def __init__(self, x, y, width, height, end):
        self.x = x  # Position x and y
        self.y = y
        self.width = width
        self.height = height
        self.isJump = False
        self.jumpCount = 10

        # Speed of moving
        self.end = end
        self.health = 10
        self.faceLeft = False
        self.faceRight = True

        # Load sprites for player 1
        self.idle = idle
        self.run_right = run_right
        self.run_left = run_left
        self.jump = jump

        # Initial index value for sprite
        self.index = 0

    def action(self, surface, velocity):
        if self.index >= 6:
            self.index = 0
        if vel > 0:             # Player is moving in a positive direction
            surface.blit(self.run_right[self.index % 7], (self.x, self.y))
            self.x += vel
            self.index += 1
        if vel < 0:
            surface.blit(self.run_left[self.index % 7], (self.x, self.y))
            self.x += vel
            self.index += 1


class PlayerDown:
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isJump = False
        self.jumpCount = 10
        # Speed of moving
        self.end = end
        self.health = 10
        self.faceLeft = False
        self.faceRight = True

       # Load sprites for player 2
        self.idle = [pygame.transform.rotate(img, 180) for img in idle]
        self.run_right = [pygame.transform.rotate(img, 180) for img in run_left]       # Loading and tilt images by 180 degree
        self.run_left = [pygame.transform.rotate(img, 180) for img in run_right]
        self.jump = [pygame.transform.rotate(img, 180) for img in jump]

        self.index = 0

    def action(self, surface, velocity):
        if self.index >= 6:
            self.index = 0
        if vel > 0:             # Player is moving in a positive direction
            surface.blit(self.run_right[self.index % 7], (self.x, self.y))
            self.x += vel
            self.index += 1
        if vel < 0:
            surface.blit(self.run_left[self.index % 7], (self.x, self.y))
            self.x += vel
            self.index += 1

# Class for incoming projectile


class Knife:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel              # variable speed of incomming projectile
        self.img = knife_img
        self.img2 = pygame.transform.rotate(knife_img, 180)
    # Knife motion

    # Incoming projectile logic
kPos_x = W                              # Positions
kPos_y = random.randrange(H // 4, H // 3 - 60)
kPos_x2 = 0
print("" + str(H // 4) + " and " + str(H // 2 - 40) + " is the rangeeee !!!!!!!!!!!")
k_speed = 20


def throwKnife(x, y, surface, frame):
    if frame == 1:
        surface.blit(k.img, (x, y))
    if frame == 2:
        surface.blit(k.img2, (x, y))
# Detect collision between player and projectile


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((W / 2), (H / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()


def detectCollision(surface, px, py, kx, ky):
    #print("range is : " + str(py) + " to " + str(py + 30))
    # if kx == px:
    #    print("X co-ordinates are equal.......")
    # if int(ky) in range(int(py), int(py + 400)) and int(kx) in range(int(px), int(px + 10)):
    #     message_display("Game Over")

    # print("px: " + str(px) + " py: " + str(py))
    # print("kx: " + str(kx) + " ky: " + str(ky))
    pass


# Player Objects
p = PlayerUP(posX, posY, 10, 10, 0)
p2 = PlayerDown(posX2, posY2, 10, 10, 0)

k = Knife(W, posY + 10, 20)

# Game Loop
while run:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and (key[K_LALT] or key[K_LALT])):
            run = False

    # Moving Background for image 1
    rel_x = bg_x % bgUp.get_rect().width
    gameDisplay.blit(bgUp, [rel_x - bgUp.get_rect().width, bg_y])
    gameDisplay.blit(bgUp, [rel_x, bg_y])                       # Overlaps image secoundary
    bg_x -= bg_speed
    if(rel_x < bgUp.get_rect().width):
        rel_x = 0

    # Moving Background for image 2
    rel_x2 = bg_x2 % bgDown.get_rect().width
    gameDisplay.blit(bgDown, [rel_x2 - bgDown.get_rect().width, bg_y2])
    gameDisplay.blit(bgDown, [rel_x2, bg_y2])
    bg_x2 += bg_speed

    # Throwing knife
    kPos_x -= k_speed
    kPos_x2 += k_speed
    throwKnife(kPos_x, kPos_y, gameDisplay, 1)
    throwKnife(kPos_x2, kPos_y + 300, gameDisplay, 2)
    # When the knife goes out of screen, regenerate the y co-ordinates and throw again
    if kPos_x <= 0:
        kPos_x = W + 20
        kPos_y = random.randrange(H // 4, H // 2 - 30)

    if kPos_x2 >= W - knife_img.get_rect().width:
        kPos_x2 = -20

    detectCollision(gameDisplay, p.x, p.y, kPos_x, kPos_y)

    keys = pygame.key.get_pressed()

    p.x -= bg_speed                         # Player x reduces with moving game cam
    p2.x += bg_speed

    if p.x <= 0:
        p.x += bg_speed
    if p2.x >= W - idle[0].get_rect().width:
        p2.x -= bg_speed

    # Motion Controls Player 1
    if keys[pygame.K_RIGHT] and p.x < W - abs(vel) - 50:
        p.faceRight, p.faceLeft = True, False
        vel = 18
        p.action(gameDisplay, vel)

    elif keys[pygame.K_LEFT] and p.x > 0:
        p.faceRight, p.faceLeft = False, True
        vel = -18
        p.action(gameDisplay, vel)

    elif p.faceRight:
        gameDisplay.blit(p.idle[0], (p.x, p.y))
    elif p.faceLeft:
        gameDisplay.blit(p.idle[1], (p.x, p.y))

    # Motion Conrtols Player 2
    if keys[pygame.K_d] and p2.x < W - abs(vel) - 50:
        p2.faceRight, p2.faceLeft = False, True
        vel = 18
        p2.action(gameDisplay, vel)

    elif keys[pygame.K_a] and p2.x > 0:
        p2.faceRight, p2.faceLeft = True, False
        vel = -18
        p2.action(gameDisplay, vel)

    elif p2.faceRight:
        gameDisplay.blit(p2.idle[0], (p2.x, p2.y))
    elif p2.faceLeft:
        gameDisplay.blit(p2.idle[1], (p2.x, p2.y))

    # Jump mechanics for player 1
    if not p.isJump:
        if keys[pygame.K_UP]:
            p.isJump = True
    else:
        if p.jumpCount >= -10:
            neg = 1
            if p.jumpCount < 0:
                neg = -1
            jumpVar = (p.jumpCount ** 2) * 0.3 * neg
            p.y -= jumpVar
            p.jumpCount -= 1

        else:
            p.isJump = False
            p.jumpCount = 10

    # player 2 jump mechanics
    if not p2.isJump:
        if keys[pygame.K_w]:
            p2.isJump = True
    else:
        if p2.jumpCount >= -10:
            neg = 1
            if p2.jumpCount < 0:
                neg = -1
            jumpVar = (p2.jumpCount ** 2) * 0.3 * neg
            p2.y += jumpVar                # Player  2 jump
            p2.jumpCount -= 1

        else:
            p2.isJump = False
            p2.jumpCount = 10
    # Player dead scenario
  #  if(p.x == )

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
