from threading import Thread
from time import strftime
from code import InteractiveInterpreter
import os,sys
import __builtin__

#Remove cached custom modules from memory except preloaded IDE modules
if __name__ == '__main__':
    if globals().has_key('InitialModules'):
         for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
            del(sys.modules[CustomModule])
    else:
        InitialModules = sys.modules.keys()

#ErrorReport and CrashHandle - Call CrashHandle within uncontrolled expections
def errorReport(prittyPrint=1):
    try:
        TrackStack = sys.exc_traceback
        ErrorReport = []
        while TrackStack:
        	FileName = TrackStack.tb_frame.f_code.co_filename
        	FunctionName = TrackStack.tb_frame.f_code.co_name
        	ErrorLine =TrackStack.tb_lineno
        	TrackStack = TrackStack.tb_next
        	ErrorReport.append([FileName,FunctionName,ErrorLine])
        ErrorReport.append([sys.exc_info()[0],sys.exc_info()[1],0])
        if prittyPrint:
            ErrorInfo=''
            for eachErrorLevel in ErrorReport:
                ErrorInfo+= '\nFile: "' + str(eachErrorLevel[0]) + '", line ' + str(eachErrorLevel[2]) + ', in ' + str(eachErrorLevel[1])
            return ErrorInfo
        else:
            return ErrorReport
    except:
        return 'Problem Preparing Error Report'

def crashHandle():
        #Prepare Report
        data = errorReport()
        f = open('CrashReport.txt','w')
        f.write(str(data))
        f.close()
        #Quit the program
        sys.exit(0)


#Safly Import Addition Modules
try:
    from PyQt4 import QtCore, QtGui, Qsci
    #import lxml
    #import xlrw
    #import xlrd
except:
    crashHandle()


#Safly Import Custom Modules
try:
    from DCwin import Ui_devConsole
    #import commandLine
    #import sysLogon
except:
    crashHandle()


class DevConsole(QtGui.QDialog, Ui_devConsole):

    '''
    DevConsole

    Arguments:s
    ShowPrint... Captures all print outputs to DevConsole o/p
    ShowError... Captures all error info outputs to DevConsole o/p

    Methods:
    appendPlainOutput(txt) ... Append plain text into DevConsole o/p
    appendSplOutput(txt) ... Append TimeStamped text into DevConsole o/p

    '''

    def __init__(self,parent=None, ShowPrint=True, ShowError=True, StatusBar=None, AsDock=False, SaveLogRefreshDays=30, ScriptsPath='Scripts/', InitalizeScripts=True):
        '''
        Parent - Pass QWIDGET based objects. Else I will create my own.
        ShowPrint - Redirect standard prints
        ShowError - Redirect standard errors
        StatusBar - Attach DevC Invoke button to this status bar else You should invoke DevC explicitly
        AsDock - If True creates DevC as a dock else as a dialog window
        '''

        if not parent:
            print 'No parent widget specified! Creating my own parent!'
            prn = QtGui.QWidget()
            prn.setObjectName('DevC')
            self.standalone=1
        else:
            prn = parent
            self.standalone=0

        if not hasattr(prn,'addDockWidget') and not self.standalone:
            AsDock = False
            print 'Current parent does not support dock!'

        if ShowPrint: sys.stdout = self
        if ShowError: sys.stderr = self
        winObj = str(prn.objectName())
        setattr(__builtin__, winObj if winObj else 'mainwin', prn)

        if AsDock:
            self.win = QtGui.QDockWidget(prn)
            base = QtGui.QWidget()
            self.setupUi(base)
            self.win.setWidget(base)
            prn.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.win)
        else:
            self.win = QtGui.QDialog(prn)
            self.setupUi(self.win)

        self.parent = prn
        self.inter = InteractiveInterpreter()
        self.inter.locals['dev'] = self
        self.inter.locals['self'] = self.parent

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
        self.sciInput.setMarginLineNumbers(1,1)
        self.sciInput.setMarginWidth(1,45)

        self.sciOutput.setReadOnly(1)
        self.sciOutput.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        self.sciOutput.setLexer(self.PLX)
        self.sciOutput.setAutoCompletionThreshold(1)
        self.sciOutput.setAutoIndent(True)
        self.sciOutput.setAutoCompletionFillupsEnabled(True)
        self.sciOutput.setBraceMatching(Qsci.QsciScintilla.StrictBraceMatch)
        self.sciOutput.setMarginLineNumbers(1,1)
        self.sciOutput.setMarginWidth(1,45)

        #Connections
        self.parent.connect(self.btnClearInput,QtCore.SIGNAL('clicked()'),self.btnRedirector)
        self.parent.connect(self.btnClearOutput,QtCore.SIGNAL('clicked()'),self.btnRedirector)
        self.parent.connect(self.btnExecute,QtCore.SIGNAL('clicked()'),self.btnRedirector)
        self.parent.connect(self.btnLoadScript,QtCore.SIGNAL('clicked()'),self.btnRedirector)
        self.parent.connect(self.btnSaveScript,QtCore.SIGNAL('clicked()'),self.btnRedirector)
        self.parent.connect(self.cline,QtCore.SIGNAL('returnPressed()'),self.commandLineExecute)

        if StatusBar:
            self.stsBtnDebugger = QtGui.QToolButton()
            self.stsBtnDebugger.setText('DevConsole')
            self.stsBtnDebugger.setToolTip('DevConsole')
            self.stsBtnDebugger.setAutoRaise(1)
            self.stsBtnDebugger.setMaximumHeight(18)
            StatusBar.addPermanentWidget(self.stsBtnDebugger,0)
            self.parent.connect(self.stsBtnDebugger,QtCore.SIGNAL('clicked()'),self.btnRedirector)
        else:
            self.stsBtnDebugger = None

        self.win.hide()

        print 'Simple Python Scripting Environment (SPSE)'
        print '--------------------------------'
        print 'Initiated!'


        print '\nLog Start Time: ' + str(strftime("%Y/%m/%d %H:%M:%S"))
        print '\n---------------------------------------\n'
        print '*** Python %s on %s.***' % (sys.version,sys.platform)
        print sys.copyright
        print ''
        print 'Platform: ' + sys.platform
        print 'Version: ' + str(sys.getwindowsversion())
        print 'FileSys encodeing: ' + str(sys.getfilesystemencoding())

        print '\n---------------------------------------\n'
        self.credit = '\n---------------------------------------\nAbout Python Interactive Interpreter! \nExpreimental Feature developed by \nL.Kumaresan \nFor ABX Studios\n---------------------------------------\n '

        self.InitalizeScripts=InitalizeScripts
        self.SaveLogRefreshDays=SaveLogRefreshDays
        self.scriptPath = ScriptsPath
        if self.scriptPath:
            if self.InitalizeScripts and self.scriptPath and not os.path.exists(self.scriptPath):
                os.makedirs(self.scriptPath)
        else:
            print 'Invalid script path!'

        try:
            if self.InitalizeScripts:
                self.execStartUp()
        except:
            print errorReport()
            print 'Error on startup'

    def __del__(self):
        self.saveLog()

    def execStartUp(self,*arg):

        #General Script:
        spath = os.getcwd()
        spath1 =  self.scriptPath
        spath2 = spath + '/' + spath1
        paths = ['\nmodulePathList.append("' + spath + '")'
                 '\nmodulePathList.append("' + spath1 + '")'
                 '\nmodulePathList.append("' + spath2 + '")'
                 ]
        paths = '\n'.join(paths)
        general =  '''import sys
import os

modulePathList = []
%s

for modulePath in modulePathList:
    modulePath = os.path.normpath(modulePath)
    if modulePath not in sys.path and os.path.exists(modulePath):
        sys.path.append(modulePath)

''' % (paths)
        self.runScript(general)

        print 'Accessing startup script folder... %s' % self.scriptPath
        if self.scriptPath:
            self.userSetup = os.path.join(self.scriptPath,'userSetup.py')
            self.userSetup = self.userSetup if os.path.exists(self.userSetup) else os.path.join(self.scriptPath,'userSetup.pyc')
            self.userSetup = self.userSetup if os.path.exists(self.userSetup) else ''
            if self.userSetup and os.path.exists(self.userSetup):
                f = open(self.userSetup,'r')
                data = str(f.read())
                f.close()
                self.sciInput.clear()
                self.sciInput.setText(data)
                print 'Parsing startup scripts...'
                self.runScript(data)
            else:
                print 'No Startup script file!'
        else:
            print 'No Startup script folder!'

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

        if actingButton == self.btnLoadScript:
            scpt = self.scriptPath
            scpt = scpt if os.path.exists(scpt) else 'D:'
            fileName = QtGui.QFileDialog.getOpenFileName(self.parent, 'Open python script file...',scpt,'All Files (*)')
            if os.path.exists(fileName):
                f = open(fileName,'r')
                data = str(f.read())
                f.close()
                self.sciInput.clear()
                self.sciInput.setText(data)

        if actingButton == self.btnSaveScript:
            fileName = QtGui.QFileDialog.getSaveFileName(self.parent, 'Open python script file...','D:','All Files (*)')
            f = open(fileName+'.py','w')
            f.write(str(self.sciInput.text()))
            f.close()

    def execute_Clicked(self):
        if not str(self.sciInput.text()) == '':
            inputs = str(self.sciInput.text()).rstrip()
            self.appendPlainOutput(inputs)
            self.appendLineOutput()
            self.runScript(inputs)
            self.sciInput.setText('')

    def runScript(self,script):
        try:
            inputs = str(script).replace('\r\n','\n')
            self.inter.runcode(inputs)
        except:
            print errorReport()

    def appendPlainOutput(self,txt):
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

    def appendSplOutput(self,txt):
        nowtime = strftime("%Y-%m-%d %H:%M:%S")
        splOutput = str(nowtime) + ' : ' + str(txt)
        self.appendPlainOutput(splOutput)

    def appendLog(self,txt):
        self.appendLineOutput()
        text = str(self.sciOutput.text())
        text += txt
        self.sciOutput.setText(text)
        text = str(self.sciOutput.text())
        vsb = self.sciOutput.verticalScrollBar()
        vsb.setValue(vsb.maximum())

    #Standard Error and Print Capture
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
        if len(fileList)==self.SaveLogRefreshDays:
            fileToDelete = fileList[0]
            delFile = logdir + '/' + fileToDelete
            os.remove(delFile)

        print '\nLog End Time: ' + str(strftime("%Y/%m/%d %H:%M:%S"))
        fileName = 'EVELOG'+strftime("%Y%m%d%H%M%S")+'.log'
        logFileName = logdir +'/'+ fileName
        data = str(self.sciOutput.text())
        fs = open(logFileName,'w')
        fs.write(data)
        fs.close()



if __name__ == '__main__':
    try:
        app = QtGui.QApplication(sys.argv)
        dc = DevConsole()
        dc.showEditor()
        app.exec_()
    except:
        crashHandle()
    sys.exit(1)