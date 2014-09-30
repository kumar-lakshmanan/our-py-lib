'''
Created on Aug 27, 2014

@author: Mukundan
'''
from PyQt5 import QtCore, QtGui, QtWidgets

class Tools(object):
    '''
    classdocs
    '''
    CallingUI = None

    def __init__(self, CallingUI):
        '''
        Constructor
        '''
        self.CallingUI = CallingUI
        
    def getFilexx(self, Title='Select a file to open...', FileName='Select File', FileType='All Files (*);;Excel Files (*.xls);;Text Files (*.txt)'):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self.CallingUI, str(Title), FileName, str(FileType))
        if(fileName[0] == ""): return ""
        return fileName[0]
           
