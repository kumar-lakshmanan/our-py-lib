from PyQt4 import QtCore, QtGui
import sip

class MDI():


    def __init__(self, MDIArea=None):

        self.MDIArea = MDIArea
        self.SubWindows = []

    def showSubWindow(self, winObj, maximized=1, disableWinControls=0):

        if winObj in self.SubWindows:
            subWin = self.__getSubWindow(winObj)
            if subWin: subWin.show()
        else:
            self.MDIArea.addSubWindow(winObj)
            self.SubWindows.append(winObj)
            if disableWinControls:
                subWin = self.__getSubWindow(winObj)
                subWin.setWindowFlags(QtCore.Qt.SubWindow|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowTitleHint)

        if maximized:
            if sip.isdeleted(winObj):
               print 'Some how subwindow has been deleted. Hide Subwindow and ignore the event by overriding closeEvent of subwindow.'
            else:
                winObj.showMaximized()

        else:
            if sip.isdeleted(winObj):
               print 'Some how subwindow has been deleted. Hide Subwindow and ignore the event by overriding closeEvent of subwindow.'
            else:
                winObj.show()



    def __getSubWindow(self, winObj):

        subWinList = self.MDIArea.subWindowList()
        for eachWin in subWinList:
            for eachChild in eachWin.children():
                if type(winObj) == type(eachChild):
                    return eachWin

        return None