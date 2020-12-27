"""
"""


import os
from com.airhork.tool import util
import shutil

JBOSS_INSTALL_PATH='d:/dev/agility-install'
JBOSS_BIN_PATH = 'server/jboss/bin'
JBOSS_SHARE_BIN_PATH= 'server/iaservices/bin'

def main():
  os.chdir('d:/dev/agility-install/server/jboss/bin/')
  os.putenv('NOPAUSE','true')
  os.popen('start run.bat')


def runJboss(path=JBOSS_INSTALL_PATH, debug=False):
	os.putenv('NOPAUSE','true')
	os.chdir( os.path.join(path , JBOSS_BIN_PATH))
	if debug:
		os.popen('start run-debug.bat')
	else:
		os.popen('start run.bat')


def runShareJboss(path=JBOSS_INSTALL_PATH, debug=False):
	os.putenv('NOPAUSE','true')
	os.chdir( os.path.join(path , JBOSS_SHARE_BIN_PATH))
	if debug:
		os.popen('start start_share_debug.bat')
	else:
		os.popen('start start_share.bat')


def killRunningJboss():
	processId = util.getJboss()
	if len(processId) > 0:
		util.killProcess(processId)

	import time
	time.sleep(5)

	processId = util.getRunningCMD()
	if len(processId) > 0:
		util.killProcess(processId)

	time.sleep(5)

	
def killRunningShareJboss():
	import time
	time.sleep(5)

	processId = util.getShareJboss()
	if len(processId) > 0:
		util.killProcess(processId)

	processId = util.getRunningShareCMD()
	if len(processId) > 0:
		util.killProcess(processId)

	time.sleep(5)




	
def scheJbossImme(path=JBOSS_INSTALL_PATH):
	os.putenv('NOPAUSE','true')
	binpath = os.path.join(path , JBOSS_BIN_PATH)
	command = os.path.join(binpath, 'run.bat')
	from com.airhork.tool import sche
	sche.delete('jboss')
	sche.scheImmediate('jboss', command)


def waitUntilRunning(host='localhost'):
	address = 'http://%s:8080/webstart' %(host)
	from time import time
	import time as ttime
	from urllib.error import HTTPError
	from urllib.error import URLError
	currenttime = time()
	expiretime = currenttime + 60 * 10 
	success = False

	print('test the connection of %s' %(address))

	while(not success and time() < expiretime):
		from urllib import request
		print('checking the startup of the jboss ...')
		try:
			response = request.urlopen(address)
			success = response.getcode() == 200
			response.close()
		except (HTTPError, URLError) as e:
			ttime.sleep(60)

	if(success):
		print('jboss start up well ...')
	else:
		raise NameError('cannot start up the jboss')

	



	



if __name__ == "__main__":
    main()


