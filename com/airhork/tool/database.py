"""
Gets the id of processes
"""

import os
from xml.etree.ElementTree import XML

from html.parser import HTMLParser

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - -  %(asctime)s %(message)s', datefmt = '[%d/%b/%Y %H:%M:%S]')

import time


def generateKillSql(sfile='d:/id.txt'):
	template = 'alter system kill session %s;'
	full = []
	with open(sfile) as f:
		for line in f.readlines():
			if(len(line) > 2):
				full.append(template %(line.replace('\n', '')))

	with open('c:/output.txt','w') as w:
		w.write('\n'.join(full))
	

	

 
  
  
