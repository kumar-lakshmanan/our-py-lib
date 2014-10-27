from code import InteractiveInterpreter
from importlib.abc import InspectLoader
from threading import Thread
from time import strftime
import atexit
import inspect
import os, sys
import traceback

from PyQt5.Qsci import QsciScintilla
from PyQt5.uic import loadUi


def errorReport():
    traceback_lines = traceback.format_exc().split('\n')
    print('\n'.join(traceback_lines))
    for i in (2, 1, -1):
        traceback_lines.pop(i)
    info = '\n'.join(traceback_lines)
    print(info)
    return info


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
    from kmxPyQt import kmxQtCommonTools
    from kmxPyQt import kmxQtTreeWidget
    from kmxGeneral import kmxTools
    import inspect
    # import commandLine
    # import sysLogon
except:
    crashHandle()


class DevConsole(QtWidgets.QDialog, Ui_devConsole):

    '''
    DevConsole
    self.qtTools = kmxQtCommonTools.CommonTools(self.win, self.iconPath)
    self.qtTools.applyStyle()
    dv = self.qtTools.getIconString('/04/16/39.png')
    self.qtConsole = DevConsolePlug.DevConsole(self.win, ShowPrint=True, ShowError=True, StatusBar=self.win.statusBar, AsDock=True, InitalizeScripts=True, logCount=30, btnIcon=dv, addObj=self)

    Arguments:s
    ShowPrint... Captures all print outputs to DevConsole o/p
    ShowError... Captures all error info outputs to DevConsole o/p

    Methods:
    appendPlainOutput(txt) ... Append plain text into DevConsole o/p
    appendSplOutput(txt) ... Append TimeStamped text into DevConsole o/p

    '''

    def __init__(self, parent=None, ShowPrint=True, ShowError=True, StatusBar=None, AsDock=False, logCount=30, ScriptsPath='Scripts/', InitalizeScripts=True, btnText="Console", btnIcon="F:/04/06/29.PNG", addObj=None):
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

        self.standalone = 0 if self.parent else 1


        if self.standalone:
            print ('No parent specified! Creating standalone console!')
            self.parent = QtWidgets.QDialog()
            self.win = self.parent
            self.setupUi(self.win)
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

        print("Outputs Redirected. Check console log for furthur system messages.")
        if ShowPrint: sys.stdout = self
        if ShowError: sys.stderr = self

        self.inter = InteractiveInterpreter()
        self.inter.locals['dev'] = self
        self.inter.locals['self'] = self.parent
        self.inter.locals['addObj'] = self.addObj
        self.inter.locals['qtTools'] = self.qtTools

        self.win.setWindowIcon(self.parent.windowIcon())
        self.win.setWindowTitle('K Python Interpreter')

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
        self.btnLoadScript.clicked.connect(self.btnRedirector)
        self.btnSaveScript.clicked.connect(self.btnRedirector)
        self.cline.returnPressed.connect(self.commandLineExecute)
#        self.cline.keyPressEvent['event'].connect(self.commandLineKeyPress)
#        self.cline.textChanged['QString'].connect(MainWindow.setWindowTitle)
        # self.connect(self.cline, QtCore.SIGNAL("clicked()"), self.button_click)
#        QtCore.QObject.connect(sigSender, QtCore.SIGNAL(signal), FunctionToInvoke)
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

        # Plugin Lister
        self.treeWidget.headerItem().setText(0, "Dev Plugins")
        self.treeWidget.itemDoubleClicked.connect(self.pluginSelected)

        self.toolButton.setChecked(False)
        self.treeWidget.setVisible(False)

        print ('Simple Python Scripting Environment (SPSE)')
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

        print ('\n---------------------------------------\n')
        self.credit = '\n---------------------------------------\nAbout Python Interactive Interpreter! \nExpreimental Feature developed by \nL.Kumaresan \nFor ABX Studios\n---------------------------------------\n '

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
        print("Loading Plugins: " + self.plugs)
        self.addToSysPath(self.plugs)

        plugFiles = os.listdir(self.plugs)
        for eachFile in plugFiles:
            plugFile = os.path.join(self.plugs, eachFile)
            exts = os.path.splitext(plugFile)
            if(str(exts[1]).upper() == ".PY") and self.ttls.isPathFile(plugFile) and eachFile != 'devPluginBase.py':
                self.loadPlugin(plugFile)

#         self.addToSysPath(self.plugs)
#         nowListingFolder = os.path.basename(self.plugs)
#         nowParentItem = None
#         rootMaps = {}
#         rootMaps[nowListingFolder] = nowParentItem
#         for root, dirs, files in os.walk(self.plugs):
#             newListingFolder = os.path.basename(root)
#             if(nowListingFolder != newListingFolder):
#                 nowListingFolder = newListingFolder
#                 newParentItem = self.qtTree.createItem(nowListingFolder, "")
#                 rootMaps[nowListingFolder] = newParentItem
#                 self.qtTree.addItem(self.treeWidget, newParentItem, nowParentItem)
#                 nowParentItem = newParentItem
#
#
#             for item in files:
#                 scriptFile = os.path.join(root, item)
#                 print ("Current File: " + str(scriptFile))
#                 scriptPath = os.path.dirname(scriptFile)
#                 self.addToSysPath(scriptPath)
#                 plugFile = os.path.join(self.plugs, scriptFile)
#                 exts = str(os.path.splitext(plugFile)[1]).upper()
#                 if(exts == ".PY") and self.ttls.isPathFile(plugFile) and scriptFile != 'devPluginBase.py':
#                     self.loadPlugin(plugFile, nowParentItem)

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
        item = self.qtTree.createItem(modName, plugFile)
        if(parentTreeItem is None):
            plugTreeItem = self.qtTree.addNewRoot(self.treeWidget, item)
        else:
            plugTreeItem = self.qtTree.addChild(item, parentTreeItem)
        print("Loading Plugin Module... " + modName)
        content = self.ttls.fileContent(plugFile)
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
                f = open(self.userSetup, 'r')
                data = str(f.read())
                while ("\n\n" in data):
                    data = data.replace("\n\n", "\n")
                f.close()
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

    def btnRedirector(self):

        actingButton = self.parent.sender()

        if actingButton == self.toolButton:
            self.treeWidget.setVisible(self.toolButton.isChecked())

        if actingButton == self.stsBtnDebugger:
            if self.win.isVisible():
                self.win.hide()
            else:
                self.win.show()

        if actingButton == self.btnClearInput:
            self.sciInput.clear()

        if actingButton == self.btnClearOutput:
            self.sciOutput.clear()

        if actingButton == self.btnExecute:
            self.execute_Clicked()

        scpt = self.scriptPath
        scpt = scpt if os.path.exists(scpt) else 'D:'

        if actingButton == self.btnLoadScript:
            fileName = QtWidgets.QFileDialog.getOpenFileName(self.parent, 'Open python script file...', scpt, 'Python(*.py);;All Files (*)')
            if fileName and fileName[0] != '' and os.path.exists(fileName[0]):
                f = open(fileName[0], 'r')
                data = str(f.read())
                while ("\n\n" in data):
                    data = data.replace("\n\n", "\n")
                f.close()
                self.sciInput.clear()
                self.sciInput.setText(data)

        if actingButton == self.btnSaveScript:
            fileName = QtWidgets.QFileDialog.getSaveFileName(self.parent, 'Open python script file...', scpt, 'Python(*.py);;All Files (*)')
            if (fileName and fileName[0] != ''):
                f = open(fileName[0], 'w')
                f.write(str(self.sciInput.text()))
                f.close()

    def execute_Clicked(self):
        if not str(self.sciInput.text()) == '':
            inputs = str(self.sciInput.text()).rstrip()
            self.appendPlainOutput(inputs)
            self.appendLineOutput()
            self.runScript(inputs)
            self.sciInput.setText('')

    def runScript(self, script):
        self.ABS.add(script)
        self.ABS.prepare()
        try:
            command = str(script).replace('\r\n', '\n')
            try:
                res = eval(command, globals(), self.inter.locals)
            except SyntaxError:
                # exec (command, globals(), locals())
                res = self.inter.runcode(command)
            QtWidgets.QApplication.processEvents()
            if res is not None:
                print(repr(res))
        except SystemExit:
            print (errorReport())
        except:
            traceback_lines = traceback.format_exc().split('\n')
            # Remove traceback mentioning this file, and a linebreak
            for i in (2, 1, -1):
            # for i in (3, 2, 1, -1):
                traceback_lines.pop(i)
            print('\n'.join(traceback_lines))

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
        data = str(self.sciOutput.text())

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
