

##-----------For Maya & Standalone Running Compatibility------------
import os,sys
scriptPath = 'D:/Kumaresanz/Quest/Test'
scriptPath = os.path.normpath(scriptPath) if scriptPath and os.path.exists(scriptPath) else ''
if scriptPath not in sys.path: sys.path.append(scriptPath)
os.chdir(scriptPath)

import pyqt4maya as p4m
reload(p4m)
if p4m.isExecInMaya():
    if not p4m.isPyQt4Ready():
        if p4m.getPyQtLib():
            from PyQt4 import QtGui, QtCore
        else:
            print 'Unable to load PyQt Lib!'
else:
    from PyQt4 import QtGui, QtCore
##-----------For Maya & Standalone Running Compatibility------------




from MainUI import Ui_MainWindow
import sys,os

class MainUI(QtGui.QMainWindow, Ui_MainWindow):


    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.defaultSize = self.size()
        self.miniSize = self.pushButton.size()
        self.connect(self.pushButton, QtCore.SIGNAL('clicked()'), self.sigButtonClick)

    def sigButtonClick(self):
        self.toolBar.setVisible(not self.toolBar.isVisible())
        self.label.setVisible(not self.label.isVisible())
        self.menuBar.setVisible(not self.menuBar.isVisible())
        self.resize(self.defaultSize) if self.toolBar.isVisible() else self.resize(self.miniSize)
        app.processEvents()

    def SampleFunction(self):
        print "TEST"


if __name__ == '__main__':
    ui,app = p4m.uiStart(MainUI)
    ui.show()



