import argparse
import sys
from Parser import Parser

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "Creates a word cloud from a given text or pdf document.")

	helpMessages = {}
	helpMessages["verbose"] 			= "Produce verbose output."
	helpMessages["wordCountOut"] 		= "Outputs word count as its own txt document."
	helpMessages["blacklisting"] 		= "This turns off the blacklist and allows words from blacklist.txt to appear in the wordcloud."
	helpMessages["fileName"]			= "Name of file to be parsed into a wordcloud."

	parser.add_argument('-v', action = "store_true",	dest = "verbose",		default = False, 	help = helpMessages["verbose"])
	parser.add_argument('-w', action = "store_true", 	dest = "wordCountOut", 	default = False,	help = helpMessages["wordCountOut"])
	parser.add_argument('-b', action = "store_false", 	dest = "blacklisting", 	default = True,		help = helpMessages["blacklisting"])
	parser.add_argument('fileName', help = helpMessages["fileName"])

	settings = parser.parse_args()

	minimumCount = 3

	parser = Parser(settings.fileName, settings.verbose, minimumCount)

	parsedList = parser.getParsedList(minimumCount = 3, blacklist = True)

	parser.logWordCountList(parsedList)

	for word, count in parsedList:
		exit(0)
		print word, count