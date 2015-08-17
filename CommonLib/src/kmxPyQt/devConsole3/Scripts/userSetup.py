import os
import socket
parent.qtTools.applyStyle('Fusion')
parent.pyDesigner = "C:\Python34\Lib\site-packages\PyQt5\designer.exe"

print("\n\n")
print("-----Auto start-----")

print("Style list: " + str(parent.qtTools.getStyleList()))
print("Applying style: Fusion")
print("Hostname: " + socket.gethostname())
print("Timestamp: " + parent.ttls.getDateTime())
print("Working Dir: " + os.getcwd())
print("PyDesigner: " + parent.pyDesigner)

print("-----End-----")
