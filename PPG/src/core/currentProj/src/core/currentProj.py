'''
Created on Sep 23, 2014 Tue - 06:38:16

@author: LKumaresan
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from interface_runner.win_main import WinMain
import sys
from general import PyQt
from general import tools
import os

class currentProj(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.win = WinMain(self)
        self.win.show()

        self.tls = tools.basic(tools.infoStyle())
        self.qtTrees = PyQt.TreeWidget()
        self.qtTools = PyQt.Tools(self.win)

    def btnClickHere(self):
        input = self.qtTools.getValue(self.win.lineEdit)
        self.qtTools.setValue(self.win.label_3, "Your input is... " + input)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = currentProj()
    sys.exit(app.exec_())