'''
Created on Sep 10, 2014

@author: Mukundan
'''
import inspect
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport

from interface_runner.win_main import WinMain
from kmxGeneral import kmxINIConfigReadWrite
from kmxGeneral import kmxTools
from kmxPyQt import kmxQtCommonTools
from kmxPyQt import kmxQtTreeWidget
from kmxPyQt.devConsole3 import DevConsolePlug

import core.icons
import core.lib


class PyProjGen():
    '''
    classdocs
    '''
    win = None
    layout = None
    currentForm = None
    ppg = None

    def __init__(self):
        '''
        Constructor
        '''
        self.win = WinMain(self)
        self.win.show()

        self.cfg = kmxINIConfigReadWrite.INIConfig("config.ini")
        self.iconPath = self.cfg.getOption('UserInterface', 'IconPath')
        self.icons = core.icons.iconSetup()
        self.infoStyle = kmxTools.infoStyle()
        self.infoStyle.errorLevel = 2
        self.infoStyle.infoLevel = 0

        self.tls = kmxTools.Tools(self.infoStyle)
        self.qtTools = kmxQtCommonTools.CommonTools(self.win, self.iconPath)
        self.qtTrees = kmxQtTreeWidget.TreeWidget()
        self.qtTools.applyStyle()
        dv = self.qtTools.getIconString('/04/16/39.png')
        self.qtConsole = DevConsolePlug.DevConsole(self.win, ShowPrint=True, ShowError=True, StatusBar=self.win.statusBar, AsDock=True, InitalizeScripts=True, SaveLogRefreshDays=30, btnIcon=dv, addObj=self)

        self.loadProject("currentProj")
        # self.win.statusBar.showMessage("READY!")


    def loadProject(self, folder):
        if(self.ppg):
            self.ppg.clearOldScreen()
        self.ppgFolder = folder
        self.ppgFolder = os.path.abspath(self.ppgFolder)
        self.ppg = core.lib.ppg(self.win, self.ppgFolder)
        self.win.lineEdit.setText(self.ppgFolder)
        self.populateScreens()
        self.setupIcons()

    def setupIcons(self):
        # Icon Item
        itms = self.qtTrees.getRootItems(self.win.treeWidget)
        iconObjs = inspect.getmembers(self.icons)
        for eachItem in itms:
            self.qtTools.setIconByObj(eachItem)
            for iconObj in iconObjs:
                if (eachItem.text(0) == iconObj[0]):
                    self.qtTools.setIconForItem(eachItem, iconObj[1])
                    break;

        self.qtTools.setIconForItem(self.win, self.icons.windowIcon, isWindow=1)
        self.qtTools.setIconForItem(self.win.label_2, '', thisImage="ppg.png")

    def populateScreens(self):
        self.win.treeWidget.clear()
        for eachScreen in self.ppg.getListOfScreenNames():
            itm = self.qtTrees.createItem(eachScreen)
            self.qtTrees.addNewRoot(self.win.treeWidget, itm)

    def listFormSelect(self, *eve):
        selectedItem = eve[0]
        selected = selectedItem.text(0)
        self.ppg.saveCurrentScreen()
        self.ppg.setCurrentScreen(selected)

    def btnNewPPG(self):
        self.ppg.saveCurrentScreen()
        x = self.qtTools.getFolder("Select a new folder to save proj content...")
        if(x != ""):
            self.loadProject(x)

    def btnLoadPPG(self):
        self.ppg.saveCurrentScreen()
        x = self.qtTools.getFolder()
        if(x != ""):
            self.loadProject(x)

    def btnSavePPG(self):
        self.ppg.saveAllScreens()
        # self.qtTools.showInfoBox("Done", "Success")

    def btnGenerateProj(self):
        self.ppg.saveCurrentScreen()
        self.ppg.reLoadAll()
        self.gen = core.lib.ppgGenerator(self.ppg)
        self.gen.doGenerate()
        self.tls.info("Completed!")
        self.qtTools.showInfoBox("Done!", "Your Python project base code is Ready!\nImport the project to your PyDev and start your work!")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = PyProjGen()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     pj = core.lib.ppg("boss")
#     print(pj.getListOfScreenNames())
