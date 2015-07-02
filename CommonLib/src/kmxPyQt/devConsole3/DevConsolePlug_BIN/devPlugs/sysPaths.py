'''
Created on Oct 14, 2014

@author: Mukundan
For DevConsole
'''
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import sys,os

class sysPaths(QDialog):
    '''
    classdocs
    '''

    def __init__(self,parent):
        '''
        Constructor
        '''
        # Parent is DEV <DEVCONSOLEPLUG>
        self.parent = parent
        self.uiName = "sysPaths.ui"
        super(sysPaths, self).__init__(parent)
        print ("Loaded!")
        self.setupUI(self.uiName)
        for path in sys.path:
            itm = QtWidgets.QListWidgetItem(path)
            self.listWidget.addItem(itm)
        self.show()
        # Connections
        #self.pushButton_2.clicked.connect(self.myFunc1)
        #self.pushButton_3.clicked.connect(self.myFunc2)
    def setupUI(self, uiFile):
        prepath = os.path.abspath(os.curdir)
        prepath = os.path.join(prepath, "devPlugs")
        uiFile = os.path.join(prepath, uiFile)
        loadUi(uiFile, self)
        self.setWindowTitle(self.__class__.__name__)        
        

    def myFunc1(self, *arg):
        print(self.lineEdit.text())
        print("FewMore")

    def myFunc2(self, *arg):
        print(self.lineEdit_2.text())

# src = 'C:/Users/Mukundan/Desktop/Test/Set1/'
# dst = 'C:/Users/Mukundan/Desktop/Test/Set2/'
# dev.ttls.copyFolder(src,dst)
