from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
import QuickTools
#For DevConsole
import inspect
import importlib
import sip

class QuickToolsCls(QtWidgets.QMainWindow):
	
	def __init__(self,parent):
		self.parent=parent	 
		self.settings=self.parent.settings	
		self.tools=self.parent.customTools		  
		self.uiFile=QuickTools.__file__.replace(".py",".ui")
		super(QuickToolsCls, self).__init__(self.parent)		
		loadUi(self.uiFile, self)
		self.existingObj=[]
		self.popsUIObjects()

	def parentName(self, object):
		for each in self.parent.__dict__:
			if self.parent.__dict__[each] == object:
				return str(each)

	def deleteAll(self):
		winObjs = self.parent.findChildren(QtWidgets.QMainWindow)
		for eachWinObj in winObjs:
			objName = self.parentName(eachWinObj)
			if(objName):
				clsObj = eachWinObj.__class__
				clsName = eachWinObj.__class__.__name__
				modObj = clsObj.__module__ 
				if (str(modObj) != '__main__'):
					m = __import__(modObj)
					importlib.reload(m)
					newCls = getattr(m,clsName)
					eachWinObj.deleteLater()
					sip.delete(eachWinObj)			 
					delattr(self.parent,objName)
					newObj = newCls(self.parent)
					setattr(self.parent,objName,newObj)
			
	def popsUIObjects(self):
		self.existingObj=[]
		self._clearItems(self.listWidget)
		lst = self.parent.children()
		rlst = lst[::-1]
		for each in rlst:
			lst = inspect.getmro(type(each))
			if(type(QtWidgets.QMainWindow()) in lst):
				if(type(each).__name__ in self.existingObj):
					each.deleteLater()
				else:
					self._addItem(self.listWidget, type(each).__name__, each)
					self.existingObj.append(type(each).__name__)
				
	def listItemDblClicked(self, itm):
		if(itm and itm.data(36)):
			obj = itm.data(36)
			if(obj):
				obj = obj.__class__(self.parent)
				obj.show()
				obj.raise_()				
		
	def _clearItems(self, listWidget):
		self.listWidget.clear()		
		
	def _addItem(self, listWidget, label, data):
		itm = QtWidgets.QListWidgetItem(str(label))
		itm.setData(36, data)
		self.listWidget.addItem(itm)					
								 
if (__name__=="__main__"):
	if(not hasattr(dev,'QuickToolsClsObj') or sip.isdeleted(dev.QuickToolsClsObj) or dev.devMode):	   
		   dev.QuickToolsClsObj = QuickToolsCls(dev)
	#dev.QuickToolsClsObj = QuickToolsCls(dev)
	dev.QuickToolsClsObj.show()
	dev.QuickToolsClsObj.raise_()