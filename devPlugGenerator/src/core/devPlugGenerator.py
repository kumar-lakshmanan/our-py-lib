'''
Created on Oct 16, 2014 Thu - 08:26:26

@author: LKumaresan
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
from kmxPyQt.devConsole3 import DevConsolePlug
import core.icons


class devPlugGenerator(object):
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
        self.qtConsole = DevConsolePlug.DevConsole(self.win, ShowPrint=True, ShowError=True, StatusBar=self.win.statusBar(), AsDock=False, InitalizeScripts=True, SaveLogRefreshDays=30)
        self.qtTrees = kmxQtTreeWidget.TreeWidget()
        self.qtTools = kmxQtCommonTools.CommonTools(self.win, self.iconPath)
        self.setupUI()

    def setupUI(self):
        self.qtTools.setIconForItem(self.win, self.icons.windowIcon, isWindow=1)

    def btnClickHere(self):
        plugName = self.qtTools.getValue(self.win.lineEdit_5)
        plugDst = self.qtTools.getValue(self.win.lineEdit_6)

        src = self.tls.getRelativeFolder('template')

        file1 = os.path.join(src, 'template.py')
        file1Dst = os.path.join(plugDst, plugName + '.py')
        file1Content = self.tls.fileContent(file1)
        file1Content = file1Content.replace('[[PLUGNAME]]', plugName, 100000)
        self.tls.writeFileContent(file1Dst, file1Content)
        print('Src: ' + file1)
        print('Dst: ' + file1Dst)

        file2 = os.path.join(src, 'template.ui')
        file2Dst = os.path.join(plugDst, plugName + '.ui')
        file2Content = self.tls.fileContent(file2)
        self.tls.writeFileContent(file2Dst, file2Content)
        print('Src: ' + file2)
        print('Dst: ' + file2Dst)

        self.qtTools.showInfoBox('Done', 'Template Ready!')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = devPlugGenerator()
    sys.exit(app.exec_())
