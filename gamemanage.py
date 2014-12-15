import pygame
from pygame.locals import *
from element import *
from gamephys import *

from gamelib import *

class Checkballoon():

	def __init__(self, player, balloon):
		self.player = player
		self.balloon = balloon
		self.collide = Collision()
		self.iscolliding = False
		self.iscollided = False

	def check(self, live):
		if self.collide.is_collide(self.player.getarect(), self.balloon.getarect()):
			self.iscolliding = True
		elif self.iscolliding == True:
			# print self.iscolliding
			# print self.iscollided
			self.iscollided = True
			self.iscolliding = False
		# print self.iscolliding
		# print self.iscollided
		if self.iscollided == True:
			self.set_state()
			return live - 1
		else:
			# self.set_state()
			return live

	def set_state(self):
		self.iscolliding = False
		self.iscollided = False



			

