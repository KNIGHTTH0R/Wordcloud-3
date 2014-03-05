import ObjectLogger
import operator


class ParsedDocument(object):

	def __init__(self):
		self.logger = ObjectLogger.ObjectLogger("ParsedDocument")
		self.logger.log("ParsedDocument created")
		self.wordDict = {}

		self.wordList = []

	# wordList/Dict generation functions

	def addWord(self, word):
		if word in self.wordDict:
			self.wordDict[word] += 1
		else:
			self.wordDict[word] = 1

		self.refreshWordList()

	def refreshWordList(self):
		self.wordList = sorted(self.wordDict.iteritems(), key = operator.itemgetter(1), reverse = True)

	def removeWordFromWordList(self, word):
		self.logger.log("Removing %s from self.wordList" % word[0])
		while word in self.wordList:
			self.wordList.remove(word)


	# Filter Functions

	def applyWordListFilters(self, minimumCount = False, blacklist = False, maxWordsLimit = 0):
		self.logger.log("Applying filters to parsed document")
		if minimumCount:
			self.logger.log("Applying minimum count requirement for words to appear in list: %d" % minimumCount)
			self.applyMinimumCountFilter(minimumCount)

		if blacklist:
			self.logger.log("Applying blacklist to wordList")
			self.applyBlacklist(blacklist)

		if maxWordsLimit:
			self.logger.log("Applying limit on words that can appear in wordList")
			self.applyMaxWordsLimit(maxWordsLimit)

	def removeWordListFilters(self):
		self.logger.log("Removing filters from wordList")
		self.refreshWordList()

	def applyBlacklist(self, blacklist):
		for blackListedWord in blacklist:
			for word in self.wordList:
				if word[0] == blackListedWord:
					self.removeWordFromWordList(word)

	def applyMinimumCountFilter(self, minimumCount):
		for word in self.wordList:
			if word[1] < minimumCount:
				self.removeWordFromWordList(word)

	def applyMaxWordsLimit(self, maxWordsLimit):
		self.wordList = self.wordList[:maxWordsLimit]