import operator
import os
import sys
import time

class Parser(object):

	def __init__(self, documentName, verbose):
		self.documentName = documentName
		self.verbose = verbose

		fileName, fileExtension = os.path.splitext(documentName)

		fileExtension = fileExtension.lower()

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
		parsedDocument = {}
		with open(documentName,'r') as f:
			for line in f:
				for word in line.split():
					if word in parsedDocument:
						parsedDocument[word] += 1
					else:
						parsedDocument[word] = 1
		if self.verbose == True:
			print "Parsing complete."

		sortedDict = sorted(parsedDocument.iteritems(), key=operator.itemgetter(1), reverse = True)

		return sortedDict

	def parsePDFDocument(self, documentName):
		print "Sorry, pdf parsing isn't implemented yet."
		exit(0)

	def getParsedWords(self):
		return self.parsedWords