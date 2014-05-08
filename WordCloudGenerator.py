import Drawer
import pygame
import sys
import os
import random
import math
from pygame.locals import *
from Parser import Parser
import ObjectLogger

class WordCloudGenerator(object):

	def __init__(self):
		self.logger = ObjectLogger.ObjectLogger("WordCloudGenerator")
		self.logger.log("Initialising pygame")
		pygame.init()

		self.windowHeight = 800
		self.windowWidth = 800

		self.logger.log("Creating DISPLAYSURF with dimensions %dx%d" % (self.windowWidth, self.windowHeight))
		self.DISPLAYSURF = pygame.display.set_mode((self.windowWidth, self.windowHeight))

		self.logger.log("Creating wordCloudContainerRect")
		self.wordCloudContainerRect = self.DISPLAYSURF.get_rect()
		self.wordCloudContainerRect.width -= 150
		self.wordCloudContainerRect.height -= 150
		self.wordCloudContainerRect.topleft = (75,75)

		self.logger.log("Creating drawer object")
		self.drawer = Drawer.Drawer(self.DISPLAYSURF)

		self.drawer.fillBackground()

	def generateWordCloud(self, parsedDocument, imageOutputPath):
		self.logger.log("Generating wordcloud")

		self.logger.log("Choosing random colour scheme")
		self.drawer.randomizeColourScheme()

		self.drawer.fillBackground()

		self.logger.log("Creating empty wordRectObj list")
		self.wordRectList = []

		self.logger.log("Placing words in wordcloud on display surface")
		self.placeWords(parsedDocument)

		self.logger.log("Exporting wordcloud to %s" % imageOutputPath)
		self.drawer.exportDisplaySurf(imageOutputPath)

		self.logger.log("Wordcloud finished generating")

	def placeWords(self, parsedDocument):
		for wordNumber, word in enumerate(parsedDocument.wordList):
			self.placeWord(word, wordNumber)
			pygame.display.update()

	def placeWord(self, word, wordNumber):

		if wordNumber == 0:
			return self.placeInitialWord(word, wordNumber)

		textSurfaceObj, textRectObj = self.drawer.createTextRects(word[0], self.getWordSize(wordNumber))

		textRectObj.center = random.choice(self.wordRectList).center
		
		# Old system of choosing initial location for word. Resulted in multiple little word cloud
		# spread around, commented out rather than deleted for posterity.
		#rand_bottom = random.randint(textRectObj.height, self.drawer.DISPLAYSURF.get_height())
		#rand_right = random.randint(textRectObj.width, self.drawer.DISPLAYSURF.get_width())
		#textRectObj.center = (rand_bottom, rand_right)

		validLocation = self.validTextRectLocation(textRectObj)

		distanceToJump = 10

		while validLocation:
			if validLocation == 2:
				textRectObj.center = random.choice(self.wordRectList).center

			if bool(random.getrandbits(1)):
				if bool(random.getrandbits(1)):
					textRectObj.left += distanceToJump
				else:
					textRectObj.left -= distanceToJump
			else:
				if bool(random.getrandbits(1)):
					textRectObj.top += distanceToJump
				else:
					textRectObj.top -= distanceToJump

			validLocation = self.validTextRectLocation(textRectObj)

		self.wordRectList.append(textRectObj)

		self.drawer.drawWord(textSurfaceObj, textRectObj)

		return True

	def placeInitialWord(self, word, wordNumber):
		textSurfaceObj, textRectObj = self.drawer.createTextRects(word[0], self.getWordSize(wordNumber))

		textRectObj.center = (random.randrange(0, self.windowHeight), random.randrange(0, self.windowWidth))

		validLocation = self.validTextRectLocation(textRectObj)

		while validLocation:
			textRectObj.center = (random.randrange(0, self.windowHeight), random.randrange(0, self.windowWidth))
			validLocation = self.validTextRectLocation(textRectObj)

		self.wordRectList.append(textRectObj)

		self.drawer.drawWord(textSurfaceObj, textRectObj)

		return True

	def validTextRectLocation(self, textRectObj):
		for textRect in self.wordRectList:
			if textRect.colliderect(textRectObj):
				return 1

		if self.wordCloudContainerRect.contains(textRectObj):
			return 0
		else:
			return 2

	def getWordSize(self, wordNumber):
		fontSize = int(math.floor(50 - (wordNumber * wordNumber)/10))

		if fontSize < 15:
			fontSize = 15

		return fontSize