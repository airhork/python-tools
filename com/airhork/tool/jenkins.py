"""
Tools to help handle the content in Jenkins
"""


import os
from com.airhork.tool import util
import shutil
from xml.etree.ElementTree import XML
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - -  %(asctime)s %(message)s', datefmt = '[%d/%b/%Y %H:%M:%S]')

address='%s/api/xml'




class Jenkins():


	def __init__(self, link):
		self.link = link

	def getLastBuildStatus(self):

		while(self.isBuildInQueue()):
			import time
			logging.info('a queue is pending, wait after 180 seconds')
			time.sleep(180)


		while(self.isBuildRunning()):
			import time
			logging.info('build is ongoing, retry after 60 seconds')
			time.sleep(60)

		content = util.getContentByLink(address %(self.latestLink))
		root = XML(content)
		return 'SUCCESS' == root.find('result').text

	def isBuildInQueue(self):
		content = util.getContentByLink(address %(self.link))
		root = XML(content)

		inQueue = root.find('inQueue').text == 'true'

		return inQueue


	def isBuildRunning(self):
		content = util.getContentByLink(address %(self.getLastBuildLink()))
		root = XML(content)

		running = root.find('building').text == 'true'

		if(running):
			logging.info(' there is a building running')

		return running

	def needToWait(self):
		return isBuildInQueue() and isBuildRunning()

	def getLastBuildLink(self):

		content = util.getContentByLink(address %(self.link))
		root = XML(content)

		lastBuildNo = root.find('build/number').text
		lastBuildLink = '%s/%s' %(self.link, lastBuildNo)

		self.latestLink= lastBuildLink

		logging.info('the latest build address is %s' %(lastBuildLink))

		return lastBuildLink
			


		

		



		



