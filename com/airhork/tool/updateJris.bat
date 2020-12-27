d:\
cd d:\dev\jris
set JRIS=%~dp0
set ASB=%~dp0..\ris-dev

REM Update and build RIS
cd %JRIS%
cmd /C "svn update d:\dev\jris "

@echo off
if %errorlevel% NEQ 0 goto error
echo on


REM source:jar			To get the sources in the target-platform plugin
REM -Dmaven.test.skip.exec 	This will compile your tests but will not execute them.
cmd /C "mvn clean install -Dmaven.test.skip "

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
