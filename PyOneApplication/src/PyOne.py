'''
Created on Oct 22, 2015

@author: MUKUND-update-yes
'''

from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt, )
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget, )
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
#from PyQt5.uic.Compiler.qtproxies import QtWidgets

import os
import sys
import atexit

import pyoneScriptWindow
import mainWindow 
import central
import crashSupport

'''
First time runner setup

- delete 'config.ini' file if present
- make sure no 'argument' attach to exe
- start the app and close the app
- will create 'userScripts' and config.ini
- setup 4 digit secret code and attach to argument of this exe
- start the app again
- open new file and run below command
print(dev.encrypt('4132'))
- get the value displayed in output 
- paste that value in 'config.ini' file for below mentioned setting
 decryptValue=9687
- make sure to add double quote for your value
eg: 
decryptValue=";67|8"
- save the config

'''

class PyOneMainWindow(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow, central.CoreCentral):
    '''
    classdocs
    '''
    def __init__(self, currentApp):
        '''
        Constructor
        '''
        self.app = currentApp
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        central.CoreCentral.__init__(self)
        atexit.register(self.sessionClosed)
        
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)
        
        self.setWindowTitle("PyOne")
        
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()
        self.startupActivity()
                
    def sessionClosed(self):
        if hasattr(self, 'outputWindow') and self.outputWindow:
            content=self.outputWindow.textEdit.text()
            f=open('PyOne.log','w')
            f.write(str(content))
            f.close()
            
    def closeEvent(self, event):           
        self.mdiArea.closeAllSubWindows()
        self.sessionClosed()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            print('closing...')
            self.shutdownActivity()
            event.accept()

    def newFile(self):
        child = self.createNewScript()
        child.newFile()
        child.show()

    def open(self):
        scpt = self.scriptsPath
        scpt = scpt if os.path.exists(scpt) else 'D:'
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open python script file...', scpt, 'Python(*.py);;All Files (*)', options=options)        
        #fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            self.loadFile(fileName)

    def loadFile(self, fileName):
        existing = self.findMdiChild(fileName)
        if existing:
            self.mdiArea.setActiveSubWindow(existing)
            return

        child = self.createNewScript()
        if child.loadFile(fileName):
            self.statusBar().showMessage("File loaded", 2000)
            child.show()
        else:
            child.close()
            
    def save(self):
        if self.activeMdiChild() and self.activeMdiChild().save():
            self.statusBar().showMessage("File saved", 2000)

    def saveAs(self):
        if self.activeMdiChild() and self.activeMdiChild().saveAs():
            self.statusBar().showMessage("File saved", 2000)

    def cut(self):
        if self.activeMdiChild():
            self.activeMdiChild().cut()

    def copy(self):
        if self.activeMdiChild():
            self.activeMdiChild().copy()

    def paste(self):
        if self.activeMdiChild():
            self.activeMdiChild().paste()

    def about(self):
        QMessageBox.about(self, "About PyOne", self.aboutInfo)

    def updateMenus(self):
        hasMdiChild = (self.activeMdiChild() is not None)
        self.saveAct.setEnabled(hasMdiChild)
        self.saveAsAct.setEnabled(hasMdiChild)
        self.pasteAct.setEnabled(hasMdiChild)
        self.closeAct.setEnabled(hasMdiChild)
        self.closeAllAct.setEnabled(hasMdiChild)
        self.tileAct.setEnabled(hasMdiChild)
        self.cascadeAct.setEnabled(hasMdiChild)
        self.nextAct.setEnabled(hasMdiChild)
        self.previousAct.setEnabled(hasMdiChild)
        self.separatorAct.setVisible(hasMdiChild)

#         hasSelection = (self.activeMdiChild() is not None and
#                         self.activeMdiChild().textCursor().hasSelection())
#         self.cutAct.setEnabled(hasSelection)
#         self.copyAct.setEnabled(hasSelection)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def createNewScript(self):
        child = pyoneScriptWindow.PyOneScript()
        child.scriptsPath = self.scriptsPath
        self.mdiArea.addSubWindow(child)
        return child

    def createActions(self):
        self.newAct = QAction(self.qtIcon.getIcon('page.png'), "&New", self,
                shortcut=QKeySequence.New, statusTip="Create a new file",
                triggered=self.newFile)

        self.openAct = QAction(self.qtIcon.getIcon('folder_page_white.png'), "&Open...", self,
                shortcut=QKeySequence.Open, statusTip="Open an existing file",
                triggered=self.open)

        self.saveAct = QAction(self.qtIcon.getIcon('page_save.png'), "&Save", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QAction(self.qtIcon.getIcon('save_as.png'), "Save &As...", self,
                shortcut=QKeySequence.SaveAs,
                statusTip="Save the document under a new name",
                triggered=self.saveAs)

        self.exitAct = QAction("E&xit", self, shortcut=QKeySequence.Quit,
                statusTip="Exit the application",
                triggered=QApplication.instance().closeAllWindows)

        self.cutAct = QAction(self.qtIcon.getIcon('cut.png'), "Cu&t", self,
                shortcut=QKeySequence.Cut,
                statusTip="Cut the current selection's contents to the clipboard",
                triggered=self.cut)

        self.copyAct = QAction(self.qtIcon.getIcon('calendar_copy.png'), "&Copy", self,
                shortcut=QKeySequence.Copy,
                statusTip="Copy the current selection's contents to the clipboard",
                triggered=self.copy)

        self.pasteAct = QAction(self.qtIcon.getIcon('paste_plain.png'), "&Paste", self,
                shortcut=QKeySequence.Paste,
                statusTip="Paste the clipboard's contents into the current selection",
                triggered=self.paste)

        self.closeAct = QAction("Cl&ose", self,
                statusTip="Close the active window",
                triggered=self.mdiArea.closeActiveSubWindow)

        self.closeAllAct = QAction("Close &All", self,
                statusTip="Close all the windows",
                triggered=self.mdiArea.closeAllSubWindows)

        self.tileAct = QAction("&Tile", self, statusTip="Tile the windows",
                triggered=self.mdiArea.tileSubWindows)

        self.cascadeAct = QAction("&Cascade", self,
                statusTip="Cascade the windows",
                triggered=self.mdiArea.cascadeSubWindows)

        self.nextAct = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                statusTip="Move the focus to the next window",
                triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = QAction("Pre&vious", self,
                shortcut=QKeySequence.PreviousChild,
                statusTip="Move the focus to the previous window",
                triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        #action = self.fileMenu.addAction("Switch layout direction")
        #action.triggered.connect(self.switchLayoutDirection)
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)

        self.toolsMenu = self.menuBar().addMenu("&Tools")

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def findMdiChild(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

def except_hook(type, value, tback):
    # manage unhandled exception here
    print(crashSupport.errorReport())
    sys.__excepthook__(type, value, tback) # then call the default handler
    
if __name__ == '__main__':
    mainPyOneApp = QtWidgets.QApplication(sys.argv)
    mainPyOneWin = PyOneMainWindow(mainPyOneApp)
    mainPyOneWin.show()
    sys.excepthook = except_hook
    sys.exit(mainPyOneApp.exec_())