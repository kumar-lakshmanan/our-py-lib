'''
Created on Sep 10, 2014

@author: Mukundan
'''
from PyQt5 import QtCore, QtGui, QtWidgets
from interface_runner.win_main import WinMain
import core.lib
import sys
from general import PyQt
from general import tools
import os


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

        self.infoStyle = tools.infoStyle()
        self.infoStyle.errorLevel = 2
        self.infoStyle.infoLevel = 0
        self.tls = tools.basic(self.infoStyle)
        self.qtTrees = PyQt.TreeWidget()
        self.qtTools = PyQt.Tools(self.win)

        self.loadProject("currentProj")

    def loadProject(self, folder):
        if(self.ppg):
            self.ppg.clearOldScreen()
        self.ppgFolder = folder
        self.ppgFolder = os.path.abspath(self.ppgFolder)
        self.ppg = core.lib.ppg(self.win, self.ppgFolder)
        self.win.lineEdit.setText(self.ppgFolder)
        self.populateScreens()

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

    def btnApply(self):
        self.ppg.saveCurrentScreen()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = PyProjGen()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     pj = core.lib.ppg("boss")
#     print(pj.getListOfScreenNames())
