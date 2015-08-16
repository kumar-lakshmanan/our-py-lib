set fPath=%~dp1
set fName=%~n1
C:\Python34\Lib\site-packages\PyQt5\pyrcc5.exe "%fPath%/%fName%.qrc" -o "%fPath%/%fName%_rc.py"
pause