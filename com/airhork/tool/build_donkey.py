"""
"""


import os
import os.path
from com.airhork.tool import util
import shutil

def main():
	import sys
	if len(sys.argv) < 2:
		print('the size is ',len(sys.argv))
		return None
	print(sys.argv)
	para = sys.argv[1]
	if para == 'full':
		_updateAndRun()
	elif para == 'mate':
		_materialize()
	elif para == 'run':
		_runJboss()
  
def action():
	from datetime import datetime
	now = datetime.now()
	print(now.strftime('%d-%m-%y-%H-%M'))
	from com.airhork.tool import maven
	maven.metainfoCheck()
	_updateAndRun()
	maven.cleanupBillOfMaterials()

def metaInfoChecker():
	os.chdir('d:/dev')
	os.system('svn up d:/dev/uct-msd > up.txt')
	content = open('d:/dev/up.txt')
	for line in content.readlines():
		if 'MANIFEST.MF' in line:
			from com.airhork.tool import mail
			mail.sendmail('The manifest has been changed')
			break





def _updateAndRun():
	os.putenv('NOPAUSE','true')
	os.chdir('c:/dev')
	os.system('c:/dev/uct-msd/UpdateJboss.bat')

	os.chdir('c:/dev/ris-dev')
	os.system('materialize-install.bat')
	os.system('create-target-platform-34.bat')


def _materialize():
	from datetime import datetime
	now = datetime.now()

	if os.path.exists('d:/dev/agility-install'):
		os.rename('d:/dev/agility-install','d:/dev/agility-install-' + now.strftime('%d-%m-%y-%H-%M'))	

	os.chdir('d:/dev/ris-dev/')
	os.system('materialize-install.bat')
	shutil.copyfile('d:/dev/jboss-log4j.xml','D:/dev/agility-install/server/jboss/server/production/conf/jboss-log4j.xml')

def _runJboss():
	os.putenv('NOPAUSE','true')
	os.chdir('D:/dev/agility-install/server/jboss/bin')
	os.popen('start run.bat')


	

		


if __name__ == "__main__":
    main()

