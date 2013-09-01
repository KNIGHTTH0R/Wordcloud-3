import sys

class logger(object):
	def __init__(self, outputToTerminal, logFileLogging):
		self.outputToTerminal = outputToTerminal
		self.logFileLogging = logFileLogging
		self.terminal = sys.stdout
		self.logFile = "log.txt"

	def write(self, message):
		if self.outputToTerminal:
			self.terminal.write(message)

		if self.logFileLogging:
			with open(self.logFile, "a") as output:
				output.write(message)