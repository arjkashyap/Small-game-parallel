#!/usr/bin/python3.6
import sys
import pygame
from pygame.locals import *

pygame.init()

# Display settings
W, H = 1366, 768

posX, posY = W // 4, H // 2 - 140    # Player co-ordinates
posX2, posY2 = posX, posY * 3 / 2 + 105

gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Parallel")
# Background Image
bgUp, bgDown = pygame.image.load('sprites/bgUp.jpg').convert(), pygame.image.load('sprites/bgDown.jpg').convert()
bgUp, bgDown = pygame.transform.scale(bgUp, (W, H // 2)), pygame.transform.scale(bgDown, (W, H // 2))
clock = pygame.time.Clock()
run = True
fps = 15
vel = 0         # inital speed of the player
# Player container


class PlayerUP(object):

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
        self.idle = [
            pygame.image.load("sprites/player/Idle/id1-r.png").convert_alpha(),
            pygame.image.load("sprites/player/Idle/id1-l.png").convert_alpha(),
        ]
        self.run_right = [
            pygame.image.load("sprites/player/running/r0.png").convert_alpha(),
            pygame.image.load("sprites/player/running/r1.png").convert_alpha(),
            pygame.image.load("sprites/player/running/r2.png").convert_alpha(),
            pygame.image.load("sprites/player/running/r3.png").convert_alpha(),
            pygame.image.load("sprites/player/running/r4.png").convert_alpha(),
            pygame.image.load("sprites/player/running/r5.png").convert_alpha(),
            pygame.image.load("sprites/player/running/r6.png").convert_alpha(),
        ]

        self.run_left = [
            pygame.image.load("sprites/player/running/l0.png").convert_alpha(),
            pygame.image.load("sprites/player/running/l1.png").convert_alpha(),
            pygame.image.load("sprites/player/running/l2.png").convert_alpha(),
            pygame.image.load("sprites/player/running/l3.png").convert_alpha(),
            pygame.image.load("sprites/player/running/l4.png").convert_alpha(),
            pygame.image.load("sprites/player/running/l5.png").convert_alpha(),
            pygame.image.load("sprites/player/running/l6.png").convert_alpha(),
        ]

        self.jump = [
            pygame.image.load("sprites/player/jump/jump-up-l.png").convert_alpha(),
            pygame.image.load("sprites/player/jump/jump-fall-l.png").convert_alpha(),
            pygame.image.load("sprites/player/jump/jump-up-r.png").convert_alpha(),
            pygame.image.load("sprites/player/jump/jump-fall-r.png").convert_alpha(),
        ]
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
        #self.img1 = pygame.transform.rotate(self.img1, 180)
        self.idle = [  
        pygame.image.load("sprites/player/Idle/id1-l.png").convert_alpha(), pygame.image.load("sprites/player/Idle/id1-r.png").convert_alpha(),
        ]
        self.idle = [pygame.transform.rotate(img, 180) for img in self.idle]
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

# Player Objects
p = PlayerUP(posX, posY, 10, 10, 0)
p2 = PlayerDown(posX2, posY2, 10, 10, 0)

# Game Loop
while run:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and (key[K_LALT] or key[K_LALT])):
            run = False
    gameDisplay.blit(bgUp, [0, 0])
    gameDisplay.blit(bgDown, [0, H // 2])

    keys = pygame.key.get_pressed()

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
    

    #Motion Conrtols Player 2

    gameDisplay.blit(p2.idle[0], (p2.x, p2.y))

    # Jump
    if not p.isJump:
        if keys[pygame.K_UP]:
            p.isJump = True
    else:
        if p.jumpCount >= -10:
            neg = 1
            if p.jumpCount < 0:
                neg = -1
            p.y -= (p.jumpCount ** 2) * 0.3 * neg
            p.jumpCount -= 1
        else:
            p.isJump = False
            p.jumpCount = 10

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
