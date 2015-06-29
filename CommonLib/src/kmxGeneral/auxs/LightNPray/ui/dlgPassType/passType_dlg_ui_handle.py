import sys
##Remove cached custom modules from memory except preloaded IDE modules
if __name__ == '__main__':
    if globals().has_key('InitialModules'):
         for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
            del(sys.modules[CustomModule])
    else:
        InitialModules = sys.modules.keys()

#BuiltIn Packs
import os

#Global Packs
from PyQt4 import QtCore, QtGui

#UI Packs
from passType_dlg_ui import Ui_Dialog

#Local Packs
from UI_DB_lib.controls import qt_common
from UI_DB_lib.controls import tree_simple
from UI_DB_lib.controls import list_box
from UI_DB_lib.controls import table
from UI_DB_lib.controls import override
from LightNPray.lib import dummy_parent
#Data Packs
#import attribute_data

class CustomDialogConfigure():
    def __init__(self):
        self.additionalData = []
        self.header = 'HEADER'
        self.message = 'MESSAGE'
        self.btnOKLabel = 'OK'
        self.btnCancelLable = 'Cancel'

class PassTypeDialog(QtGui.QDialog, Ui_Dialog):

    def __init__(self, cParent, dlgConfigObj = None):
        #Default
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.sigConnection()
        self.dlgConfig = CustomDialogConfigure() if not dlgConfigObj else dlgConfigObj

        #Custom
        self.cParent = dummy_parent.DummyParent(cParent) if not hasattr(cParent,'Config') else cParent
        self.App = self.cParent.App
        self.Config = self.cParent.Config
        self.Common = self.cParent.Common
        self.qtsCommon = qt_common.PyQtAppSupport(self, self.Config.AppInfo.IconPath)
        self.qtsList = list_box.List(self)

    def sigConnection(self):
        #Default
        self.connect(self.btnOK, QtCore.SIGNAL('clicked()'), self.__doOK )
        self.connect(self.btnCancel, QtCore.SIGNAL('clicked()'), self.__doCancel )

        self.connect(self.listWidget, QtCore.SIGNAL('itemSelectionChanged()'), self.sigListItemChange )

    def sigListItemChange(self):
        itm = self.qtsList.getSelectedItemLabel(self.listWidget)
        self.le1.setText(itm)

    def initialize(self):
        #Default
        self.ok=False
        self.cancel=True
        self.setWindowTitle(self.dlgConfig.header)
        self.label_3.setText(self.dlgConfig.message)
        self.btnOK.setText(self.dlgConfig.btnOKLabel)
        self.btnCancel.setText(self.dlgConfig.btnCancelLable)
        self.setWindowFlags(QtCore.Qt.Window|QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowTitleHint)

        #Custom
        self.qtsCommon.setIconForItem(self.btnOK, self.Config.Icon.GenericSave)
        self.qtsCommon.setIconForItem(self.btnCancel, self.Config.Icon.GenericCancel)


        self.__populate()

    def __populate(self):
        lst = self.listWidget
        self.qtsList.populateList(lst, self.dlgConfig.additionalData[0])

    def __doOK(self):
        self.ok=True
        self.cancel=False
        self.close()

    def __doCancel(self):
        self.ok=False
        self.cancel=True
        self.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    cfg = CustomDialogConfigure()
    cfg.additionalData = [['KUMAR','TEST','WIN'], ]
    cfg.header = 'Add Pass Scenes'
    cfg.message = 'Please, Select pass type anad add Pass Scene'
    cfg.btnOKLabel = 'Add'
    cd = PassTypeDialog(app, cfg)
    cd.initialize()
    cd.show()
    ec = app.exec_()
    print cd.le1.text()
    sys.exit(ec)