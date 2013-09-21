import operator
import os
import sys

class Parser(object):

	def __init__(self, documentName, verbose):
		self.documentName = documentName
		self.verbose = verbose

		self.parsedList = []

		# Pull out the file extension and lower it to check what sort of file we've been given.
		fileName, fileExtension = os.path.splitext(documentName)
		fileExtension = fileExtension.lower()

		# Send the file to different functions based upon which file we have.
		if(fileExtension == '.txt'):
			if self.verbose:
				print documentName, "is a .txt file."
			self.parsedWords = self.parseTextDocument(documentName)
		elif(fileExtension == '.pdf'):
			if self.verbose:
				print documentName, "is a .pdf file."
			self.parsedWords = self.parsePDFDocument(documentName)
		else:
			print "Sorry, this is not an accepted filetype. Try again with a .txt or .pdf file."
			exit(1)

	def parseTextDocument(self, documentName):
		'''
		Takes in a filepath to a .txt document and creates two lists, parsedList and parsedListBlacklist.
		parsedList contains all the words from the document and the count of how many times they appeared.
		parsedListBlacklisted is the same list, minus any that appear in blacklist.txt

		These lists are accessed via getParsedWords and getParsedWordsBlacklisted.
		'''

		parsedList = {}
		parsedListBlacklisted = {}

		# Pull out each word and add it to the appropriate dicts
		try:
			with open(documentName, 'r') as f:
				for line in f:
					for word in line.split():
						cleanedWord = self.cleanedWord(word)

						if not self.inBlacklist(cleanedWord):
							parsedListBlacklisted = self.addWordToDict(cleanedWord, parsedListBlacklisted)

						parsedList = self.addWordToDict(cleanedWord, parsedList)

			if self.verbose == True:
				print "Parsing complete."

			# Convert un-ordered dicts into sorted lists.
			self.parsedList = self.dictToSortedList(parsedList)
			self.parsedListBlacklisted = self.dictToSortedList(parsedListBlacklisted)

		except IOError:
			print "File does not exist, exiting program."
			exit(1)

	def parsePDFDocument(self, documentName):
		'''
		Takes in a filepath to a .pdf document and creates two lists, parsedList and parsedListBlacklist.
		parsedList contains all the words from the document and the count of how many times they appeared.
		parsedListBlacklisted is the same list, minus any that appear in blacklist.txt

		These lists are accessed via getParsedWords and getParsedWordsBlacklisted.
		'''

		print "Sorry, pdf parsing isn't implemented yet."
		exit(0)

	def cleanedWord(self, word):
		'''
		Cleans a word. Puts it to lowercase, strips whitespace and other unwanted characters, including citations from wikipedia.
		'''

		cleanedWord = word.lower()

		cleanedWord = cleanedWord.rstrip()

		return cleanedWord

	def inBlacklist(self, word):
		'''
		Returns True if a word is in blacklist.txt, False otherwise.
		'''
		try:
			with open('blacklist.txt', 'r') as blacklist:
				for line in blacklist:
					if self.cleanedWord(line) == word:
						return True
				else:
					return False
		except IOError:
			return False

	def addWordToDict(self, word, parsedDict):
		'''
		Adds word to parsedDict if it does not already appear, otherwise increases key by 1.
		'''

		if word in parsedDict:
			parsedDict[word] += 1
		else:
			parsedDict[word] = 1

		return parsedDict

	def dictToSortedList(self, parsedDict, reverse = True):
		'''
		Converts a dict to a sorted List.
		reverse determines whether it is ascending or descending.
		'''

		sortedList = sorted(parsedDict.iteritems(), key = operator.itemgetter(1), reverse = reverse)

		return sortedList

	def getParsedList(self, minimumCount = False, blacklist = False):
		'''
		Returns list of parsed words. Can apply a blacklist, a minimum requirement on a word's count, or just
		return the entire unfiltered list.
		'''

		if not minimumCount:
			minimumCount = 0

		filteredList = self.parsedList

		if blacklist:
			filteredList = self.applyBlacklist(filteredList)
		
		filteredList = self.applyMinimumCount(filteredList, minimumCount)

		return filteredList

	def applyBlacklist(self, listToClean):
		'''
		Returns listToClean, sans words in blacklist.txt
		'''
		
		newList = []

		for word in listToClean:
			if not self.inBlacklist(word[0]):
				newList.append(word)

		return newList

	def applyMinimumCount(self, listToClean, minimumCount):
		'''
		Returns listToClean, sans any words with a count under minimumCount.
		'''

		newList = []

		for word in listToClean:
			if word[1] >= minimumCount:
				newList.append(word)

		return newList

	def logWordCountList(self, wordList):
		'''
		Outputs the words and their counts from the file being parsed to a .txt file.
		File is put in a directory called wordCountLogs that is created if it doesn't already exist.
		'''

		logFileName = self.createLogFileName()

		if self.verbose:
			print "Creating ", logFileName, " with word count list."

		try:
			os.remove(logFileName)
			if self.verbose:
				print logFileName, " already exists.\n Deleting ", logFileName
		except OSError:
			pass

		if not os.path.exists('wordCountLogs'):
			os.makedirs('wordCountLogs')

		try:
			with open(logFileName, 'wr') as logFile:
				for word, count in wordList:
					logFile.write(word + " " + str(count) + '\n')
		except IOError:
			print "Failed to create word count log."

	def createLogFileName(self):
		'''
		Creates log file name for use with logList()
		'''
		
		fileNamePlusExtension = os.path.basename(self.documentName)
		fileName, fileExtension = os.path.splitext(fileNamePlusExtension)

		logNameExtension = 'Parsed.txt'

		logFileName = 'wordCountLogs/' + fileName + logNameExtension

		return logFileName