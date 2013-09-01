import argparse
import logger
import sys
from Parser import Parser

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "Creates a word cloud from a given text or pdf document.")

	helpMessages = {}
	helpMessages["outputToTerminal"] 	= "Turns console output on."
	helpMessages["wordCountOut"] 		= "Outputs word count as its own txt document."
	helpMessages["logFileLogging"] 		= "Turns logging off."
	helpMessages["fileName"]			= "For inputting name of the file to be parsed."

	parser.add_argument('-t', action = "store_true",	dest = "outputToTerminal",	default = False, 	help = helpMessages["outputToTerminal"])
	parser.add_argument('-w', action = "store_false", 	dest = "wordCountOut", 		default = False,	help = helpMessages["wordCountOut"])
	parser.add_argument('-l', action = "store_false", 	dest = "logFileLogging",	default = True, 	help = helpMessages["logFileLogging"])
	parser.add_argument('fileName', help = helpMessages["fileName"])

	settings = parser.parse_args()

	sys.stdout = logger.logger(settings.outputToTerminal, settings.logFileLogging)

	parsedWords = Parser.parseTextDocument(settings.fileName)

	for word in parsedWords:
		print word[0], word[1]