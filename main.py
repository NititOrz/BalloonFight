import pygame
from pygame.locals import *
from element import *
from gamephys import *
from gamemanage import *

from gamelib import *

class BalloonGame(SimpleGame):
    BLACK = pygame.Color('black')
    WHITE = pygame.Color('white')
    GREEN = pygame.Color('green')
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480
    
    ############################################################# 
    # main operator from gamelib
    
    def __init__(self):#constructor
        super(BalloonGame, self).__init__('Balloon')
        self.player1 = Player(posX = 10, posY = 300, pic = "player1.png")
        self.player2 = Player(posX = 610, posY = 300, pic = "player2.png")
        self.floor = [Floor(pos = (-20, 360), width = 214, height = 120, pic = "big_floor.png"),
                      Floor(pos = (426, 360), width = 270, height = 120, pic = "big_floor.png"),
                      Floor(pos = (150, 220), width = 107, height = 50, pic = "mid2_floor.png"),
                      Floor(pos = (327, 200), width = 107, height = 50, pic = "mid2_floor.png"),
                      Floor(pos = (75, 70), width = 157, height = 50, pic = "mid1_floor.png"),
                      Floor(pos = (500, 70), width = 80, height = 100, pic = "smallheight_floor.png")]
        self.balloon1 = Balloon(self.player1)
        self.balloon2 = Balloon(self.player2)
        self.water = Water(posX = 194, posY = 420)
        self.collide1 = Collision()
        self.collide2 = Collision()
        self.bounce = Bouncing()
        self.bgcheck = BG_check()
        self.ballooncheck1 = Checkballoon(self.player1,self.balloon2)
        self.ballooncheck2 = Checkballoon(self.player2,self.balloon1)
        self.p1_life = self.player1.get_life()
        self.p2_life = self.player2.get_life()
        
    def __init():
        super(BalloonGame, self).init()
    
    def update(self):
        self.handle_movement()
        self.player1.moving()
        self.player2.moving()
        self.balloon1.update_pos(self.player1)
        self.balloon2.update_pos(self.player2)
        
        self.check_balloon()
        self.balloon1.set_pic(self.p1_life)
        self.balloon2.set_pic(self.p2_life)
        self.player1.set_pic(self.p1_life, "player1die.png")
        self.player2.set_pic(self.p2_life, "player2die.png")

        self.floor_check_player_and_balloon()
        self.water_check()

        self.bgcheck.bg_check(self.player1, self.balloon1, self.bounce)
        self.bgcheck.bg_check(self.player2, self.balloon2, self.bounce)

    def render(self, surface):
        self.surface.fill(self.BLACK) # render background
        self.player1.render(surface) # render player1
        self.player2.render(surface) # render player2
        self.balloon1.render(surface) # render balloon1
        self.balloon2.render(surface) # render balloon2
        self.water.render(surface) # render water
        for x in self.floor:
            x.render(surface) # render floor
        pygame.display.flip()
        
        
    ##################################################################################################
    # other operator

    def handle_movement(self): # handle player movement
        if self.player1.is_die(self.p1_life) != True:
            if self.is_key_pressed(K_UP):
                self.player1.move_up()
            #elif self.is_key_pressed(K_DOWN):
            #    self.player1.move_down()
            if self.is_key_pressed(K_LEFT):
                self.player1.move_left()
            elif self.is_key_pressed(K_RIGHT):
                self.player1.move_right()                   # player 1
        ############################################################
        if self.player2.is_die(self.p2_life) != True:
            if self.is_key_pressed(K_w):                    # player 2
                self.player2.move_up()
            #elif self.is_key_pressed(K_s):
            #    self.player2.move_down()
            if self.is_key_pressed(K_a):
                self.player2.move_left()
            elif self.is_key_pressed(K_d):
                self.player2.move_right()

    def floor_check_player_and_balloon(self):
        for x in self.floor:
            if self.collide1.is_collide(self.player1.getarect(), x.getarect()) or self.collide1.is_collide(self.balloon1.getarect(), x.getarect()):
                self.player1.stop_moving()
                x.floor_check(self.player1, self.bounce, self.balloon1)
                break
            else:
                self.player1.set_g()

        for y in self.floor:
            if self.collide2.is_collide(self.player2.getarect(), y.getarect()) or self.collide2.is_collide(self.balloon2.getarect(), y.getarect()):
                self.player2.stop_moving()
                y.floor_check(self.player2, self.bounce, self.balloon2)
                break
            else:
                self.player2.set_g()

    def check_balloon(self): # check for gamemanage about life
        self.p1_life = self.player1.get_life()
        self.p2_life = self.player2.get_life()
        self.p1_life = self.ballooncheck2.check_state(self.p1_life)
        self.p2_life = self.ballooncheck1.check_state(self.p2_life)
        self.player1.set_life(self.p1_life)
        self.player2.set_life(self.p2_life)


    def water_check(self):
        if self.collide1.is_collide(self.player1.getarect(), self.water.getarect()):
            if self.p1_life != 0 and self.p2_life != 0:
                self.p1_life = 0
                self.player1.set_life(self.p1_life)

        if self.collide2.is_collide(self.player2.getarect(), self.water.getarect()):
            if self.p2_life != 0 and self.p2_life != 0:
                self.p2_life = 0
                self.player2.set_life(self.p2_life)

def main():
    game = BalloonGame()
    game.run()
    
if __name__ == '__main__':
    main()    