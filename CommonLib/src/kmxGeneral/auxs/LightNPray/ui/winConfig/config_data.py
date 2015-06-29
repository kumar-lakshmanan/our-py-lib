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
from PyQt4 import QtCore, QtGui

#Common Packs
from UI_DB_lib.controls import qt_common
from UI_DB_lib.controls import tree_simple
from UI_DB_lib.controls import table
from UI_DB_lib.controls import override
from UI_DB_lib import iniConfigReadWrite

#UI Packs
import config_ui_handle
import base64

class ConfigUIInput():
    def __init__(self):
        self.iniPath = 'settings.ini'
        self.isEditable = 1
        self.skipSections = []
        self.skipOptions = [] #SHOULD LIKE [('AppInfos','Fullname')]


class ConfigData():

    def __init__(self, cip, cParent=None):
        self.cParent = cParent
        self.cip = ConfigUIInput() if not cip else cip

        #InitalValues
        self.configFile = self.cip.iniPath
        self.writeFlag = self.cip.isEditable
        self.skipSections = self.cip.skipSections
        self.skipOptions = self.cip.skipOptions

        #Instance
        self.ui = config_ui_handle.ConfigUI(self)
        self.qtsCommon = qt_common.PyQtAppSupport(self.ui)
        self.qtsTree = tree_simple.TreeSimple(self.ui)
        self.qtsTable= table.Table(self.ui)
        self.qtsOverride = override.Override(self.ui)


    def initalize(self):

        self.ui.btnApply.setEnabled(self.writeFlag)
        self.configData = {}
        self.configDataOrig = {}
        self.currSection = ''
        if os.path.exists(self.configFile) and os.path.isfile(self.configFile):
            self.config = iniConfigReadWrite.INIConfig(self.configFile, self.writeFlag)
            sections = self.config.getSectionList()
            for section in sections:
                if section in self.skipSections: continue
                options = self.config.getOptionList(section)
                opts = []
                for option in options:
                    if (section, option) in self.skipOptions: continue
                    encode = 1 if option.find('enc_')==0 else 0
                    value = self.config.getOption(section,option)
                    data = {'Setting':option,'Value':value,'Encode':encode}
                    opts.append(data)
                self.configData[section] = opts
        self.configDataOrig = self.configData
        self.populateSections()


    def populateSections(self):
        for section in self.configData:
            self.qtsTree.addRootItem(self.ui.trSections,section)


    def populateSettings(self, section):
        self.currSection = section
        if self.configData.has_key(section):
            self.qtsCommon.setLabel(self.ui.lblSectionHead, section)
            self.qtsTable.clearTable(self.ui.tblSettings)
            for opt in self.configData[section]:
                setting = opt['Setting'].capitalize()
                value = opt['Value']
                encode = opt['Encode']
                rows = self.qtsTable.addRow(self.ui.tblSettings,[setting,value], append=1,allowEmpty=True)
                self.qtsTable.setHiddenData(rows[0],[encode])

    def doApply(self):
        for section in self.configDataOrig:
            for cnt, opt in enumerate(self.configDataOrig[section]):
                setting = opt['Setting']
                value = self.configData[section][cnt]['Value']
                encode = self.configData[section][cnt]['Encode']
                if self.config.writeable:
                    self.config.setOption(section, setting, value, encode)
                else:
                    self.qtsCommon.showInformationBox('INI Write','Unable to write configuration settings!')
                    self.doClose()

        self.doClose()

    def doClose(self):
        self.ui.close()

    def optionEditStart(self, arg):

        cid = arg[0]
        tbl = arg[1]
        itm = arg[2]

        if itm.column()==1:
            cid.editProceed = True

    def optionEditEnd(self, arg):

        cid = arg[0]
        tbl = arg[1]
        itm = arg[2]

        section = self.currSection
        setting = str(tbl.item(itm.row(),0).text())
        new_value = str(tbl.item(itm.row(),1).text())

        for cnt, opt in enumerate(self.configData[section]):
            if opt['Setting'] == setting.lower():
                v = base64.b64encode(new_value) if opt['Encode'] else new_value
                if opt['Encode']: tbl.item(itm.row(),1).setText(v)
                self.configData[section][cnt]['Value'] = new_value
                break

    def showUI(self,model=1):
        if model:
            self.ui.exec_()
        else:
            self.ui.show()

    def hideUI(self):
        self.ui.hide()

    def closeUI(self):
        self.ui.close()
        del(ui)


def quickConfigDlg(iniFile, launchnow = 1, model = 1, isEditable=0, skipSections=[], skipOptions=[]):
    cip = ConfigUIInput()
    cip.iniPath = iniFile
    cip.isEditable = isEditable
    cip.skipSections = skipSections
    cip.skipOptions = skipOptions
    data = ConfigData(cip)
    data.initalize()
    if launchnow:
        data.showUI(model)
    return data



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #C:\Documents and Settings\lkumaresan\Application Data\PyScripter

    iniPath = 'D:/REPO/SOURCE/SCRIPTS/PYTHON/LightNPray/data/setting.ini'
    isEditable = 1
    skipSections = []
    skipOptions = []
    cfDlg = quickConfigDlg(iniPath,1,0,isEditable,skipSections,skipOptions)
    #cfDlg.closeUI()

    sys.exit(app.exec_())