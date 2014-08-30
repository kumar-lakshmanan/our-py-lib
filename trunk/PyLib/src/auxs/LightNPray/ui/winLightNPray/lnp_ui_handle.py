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
from LightNPray.lib import dummy_parent

#UI Packs
from lnp_ui import Ui_MainWindow


class LightNPrayUI(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, cParent):
        self.cParent = dummy_parent.DummyParent(cParent) if not hasattr(cParent,'Config') else cParent
        self.App = self.cParent.App
        self.Config = self.cParent.Config
        self.Common = self.cParent.Common

        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.qtsCommon = qt_common.PyQtAppSupport(self, iconPath = self.Config.AppInfo.IconPath)
        self.qtsTree = tree_simple.TreeSimple(self)
        self.qtsTable= table.Table(self)
        self.qtsOverride = override.Override(self)

        self.uiInitalize()
        self.uiConnections()
        self.uiDesign()

    def uiInitalize(self):
        #Window Redesign
        self.setWindowTitle(self.cParent.Config.AppInfo.FullName)
        self.qtsCommon.setSkin(self.cParent.Config.LastUsed.Theme)
        self.actionSeq_N_Shots.setChecked(1)
        self.actionRender_Settings.setChecked(1)
        self.actionLogs.setChecked(0)
        self.dckSNS.setVisible(1)
        self.dckRenderSettings.setVisible(1)
        self.dckLog.setVisible(0)
        self.qtsCommon.uiLayoutRestore(self.Config.LastUsed.Layout)

        self.btnPassDefSave.setEnabled(0)
        self.btnBuildFilesSave.setEnabled(0)
        self.actionSave.setEnabled(0)

    def uiDesign(self):
        self.qtsCommon.setIconForItem(self.btnPassTypeAdd, self.Config.Icon.GenericPlus)
        self.qtsCommon.setIconForItem(self.btnPassTypeRemove, self.Config.Icon.GenericMinus)
        self.qtsCommon.setIconForItem(self.btnAOVAdd, self.Config.Icon.GenericPlus)
        self.qtsCommon.setIconForItem(self.btnAOVRemove, self.Config.Icon.GenericMinus)
        self.qtsCommon.setIconForItem(self.btnPassAdd, self.Config.Icon.GenericPlus)
        self.qtsCommon.setIconForItem(self.btnPassRemove, self.Config.Icon.GenericMinus)
        self.qtsCommon.setIconForItem(self.btnPassSceneAdd, self.Config.Icon.GenericPlus)
        self.qtsCommon.setIconForItem(self.btnPassSceneRemove, self.Config.Icon.GenericMinus)
        self.qtsCommon.setIconForItem(self.btnBuildFilesBuild, self.Config.Icon.Flag)
        self.qtsCommon.setIconForItem(self.btnBuildFilesSave, self.Config.Icon.GenericSave)
        self.qtsCommon.setIconForItem(self.btnRenderFilesRender, self.Config.Icon.Online)
        self.qtsCommon.setIconForItem(self.btnPassDefSave, self.Config.Icon.GenericSave)
        self.qtsCommon.setIconForItem(self.actionLogs, self.Config.Icon.Logs)
        self.qtsCommon.setIconForItem(self.actionQuit, self.Config.Icon.Quit)
        self.qtsCommon.setIconForItem(self.actionRender_Settings, self.Config.Icon.Render_Settings)
        self.qtsCommon.setIconForItem(self.actionSave, self.Config.Icon.GenericSave)
        self.qtsCommon.setIconForItem(self.actionSeq_N_Shots, self.Config.Icon.Seq_N_Shots)
        self.qtsCommon.setIconForItem(self.actionPass_Definition, self.Config.Icon.PassDefinition)
        self.qtsCommon.setIconForItem(self.actionBuild_Files, self.Config.Icon.BuildFiles)
        self.qtsCommon.setIconForItem(self.actionRender_Files, self.Config.Icon.RenderFiles)

    def uiConnections(self):
        self.connect(self.dckLog, QtCore.SIGNAL('visibilityChanged(bool)'), self.sigDock)
        self.connect(self.dckRenderSettings, QtCore.SIGNAL('visibilityChanged(bool)'), self.sigDock)
        self.connect(self.dckSNS, QtCore.SIGNAL('visibilityChanged(bool)'), self.sigDock)
        self.connect(self.actionSave, QtCore.SIGNAL('triggered(bool)'), self.sigAction)
        self.connect(self.actionQuit, QtCore.SIGNAL('triggered(bool)'), self.sigAction)
        self.connect(self.actionSeq_N_Shots, QtCore.SIGNAL('triggered(bool)'), self.sigAction)
        self.connect(self.actionRender_Settings, QtCore.SIGNAL('triggered(bool)'), self.sigAction)
        self.connect(self.actionLogs, QtCore.SIGNAL('triggered(bool)'), self.sigAction)
        self.connect(self.actionPass_Definition, QtCore.SIGNAL('triggered(bool)'), self.sigAction)
        self.connect(self.actionBuild_Files, QtCore.SIGNAL('triggered(bool)'), self.sigAction)
        self.connect(self.actionRender_Files, QtCore.SIGNAL('triggered(bool)'), self.sigAction)
        self.connect(self.btnPassTypeAdd, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.btnPassTypeRemove, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.btnPassAdd, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.btnPassRemove, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.btnAOVAdd, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.btnAOVRemove, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.btnPassSceneAdd, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.btnPassSceneRemove, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.btnPassDefSave, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.btnBuildFilesSave, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.btnBuildFilesBuild, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.btnRenderFilesRender, QtCore.SIGNAL('clicked()'), self.sigButtonClick)
        self.connect(self.trListSeq, QtCore.SIGNAL('itemSelectionChanged()'), self.sigTreeSelChange)
        self.connect(self.trList, QtCore.SIGNAL('itemSelectionChanged()'), self.sigTreeSelChange)
        self.connect(self.trList_2, QtCore.SIGNAL('itemSelectionChanged()'), self.sigTreeSelChange)
        self.connect(self.trList_3, QtCore.SIGNAL('itemSelectionChanged()'), self.sigTreeSelChange)
        self.connect(self.trList_4, QtCore.SIGNAL('itemSelectionChanged()'), self.sigTreeSelChange)
        self.qtsOverride.connectToDragDrop(self.trPg2List_2, self.sigTreeDragDrop)
        self.qtsOverride.connectToDragDrop(self.trPg2List, self.sigTreeDragDrop)
        self.qtsOverride.connectToKeyPress(self.trPg2List, self.sigTreeKeyPress)

    def sigTreeKeyPress(self, *arg):
        sender = self.sender()
        info = self.qtsOverride.keyEventInfo(arg[0])

        if info == 'Delete':
            self.cParent.doPassSceneAssetRemove()

    def sigTreeDragDrop(self, *arg):
        sender = self.sender()
        info = self.qtsOverride.dropEventInfo(arg[0], False)

        if info['DestiWidget'] == self.trPg2List:
            self.cParent.doPassSceneAssetDragDropped(info)

        if info['DestiWidget'] == self.trPg2List_2:
            self.cParent.doPassSceneAssetDragDroppedRemove(info)

    def sigAction(self, *arg):
        sender = self.sender()

        if sender == self.actionSeq_N_Shots or sender == self.actionLogs or sender == self.actionRender_Settings:
            self.dckSNS.setVisible(self.actionSeq_N_Shots.isChecked())
            self.dckLog.setVisible(self.actionLogs.isChecked())
            self.dckRenderSettings.setVisible(self.actionRender_Settings.isChecked())
        else:
            if sender == self.actionPass_Definition:
                self.cParent.doStackPageChange('PASSDEFINITION')
            if sender == self.actionBuild_Files:
                self.cParent.doStackPageChange('BUILDFILES')
            if sender == self.actionRender_Files:
                self.cParent.doStackPageChange('RENDERFILES')
            if sender == self.actionSave:
                self.cParent.doCommonSave()
            if sender == self.actionQuit:
                self.close()

    def sigDock(self, *arg):
        sender = self.sender()
        self.actionSeq_N_Shots.setChecked(self.dckSNS.isVisible())
        self.actionLogs.setChecked(self.dckLog.isVisible())
        self.actionRender_Settings.setChecked(self.dckRenderSettings.isVisible())

    def sigTreeSelChange(self, *arg):
        sender = self.sender()
        if sender == self.trListSeq:
            self.cParent.doSeqChanged()
        if sender == self.trList:
            self.cParent.doShotChanged()
        if sender == self.trList_2:
            self.cParent.doPassTypeChanged()
        if sender == self.trList_3:
            self.cParent.doPassChanged()
        if sender == self.trList_4:
            self.cParent.doAOVChanged()

    def sigButtonClick(self, *arg):
        sender = self.sender()

        if sender == self.btnPassAdd:
            self.cParent.doPassAdd()
        if sender == self.btnPassRemove:
            self.cParent.doPassRemove()
        if sender == self.btnPassTypeAdd:
            self.cParent.doPassTypeAdd()
        if sender == self.btnPassTypeRemove:
            self.cParent.doPassTypeRemove()
        if sender == self.btnAOVAdd:
            self.cParent.doAOVAdd()
        if sender == self.btnAOVRemove:
            self.cParent.doAOVRemove()

        if sender == self.btnPassDefSave:
            self.cParent.doSavePassDefintion()
        if sender == self.btnBuildFilesSave:
            self.cParent.doSaveBuildFiles()
        if sender == self.btnBuildFilesBuild:
            self.cParent.doBuildBuildFiles()
        if sender == self.btnRenderFilesRender:
            self.cParent.doRenderFilesRender()

        if sender == self.btnPassSceneAdd:
            self.cParent.doPassSceneAdd()
        if sender == self.btnPassSceneRemove:
            self.cParent.doPassSceneRemove()


    def sigBlock(self, off=1):
        self.actionPass_Definition.blockSignals(off)
        self.actionBuild_Files.blockSignals(off)
        self.actionRender_Files.blockSignals(off)
        self.trListSeq.blockSignals(off)
        self.trList.blockSignals(off)
        self.trList_2.blockSignals(off)
        self.trList_3.blockSignals(off)
        self.trList_4.blockSignals(off)

    def closeEvent(self, *e):
        self.qtsCommon.uiLayoutSave(self.Config.LastUsed.Layout, self)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ui = LightNPrayUI(app)
    ui.show()
    sys.exit(app.exec_())