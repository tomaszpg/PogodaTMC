@echo off
set OLD_PATH=%PATH%
SET OPENEV_HOME=x:\PROGRA~1\FWTOOL~1.7
SET FWTOOLS_DIR=x:\PROGRA~1\FWTOOL~1.7
call "%FWTOOLS_DIR%\bin\setfwenv.bat"
start pythonw "%OPENEV_HOME%\pymod\openev.py" %*
set PATH=%OLD_PATH%
