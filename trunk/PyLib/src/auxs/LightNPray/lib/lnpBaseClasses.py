import sys
import os
##cwd = os.getcwd()
##parentPath = os.path.dirname(os.path.dirname(cwd))
##pulseXmlPath = parentPath + '/PulseXML'
xmlLibLoc = 'Z:/REPO/SOURCE/SCRIPTS/PYTHON/PulseXML'
if xmlLibLoc not in sys.path :
    sys.path.append(xmlLibLoc)
##if not pulseXmlPath in sys.path :
##    sys.path.append(pulseXmlPath)
import PulseXMLLib as pxml

def removeUnWantedChars(string):
        allowedChrs = [
                        'A','B','C','D','E','F','G','H','I','J','K','L',
                        'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                        'a','b','c','d','e','f','g','h','i','j','k','l',
                        'm','n','o','p','q','r','s','t','u','v','w','x','y','z',
                        '1','2','3','4','5','6','7','8','9','0',
                       ]
        nname = ''
        for eachChr in string:
            if eachChr in allowedChrs: nname += eachChr
        return nname

class BasicDetails() :
    def __init__(self, name) :
        self.name = removeUnWantedChars(name)


class XMLCmnds() :
    def __getTree(self, xmlPath) :
##        if isinstance(self, Shot) :
##            rootName =  self.parent.name.lower() + '_' + self.name.lower()
##        elif isinstance(self, Sequence) :
##            rootName = self.name.lower()
##        else :
##            return ''

##        xmlPath = self.__getXMLPath(xmlDirFolder)
        rootName = xmlPath.split('/')[-1][:-4]


##        if path == -1 :
##            return ''
        tree = self.__setupXML(xmlPath, rootName)
        return tree


    def __setupXML(self, xmlPath, rootName) :
        xmlTree = pxml.PulseXML()
        stat = xmlTree.setup(xmlPath, rootName)
        if stat == -1 :
            return ''
        return xmlTree

    def saveXML(self, xmlDirFolder) :
        xmlPath = self.__getXMLPath(xmlDirFolder)
        if xmlPath == -1 :
            return -1
        stat = self.__createTree(xmlPath)
        if stat == -1 :
            return -1
##        if xmlPath == '' :
        xmlPath = self.xmlTree.xml_file
        return self.xmlTree.writeFile(xmlPath)

    def __createTree(self, xmlDirFolder) :
        if not isinstance(self, Sequence) and not isinstance(self, Shot) :
            return -1
        self.xmlTree = self.__getTree(xmlDirFolder)
        if self.xmlTree == '' :
            return -1
        stat = self.__addPassTypesElems(self.xmlTree)
        stat = self.__addPassSceneElems(self.xmlTree)
        return 0

    def __addPassTypesElems(self, xmlTree) :
        childElems = xmlTree.getChildElements(xmlTree.root_elem, ['passtype'])
        for eachChild in childElems :
            xmlTree.root_elem.remove(eachChild)

        passTypes = self.passTypes
        for eachPT in passTypes :
            ptElem = xmlTree.addNodeElem('passtype', '', xmlTree.root_elem)
            nameElem = xmlTree.addNodeElem('name', eachPT.name, ptElem)
            passes = eachPT.passes
            for eachPass in passes :
                passElem = xmlTree.addNodeElem('pass', '', ptElem)
                nameElem = xmlTree.addNodeElem('name', eachPass.name, passElem)
                codeElem = xmlTree.addNodeElem('code', eachPass.code, passElem)
                aovs = eachPass.aovs
                for eachAOV in aovs :
                    aovElem = xmlTree.addNodeElem('aov', '', passElem)
                    nameElem = xmlTree.addNodeElem('name', eachAOV.name, aovElem)
        return 0

    def __addPassSceneElems(self, xmlTree) :
        if not isinstance(self, Shot) :
            return -1
        childElems = xmlTree.getChildElements(xmlTree.root_elem, ['scene'])
        for eachChild in childElems :
            xmlTree.root_elem.remove(eachChild)

        for sceneObj in self.passScenes :
            psElem = xmlTree.addNodeElem('scene', '', xmlTree.root_elem)
            nameElem = xmlTree.addNodeElem('name', sceneObj.name, psElem)
            ptElem = xmlTree.addNodeElem('type', sceneObj.passType, psElem)
            for assetObj in sceneObj.assets :
                assetElem = xmlTree.addNodeElem('asset', '', psElem)
                rprElem = xmlTree.addNodeElem('rpr', assetObj.rpr, assetElem)
                pathElem = xmlTree.addNodeElem('path', assetObj.path, assetElem)
        return 0

    def __getXMLPath(self, xmlDirFolder) :
        fileName = self.name.lower() + '.xml'
        if isinstance(self, Shot) :
            fileName =  self.parent.name.lower() + '_' + fileName
        elif not isinstance(self, Sequence) :
            return -1

        if not xmlDirFolder.endswith('/') :
            xmlDirFolder += '/'

        return xmlDirFolder + fileName

    def openXML(self, xmlDirFolder, projCode) :
        xmlPath = self.__getXMLPath(xmlDirFolder)
        if xmlPath == -1 :
            return -1
        self.xmlTree = self.__getTree(xmlPath)
        if self.xmlTree == '' :
            print 'XMLCmnds.setupObjects :- Could not open XML file', xmlPath
            return -1

##        print len(self.xmlTree.getChildElements(self.xmlTree.root_elem))
        if len(self.xmlTree.getChildElements(self.xmlTree.root_elem)) :
            stat = self.__setPassTypeObjs()
            stat = self.__setPassSceneObjs()
        elif isinstance(self, Shot) :
            seqObj = Sequence(self.parent.name, projCode)
            stat = seqObj.openXML(xmlDirFolder, projCode)
            self.passTypes = seqObj.passTypes
        return 0

    def __setPassTypeObjs(self) :
        passTypeElems = self.xmlTree.getChildElements(self.xmlTree.root_elem, ['passtype'])
        for eachPT in passTypeElems :
            nameElem = self.xmlTree.getChildElements(eachPT, ['name'])
            if not len(nameElem) == 1 :
                continue
            ptName = nameElem[0].text
            ptObj = self.addPassType(ptName)
            passElems = self.xmlTree.getChildElements(eachPT, ['pass'])
            for eachPass in passElems :
                nameElem = self.xmlTree.getChildElements(eachPass, ['name'])
                if not len(nameElem) == 1 :
                    continue
                passName = nameElem[0].text
                codeElem = self.xmlTree.getChildElements(eachPass, ['code'])
                if not len(codeElem) == 1 :
                    continue
                passCode = codeElem[0].text
                passObj = ptObj.addPass(passName, passCode)
                aovElems = self.xmlTree.getChildElements(eachPass, ['aov'])
                for eachAOV in aovElems :
                    nameElem = self.xmlTree.getChildElements(eachAOV, ['name'])
                    if not len(nameElem) == 1 :
                        continue
                    aovName = nameElem[0].text
                    passObj.addAOV(aovName)
        return 0

    def __setPassSceneObjs(self) :
        if not isinstance(self, Shot) :
            return -1

        sceneElems = self.xmlTree.getChildElements(self.xmlTree.root_elem, ['scene'])
        for eachScene in sceneElems :
            nameElem = self.xmlTree.getChildElements(eachScene, ['name'])
            if not len(nameElem) == 1 :
                continue
            sceneName = nameElem[0].text

            typeElem = self.xmlTree.getChildElements(eachScene, ['type'])
            if not len(typeElem) == 1 :
                continue
            passType = typeElem[0].text
            passSceneObj = PassScene(sceneName, passType)
            self.passScenes.append(passSceneObj)

            assetElem = self.xmlTree.getChildElements(eachScene, ['asset'])
            for eachAsset in assetElem :
                rprElem = self.xmlTree.getChildElements(eachAsset, ['rpr'])
                if not len(rprElem) == 1 :
                    continue
                pathElem = self.xmlTree.getChildElements(eachAsset, ['path'])
                if not len([pathElem]) == 1 :
                    continue
                rpr = rprElem[0].text
                path = pathElem[0].text
                assetObj = Asset(rpr, path)
                passSceneObj.assets.append(assetObj)
        return 0

class PassTypeFunc() :
    def __init__(self) :
        self.passTypes = []
        return

    def addPassType(self, name) :
        obj = self.getPassTypeObj(name)
        if not obj == '' :
##            print 'PassTypeFunc.addPassType :- Pass type', name, 'already exists.'
            return -1

        ptObj = PassType(name, self)
        if not ptObj.status :
            return -1
        self.passTypes.append(ptObj)
##        print 'PassTypeFunc.addPassType :- Pass type', name, 'added successfully.'
        return ptObj

    def getPassTypeObj(self, name) :
        for eachPT in self.passTypes :
            if eachPT.name.lower() == name.lower() :
                return eachPT
        return ''

    def removePassType(self, name) :
        ptObj = self.getPassTypeObj(name)
        try :
            self.passTypes.remove(ptObj)
        except :
##            print 'PassTypeFunc.removePassType :- Unable to remove pass type', name, '.'
            return -1

##        print 'PassTypefunc.removePassType :- Pass type', name, 'removed successfully.'
        return 0

    def getPassTypes(self) :
        result = []
        for eachPassType in self.passTypes :
            result.append(eachPassType.name)
        return result


class Sequence(BasicDetails, PassTypeFunc, XMLCmnds) :
    def __init__(self, name, projectCode) :
        self.status = 1
        BasicDetails.__init__(self, name)
        PassTypeFunc.__init__(self)
        self.projectCode = projectCode
        self.shots = []
        return

    def addShot(self, shotName) :
        shotObj = self.getShotObj(shotName)
        if not shotObj == '' :
##            print 'Sequence.addShot :- Shot', shotName, 'already exists under', self.name, '.'
            return -1

        shotObj = Shot(shotName, self, self.projectCode)
        if not shotObj.status :
            return -1
        self.shots.append(shotObj)
##        print 'Sequence.addShot :- Shot', shotName, 'added successfully.'
        return shotObj

    def getShotObj(self, shotName) :
        for eachShot in self.shots :
            if eachShot.name.lower() == shotName.lower() :
                return eachShot
        return ''

    def removeShot(self, shotName) :
        shotObj = self.getShotObj(shotName)
        try :
            self.shots.remove(shotObj)
        except :
##            print 'Sequence.removeShot :- Unable to remove shot', shotName, 'in sequence', self.name, '.'
            return -1
##        print 'Sequence.removeShot :- Shot', shotName, 'removed from sequence', self.name, '.'
        return 0

    def getShots(self) :
        result = []
        for eachShot in self.shots :
            result.append(eachShot.name)
        return result



class Shot(BasicDetails, PassTypeFunc, XMLCmnds) :
    def __init__(self, name, seqObj, projectCode) :
        self.status = 0
        if not isinstance(seqObj, Sequence) :
            return
        self.status = 1
        BasicDetails.__init__(self, name)
        PassTypeFunc.__init__(self)
        self.seqname = seqObj.name
        self.projectCode = projectCode

        self.parent = seqObj
        self.passScenes = []
        self.assets = {} ## {rpr:'path'}
##        self.__getAvailableAssets()
        return
##ToDo1 Check for Pass type before adding scene file
    def addPassScene(self, name, passType) :
        passSceneObj = self.getPassSceneObj(name, passType)
        if not passSceneObj == '' and passSceneObj.passType.lower() == passType.lower() :
            return -1
        passSceneObj = PassScene(name, passType)
        if not passSceneObj.status :
            return -1
        self.passScenes.append(passSceneObj)
##        for eachScene in self.passScenes.keys() :
##            if eachScene.lower() == name.lower() :
##                return -1
##        self.passScenes[name] = passType
        return 0

    def getPassSceneObj(self, name, passType) :
        for eachObj in self.passScenes :
            if eachObj.name.lower() == name.lower() and eachObj.passType.lower() == passType.lower():
                return eachObj
        return ''

    def removePassScene(self, name, passType) :
        passSceneObj = self.getPassSceneObj(name, passType)
        if passSceneObj == '' :
            return -1
        self.passScenes.remove(passSceneObj)
        return 0

    def getPassScenes(self) :
        result = {}
        for eachObj in self.passScenes :
            i = len(result.keys())
            result[i] = {}
            result[i]['passType'] = eachObj.passType
            result[i]['assets'] = eachObj.getAssets()
            result[i]['name'] = eachObj.name
        return result

##    def getSceneFilesInfo(self, projCode, procCode) :
##        passNames = self.getPassScenes()
##
##        seqName = self.parent.name; shotName = self.name
##        result = []
##        for eachScene in passNames.keys() :
##            passTypeName = passNames[eachScene]['passType']
##            ptNames = self.getPassTypes()
##            found = 0
##            for eachPT in ptNames :
##                if eachPT.lower() == passTypeName.lower() :
##                    found = 1
##                    break
##            if not found :
##                continue
##            passTypeObj = self.getPassTypeObj(passTypeName)
##            if not isinstance(ptObj, PassType) :
##                continue
##            passes = passTypeObj.getPasses()
##            for eachPass in passes :
##                fileName = procCode.upper() + '_' + projCode.upper() + '_' + seqName.upper() + '_' + shotName.upper() + '_' + eachScene + '_' + passTypeObj.getPassCode(eachPass) + '.mb'
##                result.append(fileName)
##        return result

    def getSceneFiles(self, projCode, procCode, procName) :
        result = {}
        seqName = self.parent.name; shotName = self.name
        for eachObj in self.passScenes :
            passType = eachObj.passType
            sceneName = eachObj.name
            ptObj = self.getPassTypeObj(passType)
            if not isinstance(ptObj, PassType) :
                continue
            passes = ptObj.getPasses()
            if len(passes) :
                result[sceneName] = {}
            for eachPass in passes :
                fileName = procCode.upper() + '_' + projCode.upper() + '_' + seqName.upper() + '_' + shotName.upper() + '_' + sceneName.upper() + '_' + passType.upper() + '_' + ptObj.getPassCode(eachPass).upper() + '.ma'
                result[sceneName][fileName] = self.__getFilePath(projCode, seqName, shotName, procName, sceneName, fileName)
        return result

    def getSceneFilesByPasses(self, projCode, procCode, procName) :
        result = {}
        seqName = self.parent.name; shotName = self.name
        for eachObj in self.passScenes :
            passType = eachObj.passType
            sceneName = eachObj.name
            ptObj = self.getPassTypeObj(passType)
            if not isinstance(ptObj, PassType) :
                continue
            passes = ptObj.getPasses()
            for eachPass in passes :
                fileName = procCode.upper() + '_' + projCode.upper() + '_' + seqName.upper() + '_' + shotName.upper() + '_' + sceneName.upper() + '_' + passType.upper() + '_' + ptObj.getPassCode(eachPass).upper() + '.ma'
                if eachPass not in result.keys() :
                    result[eachPass] = {}

                result[eachPass][fileName] = self.__getFilePath(projCode, seqName, shotName, procName, sceneName, fileName)
        return result

    def __getFilePath(self, projCode, seqName, shotName, procName, sceneName, fileName) :
        username = os.getenv('USERNAME').upper()
        path = 'D:/ABX_PULSE/' + username + '/' + projCode.upper() + '/' + seqName.upper() + '/' + shotName.upper() + '/' + procName.upper() + '/' + sceneName.upper() + '/' + fileName
        return path

    def  getAvailableAssets(self) :
        xmlLoc = 'L:/' + self.parent.name.upper() + '/' + self.name.upper() + '/SHOTINFO/SHI_' + self.projectCode + '_' + self.parent.name.upper() + '_' + self.name.upper() + '.xml'
        if not os.path.exists(xmlLoc) :
            return -1
        xmlTree = pxml.PulseXML()
        stat = xmlTree.setup(xmlLoc)
        if not len(xmlTree.getChildElements(xmlTree.root_elem)) :
            return -1
        self.assets = self.__getRprNPaths(xmlTree)
        return 0

    def getOrderedAssets(self) :
        result = {}
        if not len(self.assets.keys()) :
            stat = self.getAvailableAssets()
        for rpr in self.assets.keys() :
            path = self.assets[rpr]
            pathSplit = path.split('/')
            if len(pathSplit) < 4 :
                continue
            assetTypeName = pathSplit[1]
            assetName = pathSplit[2]
            fileName = os.path.basename(path)
            fileSplit = fileName.split('_')
            if len(fileSplit) < 3 :
                continue
            baseTypeCode = fileSplit[2]
            if baseTypeCode not in result.keys() :
                result[baseTypeCode] = {}
            if assetTypeName not in result[baseTypeCode].keys() :
                result[baseTypeCode][assetTypeName] = {}
            if assetName not in result[baseTypeCode][assetTypeName].keys() :
                result[baseTypeCode][assetTypeName][assetName] = {}
            result[baseTypeCode][assetTypeName][assetName][rpr] = path
        return result

    def __hasAsset(self, path) :
        if path in self.assets.values() :
            return 1
        return 0

    def __getRprNPaths(self, xmlTree) :
        refElems = xmlTree.getChildElements(xmlTree.root_elem, ['Reference'])
        if not len(refElems) :
            return {}

        result = {}
        for eachRef in refElems :
            pathElems = xmlTree.getChildElements(eachRef, ['Path'])
            if not len(pathElems) == 1 :
                continue
            path = pathElems[0].text
            rpr = ''
            insElems = xmlTree.getChildElements(eachRef, ['Instance'])
            for eachIns in insElems :
                rprElems = xmlTree.getChildElements(eachIns, ['RPR'])
                if not len(rprElems) == 1 :
                    continue
                rpr = rprElems[0].text
                if rpr == '' :
                    continue
                result[rpr] = path
        return result



class PassScene(BasicDetails) :
    def __init__(self, name, passType) :
        BasicDetails.__init__(self, name)
        self.passType = passType
        self.assets = []
        self.status = 1
        return

    def addAsset(self, rpr, path) :
        assetObj = self.getAssetObj(rpr)
        if not assetObj == '' :
            return -1
        assetObj = Asset(rpr, path)
        if not assetObj.status :
            return -1
        self.assets.append(assetObj)
##        if rpr in self.assets.keys() :
##            return -1
##        self.assets[rpr] = path
        return 0

    def getAssetObj(self, rpr) :
        for each in self.assets :
            if each.rpr.lower() == rpr.lower() :
                return each
        return ''

    def getAssets(self) :
        result = {}
        for eachObj in self.assets :
            rpr = eachObj.rpr
            path = eachObj.path
            pathSplit = path.split('/')
            if len(pathSplit) < 4 :
                continue
            assetTypeName = pathSplit[1]
            assetName = pathSplit[2]
            fileName = os.path.basename(path)
            fileSplit = fileName.split('_')
            if len(fileSplit) < 3 :
                continue
            baseTypeCode = fileSplit[2]
            if baseTypeCode not in result.keys() :
                result[baseTypeCode] = {}
            if assetTypeName not in result[baseTypeCode].keys() :
                result[baseTypeCode][assetTypeName] = {}
            if assetName not in result[baseTypeCode][assetTypeName].keys() :
                result[baseTypeCode][assetTypeName][assetName] = {}
            result[baseTypeCode][assetTypeName][assetName][rpr] = path
        return result

    def removeAsset(self, rpr) :
        assetObj = self.getAssetObj(rpr)
        if assetObj == '' :
            return -1
        self.assets.remove(assetObj)
##        if rpr not in self.assets.keys() :
##            return -1
##        self.assets.pop(rpr)
        return 0



class Asset():
    def __init__(self, rpr, path) :
        self.path = path
        self.rpr = rpr
        self.status = 1
        return



class PassType(BasicDetails) :
    def __init__(self, name, parentObj) :
        self.status = 0
        if not isinstance(parentObj, Sequence) and not isinstance(parentObj, Shot) :
            return
        self.status = 1
        BasicDetails.__init__(self, name)
        self.parent = parentObj
        self.passes = []
        return

    def addPass(self, name, code) :
        passObj = self.getPassObjByName(name)
        if not passObj == '' :
##            print 'PassType.addPass :- Pass', name, 'already exists.'
            return -1
        passObj = self.getPassObjByCode(code)
        if not passObj == '' :
##            print 'PassType.addPass :- Pass with code', code, 'already exists.'
            return -1

        passObj = Pass(name, code, self)
        if not passObj.status :
            return -1
        self.passes.append(passObj)
##        print 'PassType.addPass :- Pass', name, 'added successfully.'
        return passObj

    def getPassObjByName(self, name) :
        for eachPass in self.passes :
            if eachPass.name.lower() == name.lower() :
                return eachPass
        return ''

    def getPassObjByCode(self, code) :
        for eachPass in self.passes :
            if eachPass.code.lower() == code.lower() :
                return eachPass
        return ''

    def removePass(self, name) :
        passObj = self.getPassObjByName(name)
        try :
            self.passes.remove(passObj)
        except :
##            print 'PassType.removePass :- Unable to remove pass', name
            return -1
##        print 'PassType.removePass :- Pass', name, 'removed successfully.'
        return 0

    def getPasses(self) :
        result = []
        for eachPass in self.passes :
            result.append(eachPass.name)
        return result

    def getPassCode(self, name) :
        passObj = self.getPassObjByName(name)
        if passObj == '' :
            return ''
        return passObj.code



class Pass(BasicDetails) :
    def __init__(self, name, code, passTypeObj) :
        self.status = 0
        if not isinstance(passTypeObj, PassType) :
            return
        if not self.__validNameCode(name, code, passTypeObj) :
            return
        self.status = 1
        BasicDetails.__init__(self, name)
        self.code = code
        self.parent = passTypeObj
        self.aovs = []
        return

## Validating name and code in shot or sequence
    def __validNameCode(self, name, code, passTypeObj) :
        try :
            grndPrntObj = passTypeObj.parent    ## Finding sequence or shot object
        except :
            return 0

        for eachPT in grndPrntObj.passTypes :
            for eachPass in eachPT.passes :
                if eachPass.name.lower() == name.lower() or eachPass.code.lower() == code.lower() :
                    if eachPass.name.lower() == name.lower() and eachPass.code.lower() == code.lower() :
                        continue
                    return 0
        return 1

    def addAOV(self, name, matteString='') :
        if name == 'mattenode' :
            return self.__addMatteNodeAOV(name, matteString)
        print name
        aovObj = self.getAOVObj(name)
        if not aovObj == '' :
            return -1
        aovObj = AOV(name, self)
        if not aovObj.status :
            return -1
        self.aovs.append(aovObj)
        return aovObj

    def __addMatteNodeAOV(self, name, matteString) :
        if matteString == '' :
            return -1

        pad = self.__getAOVPadding(matteString)
        commaSplit = matteString.split(',')
        for eachComma in commaSplit :
            eachComma = eachComma.replace(' ', '')
            if not '-' in eachComma :
                stat = self.__addMatte(name, eachComma, pad)
                continue
            stIndex = eachComma.find('-')
            edIndex = eachComma.rfind('-')
            if not stIndex == edIndex :
                continue
            try :
                stNum = int(eachComma[:stIndex])
                edNum = int(eachComma[stIndex+1:])
            except :
                continue
            for num in range(stNum, edNum+1) :
                stat = self.__addMatte(name, num, pad)
        return 0

    def __getAOVPadding(self, matteString) :
        commaSplit = matteString.split(',')
        pad = 2
        for eachComma in commaSplit :
            eachComma = eachComma.replace(' ', '')
            if not '-' in eachComma :
                if len(eachComma) > pad :
                    pad = len(eachComma)
                continue
            stIndex = eachComma.find('-')
            edIndex = eachComma.rfind('-')
            if not stIndex == edIndex :
                continue
            if len(eachComma[:stIndex]) > pad :
                pad = len(eachComma[:stIndex])
            if len(eachComma[stIndex+1:]) > pad :
                pad = len(eachComma[stIndex+1:])
            continue
        return pad

    def __addMatte(self, name, num, pad) :
        if len(str(num)) < pad :
            for i in range(len(str(num)), pad) :
                num = '0' + str(num)
        try :
            n = int(num)
        except :
            return -1
        return self.addAOV(name+str(num))

    def getAOVObj(self, name) :
        for eachAOV in self.aovs :
            if eachAOV and eachAOV.name:
                if eachAOV.name.lower() == name.lower() :
                    return eachAOV
        return ''

    def removeAOV(self, name) :
        aovObj = self.getAOVObj(name)
        try :
            self.aovs.remove(aovObj)
        except :
            return -1
        return 0

    def getAOVs(self) :
        result = []
        for eachAOV in self.aovs :
            result.append(eachAOV.name)
        return result


class AOV(BasicDetails) :
    def __init__(self, name, passObj) :
        self.status = 0
        if not isinstance(passObj, Pass) :
            return
        self.status = 1
        BasicDetails.__init__(self, name)
        return


def getSequenceShotDetails(xmlPath) :
    xmlTree = pxml.PulseXML()
    stat = xmlTree.setupURLFile(xmlPath, 'QWERTY')
    result = {}
    sequences = __getSequences(xmlTree)
    for seqName in sequences :
        shots = __getShots(xmlTree, seqName)
        if not len(shots) :
            continue
        result[seqName] = shots
    return result

def __getSequences(xmlTree) :
    result = []
    atElems = xmlTree.getChildElements(xmlTree.root_elem, ['assettype'])
    for eachAT in atElems :
        btElems = xmlTree.getChildElements(eachAT, ['basetype'])
        if not len(btElems) == 1 :
            continue
        try :
            btName = btElems[0].text.lower()
        except :
            continue
        if not btName == 'sequences' :
            continue
        nameElems = xmlTree.getChildElements(eachAT, ['name'])
        if not len(nameElems) == 1 :
            continue
        seqName = nameElems[0].text
        if seqName == '' or seqName == None :
            continue
        result.append(seqName)
    return result

def __getShots(xmlTree, seqName) :
    atElems = xmlTree.getNode('assettype', [seqName])
    result = []
    for eachAT in atElems :
        nameElems = xmlTree.getSiblingElements(eachAT, ['name'])
        if not len(nameElems) == 1 :
            continue
        shotName = nameElems[0].text
        if shotName == '' or shotName == None :
            continue
        result.append(shotName)
    return result




def addGlobal(baseFolder, name, type_, code='') :
    if type_.lower() == 'pass' and code == '' :
        return -1

    if not baseFolder.endswith('/') :
        baseFolder += '/'
    xmlPath = baseFolder + 'lnpGlobals.xml'

    xmlTree = pxml.PulseXML()
    stat = xmlTree.setup(xmlPath, 'lnp')
    if stat :
        return -1

    children = xmlTree.getChildElements(xmlTree.root_elem, [type_])
    for eachChild in children :
        nameElems = xmlTree.getChildElements(eachChild, ['name'])
        if not len(nameElems) == 1 :
            continue
        if nameElems[0].text.lower() == name.lower() :
            return -2
        if not type_.lower() == 'pass' :
            continue
        codeElems = xmlTree.getChildElements(eachChild, ['code'])
        if not len(codeElems) == 1 :
            continue
        if codeElems[0].text.lower() == code.lower() :
            return -2

    typeElem = xmlTree.addNodeElem(type_, '', xmlTree.root_elem)
    if not xmlTree.isElement(typeElem) :
        return -3
    nameElem = xmlTree.addNodeElem('name', name, typeElem)
    if type_.lower() == 'pass' :
        codeElem = xmlTree.addNodeElem('code', code, typeElem)

    return xmlTree.writeFile(xmlPath)

def getGlobals(baseFolder, type_) :
    if not baseFolder.endswith('/') :
        baseFolder += '/'
    xmlPath = baseFolder + 'lnpGlobals.xml'

    xmlTree = pxml.PulseXML()
    stat = xmlTree.setup(xmlPath, 'lnp')
    if stat :
        return -1

    result = {}
    children = xmlTree.getChildElements(xmlTree.root_elem, [type_])
    for eachChild in children :
        nameElems = xmlTree.getChildElements(eachChild, ['name'])
        if not len(nameElems) == 1 :
            continue
        result[nameElems[0].text] = ''
        if not type_.lower() == 'pass' :
            continue
        codeElems = xmlTree.getChildElements(eachChild, ['code'])
        if not len(codeElems) == 1 :
            continue
        result[nameElems[0].text] = codeElems[0].text
    return result


def removeGlobal(baseFolder, name, type_) :
    if not baseFolder.endswith('/') :
        baseFolder += '/'
    xmlPath = baseFolder + 'lnpGlobals.xml'

    xmlTree = pxml.PulseXML()
    stat = xmlTree.setup(xmlPath, 'lnp')
    if stat :
        return -1

    children = xmlTree.getChildElements(xmlTree.root_elem, [type_])
    for eachChild in children :
        nameElems = xmlTree.getChildElements(eachChild, ['name'])
        if not len(nameElems) == 1 :
            continue
        if not nameElems[0].text.lower() == name.lower() :
            continue
        stat = xmlTree.root_elem.remove(eachChild)
        return xmlTree.writeFile(xmlPath)
    return -1


if  __name__ == "__main__" :
    pass
##    seq010 = Sequence('SEQ01', 'SAMPLE')
##    shot0010 = seq010.addShot('SHOT001')
##    ptGeom = shot0010.addPassType('Geom')
##    passObj = ptGeom.addPass('Occlusion', 'Occ')
##    passObj.addAOV("mattenode", "qw-er,rt-yy,1")
    ##print ptGeom.passes, passObj.name, passObj.code89
    ##print shot0010.addPassScene('temp', 'Geom')
    ##print shot0010.getPassFiles()
    ##tree = shot0010.getTree('D:/Pankaj')
    ##if not tree == '' :
    ##    shot0010.createTree(tree)
    ##    shot0010.saveXML(tree)