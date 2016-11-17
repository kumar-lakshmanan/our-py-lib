import os
import socket
import sys
import general
import userSetting

print("-----Auto started-----")
try:
	dev.settings = userSetting.settings(dev)
	dev.settings.doInitialize()
	
	dev.customTools=general.commonTools(dev)
	dev.customTools.doStartupRun()	

	dev.devMode=0
	justfy=25
	print("Dev mode".ljust(justfy,'.') + str(dev.devMode))
	print("Style list".ljust(justfy,'.') + str(dev.qtTools.getStyleList()))
	print("Applying style".ljust(justfy,'.') + "Fusion")
	print("Hostname".ljust(justfy,'.') + socket.gethostname())
	print("Timestamp".ljust(justfy,'.') + dev.ttls.getDateTime())
	print("Working Dir".ljust(justfy,'.') + os.getcwd())
	print("PyDesigner".ljust(justfy,'.') + dev.pyDesigner)
	print("Sample Decryption".ljust(justfy,'.') + dev.decrypt('Ylhk!'))
	print("-----End-----")
	dev.customTools.trayMessage("Be Hapy and its ready for use!")

except:
	raise
	print("------- Startup Error! Please, Investigate!----------")	
