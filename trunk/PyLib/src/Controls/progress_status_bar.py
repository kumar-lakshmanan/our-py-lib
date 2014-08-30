from PyQt4 import QtGui, QtCore

class ProgressStatusBar():

    def __init__(self, CallingUi, statusBar, infoBar=False, fixWidth=200):

        self.CallingUi = CallingUi
        self.statusBar = statusBar
        self.info = 'Please Wait...!'
        self.probar = QtGui.QProgressBar(self.CallingUi)
        if fixWidth: self.probar.setMaximumWidth(fixWidth)
        self.probar.setFormat('Processing...%p%')
        self.infobar = QtGui.QLabel(self.CallingUi)
        self.probar.setVisible(0)
        self.infobar.setVisible(0)
        self.maximum = 100
        self.current = 0
        self.statusBar.addWidget(self.probar,1)
        if infoBar:
            self.statusBar.addWidget(self.infobar,0)

    def pbInitialize(self,maximum = 100,infobar=True):
        self.maximum = maximum
        self.current = 0
        self.probar.setVisible(1)
        self.infobar.setVisible(1)

    def pbDefIncr(self,info=''):
        self.current+=1
        proval = self.current * 100/self.maximum
        self.probar.setValue(proval)
        self.infobar.setText(info if info else self.info)

    def pbIncr(self, current, info=''):
        self.current = current
        proval = self.current * 100/self.maximum
        self.probar.setValue(proval)
        self.infobar.setText(info if info else self.info)

    def pbClose(self):
        self.current = 0
        self.probar.setValue(100)
        self.infobar.setText('Done!')
        self.probar.setVisible(0)
        self.infobar.setVisible(0)