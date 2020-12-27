"""
The utility tool to handle SVN related
"""

import os
from xml.etree.ElementTree import XML

from html.parser import HTMLParser
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - -  %(asctime)s %(message)s', datefmt = '[%d/%b/%Y %H:%M:%S]')

def test(*name):
	print(len(name))

class Command:
	def __init__(self, task, *parameter, command=None, directfile=None, append=False, logging=True):
		self.task = task
		self.command = command
		self.directfile = directfile
		self.append = append
		self.parameter = list(parameter)
		self.logging=logging
	

	def execute(self):
		cmd = self.toString()
		if self.logging:
			logging.info(cmd)

		os.system(cmd)
	
	def startAlone(self):
		cmd = 'start cmd /c "%s"' %(self.toString())
		if self.logging:
			logging.info(cmd)
		os.system(cmd)
	
	
	def appendParameter(self,parameter):
		self.parameter.append(parameter)
		return self
			

	def join(self,command):
		return AndCommand(self, command)	

	def link(self, command):
		return LinkCommand(self, command)

	
	def toString(self):
		cmd = '%s %s %s %s'
		append = '>> ' if self.append else ' > '
		directfile = '' if self.directfile is None else append + self.directfile
		cmd2 = '' if self.command is None else '|' + self.command.toString()
		print(self.task)
		print(self.parameter)
		return cmd %(self.task, ' '.join(self.parameter),directfile, cmd2)


		
class AndCommand(Command):
	def __init__(self, command1, command2,*parameter, command=None, directfile=None, append=False, logging=True):
		self.command1 = command1
		self.command2 = command2
		super().__init__('',*parameter,logging=logging)
	
	def toString(self):
		cmd = '%s && %s'
		return cmd % (self.command1.toString(), self.command2.toString())


class LinkCommand(Command):
	def __init__(self, command1, command2,*parameter, command=None, directfile=None, append=False, logging=True):
		self.command1 = command1
		self.command2 = command2
		super().__init__('',*parameter,logging=logging)
	
	def toString(self):
		cmd = '%s %s'
		return cmd % (self.command1.toString(), self.command2.toString())


  
  
