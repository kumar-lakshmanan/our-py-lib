from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
import random
#For DevConsole
import amILucky

class AmiluckyCls(QtWidgets.QMainWindow):
	
	def __init__(self,parent):
		self.parent=parent		
		#self.uiFile=r"DevConsolePlug_BIN\Scripts\tools\amILucky.ui".replace(os.path.sep,'/')
		self.uiFile=amILucky.__file__.replace(".py",".ui")
		super(AmiluckyCls, self).__init__(self.parent)		
		loadUi(self.uiFile, self)
		self.pushButton.clicked.connect(self.doTest)
		self.textEdit.setReadOnly(1)
		self.todaysLuckyNumber = random.randint(0,36)
		self.textEdit.setPlainText("Todays Lucky Number: " + str(self.todaysLuckyNumber))
		val = self.lineEdit_3.text()
		self.attempt=int(val)

	def update(self, data):
		old = self.textEdit.toPlainText()
		self.textEdit.setPlainText(old+"\n"+str(data))
		
	def doTest(self):
		self.goodLuckCnt=0		
		self.badLuckCnt=0
		self.textEdit.setPlainText("Todays Lucky Number: " + str(self.todaysLuckyNumber))		
		for attemptNo in range(0,self.attempt):
			now = random.randint(0,36)
			if(now==self.todaysLuckyNumber):
				self.goodLuckCnt += 1
				self.update(str(now) + "-Good")
			else:
				self.badLuckCnt += 1
				self.update(now)		  
		self.lineEdit.setText(str(self.goodLuckCnt))		  
		self.lineEdit_2.setText(str(self.badLuckCnt))
		
		if (self.goodLuckCnt>0):
			self.label_3.setText("!!! You are lucky today !!!")		 
		else:
			self.label_3.setText("!!! Don't push your luck, today !!!") 
		
if (__name__=="__main__"):
	dev.AmiluckyClsObj = AmiluckyCls(dev)
	dev.AmiluckyClsObj.show()