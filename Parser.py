import ParsedDocument
import ObjectLogger
import os
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

class Parser(object):

	def __init__(self):
		self.logger = ObjectLogger.ObjectLogger("Parser")
		self.logger.log("Parser created.")

	def parseDocument(self, documentName):
		self.documentName = documentName

		# Pull out the file extension and lower it to check what sort of file we've been given.
		fileName, fileExtension = os.path.splitext(documentName)
		fileExtension = fileExtension.lower()

		self.logger.log("Received %s for parsing" % documentName)

		# Send the file to different functions based upon which file we have.
		if(fileExtension == '.txt'):
			self.ParsedDocument = self.parseTextDocument(documentName)
		elif(fileExtension == '.pdf'):
			self.ParsedDocument = self.parsePDFDocument(documentName)
		else:
			self.ParsedDocument = self.unrecognisedFileFormat(documentName)

		return self.ParsedDocument

	def unrecognisedFileFormat(self, documentName):
		self.logger.log("Filetype not recognised.")
		return False

	def parseTextDocument(self, documentName):
		self.logger.log(".txt mode")

		parsedDocument = ParsedDocument.ParsedDocument()

		# Pull out each word and add it to the appropriate dicts
		try:
			with open(documentName, 'r') as f:
				for line in f:
					for word in line.split():
						cleanedWord = self.cleanWord(word)

						parsedDocument.addWord(cleanedWord)

		except IOError:
			self.logger.log("Error, %s not found." % documentName)
			return False

		parsedDocument.sortList()

		return parsedDocument

	def parsePDFDocument(self, documentName):
		self.logger.log(".pdf mode")

		tempFilepath = "tmp.txt"

		try:
			# PDFMiner code adapted from several online sources,
			# as well as official documentation.
			# Links now unavailable.
			manager = PDFResourceManager()
			retstr = StringIO()
			textConverter = TextConverter(	manager, 
											retstr, 
											codec = 'utf-8', 
											laparams = LAParams())

			document = file(documentName, 'rb')
			interpreter = PDFPageInterpreter(manager, textConverter)
			pagenums = set()
			pages = PDFPage.get_pages(	document, 
										pagenums, 
										maxpages = 0, 
										password = '', 
										caching = True, 
										check_extractable = True)

			for page in pages:
			    interpreter.process_page(page)

			document.close()
			textConverter.close()
			pdfText = retstr.getvalue()
			retstr.close()

			# End of PDFMiner code

			with open(tempFilepath, "w") as tmp:
				tmp.write(pdfText)

			parsedDocument = self.parseTextDocument(tempFilepath)

			os.remove(tempFilepath)

			return parsedDocument

		except:
			try:
				os.remove(tempFilepath)
			except OSError:
				pass
			return False

	def cleanWord(self, word):
		cleanedWord = word.lower()

		cleanedWord = cleanedWord.rstrip()

		cleanedWord = re.sub(r'\W+', '', cleanedWord)

		return cleanedWord