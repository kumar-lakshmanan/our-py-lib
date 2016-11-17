'''
Created on Oct 14, 2014

@author: Mukundan
For DevConsole
'''
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import sys,os
import sysPaths as sps

class sysPaths(QDialog):
	'''
	classdocs
	'''

	def __init__(self,parent):
	'''
	Constructor
	'''
	# Parent is DEV <DEVCONSOLEPLUG>
	self.parent = parent
	self.uiFile=sps.__file__.replace(".py",".ui")
	super(sysPaths, self).__init__(parent)
	print ("Loaded!")
	self.setupUI(self.uiFile)
	for path in sys.path:
		itm = QtWidgets.QListWidgetItem(path)
		self.listWidget.addItem(itm)
	self.show()

	def setupUI(self, uiFile):
	loadUi(uiFile, self)
	self.setWindowTitle(self.__class__.__name__)		

	def myFunc1(self, *arg):
	print(self.lineEdit.text())
	print("FewMore")

	def myFunc2(self, *arg):
	print(self.lineEdit_2.text())
	
if '__main__' == __name__:
	dev.sysPathsCls = sysPaths(dev)
	dev.sysPathsCls.show()	