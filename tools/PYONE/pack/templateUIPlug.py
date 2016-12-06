from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
import os
import sip
import myUIPlug
#For DevConsole

class myUIPlugCls(QtWidgets.QMainWindow):
	
	def __init__(self,parent):
		self.parent=parent 
		self.tools=self.parent.ttls		
		self.qtTools=self.parent.qtTools
		self.uiFile=myUIPlug.__file__.replace(".py",".ui")
		super(myUIPlugCls, self).__init__(self.parent)
		loadUi(self.uiFile, self)
		self.pushButton.clicked.connect(self.doRun)
		
	def initialize(self):
		self.parent.pylib.say("myUIPlugClsObj is working fine")

	def doRun(self):
		input = self.textEdit.toPlainText()
		self.label.setText(input)
		self.parent.pylib.say(input)

if (__name__=="__main__"):
	if(not hasattr(dev,'myUIPlugClsObj') or sip.isdeleted(dev.myUIPlugClsObj)):
		dev.myUIPlugClsObj = myUIPlugCls(dev)
	dev.myUIPlugClsObj.show()
	dev.myUIPlugClsObj.raise_()