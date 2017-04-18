'''
Created on Oct 23, 2015

@author: MUKUND
'''
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt, )
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget, )
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
import os

class PyOneScript(QsciScintilla):
    sequenceNumber = 1  
    ARROW_MARKER_NUM = 8
    
    def __init__(self):
        super(PyOneScript, self).__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.isUntitled = True

        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)
        
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.on_margin_clicked)
        self.markerDefine(QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"), self.ARROW_MARKER_NUM)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setEolMode(Qsci.QsciScintilla.EolUnix)
        self.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setAutoIndent(True)
        self.setIndentationsUseTabs(True)
        self.setTabWidth(4)
        self.setAutoCompletionFillupsEnabled(True)
        self.setBraceMatching(Qsci.QsciScintilla.StrictBraceMatch)
        self.setMarginLineNumbers(1, 1)
        self.setMarginWidth(1, 35)
        self.setUtf8(True)
        self.setEolVisibility(False)
        self.setMinimumSize(600, 450)        
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        self.lexer = QsciLexerPython()
        self.lexer.setDefaultFont(font)

        self.setLexer(self.lexer)
        self.sense = Qsci.QsciAPIs(self.lexer)
        self.sense.prepare()        

        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)        

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def newFile(self):
        self.isUntitled = True
        self.curFile = "PyOne%d.py" % PyOneScript.sequenceNumber
        PyOneScript.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')

        self.modificationChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "PyOne",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return False

        instr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.setText(instr.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)

        self.modificationChanged.connect(self.documentWasModified)

        return True

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        scpt = self.scriptsPath
        scpt = scpt if os.path.exists(scpt) else 'C:'
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save python script file...', scpt, 'Python(*.py);;All Files (*)', options=options)        
        #fileName, _ = QFileDialog.getSaveFileName(self, "Save As", self.curFile)
        if not fileName:
            return False

        return self.saveFile(fileName)

    def saveFile(self, fileName):
        file = QFile(fileName)

        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "PyOne",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.text()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        return True

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def currentFile(self):
        return self.curFile

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def documentWasModified(self):
        self.setWindowModified(self.isModified())

    def maybeSave(self):
        if self.isModified():
            ret = QMessageBox.warning(self, "PyOne",
                    "'%s' has been modified.\nDo you want to save your "
                    "changes?" % self.userFriendlyCurrentFile(),
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if ret == QMessageBox.Save:
                return self.save()

            if ret == QMessageBox.Cancel:
                return False

        return True

    def setCurrentFile(self, fileName):
        self.curFile = QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        self.setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()