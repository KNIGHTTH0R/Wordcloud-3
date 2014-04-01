import glob
import Parser
import WordCloudGenerator
import os
import ObjectLogger
import sys
from ConfigParser import SafeConfigParser

class Main (object):

	def __init__(self):
		self.logger = ObjectLogger.ObjectLogger("Main")
		self.logger.log("Main created")

		if not os.path.exists("input"):
			self.logger.log("Input folder does not exist. This does not bode well.")
			self.logger.log("Input folder created")
			os.makedirs("input")

		if not os.path.exists("output"):
			self.logger.log("Output folder created")
			os.makedirs("output")

		self.parser = parser = SafeConfigParser()
		parser.read('settings/config.ini')

		self.settings = {}

		self.settings["verbose"] = bool(parser.get('Config', 'verbose'))
		self.settings["blacklisting"] = bool(parser.get('Config', 'blacklisting'))
		self.settings["maxWords"] = int(parser.get('Config', 'maxWords'))
		self.settings["minimumCount"] = int(parser.get('Config', 'minimumCount'))

		self.blacklist = self.loadBlacklist()

	def main(self):
		self.logger.log("Loading list of documents in input folder")
		self.listOfFilepaths = self.getFileNameList()

		if len(self.listOfFilepaths) == 0:
			self.logger.log("No files in input folder\n")
			exit(0)

		self.logger.log("List of filepaths loaded, %d files to process: %s" % (len(self.listOfFilepaths), self.listOfFilepaths))

		self.logger.log("Creating parser")
		parser = Parser.Parser()
		self.logger.log("Creating WordCloudGenerator")
		wordCloudGenerator = WordCloudGenerator.WordCloudGenerator()

		self.completedWordClouds = 0
		for filepath in self.listOfFilepaths:
			self.logger.log("Generating word cloud from %s" % filepath)

			self.logger.log("Sending document to parser for parsing")
			parsedDocument = parser.parseDocument(filepath)

			if not parsedDocument:
				self.logger.log("Document could not be parsed")
				self.logger.log("Moving to next document")
				continue

			self.logger.log("Applying filters to parsed document")
			parsedDocument.applyWordListFilters(minimumCount = self.settings["minimumCount"], 
												blacklist = self.blacklist, 
												maxWordsLimit = self.settings["maxWords"])

			self.logger.log("Generating filepath for wordcloud output file")
			fileName, fileExtension = os.path.splitext(os.path.basename(filepath))
			imageOutputPath = "output/" + fileName + ".bmp"

			self.logger.log("Sending parsed document to WordCloudGenerator for wordcloud generation")
			wordCloudGenerator.generateWordCloud(parsedDocument, imageOutputPath)

			self.logger.log("Finished generating wordcloud for %s" % filepath)

			self.completedWordClouds += 1

		self.logger.log("Wordcloud genereation complete.")
		self.logger.log("Documents input: %d" % len(self.listOfFilepaths))
		self.logger.log("Successful wordclouds generated: %d"% self.completedWordClouds)
		print "\n"

	def getFileNameList(self):
		return glob.glob('input/*')

	def loadBlacklist(self):
		if self.settings["blacklisting"]:
			blacklist = []
			self.logger.log("Loading blacklist")
			try:
				with open("Settings/blacklist.txt", 'r') as f:
					for line in f:
						for word in line.split():
							blacklist.append(word)
			except IOError:
				self.logger.log("Error loading blacklist")
		else:
			blacklist = False

		return blacklist