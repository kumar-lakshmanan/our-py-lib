'''
Created on Aug 23, 2014

@author: Mukundan
'''

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from core.CompileUItoPY import CompileUItoPYCls
from qtui.MainUI import Ui_MainWindow
from general import PyQt
import sys
import os


class MainApplication(QtWidgets.QMainWindow, Ui_MainWindow):

    pyFile = ""
    uiFile = ""
    cmp = ""
    ttl = PyQt.Tools(None)

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.cmp = CompileUItoPYCls()
        self.ttl = PyQt.Tools(self)
        self.pyFile = ""
        self.uiFile = ""

        if(len(sys.argv) > 1):
            self.uiFile = str(sys.argv[1]).strip()
            self.pyFile = self.cmp.getPyFileName(self.uiFile)

        self.lineEdit.setText(self.uiFile)
        self.lineEdit_2.setText(self.pyFile)

        self.textEdit.setEnabled(0)
        self.pushButton.clicked.connect(self.btnClickFn)
        self.toolButton.clicked.connect(self.btnBrowseUI)
        self.toolButton_2.clicked.connect(self.btnBrowsePY)

    def btnBrowseUI(self):
        self.uiFile = self.ttl.getFile("Select a UI File..", "main.ui", "UI Files (*.ui);;All Files (*);;")
        self.lineEdit.setText(self.uiFile)

    def btnBrowsePY(self):
        self.pyFile = self.ttl.getFile("Select a PY File..", "main.py", "Py Files (*.py);;All Files (*);;")
        self.lineEdit_2.setText(self.pyFile)

    def btnClickFn(self):
        self.uiFile = self.lineEdit.text()
        if(self.uiFile != ""):
            self.pyFile = self.lineEdit_2.text()
            if(self.pyFile == ""):
                self.pyFile = self.cmp.getPyFileName(self.uiFile)
                self.lineEdit_2.setText(self.pyFile)
            self.addInfo ("Src: " + self.uiFile)
            self.addInfo ("Dst: " + self.pyFile)
            self.cmp.convertCore(self.uiFile, self.pyFile) 
            if(os.path.exists(self.pyFile)):
                self.addInfo ("PY File Created! " + self.pyFile)
        self.addInfo ("Done!")

    def addInfo(self, data):
        matter = self.textEdit.toPlainText() + "\n"
        self.textEdit.setText(matter + data)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = MainApplication()
    m.show()
    sys.exit(app.exec_())
