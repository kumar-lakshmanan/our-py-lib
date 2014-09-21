'''
Created on Sep 4, 2014

@author: Mukundan
'''

from user_interface import wgt_form1_general as formCode
from PyQt5 import QtCore, QtGui, QtWidgets
from general import PyQt
import sip
import core.lib


class Form(object):
    '''
    classdocs
    '''
    # parent = PyProjGen.PyProjGen()
    # ppjCopy = core.lib.ppg()
    parent = None
    mainWidget = None
    form = None

    def __init__(self, winHandle, currentObj, ppjCopy):
        '''
        Constructor
        '''

        self.mainWindow = winHandle
        self.ppjCopy = ppjCopy
        self.tools = PyQt.Tools(self.mainWindow)
        self.form = formCode.Ui_form()
        self.curObj = currentObj
        self.load()

    def populateUI(self):
        self.tools.setValue(self.form.lineEdit, self.curObj.projectName)
        self.tools.setValue(self.form.lineEdit_2, self.curObj.author)
        self.tools.setValue(self.form.lineEdit_3, self.curObj.location)

        if(self.curObj.projectType == 'pyqtwindows'):
            self.form.radioButton.setChecked(1)
        else:
            self.form.radioButton_2.setChecked(1)

        self.form.checkBox.setChecked(self.curObj.py2exe)

        self.form.lineEdit.setReadOnly(True)
        self.form.lineEdit_3.setReadOnly(True)

    def getUpdatedUIValues(self):
        self.curObj.projectName = self.tools.getValue(self.form.lineEdit)
        self.curObj.author = self.tools.getValue(self.form.lineEdit_2)
        self.curObj.location = self.tools.getValue(self.form.lineEdit_3)

        if(self.form.radioButton.isChecked()):
            self.curObj.projectType = 'pyqtwindows'
        else:
            self.curObj.projectType = 'commandline'

        self.curObj.py2exe = self.form.checkBox.isChecked()

        return self.curObj

    def load(self):
        # Load objects to core UI
        self.mainWidget = QtWidgets.QWidget(self.mainWindow)
        self.form.setupUi(self.mainWidget)
        self.mainWindow.gridLayout_5.addWidget(self.mainWidget, 0, 0, 1, 1)
        self.populateUI()

    def unload(self):
        # Unload objects from core UI
        self.mainWindow.gridLayout_5.removeWidget(self.mainWidget)
        sip.delete(self.mainWidget)
