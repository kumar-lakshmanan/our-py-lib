from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
#For DevConsole

import httpJSONXMLServer
import JSONServer

class JsonserverCls(QtWidgets.QMainWindow):
	
	def __init__(self,parent):
		#self.uiFile=r"DevConsolePlug_BIN/Scripts/tools\JSONServer.ui".replace(os.path.sep,'/')
		self.uiFile=JSONServer.__file__.replace(".py",".ui")
		self.parent=parent
		super(JsonserverCls, self).__init__(parent)		
		loadUi(self.uiFile, self)
		self.pushButton.clicked.connect(self.startServer)
		self.pushButton_2.clicked.connect(self.stopServer)
		self.pushButton.setEnabled(1)
		self.pushButton_2.setEnabled(0)
		
	def startServer(self):
		self.label.setText("Server Running...")
		self.server = httpJSONXMLServer.HttpDaemon()
		self.server.start()
		self.pushButton.setEnabled(0)
		self.pushButton_2.setEnabled(1)

	def stopServer(self):
		self.label.setText("Server Stopped!")
		self.server.stop()   
		self.pushButton.setEnabled(1)
		self.pushButton_2.setEnabled(0)
		
if (__name__=="__main__"):
	if(not hasattr(dev,'JsonserverClsObj')):	
		dev.JsonserverClsObj = JsonserverCls(dev)
	dev.JsonserverClsObj.show()
	dev.JsonserverClsObj.raise_()