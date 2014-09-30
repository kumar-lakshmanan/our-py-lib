'''
Created on Sep 4, 2014

@author: Mukundan
'''

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from user_interface.win_main import Ui_MainWindow


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
        self.pushButton_4.clicked.connect(self.parent.btnNewPPG)
        self.pushButton.clicked.connect(self.parent.btnLoadPPG)
        self.pushButton_3.clicked.connect(self.parent.btnGenerateProj)

        self.treeWidget.itemClicked.connect(self.parent.listFormSelect)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = WinMain(app)
    m.show()
    sys.exit(app.exec_())

