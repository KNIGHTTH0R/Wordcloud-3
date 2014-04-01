import pygame
import os
import json
import random

class Drawer (object):
	
	def __init__(self, DISPLAYSURF):
		self.DISPLAYSURF = DISPLAYSURF
		self.fontObjects = {}

		with open('Settings/colourSchemes.json') as json_data:
			self.colourSchemes = json.load(json_data)

		self.randomizeColourScheme()

	def randomizeColourScheme(self):
		self.colourScheme = self.colourSchemes[random.choice(self.colourSchemes.keys())]

	def fillBackground(self):
		self.DISPLAYSURF.fill(self.colourScheme["background"])

	# Print message to co-ordinates xPixel, yPixel.
	# Font size is also a parameter but if nothing is sent it defaults to 32.
	def createTextRects(self, message, fontSize = 32):
		if fontSize in self.fontObjects:
			fontObj = self.fontObjects[fontSize]
		else:
			fontObj = pygame.font.SysFont('helveticaneuedeskui', fontSize)
			self.fontObjects[fontSize] = fontObj

		textSurfaceObj = fontObj.render(message, 
										True, 
										random.choice(self.colourScheme["wordColours"]), 
										self.colourScheme["background"])
		textRectObj = textSurfaceObj.get_rect()

		return textSurfaceObj, textRectObj

	def drawWord(self, textSurfaceObj, textRectObj):
		self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)

	def exportDisplaySurf(self, outputPath):
		pygame.image.save(self.DISPLAYSURF, outputPath) 