"""
The utility tool to handle SVN related
"""

import os
from xml.etree.ElementTree import XML
from com.airhork.tool.command import Command

from html.parser import HTMLParser
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - -  %(asctime)s %(message)s', datefmt = '[%d/%b/%Y %H:%M:%S]')

def getLastCommiter(file): 
	cmd = 'svn log --xml -l 1 %s'
	output = os.popen(cmd % file)
	content = output.read()
	output.close()
	root = XML(content)
	for item in root.findall('logentry'):
		return item.find('author').text, item.find('msg').text, item.find('date').text

def getCheckout(path, project):
	svn = SVN()
	svn.appendParameter('co').appendParameter(path).appendParameter(project)
	return svn

def checkout(path, project):
	svn = getCheckout(path, project)
	svn.execute()


class SVN(Command):
	def __init__(self, *parameter, command=None, directfile=None, append=False, logging=True):
		super().__init__('svn', *parameter, command=command, directfile=directfile, append=append, logging=logging)

  
		

  


