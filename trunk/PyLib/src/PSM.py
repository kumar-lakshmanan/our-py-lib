from PyQt4 import QtGui, QtCore
import sys
import PyClient


class syz():

    def __init__(self, widget):
        self.temp1=sys.stdout
        self.temp2=sys.stderr
        sys.stdout=self
        sys.stderr=self
        self.widget=widget

    def write(self, *arg):
        txt = str(self.widget.toPlainText())
        self.widget.setText(txt + arg[0])

    def __del__(self):
        sys.stdout=self.temp1
        sys.stderr=self.temp2

class OutputUI(object):
    def __init__(self, parent=None):
        self.mwin = QtGui.QDialog(parent)
        self.mwin.setWindowTitle('Output')
        self.gridLayout = QtGui.QGridLayout(self.mwin)
        self.outBox = QtGui.QTextBrowser(self.mwin)
        self.gridLayout.addWidget(self.outBox, 0, 0, 1, 1)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.outBox.setFont(font)
        self.stds = syz(self.outBox)
        self.mwin.resize(500,200)
        self.mwin.show()

    def __del__(self):
        del(self.stds)


class PSMUI(object):

    def __init__(self):
        self.server='Z:/REPO/PulseServer/PyServer/PyServer.exe'
        self.mwin = QtGui.QMainWindow()
        self.baseUi(self.mwin)
        self._addModules()
        self.outputs = OutputUI(self.mwin)
        self.mwin.move(50,50)
        self.outputs.mwin.move(320,50)
        self.mwin.show()

    def baseUi(self, MainWindow):

        #Window
        MainWindow.resize(254, 472)
        self.centralwidget = QtGui.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setWindowTitle('PSM')

        #Grid
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(1)
        self.gridLayout.setSpacing(1)

        #Tools box & Added to layout
        self.moduleBox = QtGui.QToolBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.moduleBox.setFont(font)
        self.moduleBox.setFrameShape(QtGui.QFrame.NoFrame)
        self.moduleBox.setFrameShadow(QtGui.QFrame.Sunken)
        self.gridLayout.addWidget(self.moduleBox, 0, 0, 1, 1)

        #InitStyle
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Plastique'))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())



    def _addModules(self):
        pycl = PyClient.PythonClient(self.server)
        s = pycl.runServerGetData(['usermods'])
        for i in xrange(2,len(s)):
            self.__addModule(s[i])


    def _addFunctions(self, module, lstWidget):
        pycl = PyClient.PythonClient(self.server)
        s = pycl.runServerGetData([module,'functions'])
        for i in xrange(2,len(s)):
            self.__addFunction(lstWidget, s[i])

    def __addFunction(self, lstWidget, function):
        itm = QtGui.QListWidgetItem()
        itm.setText(function)
        lstWidget.addItem(itm)

    def __addModule(self, moduleName):
        page = QtGui.QWidget()
        pageLayout = QtGui.QGridLayout(page)
        pageLayout.setMargin(1)
        pageLayout.setSpacing(1)
        listWidget = QtGui.QListWidget(page)
        font = QtGui.QFont()
        font.setPointSize(9)
        listWidget.setFont(font)
        listWidget.setAlternatingRowColors(True)
        pageLayout.addWidget(listWidget, 0, 0, 1, 1)
        self._addFunctions(moduleName,listWidget)
        self.moduleBox.addItem(page, moduleName)


    def __setHiddenData(self, item, hiddenAttribute='hdata', value='Nothing'):
        setattr(item, str(hiddenAttribute), value)

    def __getHiddenData(self, item, hiddenAttribute='hdata'):
        return getattr(item, str(hiddenAttribute)) if hasattr(item, hiddenAttribute) else None

    def __del__(self):
        self.outputs.mwin.close()
        del(self.outputs)

def startPSM():
    app = QtGui.QApplication(sys.argv)
    temp1=sys.stdout
    temp2=sys.stderr
    z=PSMUI()
    exitCode = app.exec_()
    sys.stdout=temp1
    sys.stderr=temp2
    print 'Done'
    sys.exit(exitCode)

startPSM()