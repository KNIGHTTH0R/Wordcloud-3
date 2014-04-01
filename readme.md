Wordcloud Generator
===================

Takes .pdf and .txt files located in the input folder and creates wordclouds as .bmp files in the output folder.


Operation
=========

python wordcloud.py


Customization
=============

Settings/blacklist.txt contains the list of words that will be excluded from wordclouds if blacklist is set to 
true in config.ini
colourSchemes.json contains the various themes chosen from randomly during wordcloud creation. Colours are [R,G,B].

maxWords in config.ini is the maximum amount of words to appear in the wordclouds.

minimumCount is the minimum (not inclusive) amount of times a word must appear in the document to appear in a wordcloud.
If minimumCount is 0 any words that appear are candidates for appearing in the wordcloud.

Dependencies
============

python 2.7

pygame 1.91
http://pygame.org/download.shtml\

pdfminer
http://www.unixuser.org/~euske/python/pdfminer/#download