from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
#For DevConsole

class myUIPlugCls(QtWidgets.QMainWindow):
        
        def __init__(self,parent):
                self.uiFile=r"UI_myUIPlug.ui".replace(os.path.sep,'/')
                self.parent=parent
                super(myUIPlugCls, self).__init__(parent)                
                loadUi(self.uiFile, self)
                self.pushButton.clicked.connect(self.doThisActivity)
                
        def doThisActivity(self):
            input = self.textEdit.toPlainText()
            self.label.setText(input)
            print(input)
                
if (__name__=="__main__"):
        parent.myUIPlugClsObj = myUIPlugCls(parent)
        parent.myUIPlugClsObj.show()