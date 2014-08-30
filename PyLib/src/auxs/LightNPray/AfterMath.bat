del *.~* /f/s/q
del *.PYC /f/s/q
del bin /f/s/q
rd bin /s/q
del build /f/s/q
rd build /s/q
TortoiseProc /command:commit /path:"%~dp0"
pause!