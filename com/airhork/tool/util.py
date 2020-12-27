"""
Gets the id of processes
"""

import os
from xml.etree.ElementTree import XML

from html.parser import HTMLParser

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - -  %(asctime)s %(message)s', datefmt = '[%d/%b/%Y %H:%M:%S]')

import time


def db():
	o = open('d:\\b.txt','w')
	t = ''
	with open('d:\\a.txt') as f:
		for line in f.readlines():
			if len(line) > 1:
				t += "alter database rename file '%s' to '%s'; \n" %(line.replace('\n',''), line.replace('\n',''))

	o.write(t)
	o.close()



def timer(func):
	def wrapper(*args, **kwargs):
		current = time.time()
		result = func(*args, **kwargs)
		logging.info('the during of the %s is %f' %(func.__name__, time.time() - current))
		return result
	return wrapper



def replace(ofile, para={}):
	with open(ofile) as f:
		content = f.read()
	for key in para.keys():
		content = content.replace(key, para[key])
	return content


def _periodic(scheduler, interval, action, actionargs=()):
	scheduler.enter(interval, 1, _periodic, (scheduler, interval, action, actionargs))
	action(*actionargs)

def repeating_sche(interval, action, actionargs=()):
	import time
	from sched import scheduler
	sch = scheduler(time.time, time.sleep)
	_periodic(sch, interval, action, actionargs)
	sch.run()

def logCurrenttime(info=''):
	from datetime import datetime as dt
	if info == '':
		print('Current time is %s' % (dt.now().strftime('%m:%d_%H:%M:%S')))
	else:
		print('Current time for the operation %s is %s' % (info, dt.now().strftime('%m:%d_%H:%M:%S')))



def stringToBoolean(value):
	return (value.lower() == 'true' and True) or False


class Ed2kParser(HTMLParser):
	links = []
	
	def __init__(self):
		super(Ed2kParser,self).__init__()	
		print('clear the links')
		self.links=[]

	def handle_starttag(self, tag, attrs):
		pass
	def handle_startendtag(self,tag,attrs):
		attrs = dict(attrs)
		if tag == 'input':
			if attrs['type'] == 'button' and attrs['class'] == 'downloadButton':
				self.links.append(attrs['name'])
	def handle_endtag(self, tag):
		pass
	def handle_comment(self,data):
		pass
	def handle_decl(self,data):
		pass
	def unknown_decl(self, data):
		print('inside unknown_decl, do nothing')
	
def getLink():
	url = input("input url \n")
	return getLinkByURL(url)


def removeFolder(path):
	from com.airhork.tool import command
	cmd = command.Command('rd')
	cmd.appendParameter('/s').appendParameter('/q').appendParameter(path)
	cmd.execute()

def removeFileUnderCWD(filename):
	from com.airhork.tool import command
	cmd = command.Command('del')
	cmd.appendParameter('/F').appendParameter(filename)
	cmd.execute()






def startEclipse():
	import os
	os.chdir('d:/dev/eclipse/')
	os.system('start eclipse.exe -refresh')
		
def getLinkByURL(url):
	from urllib import request
	with request.urlopen(url) as response:
		content = response.read().decode('utf-8')
	import re
	a = re.compile('<input[^>]*button[^>]*[^>]*ed2k[^>]*/>',re.S)
	inputs = re.findall(a,content)
	content = ''.join(inputs)
	print(content)
	parser = Ed2kParser()
	parser.feed(content)
	if len(parser.links) != 0:
		try:
			import win32clipboard as w
			w.OpenClipboard()
			w.EmptyClipboard()
			w.SetClipboardText(parser.links[0])
			w.CloseClipboard()
		except ImportError:
			cmd = 'echo "%s" | clip'
			os.system(cmd %parser.links[0])


	return parser.links
		

def getProcess(processName):
	xmlfile = os.popen("wmic.exe process list /format:rawxml.xsl")
	xmlcontent = ''
	for line in xmlfile.readlines():
		xmlcontent += line

	root = XML(xmlcontent)

	for instance in root.findall('RESULTS/CIM/INSTANCE'):
		for property in instance.findall('PROPERTY'):
			if property.attrib['NAME'] == 'CommandLine':
				value = property.find('VALUE')
				if value != None and value.text.find(processName) != -1:
					return instance

def getContentByLink(link):
	from urllib import request
	with request.urlopen(link) as response:
		content = response.read().decode('utf-8')
	return content




def getJboss():
	return getProcessByName('org.jboss.Main')

def getShareJboss():
	return getProcessByName('iaservices')

def getEclipse():
	return getProcessByName('eclipse.exe')

def getRunningCMD():
	return getProcessByName('run.bat')

def getRunningShareCMD():
	return getProcessByName('start_share.bat')
	      
	      
def getProcessByName(name):
	instance = getProcess(name)
	if instance != None:
		ptext = getPropertyValue(instance, 'Handle')
		print('the id of the process %s is %s' %(name,ptext))
		return ptext
	else:
		print("the process doesn't exist")
		return ''
	      

def killProcess(instanceId):
	command = 'taskkill /PID:' + str(instanceId) + ' /F /T'
	os.system(command)

def getPropertyValue(ele,att):
	for property in ele.findall('PROPERTY'):
		if property.attrib['NAME'] == att:
			value = property.find('VALUE')
			if value != None:
				return value.text

	return ''

 
  
  
