'''
Created on Nov 08, 2016 Tue - 07:33:19

@author: LKumaresan
'''
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from interface_runner.win_main import WinMain
from kmxGeneral import kmxINIConfigReadWrite
from kmxGeneral import kmxTools
from kmxPyQt import kmxQtCommonTools
from kmxPyQt import kmxQtTreeWidget
from kmxPyQt.devConsole3 import DevConsolePlug
import core.icons

class CLIExecute(object):
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
        self.qtConsole = DevConsolePlug.DevConsole(self.win, ShowPrint=True, ShowError=True, StatusBar=self.win.statusBar(), AsDock=True, InitalizeScripts=True)        
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
    m = CLIExecute()
    sys.exit(app.exec_())
