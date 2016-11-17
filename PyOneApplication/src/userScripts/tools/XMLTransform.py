from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
#For DevConsole
import lxml.etree as ET
import pprint
import httpJSONXMLServer
import traceback
import XMLTransform

class XmltransformCls(QtWidgets.QMainWindow):
	
	def __init__(self,parent):
		self.uiFile=XMLTransform.__file__.replace(".py",".ui")
		self.parent=parent
		super(XmltransformCls, self).__init__(parent)		
		loadUi(self.uiFile, self)
		self.pushButton.clicked.connect(self.doThisActivity)
		
	def doThisActivity(self):
		ET.clear_error_log()
		xslFile = self.lineEdit.text()
		xmlFile = self.lineEdit_2.text()
		self.textEdit.setPlainText("")		

		try:
			xml = ET.parse(xmlFile)
			xslt = ET.parse(xslFile)	  
			
			transform = ET.XSLT(xslt)
			newxml = transform(xml)
			
			newData = ET.tostring(newxml, pretty_print=True)
			p=str(newData.decode(encoding='UTF-8'))
			self.textEdit.setPlainText(p)
		except lxml.etree.XSLTApplyError as e:
			error = httpJSONXMLServer.errorReport()
			moreInfo = e.error_log.filter_from_level(ET.ErrorLevels.FATAL)
			moreInfo2 = e.error_log.last_error
			errorInfo = error + "\n" + str(moreInfo) + str(moreInfo2)
			self.textEdit.setPlainText("Error:\n" + errorInfo)		  
			print("----\n"+errorInfo+"\n----\n")			
		except lxml.etree.XMLSyntaxError as e1 : 
			error = httpJSONXMLServer.errorReport()
			moreInfo = e1.error_log.filter_from_level(ET.ErrorLevels.FATAL)
			moreInfo2 = e1.error_log.last_error
			errorInfo = error + "\n" + str(moreInfo) + str(moreInfo2)
			
			self.textEdit.setPlainText("Error:\n" + errorInfo)		  
			print("----\n"+errorInfo+"\n----\n")
		print("Convertion Done!")
		

		
if (__name__=="__main__"):
	if(not hasattr(dev,'XmltransformClsObj')):	   
		dev.XmltransformClsObj = XmltransformCls(dev)
	dev.XmltransformClsObj.show()
	dev.XmltransformClsObj.raise_()