from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
import os
import sip
import myUIPlug
#For DevConsole

class myUIPlugCls(QtWidgets.QMainWindow):
        
        def __init__(self,parent):
                self.parent=parent 
                self.settings=self.parent.settings        
                self.tools=self.parent.customTools                           
                self.uiFile=myUIPlug.__file__.replace(".py",".ui")
                super(myUIPlugCls, self).__init__(self.parent)                
                loadUi(self.uiFile, self)
                self.pushButton.clicked.connect(self.doRun)

        def doRun(self):
                input = self.textEdit.toPlainText()
                self.label.setText(input)
                print(input)

                
if (__name__=="__main__"):
        if(not hasattr(dev,'myUIPlugClsObj') or sip.isdeleted(dev.myUIPlugClsObj) or dev.devMode):       
                dev.myUIPlugClsObj = myUIPlugCls(dev)
        dev.myUIPlugClsObj.show()
        dev.myUIPlugClsObj.raise_()