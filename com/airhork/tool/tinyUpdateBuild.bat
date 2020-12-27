SET BASE=%~dp0
SET ASB_PATH=%BASE%../%ASB%

REM Update & build the solution project (this is optional, do this once a day). These are very small projects so it will be very fast.
cd %ASB_PATH%
cmd /C "svn update %ASB_PATH%"
cmd /C "mvn clean install -Dmaven.test.skip -P uct-msd-snapshot"

