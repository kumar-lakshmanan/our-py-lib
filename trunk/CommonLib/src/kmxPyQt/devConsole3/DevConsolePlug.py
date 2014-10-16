from code import InteractiveInterpreter
from importlib.abc import InspectLoader
from threading import Thread
from time import strftime
import inspect
import os, sys
import traceback
# from PyQt5.Qsci import QsciScintilla
from PyQt5.uic import loadUi

# import __builtin__
# Remove cached custom modules from memory except preloaded IDE modules
# if __name__ == '__main__':
#     if globals().has_key('InitialModules'):
#          for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
#             del(sys.modules[CustomModule])
#     else:
#         InitialModules = sys.modules.keys()
# ErrorReport and CrashHandle - Call CrashHandle within uncontrolled expections

def errorReport(prittyPrint=1):
    traceback.print_exc(file=sys.stdout)
    return traceback.format_exc()
#
#     try:
#         TrackStack = inspect.stack()
#         ErrorReport = []
#         while TrackStack:
#         	FileName = TrackStack.tb_frame.f_code.co_filename
#         	FunctionName = TrackStack.tb_frame.f_code.co_name
#         	ErrorLine = TrackStack.tb_lineno
#         	TrackStack = TrackStack.tb_next
#         	ErrorReport.append([FileName, FunctionName, ErrorLine])
#         ErrorReport.append([sys.exc_info()[0], sys.exc_info()[1], 0])
#         if prittyPrint:
#             ErrorInfo = ''
#             for eachErrorLevel in ErrorReport:
#                 ErrorInfo += '\nFile: "' + str(eachErrorLevel[0]) + '", line ' + str(eachErrorLevel[2]) + ', in ' + str(eachErrorLevel[1])
#             return ErrorInfo
#         else:
#             return ErrorReport
#     except:
#         return 'Problem Preparing Error Report'

def crashHandle():
        # Prepare Report
        data = errorReport()
        f = open('CrashReport.txt', 'w')
        f.write(str(data))
        f.close()
        # Quit the program
        sys.exit(0)


# Safly Import Addition Modules
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
    self.qtConsole = DevConsolePlug.DevConsole(self.win, ShowPrint=True, ShowError=True, StatusBar=self.win.statusBar, AsDock=True, InitalizeScripts=True, SaveLogRefreshDays=30, btnIcon=dv, addObj=self)

    Arguments:s
    ShowPrint... Captures all print outputs to DevConsole o/p
    ShowError... Captures all error info outputs to DevConsole o/p

    Methods:
    appendPlainOutput(txt) ... Append plain text into DevConsole o/p
    appendSplOutput(txt) ... Append TimeStamped text into DevConsole o/p

    '''

    def __init__(self, parent=None, ShowPrint=True, ShowError=True, StatusBar=None, AsDock=False, SaveLogRefreshDays=30, ScriptsPath='Scripts/', InitalizeScripts=True, btnText="Console", btnIcon="F:/04/06/29.PNG", addObj=None):
        '''
        Parent - Pass QWIDGET based objects. Else I will create my own.
        ShowPrint - Redirect standard prints
        ShowError - Redirect standard errors
        StatusBar - Attach DevC Invoke button to this status bar else You should invoke DevC explicitly
        AsDock - If True creates DevC as a dock else as a dialog window
        '''

        self.addObj = addObj
        self.parent = parent
        self.SaveLogRefreshDays = SaveLogRefreshDays
        super(DevConsole, self).__init__(self.parent)

        self.qtTools = kmxQtCommonTools.CommonTools(self)
        self.ttls = kmxTools.Tools()
        self.qtTree = kmxQtTreeWidget.TreeWidget()

        if not self.parent:
            print ('No parent widget specified! Creating my own parent!')
            prn = QtWidgets.QWidget()
            prn.setObjectName('DevC')
            self.standalone = 1
        else:
            prn = self.parent
            self.standalone = 0

        if not hasattr(prn, 'addDockWidget') and not self.standalone:
            AsDock = False
            print ('Current parent does not support dock!')

        if ShowPrint: sys.stdout = self
        if ShowError: sys.stderr = self
        winObj = str(prn.objectName())
        # setattr(__builtin__, winObj if winObj else 'mainwin', prn)

        if AsDock:
            self.win = QtWidgets.QDockWidget(prn)
            base = QtWidgets.QWidget()
            self.setupUi(base)
            self.win.setWidget(base)
            prn.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.win)
        else:
            self.win = QtWidgets.QDialog(prn)
            self.setupUi(self.win)

        self.parent = prn
        self.inter = InteractiveInterpreter()
        self.inter.locals['dev'] = self
        self.inter.locals['self'] = self.parent
        self.inter.locals['addObj'] = self.addObj
        self.inter.locals['qtTools'] = self.qtTools

        self.win.setWindowIcon(prn.windowIcon())
        self.win.setWindowTitle('K Python Interpreter')

        self.PLX = Qsci.QsciLexerPython(self.win)
        self.ABS = Qsci.QsciAPIs(self.PLX)
        self.PLX.setAPIs(self.ABS)

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

        self.pushButton.setChecked(False)
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
        except:
            print (errorReport())

        try:
            if self.InitalizeScripts:
                self.execStartUp()
        except:
            print (errorReport())
            print ('Error on startup')


    def pluginSelected(self, *eve):
        selectedItem = eve[0]
        selected = selectedItem.text(0)
        script = '''z=%s(dev)
z.show()''' % selected
        self.runScript(script)

    def __del__(self):
        self.saveLog()

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

        code = '''import sys
sys.path.append("%s")
''' % (self.plugs)
        self.runScript(code)

        plugFiles = os.listdir(self.plugs)
        for eachFile in plugFiles:
            plugFile = os.path.join(self.plugs, eachFile)
            exts = os.path.splitext(plugFile)
            if(str(exts[1]).upper() == ".PY") and self.ttls.isPathFile(plugFile) and eachFile != 'devPluginBase.py':
                self.loadPlugin(plugFile)

    def loadPlugin(self, plugFile):
        modName = os.path.basename(plugFile).replace(os.path.splitext(plugFile)[1], '')
        item = self.qtTree.createItem(modName, plugFile)
        self.qtTree.addNewRoot(self.treeWidget, item)
        print("Loading Plugin Module... " + modName)
        content = self.ttls.fileContent(plugFile)
        self.runScript(content)

    def execStartUp(self, *arg):
        # General Script:
        spath = os.getcwd()
        spath1 = self.scriptPath
        spath2 = spath + '/' + spath1
        paths = ['\nmodulePathList.append("' + spath + '")'
                 '\nmodulePathList.append("' + spath1 + '")'
                 '\nmodulePathList.append("' + spath2 + '")'
                 ]
        paths = '\n'.join(paths)
        general = '''import sys
import os

modulePathList = []
%s

for modulePath in modulePathList:
    modulePath = os.path.normpath(modulePath)
    if modulePath not in sys.path and os.path.exists(modulePath):
        sys.path.append(modulePath)

''' % (paths)
        self.runScript(general)

        print ('Accessing startup script folder... %s' % self.scriptPath)
        if self.scriptPath:
            self.userSetup = os.path.join(self.scriptPath, 'userSetup.py')
            self.userSetup = self.userSetup if os.path.exists(self.userSetup) else os.path.join(self.scriptPath, 'userSetup.pyc')
            self.userSetup = self.userSetup if os.path.exists(self.userSetup) else ''
            if self.userSetup and os.path.exists(self.userSetup):
                f = open(self.userSetup, 'r')
                data = str(f.read())
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
            self.appendPlainOutput(inputs)
            self.appendLineOutput()
            self.runScript(inputs)
            self.cline.setText('')

    def btnRedirector(self):

        actingButton = self.parent.sender()

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
        try:
            inputs = str(script).replace('\r\n', '\n')
            res = self.inter.runcode(inputs)
            if res is not None:
                print(res)
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

    def saveLog(self):
        curdir = os.getcwd()
        logdir = curdir + '/ConsoleLog'
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        fileList = os.listdir(logdir)
        if len(fileList) == 30:
            fileToDelete = fileList[0]
            delFile = logdir + '/' + fileToDelete
            os.remove(delFile)

        print ('\nLog End Time: ' + str(strftime("%Y/%m/%d %H:%M:%S")))
        fileName = 'EVELOG' + strftime("%Y%m%d%H%M%S") + '.log'
        logFileName = logdir + '/' + fileName
        data = str(self.sciOutput.text())
        print(data)
        fs = open(logFileName, 'w')
        fs.write(data)
        fs.close()



if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        dc = DevConsole()
        dc.showEditor()
        app.exec_()
    except:
        crashHandle()
    sys.exit(1)
