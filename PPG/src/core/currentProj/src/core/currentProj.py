'''
Created on Sep 28, 2014 Sun - 21:08:20

@author: Kumaryes
'''
from test.test_finalization import SelfCycleBase
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from interface_runner.win_main import WinMain
from kmxGeneral import kmxINIConfigReadWrite
from kmxGeneral import kmxTools
from kmxPyQt import kmxQtCommonTools
from kmxPyQt import kmxQtTreeWidget
import core.icons

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

        self.cfg = kmxINIConfigReadWrite.INIConfig("config.ini")
        self.iconPath = self.cfg.getOption('UserInterface', 'IconPath')
        self.icons = core.icons.iconSetup()

        self.tls = kmxTools.Tools(kmxTools.infoStyle())
        self.qtTrees = kmxQtTreeWidget.TreeWidget()
        self.qtTools = kmxQtCommonTools.CommonTools(self.win, self.iconPath)

        self.setupUI()

    def setupUI(self):
        self.qtTools.setIconForItem(self.win, self.icons.windowIcon, isWindow=1)

    def btnClickHere(self):
        input = self.qtTools.getValue(self.win.lineEdit)
        self.qtTools.setValue(self.win.label_3, "Your input is... " + input)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = currentProj()
    sys.exit(app.exec_())
