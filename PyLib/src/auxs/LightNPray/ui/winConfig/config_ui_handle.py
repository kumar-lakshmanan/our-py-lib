import sys
import os

##Remove cached custom modules from memory except preloaded IDE modules
if __name__ == '__main__':
    if globals().has_key('InitialModules'):
         for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
            del(sys.modules[CustomModule])
    else:
        InitialModules = sys.modules.keys()


#Global Packs
import sys
import os
from PyQt4 import QtCore, QtGui

#Common Packs
from UI_DB_lib.controls import qt_common
from UI_DB_lib.controls import tree_simple
from UI_DB_lib.controls import table
from UI_DB_lib.controls import override
from UI_DB_lib import iniConfigReadWrite

#UI Packs
from config_ui import Ui_config


class ConfigUI(QtGui.QDialog, Ui_config):

    def __init__(self, shpParent):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.shpParent = shpParent

        self.qtsCommon = qt_common.PyQtAppSupport(self)
        self.qtsTree = tree_simple.TreeSimple(self)
        self.qtsTable= table.Table(self)
        self.qtsOverride = override.Override(self)

        self.uiConnections()
        self.uiInitalize()

    def uiInitalize(self):

        self.qtsTable.format(self.tblSettings)
        self.qtsTable.initalDesign(self.tblSettings,['Setting','Value'])

    def uiConnections(self):

        self.connect(self.btnApply, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.btnCancel, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.trSections, QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.sigTreeSelection)
        self.connect(self.trSections, QtCore.SIGNAL('itemSelectionChanged()'), self.sigTreeSelection)
        self.qtsOverride.connectToTableCellEditor(self.tblSettings, self.sigTableEditStart, self.sigTableEditEnd)


    def sigTableEditStart(self, *arg):
        sender = self.sender()
        ##print sender
        ##print arg
        self.shpParent.optionEditStart(arg)

    def sigTableEditEnd(self, *arg):
        sender = self.sender()
        ##print sender
        ##print arg
        self.shpParent.optionEditEnd(arg)

    def sigTreeSelection(self, *arg):
        sender = self.sender()
        ##print sender
        ##print arg
        selItm = self.qtsTree.getSelectedItem(sender)
        itm = arg[0] if arg and arg[0] else selItm['Item']
        self.shpParent.populateSettings(str(itm.text(0)))

    def sigTableDblClick(self, *arg):
        sender = self.sender()
        ##print sender
        ##print arg
        self.shpParent.optionEditStart(arg[0])

    def sigTableSelection(self, *arg):
        sender = self.sender()
        ##print sender
        ##print arg
        self.shpParent.optionEditEnd()

    def sigTableKeyPress(self, *arg):
        sender = self.sender()
        ##print sender
        ##print arg[0]
        if self.qtsOverride.keyEventInfo(arg[0]) == 'Enter':
            self.shpParent.optionEditEnd(arg)

    def sigTableFocusOut(self, *arg):
        sender = self.sender()
        ##print sender
        ##print arg[0]
        self.shpParent.optionEditEnd(arg)

    def sigButtonClick(self):
        sender = self.sender()
        ##print sender
        ##print arg[0]
        if sender == self.btnApply:
            self.shpParent.doApply()

        if sender == self.btnCancel:
            self.shpParent.doClose()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ui = ConfigUI(app)
    ui.show()
    sys.exit(app.exec_())