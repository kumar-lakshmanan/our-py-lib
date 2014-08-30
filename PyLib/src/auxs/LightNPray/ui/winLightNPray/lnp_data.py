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
import base64

#Common Packs
from UI_DB_lib.controls import qt_common
from UI_DB_lib.controls import tree_simple
from UI_DB_lib.controls import table
from UI_DB_lib.controls import override
from LightNPray.lib import dummy_parent
from LightNPray.ui import lighting_pass_uidata

#UI Packs
from LightNPray.ui.dlgPass import pass_dlg_ui_handle
from LightNPray.ui.dlgPassScene import passScene_dlg_ui_handle
from LightNPray.ui.dlgPassType import passType_dlg_ui_handle
from LightNPray.ui.dlgAOV import aov_dlg_ui_handle
from devConsole3 import DevConsolePlug

import lnp_ui_handle


class PassDefSelections():

    def __init__(self):
        self.sequence = ''
        self.shots = ''
        self.passtypes = ''
        self.passes = ''
        self.aovs = ''


class LightNPrayData():

    def __init__(self, cParent):
        self.cParent = dummy_parent.DummyParent(cParent) if not hasattr(cParent,'Config') else cParent
        self.App = self.cParent.App
        self.Config = self.cParent.Config
        self.Common = self.cParent.Common

        #Instance
        self.ui = lnp_ui_handle.LightNPrayUI(self)
        redirectPrint = 0 if self.Common.devmode else 1
        redirectErrors = 0 if self.Common.devmode else 1
        self.dev = DevConsolePlug.DevConsole(self.ui, ShowPrint = redirectPrint, ShowError = redirectErrors, StatusBar = self.ui.statusbar, AsDock = True)
        self.qtsCommon = qt_common.PyQtAppSupport(self.ui)
        self.qtsTree = tree_simple.TreeSimple(self.ui)
        self.qtsTable= table.Table(self.ui)
        self.qtsOverride = override.Override(self.ui)
        self.data = lighting_pass_uidata.exLightPassData(self)
        self.lightPassSel = PassDefSelections()
        self.ui.__class__.closeEvent = self.__littleHouseKeeping

        #self.ui.trList.is
    def initalize(self):
        self.modified = False
        if self.Common.curProject:

            res = self.data.setProject(self.Common.curProject)
            self.logUpdate(self.Config.Strings.lnpLibInitSuccess + ' - ' + self.Common.curProject, rest=1)
            self.logUpdate(self.Common.projFoundFrom)
            if res['STATUS']:
                self.populateSequences()
            else:
                self.logUpdate(res['MESSAGE'])
        else:
            self.Common.detectProject()
            self.logUpdate('No project given as input. \n* Use SAM to select a project, then load LNP. \n* Else, You can use -p [projectCode] in LNP executable\'s command line.\n    eg: D:\PULSE\LNP\PulseLNP.exe -p ZZP')

    def rest(self, request=''):

        if request == 'SEQUENCE':
           #UI Clear
           self.qtsTree.removeAll(self.ui.trListSeq)
           self.qtsTree.removeAll(self.ui.trList)
           self.qtsTree.removeAll(self.ui.trList_2)
           self.qtsTree.removeAll(self.ui.trList_3)
           self.qtsTree.removeAll(self.ui.trList_4)
           #Selection Info Rest
           self.lightPassSel.sequence = ''
           self.lightPassSel.shots = ''
           self.lightPassSel.passtypes = ''
           self.lightPassSel.passes = ''
           self.lightPassSel.aovs = ''

        if request == 'SHOT':
           self.qtsTree.removeAll(self.ui.trList)
           self.qtsTree.removeAll(self.ui.trList_2)
           self.qtsTree.removeAll(self.ui.trList_3)
           self.qtsTree.removeAll(self.ui.trList_4)
           self.lightPassSel.shots = ''
           self.lightPassSel.passtypes = ''
           self.lightPassSel.passes = ''
           self.lightPassSel.aovs = ''

        if request == 'PASSTYPE':
           self.qtsTree.removeAll(self.ui.trList_2)
           self.qtsTree.removeAll(self.ui.trList_3)
           self.qtsTree.removeAll(self.ui.trList_4)
           self.lightPassSel.passtypes = ''
           self.lightPassSel.passes = ''
           self.lightPassSel.aovs = ''

        if request == 'PASS':
           self.qtsTree.removeAll(self.ui.trList_3)
           self.qtsTree.removeAll(self.ui.trList_4)
           self.lightPassSel.passes = ''
           self.lightPassSel.aovs = ''

        if request == 'AOV':
           self.qtsTree.removeAll(self.ui.trList_4)
           self.lightPassSel.aovs = ''



    def populateSequences(self):
        self.ui.sigBlock(1)
        if self.data:
            self.rest('SEQUENCE')
            tree = self.ui.trListSeq
            tree.setSortingEnabled(0)
            res = self.data.getSequences()
            if res['STATUS']:
                for itm in res['DATA']:
                    self.qtsTree.addRootItem(tree, str(itm))
            else:
                self.logUpdate(res['MESSAGE'])
            tree.setSortingEnabled(1)
        self.ui.sigBlock(0)

    def populateShots(self):
        self.ui.sigBlock(1)
        if self.data:
            self.rest('SHOT')
            tree = self.ui.trList
            tree.setSortingEnabled(0)
            res = self.data.getShots(self.lightPassSel.sequence)
            if res['STATUS']:
                for itm in res['DATA']:
                    self.qtsTree.addRootItem(tree, str(itm))
            else:
                self.logUpdate(res['MESSAGE'])
            tree.setSortingEnabled(1)
        self.ui.sigBlock(0)

    def populatePassTypes(self):
        self.ui.sigBlock(1)
        if self.data:
            self.rest('PASSTYPE')
            tree = self.ui.trList_2
            res = self.data.getPassType(self.lightPassSel.sequence, self.lightPassSel.shots)
            if res['STATUS']:
                for itm in res['DATA']:
                    self.qtsTree.addRootItem(tree, str(itm))
            else:
                self.logUpdate(res['MESSAGE'])
        self.ui.sigBlock(0)

    def populatePasses(self):
        self.ui.sigBlock(1)
        if self.data:
            self.rest('PASS')
            tree = self.ui.trList_3
            res = self.data.getPass(self.lightPassSel.passtypes, self.lightPassSel.sequence, self.lightPassSel.shots)
            if res['STATUS']:
                for itm in res['DATA']:
                    self.qtsTree.addRootItem(tree, str(itm))
            else:
                self.logUpdate(res['MESSAGE'])
        self.ui.sigBlock(0)

    def populateAOVs(self):
        self.ui.sigBlock(1)
        if self.data:
            self.rest('AOV')
            tree = self.ui.trList_4
            res = self.data.getAOV(self.lightPassSel.passes, self.lightPassSel.passtypes, self.lightPassSel.sequence, self.lightPassSel.shots)
            if res['STATUS']:
                for itm in res['DATA']:
                    self.qtsTree.addRootItem(tree, str(itm))
            else:
                self.logUpdate(res['MESSAGE'])
        self.ui.sigBlock(0)

    #SCREEN 2

    def populatePassScene(self):
        if not self.lightPassSel.shots: return 0
        self.ui.sigBlock(1)
        if self.data:
            tree = self.ui.trPg2List
#            sts = self.qtsTree.getCollapseStates(tree)
            self.qtsTree.removeAll(tree)
            res = self.data.getPassScenes(self.lightPassSel.sequence, self.lightPassSel.shots)
            if res['STATUS']:
                #self.qtsTree.populateTree(tree, res['DATA'])
                self.__populatePassSceneSupport(tree, res['DATA'])
                self.qtsTree.treeOpenClose(tree)
                self.populateWorkFiles()
                self.populateAssets()
            else:
                self.logUpdate(res['MESSAGE'])
#            if sts:
#                self.qtsTree.setCollapseStates(tree,sts)
        self.ui.sigBlock(0)

    def populateAssets(self):
        if not self.lightPassSel.shots: return 0
        self.ui.sigBlock(1)
        if self.data:
            tree = self.ui.trPg2List_2
            self.qtsTree.removeAll(tree)
            wld = self.qtsCommon.waitDialog(label=self.Config.Strings.lnpLoadingShots)
            res = self.data.getAssets(self.lightPassSel.sequence, self.lightPassSel.shots)
            if res['STATUS']:
                self.qtsTree.populateTree(tree, res['DATA'])
                self.qtsTree.treeOpenClose(tree)
            else:
                self.logUpdate(res['MESSAGE'])
            wld.close()
        self.ui.sigBlock(0)

    def populateWorkFiles(self):
        if not self.lightPassSel.shots: return 0
        self.ui.sigBlock(1)
        if self.data:
            tree = self.ui.trWorkFiles
            self.qtsTree.removeAll(tree)
            res = self.data.getWorkFiles(self.lightPassSel.sequence,self.lightPassSel.shots)
            #infos = self.__passSceneFiles(data)
            if res['STATUS']:
                for passScene in res['DATA']:
                    root = self.qtsTree.addRootItem(tree, passScene)
                    for asset in res['DATA'][passScene]:
                        self.qtsTree.addChildItem(tree, root, asset)
                self.qtsTree.treeOpenClose(tree)
            else:
                self.logUpdate(res['MESSAGE'])
        self.ui.sigBlock(0)


    def doSeqChanged(self):
        self.ui.sigBlock(1)
        cseq = str(self.qtsTree.getSelectedItem(self.ui.trListSeq)['Label'])
        if cseq:
            self.lightPassSel.sequence = cseq
            self.populateShots()
            self.populatePassScene()
        self.ui.sigBlock(0)

    def doShotChanged(self):
        self.ui.sigBlock(1)
        shot = str(self.qtsTree.getSelectedItem(self.ui.trList)['Label'])
        if shot:
            self.lightPassSel.shots = shot
            self.populatePassTypes()
            self.populatePassScene()
        self.ui.sigBlock(0)

    def doPassTypeChanged(self):
        self.ui.sigBlock(1)
        passType = str(self.qtsTree.getSelectedItem(self.ui.trList_2)['Label'])
        if passType:
            self.lightPassSel.passtypes = passType
            self.populatePasses()
        self.ui.sigBlock(0)

    def doPassChanged(self):
        self.ui.sigBlock(1)
        passes = str(self.qtsTree.getSelectedItem(self.ui.trList_3)['Label'])
        if passes:
            self.lightPassSel.passes = passes
            self.populateAOVs()
        self.ui.sigBlock(0)

    def doAOVChanged(self):
        self.ui.sigBlock(1)
        aovs = str(self.qtsTree.getSelectedItem(self.ui.trList_4)['Label'])
        if aovs:
            self.lightPassSel.aovs = aovs
        self.ui.sigBlock(0)

    def doPassTypeAdd(self):
        self.ui.sigBlock(1)
        if self.data and self.lightPassSel.sequence:
            #passtype = str(self.qtsCommon.showInputBox(self.Config.AppInfo.ShortName, 'Enter Passtype: '))
            res1 = self.data.getPassType(self.lightPassSel.sequence ,self.lightPassSel.shots)
            if res1['STATUS']:
                userentry = self.__popAddPassTypeDlg()
                chk = userentry[0]
                passtype = userentry[1]
                if passtype:
                    passtype = passtype.upper()
                    res1 = self.data.doAddPassType(passtype, self.lightPassSel.sequence, self.lightPassSel.shots,ApplyToSeq=chk)
                    self.logUpdateAction('doAddPassType', (passtype, self.lightPassSel.sequence, self.lightPassSel.shots,chk))
                    if res1['STATUS']:
                        #self.modified = True
                        self.populatePassTypes()
                    else:
                        self.logUpdate(res1['MESSAGE'])
                else:
                    self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Passtype Information')
            else:
                self.logUpdate(res1['MESSAGE'])
        else:
            self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Passtype Information')
        self.ui.sigBlock(0)

    def doPassTypeRemove(self):
        self.ui.sigBlock(1)
        if self.data and self.lightPassSel.sequence and self.lightPassSel.shots and self.lightPassSel.passtypes:
            confirm = self.qtsCommon.showYesNoBox(
                                self.Config.AppInfo.ShortName,
                                '%s\n%s-->%s-->%s'%
                                (self.Config.Strings.lnpLibDeleteConfirm, self.lightPassSel.sequence,self.lightPassSel.shots,self.lightPassSel.passtypes)
                                )
            if confirm:
                res1 = self.data.doRemovePassType(self.lightPassSel.passtypes, self.lightPassSel.sequence, self.lightPassSel.shots)
                if res1['STATUS']:
                    #self.modified = True
                    self.populatePassTypes()
                else:
                    self.logUpdate(res1['MESSAGE'])
            else:
                self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/Passtype Information')
        else:
            self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/Passtype Information')
        self.ui.sigBlock(0)

    def doPassAdd(self):
        self.ui.sigBlock(1)
        if self.data and self.lightPassSel.sequence:
            res = self.data.getPass(self.lightPassSel.passtypes, self.lightPassSel.sequence, self.lightPassSel.shots)
            userentry = self.__popAddPassNameDlg()
            chk = userentry[0]
            passName, passCode = userentry[1][0], userentry[1][1]
            if passName and passCode:
                passName = passName.upper()
                passCode = passCode.upper()
                res1 = self.data.doAddPass(passName, passCode, self.lightPassSel.passtypes, self.lightPassSel.sequence, self.lightPassSel.shots, ApplyToSeq = chk)
                self.logUpdateAction('doAddPass', (passName, passCode, self.lightPassSel.passtypes, self.lightPassSel.sequence, self.lightPassSel.shots))
                if res1['STATUS']:
                    #self.modified = True
                    self.populatePasses()
                else:
                    self.logUpdate(res1['MESSAGE'])
            else:
                self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/Passtype/PassName/PassCode Information')
        else:
            self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/Passtype/PassName/PassCode Information')
        self.ui.sigBlock(0)

    def doPassRemove(self):
        self.ui.sigBlock(1)
        if self.data and self.lightPassSel.sequence and self.lightPassSel.shots and self.lightPassSel.passtypes and self.lightPassSel.passes:
            confirm = self.qtsCommon.showYesNoBox(
                                self.Config.AppInfo.ShortName,
                                '%s\n%s-->%s-->%s->%s'%
                                (self.Config.Strings.lnpLibDeleteConfirm, self.lightPassSel.sequence,self.lightPassSel.shots,self.lightPassSel.passtypes,self.lightPassSel.passes)
                                )
            if confirm:
                res1 = self.data.doRemovePass(self.lightPassSel.passes, self.lightPassSel.passtypes, self.lightPassSel.sequence, self.lightPassSel.shots)
                if res1['STATUS']:
                    #self.modified = True
                    self.populatePasses()
                else:
                    self.logUpdate(res1['MESSAGE'])
            else:
                self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/Passtype/PassName Information')
        else:
            self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/Passtype/PassName Information')
        self.ui.sigBlock(0)

    def doAOVAdd(self):
        self.ui.sigBlock(1)
        if self.data and self.lightPassSel.sequence:
            res = self.data.getAOV(self.lightPassSel.passes, self.lightPassSel.passtypes, self.lightPassSel.sequence, self.lightPassSel.shots)
            userentry = self.__popAddAOVDlg()
            chk = userentry[0]
            aovs = userentry[1]
            matteExtra = userentry[2]
            if aovs:
                res = self.data.doAddAOV(aovs,self.lightPassSel.passes, self.lightPassSel.passtypes, self.lightPassSel.sequence, self.lightPassSel.shots, ApplyToSeq=chk, MatteExtra=matteExtra)
                self.logUpdateAction('doAddAOV', (aovs,self.lightPassSel.passes, self.lightPassSel.passtypes, self.lightPassSel.sequence, self.lightPassSel.shots, chk,matteExtra))

                if not res['STATUS']:
                    self.logUpdate(res['MESSAGE'])
                self.populateAOVs()
        else:
            self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/Passtype/PassName/AOV Information')
        self.ui.sigBlock(0)

    def doAOVRemove(self):
        self.ui.sigBlock(1)
        if self.data and self.lightPassSel.sequence and self.lightPassSel.shots and self.lightPassSel.passtypes and self.lightPassSel.passes and self.lightPassSel.aovs:
            confirm = self.qtsCommon.showYesNoBox(
                                self.Config.AppInfo.ShortName,
                                '%s\n%s-->%s-->%s->%s->%s'%
                                (self.Config.Strings.lnpLibDeleteConfirm, self.lightPassSel.sequence,self.lightPassSel.shots,self.lightPassSel.passtypes,self.lightPassSel.passes,self.lightPassSel.aovs)
                                )
            if confirm:
                res1 = self.data.doRemoveAOV(self.lightPassSel.aovs, self.lightPassSel.passes, self.lightPassSel.passtypes, self.lightPassSel.sequence, self.lightPassSel.shots)
                if res1['STATUS']:
                    #self.modified = True
                    self.populateAOVs()
                else:
                    self.logUpdate(res1['MESSAGE'])
            else:
                self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/Passtype/PassName/AOV Information')
        else:
            self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/Passtype/PassName/AOV Information')
        self.ui.sigBlock(0)

    def doPassSceneAdd(self):
        self.ui.sigBlock(1)
        if self.data and self.lightPassSel.sequence and self.lightPassSel.shots:
            res1 = self.data.getPassType(self.lightPassSel.sequence ,self.lightPassSel.shots)
            if res1['STATUS']:
                userinput = self.__popAddScenePassDlg(res1['DATA'])
                if userinput['PASSTYPE'] and userinput['PASSSCENE']:
                    pt = userinput['PASSTYPE']
                    sc = userinput['PASSSCENE']
                    sc = sc.upper()
                    seq = self.lightPassSel.sequence
                    sht = self.lightPassSel.shots
                    res2 = self.data.doAddPassScene(sc,pt,seq,sht)
                    self.logUpdateAction('doAddPassScene', (sc,pt,seq,sht))
                    if res2['STATUS']:
                        #self.modified = True
                        self.populatePassScene()
                    else:
                        self.logUpdate(res2['MESSAGE'])
                else:
                    self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/Passtype/PassSceneName Information')
            else:
                self.logUpdate(res1['MESSAGE'])
        else:
            self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/Passtype/PassSceneName Information')
        self.ui.sigBlock(0)

    def doPassSceneRemove(self):
        self.ui.sigBlock(1)
        psSel = self.__getTreeSelection(self.ui.trPg2List)
        psSelItem = self.__getTreeSelection(self.ui.trPg2List, 'Item')
        psLevel = self.qtsTree.getItemLevelNo(psSelItem) if psSelItem else 100000
        passType = self.__getTreeSelection(self.ui.trPg2List,col=1)
        if self.data and self.lightPassSel.sequence and self.lightPassSel.shots and psSel and psLevel==0:
            confirm = self.qtsCommon.showYesNoBox(
                                    self.Config.AppInfo.ShortName,
                                    '%s\n%s->%s(%s)->%s' %
                                     (
                                      self.Config.Strings.lnpLibDeleteConfirm,
                                      self.lightPassSel.sequence,
                                      self.lightPassSel.shots,
                                      passType,
                                      psSel
                                      )
                                    )
            if confirm:
                res = self.data.doRemovePassScene(psSel, self.lightPassSel.sequence, self.lightPassSel.shots, passType)
                if res['STATUS']:
                    #self.modified = True
                    self.populatePassScene()
                else:
                    self.logUpdate(res['MESSAGE'])
            else:
                self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/PassSceneName Information')
        else:
            self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot/PassSceneName Information')
        self.ui.sigBlock(0)


    def doPassSceneAssetDragDropped(self, info):
        self.ui.sigBlock(1)
        destiItem = info['DestiItems']
        destWidget = info['DestiWidget']
        sourceItems = info['SourceItems']
        sourceWidget = info['SourceWidget']
        event = info['Event']
        if destiItem and sourceItems and self.lightPassSel.sequence and self.lightPassSel.shots:
            results = []
            for sourceItem in sourceItems:
                #isLeaf = self.qtsTree.isGivenItemAChild(sourceItem)
                #isRoot = self.qtsTree.isGivenItemARoot(destiItem)
                destiRootItem = self.qtsTree.getRootItemFor(destWidget, destiItem)
                sourceChildrensItem = self.qtsTree.getLeafItemFor(sourceWidget, sourceItem)
                for eachSourceChild in sourceChildrensItem:
                    if sourceWidget == self.ui.trPg2List_2:
                        rnName = str(self.qtsTree.getItemLabel(eachSourceChild)['Label'])
                        rnPath = str(self.qtsTree.getItemLabel(eachSourceChild)['Data'])
                        scnName = str(self.qtsTree.getItemLabel(destiRootItem)['Label'])
                        seqName = self.lightPassSel.sequence
                        shotName = self.lightPassSel.shots
                        passType = str(self.qtsTree.getItemLabel(destiRootItem,1)['Label'])
                        res = self.data.doAddPassSceneAsset(rnName,rnPath,scnName,seqName,shotName,passType)
                        self.logUpdateAction('doAddPassSceneAsset',(rnName,rnPath,scnName,seqName,shotName,passType))
                        if res['STATUS']:
                            #event.accept()
                            #self.modified = True
                            #self.populatePassScene()
                            pass
                        else:
                            self.logUpdate(res['MESSAGE'])
                    else:
                        self.logUpdate(self.Config.Strings.lnpLibInvalidDragDrop)
                        #event.ignore()

            self.populatePassScene()

        else:
            self.logUpdate(self.Config.Strings.lnpLibInvalidDragDrop)
            event.ignore()
        self.ui.sigBlock(0)

    def doPassSceneAssetDragDroppedRemove(self, info):
        self.ui.sigBlock(1)
        destiItem = info['DestiItems']
        destWidget = info['DestiWidget']
        sourceItems = info['SourceItems']
        sourceWidget = info['SourceWidget']
        event = info['Event']
        self.doPassSceneAssetRemove()
        self.ui.sigBlock(0)

    def doPassSceneAssetRemove(self):
        self.ui.sigBlock(1)
        rnName = self.__getTreeSelection(self.ui.trPg2List)
        rnItm =  self.__getTreeSelection(self.ui.trPg2List, 'Item')
        seqName = self.lightPassSel.sequence
        shotName = self.lightPassSel.shots
        scnItm = self.qtsTree.getRootItemFor(self.ui.trPg2List, rnItm) if rnItm else None
        scnName = self.qtsTree.getItemLabel(scnItm)['Label'] if scnItm else ''
        passType = self.qtsTree.getItemLabel(scnItm,1)['Label'] if scnItm else ''
        if rnName and scnName and seqName and shotName:
            confirm = self.qtsCommon.showYesNoBox(
                                    self.Config.AppInfo.ShortName,
                                    '%s\n%s->%s->%s(%s)->%s' %
                                     (
                                      self.Config.Strings.lnpLibDeleteConfirm,
                                      self.lightPassSel.sequence,
                                      self.lightPassSel.shots,
                                      scnName,
                                      passType,
                                      rnName
                                      )
                                    )
            if confirm:
                res = self.data.doRemovePassSceneAsset(rnName, scnName, seqName, shotName, passType)
                if res['STATUS']:
                    #self.modified = True
                    self.populatePassScene()
                else:
                    self.logUpdate(res['MESSAGE'])
            else:
                self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... RNNode/SceneName/Seq/Shot Information')
        else:
            self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... RNNode/SceneName/Seq/Shot Information')
        self.ui.sigBlock(0)

    def doCommonSave(self):
        self.__commonSave()

    def doSavePassDefintion(self):
        self.__commonSave()

    def doSaveBuildFiles(self):
        self.__commonSave()

    def doBuildBuildFiles(self):
        self.ui.sigBlock(1)
        wdlg = None

        rnName = self.__getTreeSelection(self.ui.trPg2List)
        rnItm =  self.__getTreeSelection(self.ui.trPg2List, 'Item')
        seqName = self.lightPassSel.sequence
        shotName = self.lightPassSel.shots
        scnItm = self.qtsTree.getRootItemFor(self.ui.trPg2List, rnItm) if rnItm else None
        scnName = self.qtsTree.getItemLabel(scnItm)['Label'] if scnItm else []
        passType = self.qtsTree.getItemLabel(scnItm,1)['Label'] if scnItm else ''


        if self.data and self.lightPassSel.sequence and self.lightPassSel.shots:
            confirm = self.qtsCommon.showYesNoBox(
                                    self.Config.AppInfo.ShortName,
                                    '%s\n%s-->%s %s' %
                                    (self.Config.Strings.lnpLibBuildStartConfirm, self.lightPassSel.sequence,self.lightPassSel.shots, '(%s)'%scnName if scnName else '')
                                )
            if confirm:
                wdlg = self.qtsCommon.waitDialog()
                res1 = self.data.doBuildFiles(self.lightPassSel.sequence, self.lightPassSel.shots, [scnName] if scnName else [], 'MAYA2008')
                if res1['STATUS']:
                    #self.modified = True
                    self.qtsCommon.showInformationBox(
                                                    self.Config.AppInfo.ShortName,
                                                    self.Config.Strings.lnpLibBuildFilesSuccessfull,
                                                    )
                    self.logUpdate(self.Config.Strings.lnpLibBuildFilesSuccessfull)
                else:
                    self.qtsCommon.showInformationBox(
                                                    self.Config.AppInfo.ShortName,
                                                    self.Config.Strings.lnpLibBuildFilesFail,
                                                    )
                    self.logUpdate(res1['MESSAGE'])
            else:
                self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot Information')
        else:
            self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot Information')
        if wdlg: wdlg.close()
        self.ui.sigBlock(0)

    def doRenderFilesRender(self):
        pass

    def doStackPageChange(self, request):
        self.ui.sigBlock(1)
        if request == 'PASSDEFINITION':
            self.ui.stkMainPages.setCurrentWidget(self.ui.pgPassDefinition)
            self.ui.actionPass_Definition.setChecked(True)
            self.ui.actionBuild_Files.setChecked(False)
            self.ui.actionRender_Files.setChecked(False)
        if request == 'BUILDFILES':
            self.ui.stkMainPages.setCurrentWidget(self.ui.pgBuildPass)
            self.ui.actionPass_Definition.setChecked(False)
            self.ui.actionBuild_Files.setChecked(True)
            self.ui.actionRender_Files.setChecked(False)
        if  request == 'RENDERFILES':
            self.ui.stkMainPages.setCurrentWidget(self.ui.pgRenderFiles)
            self.ui.actionPass_Definition.setChecked(False)
            self.ui.actionBuild_Files.setChecked(False)
            self.ui.actionRender_Files.setChecked(True)
        self.ui.sigBlock(0)


    def __populatePassSceneSupport(self, tree, data):
        for ps in data:
            passType = data[ps]['passType']
            assetsDict = data[ps]['assets']
            name = data[ps]['name']
            rootItem = self.qtsTree.addRootItem(tree, name)
            rootItem.setText(1, passType)
            self.__populatePassSceneAssetsSupport(assetsDict, tree, rootItem)

    def __populatePassSceneAssetsSupport(self, assetsDict, tree, rootItem):
        for eachRoot in assetsDict:
            if type(assetsDict[eachRoot]) == type({}):
                newChildItem = self.qtsTree.addChildItem(tree,rootItem, str(eachRoot))
                self.qtsTree.populateTreeChildren(tree, newChildItem, assetsDict[eachRoot])
            else:
                childItem = self.qtsTree.addChildItem(tree, rootItem, str(eachRoot))


    def __popAddPassTypeDlg(self, passtypes=''):

        uiCDcfg = passType_dlg_ui_handle.CustomDialogConfigure()
        uiCDcfg.header = 'New Pass type'
        uiCDcfg.message = 'Create new pass type...'
        uiCDcfg.additionalData = [self.data.getGlobal('PASSTYPE')]
        uiCD = passType_dlg_ui_handle.PassTypeDialog(self.cParent, uiCDcfg)
        uiCD.initialize()
        uiCD.exec_()

        if uiCD.ok and not uiCD.cancel:
            chk = uiCD.checkBox.isChecked()
            pst = str(uiCD.le1.text())
            if pst:
                return (chk,pst)
            else:
                return (False,'')
        else:
            return (False,'')

    def __popAddPassNameDlg(self, passNames=''):

        uiCDcfg = pass_dlg_ui_handle.CustomDialogConfigure()
        uiCDcfg.header = 'New Pass'
        uiCDcfg.message = 'Create new pass...'
        glbPassNCode = self.data.getGlobal('PASS')
        data = [(ps,glbPassNCode[ps]) for ps in glbPassNCode]
        uiCDcfg.additionalData = [data]
        uiCD = pass_dlg_ui_handle.PassDialog(self.cParent, uiCDcfg)
        uiCD.initialize()
        uiCD.exec_()

        if uiCD.ok and not uiCD.cancel:
            chk = uiCD.checkBox.isChecked()
            ps = str(uiCD.le1.text())
            psc = str(uiCD.le2.text())
            if ps and psc:
                return (chk,(ps,psc))
            else:
                return (False,('',''))
        else:
            return (False,('',''))

    def __popAddAOVDlg(self, aovs=''):
        uiCDcfg = aov_dlg_ui_handle.CustomDialogConfigure()
        uiCDcfg.header = 'New AOV'
        uiCDcfg.message = 'Create new AOV...'
        uiCDcfg.additionalData = [self.data.getGlobal('AOV')]
        uiCD = aov_dlg_ui_handle.AOVDialog(self.cParent, uiCDcfg)
        uiCD.initialize()
        uiCD.exec_()

        if uiCD.ok and not uiCD.cancel:
            chk = uiCD.checkBox.isChecked()
            selectedAovs = uiCD.qtsList.getSelectedItemLabels(uiCD.listWidget)
            typedAovs = [str(uiCD.le1.text())]
            aovs = []
            if typedAovs[0] == 'Multi Selected':
                aovs = selectedAovs
            if len(selectedAovs)==1 and typedAovs[0]!='':
                aovs = typedAovs
            mat = str(uiCD.le3.text())
            if len(aovs)>0:
                return (chk,aovs,mat)
            else:
                return (False,[],'')
        else:
            return (False,[],'')

    def __popAddScenePassDlg(self, passtypes):

        uiCDcfg = passScene_dlg_ui_handle.CustomDialogConfigure()
        uiCDcfg.header = 'Add Pass Scene'
        uiCDcfg.message = 'Create new pass scene...'
        res = self.data.getPassType(self.lightPassSel.sequence,self.lightPassSel.shots)
        uiCDcfg.additionalData = [res['DATA'] if res['STATUS'] else []]
        uiCD = passScene_dlg_ui_handle.PassSceneDialog(self.cParent, uiCDcfg)
        uiCD.initialize()
        uiCD.exec_()

        if uiCD.ok and not uiCD.cancel:
            pt = str(uiCD.lineEdit_4.text())
            nps = str(uiCD.lineEdit_2.text())
            if pt and nps:
                return {'PASSTYPE': pt, 'PASSSCENE': nps}
            else:
                return {'PASSTYPE': '', 'PASSSCENE': ''}
        else:
            return {'PASSTYPE': '', 'PASSSCENE': ''}

    def __getTreeSelection(self, tree, requesting='Label', col=0):
        sel = self.qtsTree.getSelectedItem(tree,col=col)
        if sel:
            if type(sel)==type([]):
                return sel[0][requesting]
            else:
                return sel[requesting]
        else:
            return ''

    def __getCurrentStackPage(self):

        if self.ui.stkMainPages.currentWidget() == self.ui.pgPassDefinition:
            return 'PASSDEFINITION'
        if self.ui.stkMainPages.currentWidget() == self.ui.pgBuildPass:
            return 'BUILDFILES'
        if self.ui.stkMainPages.currentWidget() == self.ui.pgRenderFiles:
            return 'RENDERFILES'

        return ''

    def __passSceneFiles(self, dct):
        mlst = {}
        for itm in dct:
            toProc = dct[itm]
            assets = toProc['assets']
            mlst[itm] = self.__getDctLeafs(assets, [])
        return mlst

    def __getDctLeafs(self, dct, lst=[]):
        for itm in dct:
            if type(dct[itm]) == type({}):
                newdt = dct[itm]
                self.__getDctLeafs(newdt,lst)
            else:
                lst.append(dct[itm])
        return lst


    def __commonSave(self, skipConfirm = 0):
        self.ui.sigBlock(1)
        if self.data and self.lightPassSel.sequence and self.lightPassSel.shots:

            if not self.modified and not skipConfirm:
                self.qtsCommon.showInformationBox(self.Config.AppInfo.ShortName, self.Config.Strings.lnpLibNothingToSave)
                self.logUpdate(self.Config.Strings.lnpLibNothingToSave)
                self.ui.sigBlock(0)
                return 0

            #Some times you may force save... like on close event.
            if skipConfirm:
                confirm = 1
            else:
                confirm = self.qtsCommon.showYesNoBox(self.Config.AppInfo.ShortName, self.Config.Strings.lnpLibConfirmSave)

            if confirm:
                res1 = self.data.doSave(self.lightPassSel.sequence, self.lightPassSel.shots)
                if res1['STATUS']:
                    self.modified = False
                    self.qtsCommon.showInformationBox(self.Config.AppInfo.ShortName, self.Config.Strings.lnpLibSaveSuccess)
                else:
                    self.qtsCommon.showInformationBox(self.Config.AppInfo.ShortName, self.Config.Strings.lnpLibSaveFail)
                    self.logUpdate(res1['MESSAGE'])
            else:
                self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot Information')
        else:
            self.logUpdate(self.Config.Strings.lnpLibInvalidInputs + '\nAction needs... Seq/Shot Information')

        self.ui.sigBlock(0)

    def __littleHouseKeeping(self, *eve):

        proceedClose = False
        if self.modified:
            saveConfirm = self.qtsCommon.showYesNoCancelBox(self.Config.AppInfo.ShortName, self.Config.Strings.lnpLibRemindSave)
            if saveConfirm == 1:
                self.__commonSave(skipConfirm = 1)
                proceedClose = True
            if saveConfirm == 0:
                proceedClose = True
            if saveConfirm == -1:
                proceedClose = False
        else:
            proceedClose = True

        if proceedClose:
            self.__saveLastSettings()
            eve[0].accept()
        else:
            eve[0].ignore()



    def __loadLastSettings(self):
        self.ui.qtsCommon.uiLayoutRestore(self.Config.LastUsed.Layout)
        self.doStackPageChange(self.Config.LastUsed.LastPage)

    def __saveLastSettings(self):
        self.ui.qtsCommon.uiLayoutSave(self.Config.LastUsed.Layout)
        if self.__getCurrentStackPage(): self.Config.LastUsed.LastPage = self.__getCurrentStackPage()
        self.Config.UpdateConfigValues(self.Config.LastUsed)



    def logUpdate(self, data='',rest=0):

        data = str(data)
        data = data.strip()

        print data
        prvData = self.ui.tbLog.toPlainText()
        newData = '%s'%(data) if rest else '%s\n%s'%(prvData, data)
        self.ui.tbLog.setPlainText(newData)
        vsb = self.ui.tbLog.verticalScrollBar()
        vsb.setValue(vsb.maximum())

    def logUpdateAction(self, functionName, Inputs):

        prvData = self.ui.tbLog.toPlainText()
        newData = '%s\nAction - %s, Inputs - %s' % (prvData, functionName, Inputs)
        self.ui.tbLog.setPlainText(newData)
        vsb = self.ui.tbLog.verticalScrollBar()
        vsb.setValue(vsb.maximum())


    def logReset(self):
        self.ui.tbLog.setPlainText('')

    def showUI(self):
        self.ui.show()
        self.__loadLastSettings()

    def hideUI(self):
        self.ui.hide()

    def closeUI(self):
        self.ui.close()
        del(ui)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    data = LightNPrayData(app)
    data.initalize()
    data.showUI()
    sys.exit(app.exec_())