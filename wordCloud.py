import Main
import Logger
import sys

if __name__ == '__main__':
	sys.stdout = Logger.Logger(outputToTerminal = True)
	main = Main.Main()
	main.main()