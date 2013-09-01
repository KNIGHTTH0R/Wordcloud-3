import argparse
import logger
import sys
from Parser import Parser

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "Creates a word cloud from a given text or pdf document.")

	helpMessages = {}
	helpMessages["verbose"] 			= "Produce verbose output."
	helpMessages["wordCountOut"] 		= "Outputs word count as its own txt document."
	helpMessages["fileName"]			= "For inputting name of the file to be parsed."

	parser.add_argument('-v', action = "store_true",	dest = "verbose",	default = False, 	help = helpMessages["verbose"])
	parser.add_argument('-w', action = "store_false", 	dest = "wordCountOut", 		default = False,	help = helpMessages["wordCountOut"])
	parser.add_argument('fileName', help = helpMessages["fileName"])

	settings = parser.parse_args()

	parser = Parser(settings.fileName, settings.verbose)

	parsedWords = parser.getParsedWords()