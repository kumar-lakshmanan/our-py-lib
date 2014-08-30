import maya.cmds as mc
import sys
import os

##xmlLibPath = 'Z:/Repo/Source/Apps'
##if xmlLibPath not in sys.path :
##    sys.path.append(xmlLibPath)
##
xmlLibLoc = 'Z:/REPO/SOURCE/SCRIPTS/PYTHON/PulseXML'
if xmlLibLoc not in sys.path :
    sys.path.append(xmlLibLoc)
import PulseXMLLib

##if 'C:/Python25/Lib/site-packages' not in sys.path :
##    sys.path.append('C:/Python25/Lib/site-packages')

lnpPath = 'Z:/REPO/SOURCE/SCRIPTS/PYTHON/LightNPray/lib'
if lnpPath not in sys.path :
    sys.path.append(lnpPath)
import lnpLib

##commonPath = 'D:/Pankaj/ABXpulse/repo/source/scripts/python/common'
##if commonPath not in sys.path :
##    sys.path.append(commonPath)
import ABXXMLLib

##mdPath = 'D:/Pankaj/ABXpulse/REPO/SOURCE/SCRIPTS/PYTHON/ASSETPUBLISH/lib'
##if not mdPath in sys.path :
##    sys.path.append(mdPath)
import writeSceneXML as wsx




def updateShotAssets() :
    filePath = mc.file(q=True, sn=True)
    fileName = os.path.basename(filePath)
    fileSplit = fileName.split('.')[0].split('_')
    if len(fileSplit) < 6 :
        print 'loadShot.updateShotAssets :- Invalid file name', fileName, '.'
        return -1
    projectCode = fileSplit[1]
    seq = fileSplit[2]
    shot = fileSplit[3]
    sceneName = fileSplit[4]
##    passName = fileSplit[6]

    xmlPath = 'L:/' + seq + '/' + shot + '/SHOTINFO/SHI_'+ projectCode + '_' + seq + '_' + shot + '.xml'
    if not os.path.exists(xmlPath) :
        print 'loadShot.updateShotAssets :- Could not find shot info file.'
        print 'Expected', xmlPath
        return -1

    x = lnpLib.LNPLib(projectCode)
    print x.getSceneFiles(seq, shot)
##    if not fileName in x.getSceneFiles(seq, shot) :
##        return -1

    rprs = x.getPassSceneAssetRprs(sceneName, seq, shot)
    result = []
    for each in rprs :
        result.append(each[:-2])
    return compute(xmlPath, result)

def compute(xmlPath, rprs) :
    rsx = wsx.readSceneXML()
    xml = ABXXMLLib.ABXXML()
    stat = xml.setup(xmlPath, 'Scene')
    data = rsx.getReferenceNodes(xml)
    print 'Refering objects.'
    stat = rsx.referObjects(data, selectedRPRs=rprs, updateOnly=True)
    stat = rsx.getAnimCurveData(xml)
    sceneData = rsx.getSettingsData(xml)
    stat = __addSceneSettings(sceneData)
    return 0

def __addSceneSettings(data) :
    try :
        dar = data['deviceAspectRatio']
        par = data['pixelAspectRatio']
        height = data['resolutionHeight']
        width = data['resolutionWidth']
        startFrame = data['startFrame']
        endFrame = data['endFrame']
        stat = __setFrameRange(startFrame, endFrame)
        stat = __setDarPar(dar, par)
        stat = __setRez(width, height)
    except :
        print 'Add scene settings failed'
        print data
        pass
    return 0

def __setFrameRange(startFrame, endFrame) :
    try :
        startFrame = float(startFrame)
        endFrame = float(endFrame)
    except :
        print 'Invalid value for start and end frame', startFrame, endFrame
        return -1
    try :
        mc.playbackOptions(ast=startFrame, aet=endFrame, min=startFrame, max=endFrame)
    except :
        print 'Unable to set start and end frame to', startFrame, endFrame
    return 0

def __setDarPar(dar, par) :
    try :
        dar = float(dar)
        par = float(par)
    except :
        print 'Invalid value for device and pixel aspect ratio', dar, par
        return -1
    try :
        mc.setAttr("defaultResolution.deviceAspectRatio", dar)
    except :
        print 'Unable to set device aspect ratio', dar
    try :
        mc.setAttr("defaultResolution.pixelAspectRatio", par)
    except :
        print 'Unable to set pixel aspect ratio', par
    return 0

def __setRez(width, height) :
    try :
        width = float(width)
        height = float(height)
    except :
        print 'Invalid value for device and pixel aspect ratio', width, height
        return -1
    try :
        mc.setAttr("defaultResolution.width", width)
    except :
        print 'Unable to set device aspect ratio', width
    try :
        mc.setAttr("defaultResolution.height", height)
    except :
        print 'Unable to set pixel aspect ratio', height

    return 0


def getAOVs() :
    filePath = mc.file(q=True, sn=True)
    fileName = os.path.basename(filePath)
    fileSplit = fileName.split('.')[0].split('_')
    if len(fileSplit) < 6 :
        print 'loadShot.getAOVs :- Invalid file name', fileName
        return []
    projectCode = fileSplit[1]
    seq = fileSplit[2]
    shot = fileSplit[3]
    sceneName = fileSplit[4]
    passType = fileSplit[5]
    passCode = fileSplit[6]

    x = lnpLib.LNPLib(projectCode)
##    pt = x.getScenePassType(sceneName, seq, shot)
    passName = x.getPassNameFromCode(passCode, passType, seq, shot)
    if passName == '' :
        print 'loadShot.getAOVs :- Could not find pass name from code', passCode
        return []
    aovs = x.getAOVs(passName, passType, seq, shot)
    result = []
    for each in aovs :
        result.append('__' + each.lower())
    return result
