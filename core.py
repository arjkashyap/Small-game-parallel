#!/usr/bin/python3.6
import sys
import pygame
from pygame.locals import *
import random

pygame.init()

# Display settings
W, H = 1366, 768
bg_speed = 5
posX, posY = W // 4, H // 2 - 140    # Player co-ordinates
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
        self.faceLeft = True
        self.faceRight = False

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
        self.img = pygame.image.load("./sprites/knife/knife.png").convert_alpha()
        self.throwKnife = [x for x in range(0, 50, 5)]      # throw knife when num is present in list

    # Knife motion
    def action(self, surface):
        surface.blit(self.img, (self.x, self.y))
        self.x -= self.vel

    # function for throwing knife at random intervals
  #  def incoming(self, surface):
  #      inst_num = random.randint(0, 50)            # random number generated
    #    print(inst_num)
  #      if inst_num in self.throwKnife:


def throwKnife(x, y, surface):
    print("Object thrown " + str(x) + " " + str(y))
    surface.blit(k.img, (x, y))

    # Incoming projectile logic
kPos_x = W                              # Positions
kPos_y = random.randrange(0, H // 2)
k_speed = 10


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
    bg_x2 -= bg_speed

    # Throwing knife
    kPos_x -= k_speed
    kPos_y = random.randrange(0, H // 2)
    throwKnife(kPos_x, kPos_y, gameDisplay)

    keys = pygame.key.get_pressed()

    p.x -= bg_speed                         # Player x reduces with moving game cam
    p2.x -= bg_speed

    if p.x <= 0 or p2.x <= 0:
        p.x += bg_speed
        p2.x += bg_speed

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
    if keys[pygame.K_RIGHT] and p2.x < W - abs(vel) - 50:
        p2.faceRight, p2.faceLeft = False, True
        vel = 18
        p2.action(gameDisplay, vel)

    elif keys[pygame.K_LEFT] and p2.x > 0:
        p2.faceRight, p2.faceLeft = True, False
        vel = -18
        p2.action(gameDisplay, vel)

    elif p2.faceRight:
        gameDisplay.blit(p2.idle[0], (p2.x, p2.y))
    elif p2.faceLeft:
        gameDisplay.blit(p2.idle[1], (p2.x, p2.y))
    # Jump movement for both players
    if not p.isJump:
        if keys[pygame.K_UP]:
            p.isJump = p2.isJump = True

    else:
        if p.jumpCount >= -10:
            neg = 1
            if p.jumpCount < 0:
                neg = -1
            jumpVar = (p.jumpCount ** 2) * 0.3 * neg
            p.y -= jumpVar
            p2.y += jumpVar                # Player  2 jump
            p.jumpCount -= 1

        else:
            p.isJump = False
            p2.isJump = False
            p.jumpCount = 10

    # Player dead scenario
  #  if(p.x == )

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
