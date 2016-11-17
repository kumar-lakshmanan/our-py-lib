from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
import os
import sip
import myCalc
#For DevConsole

class myCalcCls(QtWidgets.QMainWindow):
	
	def __init__(self,parent):
		self.parent=parent 
		self.settings=self.parent.settings
		self.tools=self.parent.customTools
		self.uiFile=myCalc.__file__.replace(".py",".ui")
		super(myCalcCls, self).__init__(self.parent)
		loadUi(self.uiFile, self)
		#self.pushButton.clicked.connect(self.doRun)
		self.showResult(0)

	def doRun(self):
		obj = self.sender()
		name = obj.objectName()
		print("Call from " + str(obj.objectName()))
		
		self.showResult(0)
		if (name == 'lineEdit' or name == 'lineEdit_2'):
			self.doPercentage1()
		if (name == 'lineEdit_4' or name == 'lineEdit_3'):
			self.doPercentage2()	
		#input = self.textEdit.toPlainText()
		#self.label.setText(input)
	
	def showResult(self, val):
		print('Result: ' + str(val))
		self.label.setText(str(val))
		
	def doPercentage1(self):
		val = float(self.lineEdit.text())
		val2 = float(self.lineEdit_2.text())
		
		print (val)
		print (val2)
		
		result = val * (val2/100)
		
		self.showResult(result)
		
if (__name__=="__main__"):
	if(not hasattr(dev,'myCalcClsObj') or sip.isdeleted(dev.myCalcClsObj) or dev.devMode):
		dev.myCalcClsObj = myCalcCls(dev)
	dev.myCalcClsObj.show()
	dev.myCalcClsObj.raise_()