'''
Created on Oct 14, 2014

@author: Mukundan
'''
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
import devPluginBase
import sys

class sysPaths(devPluginBase.PluginBase):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        # Parent is DEV <DEVCONSOLEPLUG>
        self.parent = parent
        self.uiName = "sysPaths.ui"
        super(sysPaths, self).__init__(parent, self.uiName)
        print ("Loaded!")
   
        for path in sys.path:
            itm = QtWidgets.QListWidgetItem(path)
            self.listWidget.addItem(itm)
             
        # Connections
        #self.pushButton_2.clicked.connect(self.myFunc1)
        #self.pushButton_3.clicked.connect(self.myFunc2)
        
        

    def myFunc1(self, *arg):
        print(self.lineEdit.text())

    def myFunc2(self, *arg):
        print(self.lineEdit_2.text())

# src = 'C:/Users/Mukundan/Desktop/Test/Set1/'
# dst = 'C:/Users/Mukundan/Desktop/Test/Set2/'
# dev.ttls.copyFolder(src,dst)
