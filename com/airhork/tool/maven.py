"""
"""


import os,  re
import os.path as path
from configparser import ConfigParser
from com.airhork.tool import util
import shutil



ConfigParser.OPTCRE = re.compile(r'(?P<option>[^=\s][^=]*)\s*(?P<vi>[=])\s*(?P<value>.*)$')
COMMON_CONFIG = ConfigParser()
COMMON_CONFIG.read(os.path.splitext(__file__)[0] + '.ini')

DEV_PATH = COMMON_CONFIG.get('maven', 'dev_path', fallback='d:/dev')
BRANCH = COMMON_CONFIG.get('maven', 'branch', fallback='uct-msd')
UCT_MSD_UI_TEST= COMMON_CONFIG.get('maven', 'uct-msd-ui-test', fallback='uct-msd-ui-test')
BRANCH_DEV = COMMON_CONFIG.get('maven', 'branch_dev', fallback='uct-msd-dev')
BRANCH_DEV_RC = COMMON_CONFIG.get('maven', 'branch_dev_rc', fallback='asb-rc')
UPDATE_BUILD_FILE = 'updateBuild.bat'
SNAPSHOT_UPDATE_BUILD_FILE = 'updateBuildFull.bat'
TINY_UPDATE_BUILD_FILE = 'tinyUpdateBuild.bat'


JBOSS_LOG4J_LOCATION= COMMON_CONFIG.get('maven', 'jboss_log_path', fallback='d:/dev/jboss-log4j.xml')
DEFAULT_JBOSS_LOG4J_LOCATION = 'server/jboss/server/production/conf/jboss-log4j.xml'
COMMAND_FILE = path.join(path.dirname(__file__),UPDATE_BUILD_FILE)
SNAPSHOT_COMMAND_FILE = path.join(path.dirname(__file__),SNAPSHOT_UPDATE_BUILD_FILE)
TINY_COMMAND_FILE = path.join(path.dirname(__file__),TINY_UPDATE_BUILD_FILE)
HTML_TEMPLATE = path.join(path.dirname(__file__), 'mail.template.html')

JENKINS_UCT_MSD_URL=COMMON_CONFIG.get('Jenkins', 'uct-msd')

###
### GLOBAL VARIABLES start
###
BRANCH_PATH = path.join(DEV_PATH, BRANCH)
UCT_MSD_UI_TEST_PATH = path.join(DEV_PATH, UCT_MSD_UI_TEST)
JBOSS_INSTALL_PATH = path.join(DEV_PATH , 'agility-install')
KEY_STORE='keystore.jks'
JBOSS_JPS= path.join(JBOSS_INSTALL_PATH, 'common/security/' + KEY_STORE)
JBOSS_ISHARE= path.join(JBOSS_INSTALL_PATH, 'server/iaservices/' + KEY_STORE) 
BRANCH_DEV_PATH = path.join(DEV_PATH , BRANCH_DEV)
TARGET_PLATFORM=path.join(DEV_PATH, 'target-platform')
###
### GLOBAL VARIABLES end
###

# build this projects seperatellgy
standalone = ['jris','ris-server']

enable_echo = util.stringToBoolean(COMMON_CONFIG.get('command', 'echosupport'))
enable_pause = util.stringToBoolean(COMMON_CONFIG.get('command', 'pausesupport'))

commandMap = {}

for sl in standalone:
	commandMap[sl] =  COMMON_CONFIG.get('command', sl)

branch=''
killeclipse=True
jenkinMode=False

branchfilter = (lambda x : '%s-%s' % (x, branch) if len(branch) > 0 else x)
plainBranch= (lambda x : '-%s' %branch if len(branch) > 0 else 'doesnt')
host=''

import re
folderPattern = re.compile('.*v(\d{8}).*')
folderPattern2 = re.compile('.*v(\d{8}_\d{4})')

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - -  %(asctime)s %(message)s', datefmt = '[%d/%b/%Y %H:%M:%S]')

from com.airhork.tool.util import timer


def main():
	import sys
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("-b","--branch",default="")
	parser.add_option("-a","--location",default="d:\dev")
	parser.add_option("-p","--notkilleclipse",action="store_true", default=False)
	parser.add_option("-j","--jenkinMode",action="store_true", default=False)
	parser.add_option("-s","--snapshot",action="store_true", default=False)
	parser.add_option("-l","--host", default="localhost")
	(options, args) = parser.parse_args()

	updateVaribles(options)

	if len(sys.argv) < 2:
		print('the size is ',len(sys.argv))
		return None
	logging.info(sys.argv)
	para = sys.argv[1]
	if para == 'build':
		_updateAndRun()
	elif para == 'tinybuild':
		_tinyUpdateAndRun()
	elif para == 'mate':
		_materialize()
	elif para == 'runshare':
		_runShareJboss()
	elif para == 'run':
		_runJboss()
	elif para == 'create':
		_createTargetPlatform()
	elif para == 'slowfull':
		_slowFull()
	elif para == 'cleanup':
		cleanup()
	elif para == 'cleanmaven':
		cleanMaven()
	elif para == 'test':
		_test()
	elif para == 'replace':
		_replace()


def updateVaribles(options):
	global	branch,killeclipse,JBOSS_INSTALL_PATH,DEV_PATH,BRANCH_DEV_PATH,BRANCH_PATH,TARGET_PLATFORM,jenkinMode,snapshot,location 
	global host
	branch = options.branch
	location = options.location
	killeclipse = not options.notkilleclipse
	jenkinMode = options.jenkinMode
	snapshot = options.snapshot
	host = options.host
	if location != None:
		DEV_PATH = location
		BRANCH_PATH = path.join(DEV_PATH, BRANCH)
		UCT_MSD_UI_TEST_PATH = path.join(DEV_PATH, UCT_MSD_UI_TEST)
		JBOSS_INSTALL_PATH = path.join(DEV_PATH , 'agility-install')
		JBOSS_JPS= path.join(JBOSS_INSTALL_PATH, 'common/security/' + KEY_STORE)
		JBOSS_ISHARE= path.join(JBOSS_INSTALL_PATH, 'server/iaservices/' + KEY_STORE) 
		BRANCH_DEV_PATH = path.join(DEV_PATH , BRANCH_DEV)
		TARGET_PLATFORM = path.join(DEV_PATH, 'target-platform')
		logging.info('using new location %s, and branch location %s' % (DEV_PATH, BRANCH_PATH))

	        
	if branch == 'rc':
		JBOSS_INSTALL_PATH = JBOSS_INSTALL_PATH + '-rc'
		BRANCH_DEV_PATH=DEV_PATH + '/' + BRANCH_DEV_RC
		TARGET_PLATFORM=TARGET_PLATFORM  + '-rc'
		logging.info('using jboss location %s, and branch location %s' % (JBOSS_INSTALL_PATH, BRANCH_DEV_PATH))

	


def _test():
	import sys
	logging.info('inside')
	print('inside')
	print(killeclipse)
	print('snapshot %s' %snapshot)
	print(path)
	print(path.join(path.dirname(__file__) , 'updateBuild.bat'))
	setasb =  (lambda x : '-rc' if x == 'rc' else '')
	asbvalue = (lambda x : BRANCH_DEV_RC if x == 'rc' else BRANCH_DEV)
	print(asbvalue(branch))
	os.putenv('ASB',asbvalue(branch))
	print(os.getenv('ASB'))
	for project in map(branchfilter,standalone):
		print(project)		
	cleanupBillOfMaterials()
	
def buildCommand(commandStr, project):  
	cmd = None
	from com.airhork.tool import command
	if enable_echo :
		cmd = command.Command('echo', project)
	rcmd = command.Command(commandStr)
	cmd = rcmd if cmd is None else cmd.join(rcmd)
	if enable_pause :
		cmd = cmd.join(command.Command('pause'))
	return cmd

def _slowFull():
	util.logCurrenttime()	
	for project in standalone:
		pname = _getName(project,plainBranch(project))
		startAlone(project,commandMap.get(pname))
	_updateAndRun()
	_createTargetPlatform()
	util.logCurrenttime()	
	cleanupBillOfMaterials()

def _getName(name,plainBranch):
	bindex = lambda name,plainBranch : name.rfind(plainBranch) if name.rfind(plainBranch) > 0 else len(name) 
	return name[0:bindex(name,plainBranch)]
	


def testCommand():
	from com.airhork.tool.command import Command
	logging.info('we are going to check the change status of the metainfo')
	os.chdir(DEV_PATH)
	from com.airhork.tool.svn import SVN
	from com.airhork.tool.command import Command
	directoutput = path.join(DEV_PATH, 'up.txt')
	svn = SVN('up', directfile=directoutput).appendParameter(BRANCH_PATH)
	echo = Command('echo', directfile=directoutput, append=True).appendParameter(BRANCH_PATH)
	svn.execute()
	echo.execute()
	svn = SVN('up', directfile=directoutput,append=True).appendParameter(UCT_MSD_UI_TEST_PATH)
	svn.execute()
	echo.execute()
	

def metainfoCheck():
	from com.airhork.tool.command import Command
	logging.info('we are going to check the change status of the metainfo')
	os.chdir(DEV_PATH)
	from com.airhork.tool.svn import SVN
	from com.airhork.tool.command import Command
	directoutput = path.join(DEV_PATH, 'up.txt')
	svn = SVN('up', directfile=directoutput).appendParameter(BRANCH_PATH)
	echo = Command('echo',directfile=directoutput,append=True).appendParameter('---------------')
	svn.execute()
	echo.execute()
	svn = SVN('up', directfile=directoutput,append=True).appendParameter(UCT_MSD_UI_TEST_PATH)
	svn.execute()
	echo.execute()

	ff = open(path.join(DEV_PATH, 'up.txt'))
	mlines = []
	for line in ff.readlines():
		if 'MANIFEST.MF' in line:
			mlines.append(line)

	ff.close()
	if len(mlines) == 0:
		return

	try:
		os.remove(path.join(DEV_PATH,'log.txt'))
	except WindowsError:
		pass
	for line in mlines:
		metafile = line[5:].replace('\n','')
		logging.debug('we are going to check the diff of %s' %metafile)
		from com.airhork.tool import svn
		(author,msg,date) = svn.getLastCommiter(metafile)
		logfile = path.join(DEV_PATH, 'log.txt')
		echo = Command('echo','log -- ',directfile=logfile, append=True).appendParameter('%s:%s:%s' %(author, msg, date ))
		echo.execute()
		svn = SVN('diff', directfile=logfile, append=True).appendParameter('-r').appendParameter('PREV:HEAD').appendParameter(metafile)
		svn.execute()
	
	ff = open(path.join(DEV_PATH, 'log.txt'))
	from com.airhork.tool import util
	para = {'#content#':'someone has changed metainfo','#detail#':ff.read().replace('\n','<br>')}
	ff.close()
	logging.debug(HTML_TEMPLATE)
	mailcontent = util.replace(HTML_TEMPLATE, para)
	from com.airhork.tool import mail
	mail.textMail(mailcontent)


	

	

def startAlone(project, command):

	logging.info('start build %s' %project)
	global COMMON_CONFIG
	fpath = path.join(DEV_PATH, project)
	if not path.exists(fpath):
		svnaddress = COMMON_CONFIG.get('svn', project) + '/' + branch
		os.chdir(DEV_PATH)
		from com.airhork.tool import svn
		svn.checkout(svnaddress, project)

	os.chdir(fpath)
	cmd = buildCommand(command, project)
	cmd.startAlone()


@timer
def _updateAndRun():

	if(jenkinMode):
		from com.airhork.tool import jenkins
		jk = jenkins.Jenkins(JENKINS_UCT_MSD_URL)
		if(not jk.getLastBuildStatus()):
			import sys
			sys.exit('the build of current uct-msd is failed, force to abort')

	from com.airhork.tool import svn

	base_path = BRANCH_PATH
	logging.info('base path %s' % (base_path))
	if not path.exists(base_path):
		os.chdir(DEV_PATH)
		uctmsd_address = COMMON_CONFIG.get('svn', 'uct-msd') + '/' + branch
		svn.checkout(uctmsd_address, 'uct-msd')

	if not path.exists(BRANCH_DEV_PATH):
		os.chdir(DEV_PATH)
		asb_address = COMMON_CONFIG.get('svn', 'asb') + '/' + branch
		svn.checkout(asb_address, 'asb')

	if not path.exists(path.join(DEV_PATH, 'asb-uct-msd-solution-ui-tests')):
		os.chdir(DEV_PATH)
		uct_msd_tests = COMMON_CONFIG.get('svn', 'uct-msd-tests') + '/' + branch
		svn.checkout(uct_msd_tests, 'asb-uct-msd-solution-ui-tests')

	os.chdir(base_path)
	asbvalue = (lambda x : BRANCH_DEV_RC if x == 'rc' else BRANCH_DEV)
	os.putenv('ASB',asbvalue(branch))

	if(not snapshot):
		updatefilepath = path.join(base_path, UPDATE_BUILD_FILE)
		shutil.copyfile(COMMAND_FILE, updatefilepath)
		result = os.system(UPDATE_BUILD_FILE)
	else:
		updatefilepath = path.join(base_path, SNAPSHOT_UPDATE_BUILD_FILE)
		shutil.copyfile(SNAPSHOT_COMMAND_FILE, updatefilepath)
		result = os.system(SNAPSHOT_UPDATE_BUILD_FILE)
		
	util.logCurrenttime('update and  build ')	

@timer
def _tinyUpdateAndRun():
	base_path = branchfilter(BRANCH_PATH)
	os.chdir(base_path)
	asbvalue = (lambda x : BRANCH_DEV_RC if x == 'rc' else BRANCH_DEV)
	os.putenv('ASB',asbvalue(branch))

	updatefilepath = path.join(base_path, TINY_UPDATE_BUILD_FILE)
	shutil.copyfile(TINY_COMMAND_FILE, updatefilepath)
		
	result = os.system(TINY_UPDATE_BUILD_FILE)
	util.logCurrenttime('update and  build ')	


@timer
def _createTargetPlatform():
	if killeclipse:
		'''kill eclipse first'''
		processId = util.getEclipse()
		if len(processId) > 0:
			util.killProcess(processId)
	os.chdir(BRANCH_DEV_PATH)
	os.system('create-target-platform-34.bat')

	

@timer
def _materialize():
	''' kill jboss first '''
	from com.airhork.tool import jboss
	jboss.killRunningJboss()
	jboss.killRunningShareJboss()

	'''rename the agility-install folder if necessary '''
	from datetime import datetime
	now = datetime.now()


	if os.path.exists(JBOSS_INSTALL_PATH):
		try:
			os.rename(JBOSS_INSTALL_PATH,JBOSS_INSTALL_PATH + '-' + now.strftime('%d-%m-%y-%H-%M'))	
		except OSError :
			logging.warn('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
			input("Cannot rename the agilty-install")

	os.chdir(BRANCH_DEV_PATH)
	os.system('materialize-install.bat')
	shutil.copyfile(JBOSS_JPS, JBOSS_ISHARE)




def _runJboss():
	from com.airhork.tool import jboss
	if(jenkinMode):
		jboss.scheJbossImme(JBOSS_INSTALL_PATH)
		jboss.waitUntilRunning(host)
	else:
		jboss.runJboss(JBOSS_INSTALL_PATH)

def _runShareJboss():
	from com.airhork.tool import jboss
	jboss.runShareJboss(JBOSS_INSTALL_PATH)

def _replace():
	shutil.copyfile(JBOSS_LOG4J_LOCATION, path.join(JBOSS_INSTALL_PATH ,DEFAULT_JBOSS_LOG4J_LOCATION))



	
def findDifference(left='d:/dev/ris-dev/pom.xml', right='d:/dev/uct-msd-dev/pom.xml'):
	from xml.etree.ElementTree import ElementTree
	ns = '{http://maven.apache.org/POM/4.0.0}'
	et = ElementTree()
	left = et.parse(left)
	leftVersions = {}
	for element in left.find(ns + 'properties').iter():
		leftVersions[element.tag[len(ns):]] = element.text	
	et = ElementTree()
	right = et.parse(right)

	changed = {}

	elements = [element for element in right.find(ns + 'properties').iter() if element.tag[len(ns):] != 'properties']
	
	for element in elements:
		key = element.tag[len(ns):]
		if key in leftVersions and leftVersions[key] != element.text:
			changed[key] = [leftVersions[key] ,element.text]
	
	for k,v in changed.items():
		print('%s, %s, %s' %(k, v[0], v[1]))
	
	return changed

def localCleanup():
	localPath = 'c:\\maven\\maven-repo\\com\\agfa'
	cleanMaven(localPath, monthCondition)


def monthCondition(timevalue, monthDuration=6):
	year = timevalue[0:4]
	month = timevalue[4:6]
	from datetime import datetime
	nowdate = datetime.now()
	currentValue = nowdate.year * 12 + nowdate.month
	actuaValue = int(year) * 12 + int(month)

	return True if currentValue - actuaValue >= monthDuration else False



def defaultCondition(timevalue):
	year = timevalue[0:4]
	month = timevalue[4:6]
	day = timevalue[6:8]
	return True if int(year) < 2012 else False

	

@timer
def cleanMaven(rootdir = 'd:\\maven\\maven-repo\\com\\agfa',condition=defaultCondition):
	import os
	import re
	namepattern = re.compile('\.\d+')
	for diritem in filter(lambda x : namepattern.search(x) == None , os.listdir(rootdir)): 
		np = path.join(rootdir, diritem)
		if path.isdir(np):
			_legacy_cleanup(np, condition)
			cleanMaven(np,condition)


def _legacy_cleanup(dirpath, condition=defaultCondition):
	import os
	logging.debug(dirpath)
	for legacy in filter(lambda x : folderPattern.search(x) != None  ,os.listdir(dirpath)):
		pvalue = folderPattern.search(legacy).group(1)	
		logging.info('the current pvalue %s', pvalue)
		
		if condition(pvalue):
			from com.airhork.tool import util
			util.removeFolder(path.join(dirpath, legacy))
	

datevalue = lambda x,y : int(x) * 30 + int(y)

@timer
def cleanup(suffix='agility-install-'):
	import os
	from datetime import datetime
	os.chdir(DEV_PATH)
	for to_be_deleted in filter(lambda x : suffix in x, os.listdir(DEV_PATH)):
		strdate = to_be_deleted[-14:].split('-')
		nowdate = datetime.now()
		today = nowdate.month * 31 + nowdate.day
		try:
			if int(strdate[2]) + 2000 < int(nowdate.year) or datevalue(strdate[1], strdate[0]) < datevalue(nowdate.month, nowdate.day):
				from com.airhork.tool import util
				util.removeFolder(to_be_deleted)

		except IndexError:
			print('index error with %s, just ignore' %to_be_deleted)
			#we don't care the index error
			pass

@timer
def cleanupBillOfMaterials(suffix='billOfMaterials-'):
	cleanFileBeforeToday(TARGET_PLATFORM,suffix)
	cleanFileBeforeToday(JBOSS_INSTALL_PATH,suffix)

@timer
def cleanFileBeforeToday(path, suffix):
	import os
	from datetime import datetime
	nowdate = datetime.now()
	os.chdir(path)
	for to_be_deleted in filter(lambda x : suffix in x, os.listdir(path)):
		bdate = to_be_deleted.split('-')
		if len(bdate) > 0:
			year = bdate[1][0:4]
			month = bdate[1][4:6]
			day = bdate[1][6:8]
			if int(year) < nowdate.year or datevalue(month, day) < datevalue(nowdate.month, nowdate.day):
				from com.airhork.tool import util
				util.removeFileUnderCWD(to_be_deleted)
			



		

def syncVersion(right='d:/dev/uct-msd-dev/pom.xml',output='d:/test.xml'):
	from xml.etree.ElementTree import ElementTree
	ns = '{http://maven.apache.org/POM/4.0.0}'
	et = ElementTree()
	left = et.parse(right)

	changed = findDifference()

	for k, v in changed.items():
		element = left.find(ns + 'properties/' + ns + k)
		if element is not None and 'SNAPSHOT' not in v[1] and 'SNAPSHOT' not in v[0]:
			print('the value for %s has been set to %s' %(k,v[0]))
			element.text = v[0] 
	
	from xml.etree import ElementTree as pet
	pet.register_namespace('','http://maven.apache.org/POM/4.0.0')
	et.write(output)

if __name__ == "__main__":
    main()

