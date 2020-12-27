"""
The utility tool to schedule tasks 
"""

import os
from com.airhork.tool.command import Command

import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - -  %(asctime)s %(message)s', datefmt = '[%d/%b/%Y %H:%M:%S]')


class SCHEDULE(Command):
	def __init__(self, *parameter, command=None, directfile=None, append=False, logging=True):
		super().__init__('schtasks', *parameter, command=command, directfile=directfile, append=append, logging=logging)
	
	def taskName(self, taskName):
		self.parameter.append('/tn')
		self.parameter.append(taskName)
		return self

	def system(self):
		self.parameter.append('/ru')
		self.parameter.append('system')
		return self


	def create(self):
		self.parameter.append('/create')
		return self

	def delete(self):
		self.parameter.append('/delete')
		return self

	def withDay(self, sd):
		self.parameter.append('/sd')
		self.parameter.append(sd)
		return self

	def withTime(self, st):
		self.parameter.append('/st')
		self.parameter.append(st)
		return self

	def withCommand(self, command):
		self.parameter.append('/tr')
		self.parameter.append(command)
		return self

	def force(self):
		self.parameter.append('/f')
		return self

	def once(self):
		self.parameter.append('/sc once')
		return self



	
def deleteCommand():
	delete = SCHEDULE()
	delete.delete()
	return delete

def delete(taskName):
	delete = deleteCommand()
	delete.taskName(taskName)
	delete.force()
	delete.execute()

def scheImmediate(taskName, command):
	sche = SCHEDULE()
	sche.create().once().system()
	sche.withDay(getSD())
	sche.withTime(getNextST())
	sche.taskName(taskName).withCommand(command)
	sche.execute()


  
		

strdate = lambda x : '0' + str(x) if x < 10 else str(x)

def getSD():
	from datetime import datetime
	current = datetime.now()
	return '%s/%s/%s' %(strdate(current.month), strdate(current.day), strdate(current.year))

	
def getNextST():
	from datetime import datetime
	current = datetime.now()
	hour = current.hour if current.minute <= 57 else current.hour + 1
	return '%s:%s:%s' %(strdate(hour), strdate((current.minute + 2) % 60), '00')

	


