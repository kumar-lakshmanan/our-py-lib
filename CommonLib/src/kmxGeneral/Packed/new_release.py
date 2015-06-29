import os, sys
from PyQt4 import QtGui, QtCore
from new_release_ui import Ui_Dialog
import software_versioning as sv

class NewRelease(QtGui.QDialog, Ui_Dialog):

    def __init__(self, logXml=None):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        self.xml=logXml
        self.svc=None
        self.appName=''
        self.appDispName=''

        if os.path.exists(self.xml):
            self.svc = sv.versioning(self.xml)
            self.appName = self.svc.getAppName()
            self.appDispName = self.appName.upper()

        self.connect(self.btnClose, QtCore.SIGNAL('clicked()'), self.close)
        self.connect(self.btnRelease, QtCore.SIGNAL('clicked()'), self.doRelease)


    def doRelease(self):
        changeLogs = str(self.txtChange.toPlainText())
        if changeLogs:
            changeLogs = list(changeLogs.split('\n'))
            rtype = self._rtype()

            if len(changeLogs) and rtype:
                self.svc.releaseNewVersion(rtype, changeLogs)
                print 'Released'

            self.close()

    def _rtype(self):

        if self.rbMajor.isChecked():
            return 1


        if self.rbMinor.isChecked():
            return 2


        if self.rbPatch.isChecked():
            return 3


        if self.rbDev.isChecked():
            return 4

        return 0


def show(arg):

    file_ = arg[0] if len(arg)>0 else ''
    if file_:
        app = QtGui.QApplication(sys.argv)
        rl = NewRelease(file_)
        rl.show()
        app.exec_()



if '__main__' == __name__:
##    arg = sys.argv
##    arg.remove(arg[0])
##    main(arg)

    show(['Z:/REPO/PulseServer/ProgramFiles/SHIP/ReleaseLog.xml'])