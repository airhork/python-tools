SET BASE=%~dp0
SET ASB_PATH=%BASE%../%ASB%

if [%1] == [] goto uctmsd
cd %BASE%../%1
cmd /C "svn update && mvnci"



:uctmsd
REM Update and build RIS
cd %BASE%
cmd /C "svn update && mvnci"

cd ../asb-uct-msd-solution-ui-tests
cmd /C "svn update && mvnci"


REM Update & build the solution project (this is optional, do this once a day). These are very small projects so it will be very fast.
cd %ASB_PATH%
cmd /C "svn cleanup"
cmd /C "svn update %ASB_PATH%"
cmd /C "mvn clean install -Dmaven.test.skip "

