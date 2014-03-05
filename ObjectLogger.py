class ObjectLogger(object):

	def __init__(self, objectName):
		self.objectName = objectName

	def log(self, message):
		print "%s: %s" % (self.objectName, message)