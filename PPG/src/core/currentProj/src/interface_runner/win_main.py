'''
Created on Sep 23, 2014 Tue - 06:38:16

@author: LKumaresan
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from user_interface.win_main import Ui_MainWindow
import sys
import os


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

    def connectSignalSlots(self):
        self.pushButton.clicked.connect(self.parent.btnClickHere)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = WinMain(app)
    m.show()
    sys.exit(app.exec_())
    
