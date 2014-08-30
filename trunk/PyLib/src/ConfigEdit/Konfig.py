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
import qt_common
import tree_simple
import table
import override
import iniConfigReadWrite

#UI Packs
import config_ui_handle

import base64

class ConfigData():

    def __init__(self, configFile):
        #self.shpParent = shpParent

        #InitalValues
        self.configFile = configFile
        self.writeFlag = 1

        #Instance
        self.ui = config_ui_handle.ConfigUI(self)
        self.qtsCommon = qt_common.PyQtAppSupport(self.ui)
        self.qtsTree = tree_simple.TreeSimple(self.ui)
        self.qtsTable= table.Table(self.ui)
        self.qtsOverride = override.Override(self.ui)


    def initalize(self):
        self.configData = {}
        self.configDataOrig = {}
        self.currSection = ''
        #self.ui.initalize()
        self.qtsTable.clearTable(self.ui.tblSettings)
        self.qtsTree.removeAll(self.ui.trSections)
        if os.path.exists(self.configFile) and os.path.isfile(self.configFile):
            self.config = iniConfigReadWrite.INIConfig(self.configFile, self.writeFlag)
            sections = self.config.getSectionList()
            for section in sections:
                options = self.config.getOptionList(section)
                opts = []
                for option in options:
                    encode = 1 if option.find('enc_')==0 else 0
                    value = self.config.getOption(section,option)
                    data = {'Setting':option,'Value':value,'Encode':encode}
                    opts.append(data)
                self.configData[section] = opts
        self.configDataOrig = self.configData
        self.populateSections()

    def getVal(self, section, attribute):

        val = ''
        if self.configDataOrig and section and attribute and self.configDataOrig.has_key(section):
            for attr in self.configDataOrig[section]:
                if attr.has_key('Setting') and attr['Setting'] == str(attribute).lower():
                    if attr.has_key('Encode'):
                        val = attr['Value']
                        if attr['Encode']==1: val = base64.b64decode(val)
        return val

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
                setting = setting[4:].capitalize() if encode else setting
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

        if cid.editProceed:
            section = self.currSection
            setting = str(tbl.item(itm.row(),0).text())
            new_value = str(tbl.item(itm.row(),1).text())
            encode = int(self.qtsTable.getHiddenData(tbl.item(itm.row(),0))[0])
            if encode: setting = 'Enc_%s' % setting

            for cnt, opt in enumerate(self.configData[section]):
                if opt['Setting'] == setting.lower():
                    v = base64.b64encode(new_value) if opt['Encode'] else new_value
                    if opt['Encode']: tbl.item(itm.row(),1).setText(v)
                    self.configData[section][cnt]['Value'] = new_value
                    cid.editProceed = False
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


def edit(args):
    file_ = args[0] if len(args)>0 else ''
    if file_ and os.path.exists(file_):
        app = QtGui.QApplication(sys.argv)
        app.cfFilePath = file_
        app.cfWriteFlg = 1
        data = ConfigData(app.cfFilePath)
        data.initalize()
        data.showUI(0)
        sys.exit(app.exec_())
    else:
        print 'Please provide .ini file to edit!'


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #C:\Documents and Settings\lkumaresan\Application Data\PyScripter
    app.cfFilePath = 'configs.ini'
    app.cfWriteFlg = 1
    data = ConfigData(app.cfFilePath)
    data.initalize()
    data.showUI(0)
    sys.exit(app.exec_())