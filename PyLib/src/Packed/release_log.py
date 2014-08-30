import os, sys
from PyQt4 import QtGui, QtCore
from release_log_ui import Ui_MainWindow
import software_versioning as sv
import new_release

class ReleaseLog(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, logXml=None, state=0):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        self.xml=logXml
        self.svc=None
        self.appName=''
        self.appDispName=''
        self.state = state
        if os.path.exists(self.xml):
            self.svc = sv.versioning(self.xml)
            self.appName = self.svc.getAppName()
            self.appDispName = self.appName.upper()
            self.lblAppName.setText(self.appDispName)

            self.__loadCurrentVersion()
            self.__loadChangeLog()

        self.btnRelease.setEnabled(self.state)
        self.connect(self.btnClose, QtCore.SIGNAL('clicked()'), self.close)
        self.connect(self.btnRelease, QtCore.SIGNAL('clicked()'), self.doRelease)

    def doRelease(self):
        n = new_release.NewRelease(self.xml)
        n.exec_()
        self.svc = sv.versioning(self.xml)
        self.__loadCurrentVersion()
        self.__loadChangeLog()

    def __loadCurrentVersion(self):
        vr = self.svc.getRecentVersion(1)
        date = '%s-%s-%s' % (str(vr[5])[0:4], str(vr[5])[4:6], str(vr[5])[6:8])
        info = 'Application: ' + self.appDispName
        info += '\nVersion: %s.%s.%s' % (str(vr[0]).zfill(1),str(vr[1]).zfill(2),str(vr[2]).zfill(3))
        info += '\nBuild No: %s \nRelease Date: %s' % (str(vr[3]).zfill(4), date)
        info += '\nRelease Machine: %s \nRelease Owner: %s' % (vr[6], vr[7])
        info += '\n\nRecent Changes:'
        for i in vr[8]:
            info += '\n%s' % i
        self.txtCurrent.setText(info)

    def __loadChangeLog(self):
        vrx = self.svc.getVersions()
        info = ''
        for vr in vrx:
            date = '%s-%s-%s' % (str(vr[5])[0:4], str(vr[5])[4:6], str(vr[5])[6:8])
            info += '\nVersion: %s.%s.%s' % (str(vr[0]).zfill(1),str(vr[1]).zfill(2),str(vr[2]).zfill(3))
            info += '\nBuild No: %s \nRelease Date: %s' % (str(vr[3]).zfill(4), date)
            info += '\nRelease Machine: %s \nRelease Owner: %s' % (vr[6], vr[7])
            info += '\nRecent Changes:'
            for i in vr[8]:
                info += '\n--%s' % i
            info += '\n-----------------------------------------------------------------'

        self.txtLog.setText(info)


def show(arg):

    file_ = arg[0] if len(arg)>0 else ''
    if file_:
        app = QtGui.QApplication(sys.argv)
        rl = ReleaseLog(file_, 0)
        rl.show()
        app.exec_()

def edit(arg):

    file_ = arg[0] if len(arg)>0 else ''
    if file_:
        app = QtGui.QApplication(sys.argv)
        rl = ReleaseLog(file_, 1)
        rl.show()
        app.exec_()



if '__main__' == __name__:
##    arg = sys.argv
##    arg.remove(arg[0])
##    main(arg)

    edit(['Z:/REPO/PulseServer/ProgramFiles/SHIP/ReleaseLog.xml'])