Wordcloud
=========

A program for creating word clouds from .txt and .pdf documents.

Usage
=====

python wordCloud.py [-h] [-v] [-w] [-b] fileName

positional arguments:
  fileName    Name of file to be parsed into a wordcloud.

optional arguments:
  -h, --help  show help message and exit
  -v          Produce verbose output.
  -w          Outputs word count as its own .txt document. Output stored in wordCountLogs directory.
  -b          This turns off the blacklist and allows words from blacklist.txt to appear in the wordcloud.
