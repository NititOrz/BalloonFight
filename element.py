import pygame
from pygame.locals import *
import gamelib
from gamelib import *
from gamephys import *

#######################################################################################################################################################################################
class Player():

    PLAYER_ACC_X = 0.5
    PLAYER_ACC_Y = 1.0
    PLAYER_G = 0.1
    PLAYER_WIDTH = 20.0
    PLAYER_HEIGHT = 35.0
    MAX_VELOCITY = 5.0
    PLAYER_LIFE = 2.0
    
    def __init__(self, posX, posY, width = PLAYER_WIDTH, height = PLAYER_HEIGHT, pic = "player1.png"):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.rect = Rect(self.posX, self.posY, self.width, self.height)
        self.vx = 0
        self.vy = 0
        self.friction = Friction()
        self.turnright = False
        self.turnleft = False
        self.turn = False
        self.pic = pic
        self.life = self.PLAYER_LIFE

    def render(self, surface):
        # render player pic
        self.player = pygame.image.load(self.pic)
        self.rect = surface.blit(self.player, (self.posX, self.posY))

    def update(self):
        self.get()
        #########################################
        
    def move_up(self):
        if self.vy > -self.MAX_VELOCITY:
            self.vy -= self.PLAYER_ACC_Y
        else:
            self.vy = -self.MAX_VELOCITY + 0.1
        
    def move_down(self):
        self.vy = self.PLAYER_ACC_Y
    
    def move_right(self):
        if self.vx < self.MAX_VELOCITY:
            self.vx += self.PLAYER_ACC_X
        else:
            self.vx = self.MAX_VELOCITY - 0.1

        self.set_turnright()   

    def move_left(self):
        if self.vx > -self.MAX_VELOCITY:
            self.vx -= self.PLAYER_ACC_X
        else:
            self.vx = -self.MAX_VELOCITY + 0.1

        self.set_turnleft()

    def stop_moving(self):
        self.vy = 0
        self.g = 0
        self.vx = self.friction.goingbreak(self.turnright, self.turnleft, self.vx)

    def set_g(self):
        if self.vy < self.MAX_VELOCITY:
            self.vy += self.PLAYER_G
        else:
            self.vy = self.MAX_VELOCITY - 0.1

    def moving(self):
        self.posX += self.vx
        self.posY += self.vy

    def getarect(self):
        return self.rect

    def set_XY(self, posX, posY):
        self.posX = posX
        self.posY = posY

    def get_X(self):
        return self.posX

    def get_Y(self):
        return self.posY

    def set_V(self, vx, vy):
        self.vy = vy
        self.vx = vx

    def get_VX(self):
        return self.vx

    def get_VY(self):
        return self.vy

    def set_turnleft(self):
        self.turnleft = True
        self.turnright = False
        
    def set_turnright(self):
        self.turnright = True
        self.turnleft = False

    def get_life(self):
        return self.life

    def set_life(self, life):
        self.life = life

    def is_die(self, life):
        if(life <= 0):
            return True
        else:
            return False

    def set_pic(self, life, pic):
        if life == 0:
            self.pic = pic

        
#######################################################################################################################################################################################
class Floor():
    
    def __init__(self, pos, width, height, pic): # consturctor
        (self.posX, self.posY) = pos
        self.width = width
        self.height = height
        self.rect = Rect(self.posX, self.posY, self.width, self.height)
        self.floor = pygame.image.load(pic)
    
    def render(self, surface):
        surface.blit(self.floor, (self.posX, self.posY))

    def getarect(self):
        return self.rect

    def floor_check(self, player, bounce, balloon):
        self.bounce = bounce
        self.player = player
        self.balloon = balloon
        self.py = player.get_Y()
        self.px = player.get_X()
        self.vy = player.get_VY()
        self.vx = player.get_VX()

        if  self.posY + self.height - 11 < self.py - Balloon.BALLOON_HEIGHT < self.posY + self.height: # bottom
            self.player.set_XY(posX = self.px, posY = self.posY + self.height + Balloon.BALLOON_HEIGHT + 1)
            self.balloon.set_XY(posX = self.px, posY = self.posY + self.height + 1)
            self.player.set_V(vx = self.vx,vy = self.bounce.bounce_Y(self.vy))

        elif self.posY < self.py + Player.PLAYER_HEIGHT < self.posY + 11: # top
            self.player.set_XY(posX = self.px, posY = self.posY - Player.PLAYER_HEIGHT + 1)
            self.balloon.set_XY(posX = self.px, posY = self.posY - Player.PLAYER_HEIGHT - Balloon.BALLOON_HEIGHT +1)            


        elif self.posX < self.px + Player.PLAYER_WIDTH < self.posX + 12: # left
            self.player.set_XY(posX = self.posX - Player.PLAYER_WIDTH, posY = self.py)
            self.balloon.set_XY(posX = self.posX - Balloon.BALLOON_WIDTH, posY = self.py - Balloon.BALLOON_HEIGHT)
            self.player.set_V(vx = self.bounce.bounce_X(self.vx),vy = self.vy)
            self.player.set_turnleft()

        elif self.posX + self.width -12 < self.px < self.posX + self.width: #right
            self.player.set_XY(posX = self.posX + self.width, posY = self.py)
            self.balloon.set_XY(posX = self.posX + self.width, posY = self.py - Balloon.BALLOON_HEIGHT)
            self.player.set_V(vx = self.bounce.bounce_X(self.vx),vy = self.vy)
            self.player.set_turnright()

#######################################################################################################################################################################################

class Balloon():

    BALLOON_HEIGHT = 30
    BALLOON_WIDTH = 20

    def __init__(self, player):
        self.posX = player.get_X()
        self.posY = player.get_Y() - self.BALLOON_HEIGHT
        self.width = self.BALLOON_WIDTH
        self.height = self.BALLOON_HEIGHT
        self.balloon_pic = "2balloon.png"
        self.rect = Rect(self.posX, self.posY, self.width, self.height)

    def render(self, surface):
        self.balloon = pygame.image.load(self.balloon_pic)  
        self.rect = surface.blit(self.balloon, (self.posX, self.posY))

    def update_pos(self, player):
        self.posX = player.get_X()
        self.posY = player.get_Y() - self.BALLOON_HEIGHT

    def getarect(self):
        return self.rect

    def get_X(self):
        return self.posX

    def get_Y(self):
        return self.posY

    def set_XY(self, posX, posY):
        self.posX = posX
        self.posY = posY

    def set_pic(self, life):
        if life == 1:
            self.balloon_pic = "balloon.png"
        elif life == 0:
            self.balloon_pic = "noballoon.png"


#######################################################################################################################################################################################
class Water():

    WATER_HEIGHT = 60
    WATER_WIDTH = 232

    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.width = self.WATER_WIDTH
        self.height = self.WATER_HEIGHT
        self.water_pic = "water.png"
        self.rect = Rect(self.posX, self.posY, self.width, self.height)

    def render(self, surface):
        self.water = pygame.image.load(self.water_pic)
        self.rect = surface.blit(self.water, (self.posX, self.posY))


    def getarect(self):
        return self.rect