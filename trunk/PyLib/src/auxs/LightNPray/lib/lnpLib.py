import os
import shutil
import lnpBaseClasses as lnpbc

import launchRender as lr
reload(lr)



class LNPLib() :
    def __init__(self, projCode, seqName='', baseFolder='http://192.168.20.93:85/pulse/beat/projects') :
        self.projCode = projCode
        self.lightProc = 'LIGHTING'
        self.lightProcCode = 'LIT'
        self.baseFolder = baseFolder
        if not self.baseFolder.endswith('/') :
            self.baseFolder += '/'
        self.xmlRoot = self.baseFolder + self.projCode + '/WORK/XML/LNP'

        seqShots = self.__getDetails()
        data = {}
        if seqName in seqShots.keys() :
            data[seqName] = seqShots[seqName]
        else :
            data = seqShots

        data = self.__checkLock(data)
        self.seqShotObjs = self.__setupObjs(data)
        return

    def __checkLock(self, data) :
        return data

    def __getDetails(self) :
        assetXMLPath = self.baseFolder + self.projCode + '/WORK/XML/PROCESS/project_assets.xml'
        return lnpbc.getSequenceShotDetails(assetXMLPath)

    def getSequences(self) :
        return self.seqShotObjs.keys()

    def getShots(self, seqName) :
        for eachSeq in self.seqShotObjs.keys() :
            if eachSeq.lower() == seqName.lower() :
                return self.seqShotObjs[eachSeq]['shots'].keys()
        return []

    def __setupObjs(self, seqShots) :
        seqShotObjs = {}
        for seqName in seqShots.keys() :
            seqObj = lnpbc.Sequence(seqName, self.projCode)
            if not seqObj.status :
                continue
            stat = seqObj.openXML(self.xmlRoot, self.projCode)
            if stat == -1 :
                continue
            seqShotObjs[seqName] = {}
            seqShotObjs[seqName]['obj'] = seqObj
            seqShotObjs[seqName]['shots'] = {}
            for shotName in seqShots[seqName] :
                if seqName == 'SEQ002' and shotName == 'SHOT0001' :
                    pass
                shotObj = lnpbc.Shot(shotName, seqObj, self.projCode)
                if not shotObj.status :
                    continue
                stat = shotObj.openXML(self.xmlRoot, self.projCode)
                if stat == -1 :
                    continue
                seqObj.shots.append(shotObj)
                seqShotObjs[seqName]['shots'][shotName] = shotObj
        return seqShotObjs

    def __getSeqShotObj(self, seqName, shotName='') :
        if not seqName in self.seqShotObjs.keys() :
            return ''
        if shotName == '' :
            obj = self.seqShotObjs[seqName]['obj']
        else :
            if shotName not in self.seqShotObjs[seqName]['shots'].keys() :
                return ''
            obj = self.seqShotObjs[seqName]['shots'][shotName]
        return obj

    def addPassType(self, passTypeName, seqName, shotName='', addToSeq=False) :
        obj = self.__getSeqShotObj(seqName, shotName)
        if obj == '' :
            return -1
        ptObj = obj.addPassType(passTypeName)
        if not isinstance(ptObj, lnpbc.PassType) :
            return -1
        if addToSeq :
            shots = self.getShots(seqName)
            for eachShot in shots :
                stat = self.addPassType(passTypeName, seqName, eachShot)
        return 0

    def getPassTypes(self, seqName, shotName='') :
        obj = self.__getSeqShotObj(seqName, shotName)
        if obj == '' :
            return []
        return obj.getPassTypes()

    def removePassType(self, passTypeName, seqName, shotName='') :
        obj = self.__getSeqShotObj(seqName, shotName)
        if obj == '' :
            return []
        return obj.removePassType(passTypeName)

    def __getPassTypeObj(self, passTypeName, seqName, shotName='') :
        obj = self.__getSeqShotObj(seqName, shotName)
        if obj == '' :
            return ''
        return obj.getPassTypeObj(passTypeName)

    def addPass(self, passName, passCode, passTypeName, seqName, shotName='', addToSeq=False) :
        ptObj = self.__getPassTypeObj(passTypeName, seqName, shotName)
        if not isinstance(ptObj, lnpbc.PassType) :
            return -1
        passObj = ptObj.addPass(passName, passCode)
        if not isinstance(passObj, lnpbc.Pass) :
            return -1
        if addToSeq :
            shots = self.getShots(seqName)
            for eachShot in shots :
                stat = self.addPass(passName, passCode, passTypeName, seqName, eachShot)
        return 0

    def getPasses(self, passTypeName, seqName, shotName = '') :
        ptObj = self.__getPassTypeObj(passTypeName, seqName, shotName)
        if not isinstance(ptObj, lnpbc.PassType) :
            return []
        return ptObj.getPasses()

    def removePass(self, passName, passTypeName, seqName, shotName='') :
        ptObj = self.__getPassTypeObj(passTypeName, seqName, shotName)
        if not isinstance(ptObj, lnpbc.PassType) :
            return -1
        return ptObj.removePass(passName)

    def __getPassObj(self, passName, passTypeName, seqName, shotName='') :
        ptObj = self.__getPassTypeObj(passTypeName, seqName, shotName)
        if not isinstance(ptObj, lnpbc.PassType) :
            return ''
        return ptObj.getPassObjByName(passName)

    def getPassNameFromCode(self, passCode, passTypeName, seqName, shotName='') :
        ptObj = self.__getPassTypeObj(passTypeName, seqName, shotName)
        if not isinstance(ptObj, lnpbc.PassType) :
            return ''
        passObj = ptObj.getPassObjByCode(passCode)
        if not isinstance(passObj, lnpbc.Pass) :
            return ''
        return passObj.name

    def addAOV(self, aovName, passName, passTypeName, seqName, shotName='', addToSeq=False, matteString='') :
        passObj = self.__getPassObj(passName, passTypeName, seqName, shotName)
        if not isinstance(passObj, lnpbc.Pass) :
            return -1
        aovObj =  passObj.addAOV(aovName, matteString)
        if not isinstance(aovObj, lnpbc.AOV) :
            return -1
        if addToSeq :
            shots = self.getShots(seqName)
            for eachShot in shots :
                stat = self.addAOV(aovName, passName, passTypeName, seqName, eachShot, matteString=matteString)
        return 0

    def getAOVs(self, passName, passTypeName, seqName, shotName='') :
        passObj = self.__getPassObj(passName, passTypeName, seqName, shotName)
        if not isinstance(passObj, lnpbc.Pass) :
            return -1
        return passObj.getAOVs()

    def removeAOV(self, aovName, passName, passTypeName, seqName, shotName='') :
        passObj = self.__getPassObj(passName, passTypeName, seqName, shotName)
        if not isinstance(passObj, lnpbc.Pass) :
            return -1
        return passObj.removeAOV(aovName)

    def addPassScene(self, sceneName, passType, seqName, shotName) :
        shotObj = self.__getSeqShotObj(seqName, shotName)
        if not isinstance(shotObj, lnpbc.Shot) :
            return -1
        return shotObj.addPassScene(sceneName, passType)

    def getPassScenes(self, seqName, shotName) :
        shotObj = self.__getSeqShotObj(seqName, shotName)
        if not isinstance(shotObj, lnpbc.Shot) :
            return {}
        return shotObj.getPassScenes()

    def removePassScene(self, sceneName, seqName, shotName, passType) :
        shotObj = self.__getSeqShotObj(seqName, shotName)
        if not isinstance(shotObj, lnpbc.Shot) :
            return -1
        return shotObj.removePassScene(sceneName, passType)

    def getSceneFiles(self, seqName, shotName) :
        shotObj = self.__getSeqShotObj(seqName, shotName)
        if not isinstance(shotObj, lnpbc.Shot) :
            return []
        return shotObj.getSceneFiles(self.projCode, self.lightProcCode, self.lightProc)

    def getSceneFilesByPasses(self, seqName, shotName) :
        shotObj = self.__getSeqShotObj(seqName, shotName)
        if not isinstance(shotObj, lnpbc.Shot) :
            return []
        return shotObj.getSceneFilesByPasses(self.projCode, self.lightProcCode, self.lightProc)

    def getShotAssets(self, seqName, shotName) :
        shotObj = self.__getSeqShotObj(seqName, shotName)
        if not isinstance(shotObj, lnpbc.Shot) :
            return []
        return shotObj.getOrderedAssets()

    def __getPassSceneObj(self, sceneName, seqName, shotName, passType) :
        shotObj = self.__getSeqShotObj(seqName, shotName)
        if not isinstance(shotObj, lnpbc.Shot) :
            return ''
        return shotObj.getPassSceneObj(sceneName, passType)

    def getScenePassType(self, sceneName, seqName, shotName) :
        sceneObj = self.__getPassSceneObj(sceneName, seqName, shotName)
        if not isinstance(sceneObj, lnpbc.PassScene) :
            return ''
        return sceneObj.passType

    def getPassSceneAssetRprs(self, sceneName, seqName, shotName) :
        sceneObj = self.__getPassSceneObj(sceneName, seqName, shotName)
        if not isinstance(sceneObj, lnpbc.PassScene) :
            return []
        result = []
        for each in sceneObj.assets :
            result.append(each.rpr)
        return result

    def addPassSceneAsset(self, rpr, path, sceneName, seqName, shotName, passType) :
        passSceneObj = self.__getPassSceneObj(sceneName, seqName, shotName, passType)
        if not isinstance(passSceneObj, lnpbc.PassScene) :
            return -1
        return passSceneObj.addAsset(rpr, path)

    def getPassSceneAssets(self, sceneName, seqName, shotName, passType) :
        passSceneObj = self.__getPassSceneObj(sceneName, seqName, shotName, passType)
        if not isinstance(passSceneObj, lnpbc.PassScene) :
            return {}
        return passSceneObj.getAssets()

    def removePassSceneAsset(self, rpr, sceneName, seqName, shotName, passType) :
        passSceneObj = self.__getPassSceneObj(sceneName, seqName, shotName, passType)
        if not isinstance(passSceneObj, lnpbc.PassScene) :
            return -1
        return passSceneObj.removeAsset(rpr)

    def save(self, seqName, shotName='') :
        obj = self.__getSeqShotObj(seqName, shotName)

        stat = obj.saveXML(self.xmlRoot)
        if stat == -1 :
            return -1

        if not isinstance(obj, lnpbc.Sequence) :
            return 0

        for eachShotObj in obj.shots :
            stat = eachShotObj.saveXML(self.xmlRoot)
            if stat == -1 :
                print 'Error saving xml of shot', eachShotObj.name, 'of sequence', obj.name
        return 0

    def buildFiles(self, seqName, shotName, mayaVersion='MAYA2008', sceneFiles=[], templatesPath='Z:/repo/source/scripts/python/LightNPray/templates') :
        localDir = 'D:/ABX_PULSE/' + os.getenv('USERNAME').upper() + '/' + self.projCode.upper() + '/WORK/' + seqName.upper() + '/' + shotName.upper() + '/' + self.lightProc.upper()
        if not templatesPath.endswith('/') :
            templatesPath += '/'

        mayaVer = mayaVersion.upper().replace(' ', '')
        if mayaVer == 'MAYA2008' :
            mayaFilePath = templatesPath + '/MAYA2008.ma'
        elif mayaVer == 'MAYA2009' :
            mayaFilePath = templatesPath + '/MAYA2009.ma'
        elif mayaVer == 'MAYA2011' :
            mayaFilePath = templatesPath + '/MAYA2011.ma'
        else :
            return -1

        if not os.path.exists(localDir) :
            stat = os.makedirs(localDir)
        sceneData = self.getSceneFiles(seqName, shotName)
        if len(sceneFiles) :
            tempData = sceneData
            sceneData = {}
            for eachScene in sceneFiles :
                if not eachScene in tempData.keys():
                    continue
                sceneData[eachScene] = tempData[eachScene]

        for eachScene in sceneData.keys() :
            sceneDir = localDir + '/' + eachScene.upper()
            if os.path.exists(sceneDir+'/'+eachScene) :
                continue
            if not os.path.exists(sceneDir) :
                try :
                    stat = os.mkdir(sceneDir)
                except :
                    continue
            fileNames = sceneData[eachScene]
            for eachFile in fileNames :
                if os.path.exists(sceneDir+"/"+eachFile) :
                    continue
                stat = shutil.copy(mayaFilePath, sceneDir+'/'+eachFile)

        return 0

    def addGlobalPassType(self, name) :
        return lnpbc.addGlobal(self.baseFolder, name, 'passtype')

    def addGlobalPass(self, name, code) :
        return lnpbc.addGlobal(self.baseFolder, name, 'pass', code)

    def addGlobalAOV(self, name) :
        return lnpbc.addGlobal(self.baseFolder, name, 'aov')

    def getGlobalPassTypes(self) :
        return lnpbc.getGlobals(self.baseFolder, 'passtype')

    def getGlobalPasses(self) :
        return lnpbc.getGlobals(self.baseFolder, 'pass')

    def getGlobalAOVs(self) :
        return lnpbc.getGlobals(self.baseFolder, 'aov')

    def removeGlobalPassType(self, name) :
        return lnpbc.removeGlobal(self.baseFolder, name, 'passtype')

    def removeGlobalPass(self, name, code) :
        return lnpbc.removeGlobal(self.baseFolder, name, 'pass')

    def removeGlobalAOV(self, name) :
        return lnpbc.removeGlobal(self.baseFolder, name, 'aov')

##    def render(self, filePath) :
##        return lr.launchRocket(filePath)
##
    def updatePassFile(self) :
        return lr.updatePassFile()

##l = LNPLib('ZZP')
##seq01 = 'SEQ002'
##shot01 = 'SHOT0008'
##x = l.getShotAssets(seq01, shot01)
##for k1 in x.keys() :
##    for k2 in x[k1].keys() :
##        for k3 in x[k1][k2].keys() :
##            for k4 in x[k1][k2][k3].keys() :
##                print k4
##print l.addPassType('GEOM', seq01, shot01)
##print l.addPassType('Foliage', seq01, shot01)
##print l.addPass('Occlusion', 'OCC', 'Geom', seq01, shot01)
##print l.addPass('Key', 'KEY', 'Geom', seq01, shot01)
##print l.addPass('Rim', 'RIM', 'Geom', seq01, shot01)
##print l.addAOV('Shadow', 'Occlusion', 'Geom', seq01, shot01)
##print l.addAOV('Specular', 'Occlusion', 'Geom', seq01, shot01)
##print l.addAOV('lights', 'KEY', 'FOLIAGE', seq01, shot01, True)
##print l.addPassScene('LNPTEST', 'GEOM', seq01, shot01)
##print l.getSceneFilesByPasses(seq01, shot01)
##print l.getSceneFiles(seq01, shot01)
##print l.removePassType('Geom', seq01, shot01)
##print l.removePassType('Foliage', seq01, shot01)
##print l.removePassScene('TINKWIDIA', seq01, shot01)
##print l.save(seq01, shot01)
##print l.getPassTypes(seq01, shot01)
##print l.getPasses('GEOM', seq01, shot01)
##print l.getShotAssets(seq01, shot01)
##print l.getPassScenes(seq01, shot01)
##print l.getScenePassType('TWSN', seq01, shot01)
##print l.getPassNameFromCode('OCC', 'GEOM', seq01, shot01)
##print l.addPassSceneAsset('PROP_SKYDOME_001RN', 'L:/MATTE/SKYDOME/GEOM/GEO_ZZP_PROP_SKYDOME.mb', 'LNPTEST', seq01, shot01, "GEOM")
##print l.getPassSceneAssets('TINKWIDIA', seq01, shot01)
##print l.save(seq01, shot01)

##print l.getAOVs('OCCLUSION', "GEOM", seq01, shot01)
##print l.buildFiles(seq01, shot01, 'MAYA2008')
##temp = ['ambient','constant', 'diffuse', 'diffuse_unshadowed', 'specular', 'shadow', 'reflect', 'refract', 'incandescence',
## 'indirect', 'bleed', 'occl', 'translucence', 'normal', 'xyz', 'front_scatter', 'multiple_scatter', 'back_scatter',
## 'constant_no_opac', 'facing_ratio', 'uvw', 'normalC', 'scatter_mix_map', 'rsmb', 'rsmbtransp']

##temp = {'OCCLUSION':'OCC', "KEY":'KEY', 'LIGHT':'LIGHT', 'EXTRALIGHT':'EXTRA', 'FILL':'FILL', 'RIM':'RIM', "INTERACTIVE":'INT', 'LIGHTS':'LIGHTS', 'FILL':'FILL'
##        ,'KEYKICKER':'KICK', 'BOUNCE':'BNC', 'EYES':'EYE', 'SHADOW':'SHD', "CONTACTSHADOW":"CSHD", "GOBO":"GOBO", "SSS":"SSS", "LAYER":"LYR", "BASE":"BASE"
##        , "POINTCLOUD":"PTC", "REFLREFR":"REFLREFR", "CONSTANT":"CONST", "MISC":"MISC"}
##
##for each in temp.keys() :
##    print l.addGlobalPass(each, temp[each])

##print l.getGlobalAOVs()
##print l.removeGlobalAOV('diffuse')
##l.addGlobalAOV('mattenode')


##occ - occlusion
##key - key
##kick - key kicker
##light - light
##extra - extra light
##fill - fill
##rim - rim
##bnc -bounce
##int -interactive
##eyes -eyes
##shd -shadow
##cshd - contact shadow
##gobo = gobo
##sss - sub surface scattering
##lyr - layer
##base = base
##ptc - point cloud
##refl_refr = reflection refraction
##fol_const = foliage constant
##fol_misc = foliage miscellaneous

##l.render("D:/ABX_PULSE/SINGHP/ZZP/WORK/SEQ002/SHOT0008/LIGHTING/LIT_ZZP_SEQ002_SHOT0008_TWSN_OCC.ma")


##import sys
##if "Z:/REPO/SOURCE/SCRIPTS/PYTHON/LightNPray/lib" not in sys.path :
##    sys.path.append("Z:/REPO/SOURCE/SCRIPTS/PYTHON/LightNPray/lib")
##import lnpLib as ll
##reload(ll)
##
##x = ll.LNPLib("ZZP", "SEQ002")
##x.render("D:/ABX_PULSE/SINGHP/ZZP/WORK/SEQ002/SHOT0008/LIGHTING/TWSN/LIT_ZZP_SEQ002_SHOT0008_TWSN_GEOM_OCC.ma")
