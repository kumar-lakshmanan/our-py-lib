from PyQt4 import QtCore, QtGui
import sys,os
import base64

currentFolder = os.getcwd()
parentFolder = os.path.dirname(currentFolder)
grandparentFolder = os.path.dirname(parentFolder) #Root

modulePathList = [
                  grandparentFolder   + '/PulseXML',
                  grandparentFolder   + '/UI_DB_lib',
                    ]

for eachModulePath in modulePathList:
    if sys.path.count(eachModulePath)==0:
        sys.path.append(eachModulePath)


import iniConfigReadWrite
import konfigWin




class konfig(QtGui.QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        konfigWin.Ui_konfigWin().setupUi(self)



app = QtGui.QApplication(sys.argv)
mainWin = konfig()
mainWin.show()
sys.exit(app.exec_())