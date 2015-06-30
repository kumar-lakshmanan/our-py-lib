'''
Created on Jun 26, 2015 Fri - 22:58:49

@author: LKumaresan
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from user_interface.win_main import Ui_MainWindow
import sys
import os
#from kmxPyQt.qne import qnodeseditor
from kmxPyQt.qne.qnodeseditor import QNodesEditor

class WinMain(QtWidgets.QMainWindow, Ui_MainWindow):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.parent = parent
        self.connectSignalSlots()
        self.createScene()

    def connectSignalSlots(self):
        #self.btnPropApply.clicked.connect(self.parent.btnClickHere)
        pass
        
    def createScene(self):
        self.scene = QtWidgets.QGraphicsScene(self)
        bgcolor = QtWidgets.QApplication.palette().color(QtGui.QPalette.Window)
        self.scene.setBackgroundBrush(QtGui.QBrush(bgcolor, QtCore.Qt.SolidPattern))

        self.graphicsView.setScene(self.scene)

        self.nodesEditor = QNodesEditor(self)
        self.nodesEditor.install(self.scene)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = WinMain(app)
    m.show()
    sys.exit(app.exec_())
    
