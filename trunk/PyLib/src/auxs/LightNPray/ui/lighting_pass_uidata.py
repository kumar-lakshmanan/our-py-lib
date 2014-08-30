#-------------------------------------------------------------------------------
# Name:        LNP Lib uidata wrapper
#
# Author:      lkumaresan
#
# Created:     22/10/2010
# Copyright:   (c) lkumaresan 2010
# Licence:     Personal
#
# Description:
#
#
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import os
import sys

##Remove cached custom modules from memory except preloaded IDE modules
if __name__ == '__main__':
    if globals().has_key('InitialModules'):
         for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
            del(sys.modules[CustomModule])
    else:
        InitialModules = sys.modules.keys()



#Global Lib
import time
import base64

#Application Lib
from LightNPray.lib import lnpLib
from LightNPray.lib import dummy_parent


class exLightPassData():

    def __init__(self, cParent):
        self.cParent = dummy_parent.DummyParent(cParent) if not hasattr(cParent,'Config') else cParent
        self.App = self.cParent.App
        self.Config = self.cParent.Config
        self.Common = self.cParent.Common

        self._dlib =  lnpLib.LNPLib() if 0 else None

    def setProject(self, project):
        data = ''
        ErrorFree = 0
        try:
            self._dlib = lnpLib.LNPLib(str(project))
            ErrorFree = 1
        except:
            print self.cParent.Common.errorReport()

        if self._dlib and ErrorFree:
            return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibInitFailed}

    def getSequences(self):
        data = ''
        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.getSequences()
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibGetSeqFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def getShots(self,seqName):
        data = ''
        if seqName == '' or seqName =='None' or not seqName:
            print 'Invalid Input for getShots'
            return {'DATA': '', 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.getShots(str(seqName))
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibGetShotFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def getPassType(self, seq, shots):
        data = ''
        if seq == '' or seq == 'None' or not seq or type(seq) != type(''):
            print 'Invalid Input for getPassType'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.getPassTypes(seq, shots)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibGetPassTypeFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def getPass(self, passTypeName, seq, shots):
        data = ''
        if passTypeName == '' or seq == '' or seq == 'None' or not seq or type(seq) != type(''):
            print 'Invalid Input for get pass'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.getPasses(passTypeName, seq, shots)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibGetPassFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def getAOV(self, passName, passTypeName, seq, shots):
        data = ''
        if passTypeName == '' or passName == '' or seq == '' or shots == '':
            print 'Invalid Input for get AOV'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.getAOVs(passName, passTypeName, seq, shots)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibGetAOVFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def getPassScenes(self, seq, shot):
        data = ''
        if seq == '':
            print 'Invalid Input for get pass scenes'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.getPassScenes(seq, shot)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibGetPassSceneFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def getPassScenesAssests(self, scname, seq, shot, passType):
        data = ''
        if scname == '' or seq == '' or shot == '':
            print 'Invalid Input for get pass scene assets'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.getPassSceneAssets(scname, seq, shot, passType)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibGetPassSceneAssetFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}

    def getWorkFiles(self, seq, shot):
        data = ''
        if seq == '' or shot == '':
            print 'Invalid Input for get work files'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.getSceneFiles(seq, shot)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibGetWorkFilesFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def getAssets(self, seq, shot):
        data = ''
        if seq == '' or shot == '':
            print 'Invalid Input for get assets'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.getShotAssets(seq, shot)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibGetAssetsFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def getGlobal(self, request='PASSTYPE'):
        '''
        request = 'PASSTYPE', 'PASS', 'AOV'
        '''
        if request=='PASSTYPE':
            return self.__globals(request)['DATA']
        if request=='PASS':
            return self.__globals(request)['DATA']
        if request=='AOV':
            return self.__globals(request)['DATA']

    def __globals(self,request='PASSTYPE'):
        data = []

        if self._dlib:
            ErrorFree = 0
            try:
                #data = ['SAMPLE1','SAMPLE2','SAMPLE3']
                if request=='PASSTYPE':
                    data = self._dlib.getGlobalPassTypes()
                if request=='PASS':
                    data = self._dlib.getGlobalPasses()
                if request=='AOV':
                    data = self._dlib.getGlobalAOVs()
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibGetGlobalsFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}



    def doAddPassScene(self, passSceneName, passType, seqName, shotName):
        data = ''
        if seqName == '':
            print 'Invalid Input for add pass scene'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.addPassScene(passSceneName, passType, seqName, shotName)
                self.doSave(seqName, shotName)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibAddPassSceneFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def doRemovePassScene(self, passSceneName, seqName, shotName, passType):
        data = ''
        if seqName == '':
            print 'Invalid Input for removing pass scene'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.removePassScene(passSceneName, seqName, shotName, passType)
                self.doSave(seqName, shotName)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibRemovePassSceneFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def doAddPassSceneAsset(self, rnName, rnPath, scnName, seqName, shotName, passType):
        data = ''
        if rnName == '' or rnPath == '' or scnName == '' or seqName == '' or shotName == '':
            print 'Invalid Input for add pass scene asset'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.addPassSceneAsset(rnName, rnPath, scnName, seqName, shotName, passType)
                self.doSave(seqName, shotName)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibAddPassSceneAssetFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def doRemovePassSceneAsset(self, rnName, scnName, seqName, shotName, passType):
        data = ''
        if seqName == '':
            print 'Invalid Input for remove pass scene asset'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.removePassSceneAsset(rnName, scnName, seqName, shotName, passType)
                self.doSave(seqName, shotName)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibAddPassSceneAssetFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def doAddPassType(self, passTypeName, seqName, shotName, ApplyToSeq=False):
        data = ''
        if passTypeName == '' or seqName == '' or shotName=='':
            print 'Invalid Input for add passtype'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.addPassType(passTypeName, seqName, shotName, addToSeq=ApplyToSeq)
                self.doSave(seqName,'') if ApplyToSeq else self.doSave(seqName, shotName)
                #dgdata = self._dlib.addGlobalPassType(passTypeName)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibAddPassTypeFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def doRemovePassType(self, passTypeName, seqName, shotName):
        data = ''
        if passTypeName == '' or seqName == '' or shotName == '':
            print 'Invalid Input for remove passtype'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.removePassType(passTypeName, seqName, shotName)
                self.doSave(seqName, shotName)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibRemovePassTypeFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}




    def doAddPass(self, passName, passCode, passTypeName, seqName, shotName, ApplyToSeq=False):
        data = ''
        if passTypeName == '' or seqName == '' or shotName == '':
            print 'Invalid Input for add pass'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.addPass(passName, passCode, passTypeName, seqName, shotName, addToSeq=ApplyToSeq)
                self.doSave(seqName,'') if ApplyToSeq else self.doSave(seqName, shotName)
                #dgdata = self._dlib.addGlobalPass(passName, passCode)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibAddPassFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def doRemovePass(self, passName, passTypeName, seqName, shotName):

        data = ''
        if passTypeName == '' or seqName == '' or shotName == '':
            print 'Invalid Input for remove pass'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.removePass(passName, passTypeName, seqName, shotName)
                self.doSave(seqName, shotName)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibRemovePassFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}




    def doAddAOV(self, aovNames, passName, passTypeName, seqName, shotName, ApplyToSeq=False, MatteExtra=''):
        data = ''
        if aovNames==[] or passTypeName == '' or seqName == '' or shotName == '':
            print 'Invalid Input for AOV add'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                res = []
                for aovName in aovNames:
                    print 'Adding aov...' + aovName
                    data = self._dlib.addAOV(aovName, passName, passTypeName, seqName, shotName, addToSeq=ApplyToSeq, matteString=MatteExtra)
                    res.append(data)
                self.doSave(seqName,'') if ApplyToSeq else self.doSave(seqName, shotName)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            Prob = 0
            for each in res:
                if each==-1:
                    Prob = 1

            if ErrorFree and not Prob:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibAddAOVFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def doRemoveAOV(self, aovName, passName, passTypeName, seqName, shotName):

        data = ''
        if passTypeName == '' or seqName == '' or shotName == '':
            print 'Invalid Input for remove aov'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.removeAOV(aovName, passName, passTypeName, seqName, shotName)
                self.doSave(seqName, shotName)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibRemoveAOVFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


    def doBuildFiles(self, seqName, shotName, sceneFiles,  mayaVersion='MAYA2008'):
        data = ''
        if seqName == '':
            print 'Invalid Input for building files.'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.buildFiles(seqName, shotName, mayaVersion, sceneFiles)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibGetSeqFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}



    def doSave(self, seqName, shotName=''):
        data = ''
        if seqName == '':
            print 'Invalid Input for saving XML'
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': ''}

        if self._dlib:
            ErrorFree = 0
            try:
                data = self._dlib.save(seqName, shotName)
                ErrorFree = 1
            except:
                print self.cParent.Common.errorReport()

            if ErrorFree and data!=-1:
                return {'DATA': data, 'STATUS': 1, 'MESSAGE': ''}
            else:
                return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibGetSeqFail}
        else:
            return {'DATA': data, 'STATUS': 0, 'MESSAGE': self.Config.Strings.lnpLibNotInitalized}


if __name__ == '__main__':
    data = exLightPassData(None)
    #data.setProject('DOZ')
    #print data.getSequences()
    #print data.getShots('SQ040')
    #print data.getPassType('SQ040', 'SC039')
    #print data.getPass('GEOM','SQ040', 'SC039')
    #print data.getAOV('Occlusion','GEOM','SQ040', 'SC039')
    #print data.getPassScenes('SQ040', 'SC039')


    data.setProject('ZZP')
    seq01 = 'SEQ002'
    shot01 = 'SHOT0001'
    print data.getWorkFiles(seq01, shot01)
    #print data.getAssets('SEQ002', 'SHOT0001')


    #print data.doAddPassType('NewPass2','SQ040','SC039')
    #print data.doRemovePassType('NewPass2','SQ040','SC039')

    #print data.doAddPass('Key2','ky2','GEOM','SQ040', 'SC039')
    #print data.doRemovePass('Key2','GEOM','SQ040', 'SC039')

    #print data.doAddAOV('SSS', 'Occlusion','GEOM','SQ040', 'SC039')
    #print data.doRemoveAOV('SSS', 'Occlusion','GEOM','SQ040', 'SC039')

    #print data.doAddPassScene('SCPASS2', 'GEOM', 'SQ040', 'SC039')

    #print data.doSave('SQ040','SC039')