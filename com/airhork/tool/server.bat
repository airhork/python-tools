
cd d:\dev\ris-server
REM Update the install without signing the jars (faster)

REM Build the dev by the specified version 
cmd /C "svn up && mvncit && mvn -U eclipse:eclipse -DdownloadSoruces"



