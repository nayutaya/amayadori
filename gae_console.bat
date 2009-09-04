@echo off

if "%COMPUTERNAME%" == "MACBETH" goto MACBETH
if "%COMPUTERNAME%" == "CAESAR" goto CAESAR
goto ELSE

:MACBETH
set PATH=%PATH%;C:\Python25
set GAE_SDK_HOME=C:\Program Files (x86)\Google\google_appengine
goto END

:CAESAR
set PATH=%PATH%;C:\Python25
set GAE_SDK_HOME=D:\Program Files\Google\google_appengine
goto END

:ELSE
echo Unknown Host
goto END

:END

cmd
