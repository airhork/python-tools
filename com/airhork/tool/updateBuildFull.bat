SET BASE=%~dp0
SET ASB_PATH=%BASE%../%ASB%

cd d:\dev\agility-ris-mobile
cmd /c "svn update && mvnci"

cd d:\dev\ris-server
cmd /c "svn update && mvncit"


cd d:\dev\jris
cmd /c "svn update && mvn clean install -Dmaven.test.skip -P server-snapshot"

cd d:\dev\uct-msd
cmd /c "svn update && mvn clean install -Dmaven.test.skip -Dris.version=1.0.0-SNAPSHOT -Dris.server.version=0.13.0-SNAPSHOT "


REM Update & build the solution project (this is optional, do this once a day). These are very small projects so it will be very fast.
cd %ASB_PATH%
cmd /C "svn cleanup"
cmd /C "svn update %ASB_PATH%"
cmd /C "mvn clean install -Dmaven.test.skip -P uct-msd-snapshot,mobile-snapshot,ris-server-snapshot,ris-client-snapshot"

