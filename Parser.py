import operator

class Parser(object):

	@staticmethod
	def parseTextDocument(documentName):
		parsedDocument = {}

		with open(documentName,'r') as f:
			for line in f:
				for word in line.split():
					if word in parsedDocument:
						parsedDocument[word] += 1
					else:
						parsedDocument[word] = 1

		sortedDict = sorted(parsedDocument.iteritems(), key=operator.itemgetter(1), reverse = True)

		return sortedDict
		