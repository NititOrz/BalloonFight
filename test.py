import pygame
from pygame.locals import *

a = Rect(1,1,10,10)

b = Rect(0,0,1,1)

print a.colliderect(b)