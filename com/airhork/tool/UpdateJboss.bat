set JRIS=%~dp0
set ASB=%~dp0..\ris-dev

REM Update and build RIS
cd %JRIS%
cmd /C "svn update d:\dev\uct-msd > %~dp0..\update.txt"

@echo off
if %errorlevel% NEQ 0 goto error
echo on

echo The number of conflicts during update:
FIND /C "C  " "%~dp0..\update.txt"
@echo off
if %errorlevel% NEQ 0 goto updateSuccess
echo on
echo [ERROR] CONFLICT during update!!!
start %~dp0..\update.txt
goto error
:updateSuccess

REM source:jar			To get the sources in the target-platform plugin
REM -Dmaven.test.skip.exec 	This will compile your tests but will not execute them.
cmd /C "mvn clean install -Dmaven.test.skip "

@echo off
if %errorlevel% NEQ 0 goto error
echo on

cd d:\dev\asb-uct-msd-solution-ui-tests
cmd /C "svn up d:\dev\asb-uct-msd-solution-ui-tests"
cmd /C "mvn clean install -Dmaven.test.skip "

REM Update & build the solution project (this is optional, do this once a day). These are very small projects so it will be very fast.
cd %ASB%
cmd /C "svn update D:\dev\ris-dev"
cmd /C "mvn clean install -Dmaven.test.skip -P uct-msd-snapshot"


@echo off
if %errorlevel% NEQ 0 goto error
echo on



REM Update the install without signing the jars (faster)
cd %ASB%
REM call materialize-install.bat

@echo off
if %errorlevel% NEQ 0 goto error
echo on

goto end

:error

echo.
echo [INFO] ------------------------------------------------------------------------
echo [ERROR] FATAL ERROR
echo [INFO] ------------------------------------------------------------------------
echo.
pause


:end
