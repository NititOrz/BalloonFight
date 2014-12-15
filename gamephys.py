import pygame
from pygame.locals import *

#############################################################
class Collision():
  
    def __init__(self):
        pass

    def is_collide(self, rect1, rect2):
        self.rect1 = rect1
        self.rect2 = rect2

        return self.rect1.colliderect(self.rect2)
        
##########################################################################################################################

class Friction():

    PLAYER_FRICTION = 0.2

    def __init__(self):
        pass

    def goingbreak(self, is_turnright, is_turnleft, vx):
        self.friction = self.PLAYER_FRICTION
        if is_turnright:
            if vx >= 0:
                vx -= self.friction
                return vx
            else:
                self.friction = 0
                vx = 0.1
                return vx
        elif is_turnleft:
            if vx <= 0:
                vx += self.friction
                return vx
            else:
                self.friction = 0
                vx = -0.1
                return vx
        else:
            return vx

##########################################################################################################################

class Bouncing():

    def __init__(self):
        pass

    def bounce_Y(self, vy):
        return -vy

    def bounce_X(self, vx):
        return -vx

##########################################################################################################################


class BG_check():

    WINDOW_WIDTH = 640

    def bg_check(self, player, balloon, bounce):
        y = player.get_Y()
        x = player.get_X()
        vy = player.get_VY()
        if x + player.PLAYER_WIDTH/2 < 0: # left
            player.set_XY(posX = self.WINDOW_WIDTH - player.PLAYER_WIDTH + 15, posY = y) # 15 is various
        elif x - player.PLAYER_WIDTH/2 > self.WINDOW_WIDTH: # right
            player.set_XY(posX = 0 - player.PLAYER_WIDTH + 15, posY = y +3)
        if y + player.PLAYER_HEIGHT/2 + 5 - balloon.BALLOON_HEIGHT < 0:
            player.set_XY(posX = x, posY = 0 - player.PLAYER_HEIGHT/2 + balloon.BALLOON_HEIGHT)
            vy = bounce.bounce_Y(vy)
            player.set_V(vx = player.get_VX(),vy = vy)

