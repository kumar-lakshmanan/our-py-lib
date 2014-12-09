from code import InteractiveInterpreter
from importlib.abc import InspectLoader
# from test.test_finalization import SelfCycleBase
from threading import Thread
from time import strftime
import atexit
import cgi
import inspect
import mimetypes
import os, sys
import re
import shutil
import traceback
import urllib

"""
In UI File REPLACE below line
from Qsci.qsciscintilla import QsciScintilla
with this line
from PyQt5.Qsci import QsciScintilla
"""
from PyQt5.Qsci import QsciScintilla
from PyQt5.uic import loadUi
import win32com
import win32com.client

from kmxPyQt import kmxQtMenuBuilder

def errorReport():
    # Show/Return Error Report
    traceback_lines = traceback.format_exc().split('\n')
    data = '\n'.join(traceback_lines)
    print(data)
    return data

def crashHandle():
        # Prepare Report
        data = errorReport()
        f = open('CrashReport.txt', 'w')
        f.write(str(data))
        f.close()
        sys.exit(0)

# Safly Import Additional Modules
try:
    from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
    # import lxml
    # import xlrw
    # import xlrd
except:
    crashHandle()


# Safly Import Custom Modules
try:
    from kmxPyQt.devConsole3.DCwin import Ui_devConsole
    from kmxPyQt import kmxQtTreeWidget
    from kmxPyQt import kmxQtCommonTools
    from kmxGeneral import kmxTools
except:
    crashHandle()


class DevConsole(QtWidgets.QMainWindow, QtWidgets.QDialog, Ui_devConsole):

    '''
    DevConsole
    self.qtTools = kmxQtCommonTools.CommonTools(self.win, self.iconPath)
    self.qtTools.applyStyle()
    dv = self.qtTools.getIconString('/04/16/39.png')
    self.qtConsole = DevConsolePlug.DevConsole(self.win,
                                                ShowPrint=True,
                                                ShowError=True,
                                                StatusBar=self.win.statusBar,
                                                AsDock=True,
                                                InitalizeScripts=True,
                                                logCount=30,
                                                btnIcon=dv,
                                                addObj=self)

    Arguments:
    ShowPrint... Captures all print outputs to DevConsole o/p
    ShowError... Captures all error info outputs to DevConsole o/p

    Methods:
    appendPlainOutput(txt) ... Append plain text into DevConsole o/p
    appendSplOutput(txt) ... Append TimeStamped text into DevConsole o/p

    '''

    def __init__(self, parent=None,
                    ShowPrint=True,
                    ShowError=True,
                    StatusBar=None,
                    AsDock=False,
                    logCount=30,
                    ScriptsPath='Scripts/',
                    InitalizeScripts=True,
                    btnText="Console",
                    btnIcon="F:/04/06/29.PNG",
                    addObj=None):
        '''
        Parent - Pass QWIDGET based objects. Else I will create my own.
        ShowPrint - Redirect standard prints
        ShowError - Redirect standard errors
        StatusBar - Attach DevC Invoke button to this status bar else You should invoke DevC explicitly
        AsDock - If True creates DevC as a dock else as a dialog window
        '''

        self.addObj = addObj
        self.parent = parent
        self.asDock = AsDock
        self.logCount = logCount
        self.history = []
        super(DevConsole, self).__init__(self.parent)
        atexit.register(self.writeToLog)

        self.qtTools = kmxQtCommonTools.CommonTools(self)
        self.ttls = kmxTools.Tools()
        self.qtTree = kmxQtTreeWidget.TreeWidget()
        self.qtMenu = kmxQtMenuBuilder.MenuBuilder()

        self.standalone = 0 if self.parent else 1

        if self.standalone:
            print ('No parent specified! Creating standalone console!')
            self.parent = self.win = QtWidgets.QMainWindow()
            self.win.resize(689, 504)
            self.mainWidget = QtWidgets.QWidget(self.win)
            self.setupUi(self.mainWidget)
            self.win.setCentralWidget(self.mainWidget)
            self.setStandAloneModeFeatures()
        elif self.asDock:
            if hasattr(self.parent, 'addDockWidget'):
                print ('Creating dock based console!')
                self.win = QtWidgets.QDockWidget(self.parent)
                base = QtWidgets.QWidget()
                self.setupUi(base)
                self.win.setWidget(base)
                self.parent.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.win)
            else:
                print ('Unsupported Parent for creating dock based console! ' + str(self.parent))
                print ('Connecting console to given parent as a dialog...' + str(self.parent))
                self.win = QtWidgets.QDialog(self.parent)
                self.setupUi(self.win)
        else:
            print ('Connecting console to given parent as a dialog...' + str(self.parent))
            self.win = QtWidgets.QDialog(self.parent)
            self.setupUi(self.win)

        print("Outputs Redirected to HPSE. Check HPSE console log for furthur system messages.")
        if ShowPrint: sys.stdout = self
        if ShowError: sys.stderr = self

        self.inter = InteractiveInterpreter()
        self.inter.locals['dev'] = self
        self.inter.locals['self'] = self.parent
        self.inter.locals['addObj'] = self.addObj
        self.inter.locals['qtTools'] = self.qtTools

        self.win.setWindowIcon(self.parent.windowIcon())
        self.win.setWindowTitle('HPSE')

        self.PLX = Qsci.QsciLexerPython(self)
        self.ABS = Qsci.QsciAPIs(self.PLX)
        # self.PLX.setAPIs(self.ABS)
        self.ABS.prepare()

        self.sciInput.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        self.sciInput.setLexer(self.PLX)
        self.sciInput.setAutoCompletionThreshold(1)
        self.sciInput.setAutoIndent(True)
        self.sciInput.setAutoCompletionFillupsEnabled(True)
        self.sciInput.setBraceMatching(Qsci.QsciScintilla.StrictBraceMatch)
        self.sciInput.setMarginLineNumbers(1, 1)
        self.sciInput.setMarginWidth(1, 45)

        self.sciOutput.setReadOnly(1)
        self.sciOutput.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        self.sciOutput.setLexer(self.PLX)
        self.sciOutput.setAutoCompletionThreshold(1)
        self.sciOutput.setAutoIndent(True)
        self.sciOutput.setAutoCompletionFillupsEnabled(True)
        self.sciOutput.setBraceMatching(Qsci.QsciScintilla.StrictBraceMatch)
        self.sciOutput.setMarginLineNumbers(1, 1)
        self.sciOutput.setMarginWidth(1, 45)

        # Connections
        self.btnClearInput.clicked.connect(self.btnRedirector)
        self.btnClearOutput.clicked.connect(self.btnRedirector)
        self.btnExecute.clicked.connect(self.btnRedirector)
        self.btnExecute_2.clicked.connect(self.btnRedirector)
        self.btnLoadScript.clicked.connect(self.btnRedirector)
        self.btnSaveScript.clicked.connect(self.btnRedirector)
        self.btnQuickSave.clicked.connect(self.btnRedirector)
        self.cline.returnPressed.connect(self.commandLineExecute)
        self.cline.__class__.keyReleaseEvent = self.commandLineKeyPress
        self.toolButton.clicked.connect(self.btnRedirector)

        if StatusBar:
            self.stsBtnDebugger = QtWidgets.QToolButton(self.parent)
            self.stsBtnDebugger.setText(btnText)
            self.stsBtnDebugger.setToolTip(btnText)
            self.stsBtnDebugger.setAutoRaise(1)
            self.stsBtnDebugger.setMaximumHeight(18)
            StatusBar.addPermanentWidget(self.stsBtnDebugger, 0)
            self.stsBtnDebugger.clicked.connect(self.btnRedirector)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(btnIcon), QtGui.QIcon.Normal, QtGui.QIcon.On)
            self.stsBtnDebugger.setIcon(icon)
        else:
            self.stsBtnDebugger = None

        self.win.hide()

        # Load File
        self.loadedFile = False
        self.loadedFileName = ''

        # Plugin Lister
        self.treeWidget.headerItem().setText(0, "DevPlugins")
        self.treeWidget.itemDoubleClicked.connect(self.pluginSelected)

        self.toolButton.setChecked(False)
        self.treeWidget.setVisible(False)

        print ('Handy Python Scripting Environment-')
        print ('--------------------------------')
        print ('Initiated!')

        print ('\nLog Start Time: ' + str(strftime("%Y/%m/%d %H:%M:%S")))
        print ('\n---------------------------------------\n')
        print ('*** Python %s on %s.***' % (sys.version, sys.platform))
        print (sys.copyright)
        print ('')
        print ('Platform: ' + sys.platform)
        print ('Version: ' + str(sys.getwindowsversion()))
        print ('FileSys encodeing: ' + str(sys.getfilesystemencoding()))

        drline = "\n---------------------------------------\n"
        self.credit = drline + '\nAbout HPSE:\nHandy Python Scripting Environment - Python Interactive Interpreter \nAn expreimental project developed by \nKumaresan Lakshmanan\nFor Quick Windows Automation. Date: Jan 12 2013\n' + drline
        print(self.credit)

        self.InitalizeScripts = InitalizeScripts
        self.scriptPath = ScriptsPath
        if self.scriptPath:
            if self.InitalizeScripts and self.scriptPath and not os.path.exists(self.scriptPath):
                os.makedirs(self.scriptPath)
        else:
            print ('Invalid script path!')

        self.plugs = os.path.join(os.path.abspath(os.curdir), "devPlugs")
        if self.plugs:
            self.ttls.makePath(self.plugs)
        else:
            print ('Invalid plug scripts path!')


        try:
            if self.ttls.isPathOK(self.plugs):
                self.execPlugin()
                self.toolButton.setChecked(True)
                self.treeWidget.setVisible(True)
        except:
            print (errorReport())

        try:
            if self.InitalizeScripts:
                self.execStartUp()
        except:
            print (errorReport())

    def setStandAloneModeFeatures(self):

        # Ready Menu Bar
        self.menubar = self.qtMenu.createMenuBar(self.win)
        self.mnuFile = self.qtMenu.createMenu(self.menubar, "File")
        self.mnuEdit = self.qtMenu.createMenu(self.menubar, "Edit")
        self.mnuRun = self.qtMenu.createMenu(self.menubar, "Run")
        self.mnuAbout = self.qtMenu.createMenu(self.menubar, "About")

        self.mnuFileLoadScript = self.qtMenu.createMenuItem(self.win, self.mnuFile, "Load Script", self.btnRedirector)
        self.mnuFileSaveScript = self.qtMenu.createMenuItem(self.win, self.mnuFile, "Save Script As", self.btnRedirector)
        self.qtMenu.createMenuItemSeperator(self.mnuFile)
        self.mnuFileQuit = self.qtMenu.createMenuItem(self.win, self.mnuFile, "Quit", self.btnRedirector)

        self.mnuEditClearOutput = self.qtMenu.createMenuItem(self.win, self.mnuEdit, "Clear Outputs", self.btnRedirector)
        self.mnuEditClearInput = self.qtMenu.createMenuItem(self.win, self.mnuEdit, "Clear Inputs", self.btnRedirector)

        self.mnuRunExecuteNoClear = self.qtMenu.createMenuItem(self.win, self.mnuRun, "Execute Script + No Clear", self.execute_Clicked_NoClear)
        self.mnuRunExecuteNoClear.setShortcut("Ctrl+Enter")
        self.mnuRunExecute = self.qtMenu.createMenuItem(self.win, self.mnuRun, "Execute Script", self.execute_Clicked)
        self.mnuRunExecute.setShortcut("Ctrl+Alt+Enter")

        self.mnuAboutHPSE = self.qtMenu.createMenuItem(self.win, self.mnuAbout, "About HPSE", self.btnRedirector)

        '''
        # Remove other buttons
        self.btnClearOutput.setVisible(0)
        self.toolButton.setVisible(0)
        self.line_5.setVisible(0)
        self.line_6.setVisible(0)
        self.line_7.setVisible(0)

        self.btnLoadScript.setVisible(0)
        self.btnSaveScript.setVisible(0)
        self.line.setVisible(0)

        self.btnClearInput.setVisible(0)
        self.btnExecute.setVisible(0)
        self.line_2.setVisible(0)
        self.line_3.setVisible(0)
        self.line_4.setVisible(0)

        self.sciOutput.resize(self.sciOutput.width(), self.sciOutput.height() + 90)
        self.label.setText("Output:")
        self.label_2.setText("Workspace:")
        self.label_3.setText("Quick Commands:")
        '''

    def pluginSelected(self, *eve):
        selectedItem = eve[0]
        selected = selectedItem.text(0)
        script = '''z=%s(dev)
z.show()''' % selected
        self.runScript(script)

    def showAttrs(self, obj):
        dlg = QtWidgets.QDialog(self.win)
        dlg.setWindowTitle(str(type(obj)))
        lt = QtWidgets.QListWidget(dlg)
        for each in inspect.getmembers(obj):
            itm = QtWidgets.QListWidgetItem()
            attrName = str(each[0])
            fnSymbol = ""
            if(inspect.isfunction(each[1]) or inspect.ismethod(each[1])):
                args = inspect.getargspec(each[1])[0]
                fnSymbol = "(" + str(args) + ")"
            itm.setText(attrName + fnSymbol)
            lt.addItem(itm)
        dlg.setFixedHeight(190)
        dlg.setFixedWidth(255)
        dlg.show()

    def execPlugin(self, *arg):

        '''
        To Refresh Plugin list
        :param arg:
        :return:
        '''
        print("Loading Plugins: " + self.plugs)
        self.addToSysPath(self.plugs)

        plugFiles = os.listdir(self.plugs)
        for eachFile in plugFiles:
            plugFile = os.path.join(self.plugs, eachFile)
            exts = os.path.splitext(plugFile)
            if(str(exts[1]).upper() == ".PY") and self.ttls.isPathFile(plugFile) and eachFile != 'devPluginBase.py' and not '_' in eachFile:
                self.loadPlugin(plugFile)

    def addToSysPath(self, path):
        path = os.path.abspath(path)
        print ("Adding path to system... " + path)
        code = '''import sys,os
path2Add="%s"
if path2Add not in sys.path and os.path.exists(path2Add):
    sys.path.append(path2Add)
''' % (path)
        self.runScript(code)

    def loadPlugin(self, plugFile, parentTreeItem=None):
        modName = os.path.basename(plugFile).replace(os.path.splitext(plugFile)[1], '')
        content = self.ttls.fileContent(plugFile)
        expecting = "class %s(devPluginBase.PluginBase):" % modName
        if(expecting in content):
            item = self.qtTree.createItem(modName, plugFile)
            if(parentTreeItem is None):
                plugTreeItem = self.qtTree.addNewRoot(self.treeWidget, item)
            else:
                plugTreeItem = self.qtTree.addChild(item, parentTreeItem)
            print("Loading Plugin Module... " + modName)
        else:
            print ("Expected Class Header '%s' not found in '%s' module !" % (expecting, modName))
            plugTreeItem = None
        self.runScript(content)

        return plugTreeItem

    def execStartUp(self, *arg):

        spath = os.getcwd()
        spath1 = self.scriptPath
        spath2 = os.path.join(spath, spath1)
        self.addToSysPath(spath)
        self.addToSysPath(spath1)
        self.addToSysPath(spath2)

        print ('Accessing startup script folder... %s' % self.scriptPath)
        if self.scriptPath:
            self.userSetup = os.path.join(self.scriptPath, 'userSetup.py')
            self.userSetup = self.userSetup if os.path.exists(self.userSetup) else os.path.join(self.scriptPath, 'userSetup.pyc')
            self.userSetup = self.userSetup if os.path.exists(self.userSetup) else ''
            if self.userSetup and os.path.exists(self.userSetup):
                data = self.ttls.fileContent(self.userSetup)
                self.sciInput.clear()
                self.sciInput.setText(data)
                print ('Parsing startup scripts...')
                self.runScript(data)
            else:
                print ('No Startup script file! ' + self.userSetup)
        else:
            print ('No Startup script folder!' + self.scriptPath)

    def commandLineExecute(self):
        if not str(self.cline.text()) == '':
            inputs = str(self.cline.text()).rstrip()
            self.appendPlainOutput(">>> " + inputs)
            self.appendLineOutput()
            self.addToHistory(inputs)
            self.runScript(inputs)
            self.cline.setText('')

    def commandLineKeyPress(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self.setCommand(self.getPrevHistoryEntry())
            return
        elif event.key() == QtCore.Qt.Key_Down:
            self.setCommand(self.getNextHistoryEntry())
            return

    def setCommand(self, command):
        self.cline.setText(command)

    def doQuickSave(self):
        if (self.loadedFile):
            fileName = self.loadedFileName
            data = str(self.sciInput.text()).replace('\r\n', '\n', 1000000000)
            self.ttls.writeFileContent(fileName, data)
            self.qtTools.showInfoBox('Quick Save', 'File Saved!')

    def btnRedirector(self):

        actingButton = self.parent.sender()
        scpt = self.scriptPath
        scpt = scpt if os.path.exists(scpt) else 'D:'

        if actingButton == self.toolButton:
            self.treeWidget.setVisible(self.toolButton.isChecked())
        elif actingButton == self.stsBtnDebugger:
            if self.win.isVisible():
                self.win.hide()
            else:
                self.win.show()
        elif actingButton == self.btnQuickSave:
            self.doQuickSave()
        elif (actingButton == self.btnClearInput or (self.standalone and actingButton == self.mnuEditClearInput)):
            self.sciInput.clear()
        elif (actingButton == self.btnClearOutput or (self.standalone and actingButton == self.mnuEditClearOutput)):
            self.sciOutput.clear()
            self.loadedFileName = ''
            self.loadedFile = False
            self.lblFileLoadInfo.setText('No File Loaded!')
        elif (actingButton == self.btnExecute):
            self.execute_Clicked()
        elif (actingButton == self.btnExecute_2):
            self.execute_Clicked_NoClear()
        elif (actingButton == self.btnLoadScript or (self.standalone and actingButton == self.mnuFileLoadScript)):
            fileName = QtWidgets.QFileDialog.getOpenFileName(self.parent, 'Open python script file...', scpt, 'Python(*.py);;All Files (*)')
            if fileName and fileName[0] != '' and os.path.exists(fileName[0]):
                fileName = fileName[0]
                self.loadedFileName = fileName
                self.loadedFile = True
                self.lblFileLoadInfo.setText(self.loadedFileName)
                data = str(self.ttls.fileContent(fileName))
                self.sciInput.clear()
                # data = QtGui.QStaticText(data)
                self.sciInput.setText(data)
        elif (actingButton == self.btnSaveScript or (self.standalone and actingButton == self.mnuFileSaveScript)):
            fileName = QtWidgets.QFileDialog.getSaveFileName(self.parent, 'Open python script file...', scpt, 'Python(*.py);;All Files (*)')
            if (fileName and fileName[0] != ''):
                fileName = fileName[0]
                data = str(self.sciInput.text()).replace('\r\n', '\n', 1000000000)
                self.ttls.writeFileContent(fileName, data)
        elif (self.standalone and actingButton == self.mnuAboutHPSE):
            print (self.credit)
        elif (self.standalone and actingButton == self.mnuFileQuit):
            sys.exit(0)
        else:
            print ('Unkown button' + str(actingButton))

    def execute_Clicked(self):
        self.doExecute()
        self.sciInput.setText('')

    def execute_Clicked_NoClear(self):
        self.doExecute()

    def doExecute(self):
        if not str(self.sciInput.text()) == '':
            inputs = str(self.sciInput.text()).rstrip()
            self.appendPlainOutput(inputs)
            self.appendLineOutput()
            self.ABS.add(inputs)
            self.ABS.prepare()
            self.runScript(inputs)

    def runScript(self, script):
        try:
            command = str(script).replace('\r\n', '\n')
            try:
                res = eval(command, globals(), self.inter.locals)
                #res = exec(command, globals(), self.inter.locals)
                #print('Done1')
            except SyntaxError:
                # self.inter.showtraceback()
                # exec (command, globals(), locals())
                res = self.inter.runcode(command)
                #print('Done2')
            QtWidgets.QApplication.processEvents()
            if res is not None:
                print(repr(res))
        except SystemExit:
            self.inter.showsyntaxerror()
            #print (errorReport())
            crashHandle()
            sys.exit(0)
        except:
            print (errorReport())

    def appendPlainOutput(self, txt):
        text = str(self.sciOutput.text())
        text += txt
        self.sciOutput.setText(text)
        text = str(self.sciOutput.text())
        vsb = self.sciOutput.verticalScrollBar()
        vsb.setValue(vsb.maximum())

    def appendLineOutput(self):
        text = str(self.sciOutput.text())
        text += '\n'
        self.sciOutput.setText(text)
        text = str(self.sciOutput.text())
        vsb = self.sciOutput.verticalScrollBar()
        vsb.setValue(vsb.maximum())

    def appendSplOutput(self, txt):
        nowtime = strftime("%Y-%m-%d %H:%M:%S")
        splOutput = str(nowtime) + ' : ' + str(txt)
        self.appendPlainOutput(splOutput)

    def appendLog(self, txt):
        self.appendLineOutput()
        text = str(self.sciOutput.text())
        text += txt
        self.sciOutput.setText(text)
        text = str(self.sciOutput.text())
        vsb = self.sciOutput.verticalScrollBar()
        vsb.setValue(vsb.maximum())
        pass

    # Standard Error and Print Capture
    def write(self, txt):
        self.appendPlainOutput(txt)
        vsb = self.sciOutput.verticalScrollBar()
        vsb.setValue(vsb.maximum())

    def showEditor(self, exec_=0):
        if exec_:
            self.win.exec_()
        else:
            self.win.show()

    def writeToLog(self):
        curdir = os.getcwd()
        logdir = curdir + '/ConsoleLog'
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        fileList = os.listdir(logdir)
        if len(fileList) >= self.logCount:
            fileToDelete = fileList[0]
            delFile = logdir + '/' + fileToDelete
            os.remove(delFile)

        print ('\nLog End Time: ' + str(strftime("%Y/%m/%d %H:%M:%S")))
        fileName = 'DC' + strftime("%Y%m%d%H%M%S") + '.log'
        logFileName = logdir + '/' + fileName
        data = str(self.sciOutput.text()).replace('\r\n', '\n', 1000000000)
        self.ttls.writeFileContent(logFileName, data)

    def getHistory(self):
        return self.history

    def setHisory(self, history):
        self.history = history

    def addToHistory(self, command):
        if command and (not self.history or self.history[-1] != command):
            self.history.append(command)
        self.history_index = len(self.history)

    def getPrevHistoryEntry(self):
        if self.history:
            self.history_index = max(0, self.history_index - 1)
            return self.history[self.history_index]
        return ''

    def getNextHistoryEntry(self):
        if self.history:
            hist_len = len(self.history)
            self.history_index = min(hist_len, self.history_index + 1)
            if self.history_index < hist_len:
                return self.history[self.history_index]
        return ''

if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        dc = DevConsole()
        dc.showEditor()
        sys.exit(app.exec_())
    except:
        crashHandle()
    sys.exit(1)
