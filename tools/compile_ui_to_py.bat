set fPath=%~dp1
set fName=%~n1
C:\Python34\Lib\site-packages\PyQt5\pyuic5.bat "%fPath%/%fName%.ui" -o "%fPath%/%fName%.py"