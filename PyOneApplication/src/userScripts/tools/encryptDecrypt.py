from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
import sip
import encryptDecrypt
#For DevConsole

class encryptDecryptCls(QtWidgets.QMainWindow):
	
	def __init__(self,parent):
		self.parent=parent		
		self.uiFile=encryptDecrypt.__file__.replace(".py",".ui")
		super(encryptDecryptCls, self).__init__(self.parent)		
		loadUi(self.uiFile, self)

	def doEncryption(self):
		input = self.lineEdit.text()
		res = self.parent.encrypt(input)
		self.plainTextEdit.setPlainText(res)
		matter = 'self.parent.decrypt(\'' + res + '\')'
		print(matter)

	def doDecryption(self):
		input = self.lineEdit_2.text()
		res = self.parent.decrypt(input)
		self.plainTextEdit_2.setPlainText(res)
		matter = 'self.parent.encrypt(\'' + res + '\')'
		print(matter)
				
if (__name__=="__main__"):
	if(not hasattr(dev,'encryptDecryptClsObj') or sip.isdeleted(dev.encryptDecryptClsObj)):	   
		dev.encryptDecryptClsObj = encryptDecryptCls(dev)
	#dev.encryptDecryptClsObj = encryptDecryptCls(dev)		
	dev.encryptDecryptClsObj.show()
	dev.encryptDecryptClsObj.raise_()