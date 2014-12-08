'''
Created on Oct 14, 2014

@author: Mukundan
'''
import os

from PyQt5 import QtCore, QtGui, Qsci, QtWidgets

from kmxGeneral import kmxTools
from kmxPyQt import kmxQtCommonTools
import devPluginBase


class newPlugGenerator(devPluginBase.PluginBase):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        # Parent is DEV <DEVCONSOLEPLUG>
        self.parent = parent
        self.uiName = "newPlugGenerator.ui"
        super(newPlugGenerator, self).__init__(parent, self.uiName)
        print ("Loaded!")

        self.qtTools = kmxQtCommonTools.CommonTools(self)
        self.ttls = kmxTools.Tools()

        self.PLX = Qsci.QsciLexerPython(self)
        self.ABS = Qsci.QsciAPIs(self.PLX)
        # self.PLX.setAPIs(self.ABS)
        self.ABS.prepare()

        self.textEdit.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        self.textEdit.setLexer(self.PLX)
        self.textEdit.setAutoCompletionThreshold(1)
        self.textEdit.setAutoIndent(True)
        self.textEdit.setAutoCompletionFillupsEnabled(True)
        self.textEdit.setBraceMatching(Qsci.QsciScintilla.StrictBraceMatch)
        self.textEdit.setMarginLineNumbers(1, 1)
        self.textEdit.setMarginWidth(1, 45)

        self.textEdit_2.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        self.textEdit_2.setLexer(self.PLX)
        self.textEdit_2.setAutoCompletionThreshold(1)
        self.textEdit_2.setAutoIndent(True)
        self.textEdit_2.setAutoCompletionFillupsEnabled(True)
        self.textEdit_2.setBraceMatching(Qsci.QsciScintilla.StrictBraceMatch)
        self.textEdit_2.setMarginLineNumbers(1, 1)
        self.textEdit_2.setMarginWidth(1, 45)

        # Connections
        self.pushButton.clicked.connect(self.generate)
        # self.pushButton_3.clicked.connect(self.myFunc2)

        self.start()

    def start(self):
        path = os.path.join(self.ttls.getCurrentPath(), 'devPlugs')
        f1 = os.path.join(path, '_plugTemplate.ui')
        f2 = os.path.join(path, '_plugTemplate.py')
        f1c = self.ttls.fileContent(f1)
        f2c = self.ttls.fileContent(f2)
        self.textEdit.setText(f1c)
        self.textEdit_2.setText(f2c)

    def generate(self):
        plugName = self.qtTools.showInputBox("Plugin name", "Enter the new plugin name", "myPlug")
        f1n = plugName + '.ui'
        f2n = plugName + '.py'
        path = os.path.join(self.ttls.getCurrentPath(), 'devPlugs')
        f1 = os.path.join(path, f1n)
        f2 = os.path.join(path, f2n)
        f1c = self.textEdit.text()
        f2c = self.textEdit_2.text()
        print(f1)
        self.ttls.writeFileContent(f1, f1c)
        self.ttls.writeFileContent(f2, f2c)
        self.qtTools.showInfoBox("Done", "Plug Generated!")


    def myFunc2(self, *arg):
        print(self.lineEdit_2.text())

