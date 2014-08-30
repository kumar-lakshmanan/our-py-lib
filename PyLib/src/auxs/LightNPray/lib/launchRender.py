import os

active = 1
try :
    import maya.mel as mm
except :
    active = 0


def launchRocket(filePath, renData) :
    if not active :
        return -1

    fileName = os.path.basename(filePath)
    fileSplit = fileName.split('_')
    projCode = fileSplit[1]
    passType = fileSplit[5]
    musterPath = 'C:/Program Files/Virtual Vertex/Muster 6'
    templateID = '108,105'
    packetSize = '10'
    priority = '0'
    smedgeRenpool = "WS"
    mustServerName = "muster01"
    mustRenpool = "WS"
    mustUsername = "savelaunch"
    mustPassword = "r3nd3rN0W"
    mayaWrapperPath = ''
    saveOrLaunch = '1'
    ribName = ""
    renderFarm = 'Muster'

    if 'render_file' not in renData.keys() :
        renFile = renData['render_file']

    if 'template_id' in renData.keys() :
        templateID = renData['template_id']

    if 'camera' not in renData.keys() :
        print 'Camera information missing. Expected key "camera"'
        return -1
    cameras = renData['camera']
    cameras = __getCameraString(cameras)

    if 'is_stereo' not in renData.keys() :
        print 'Is stereo information missing. Expected key "is_stereo"'
        return -1
    isStereo = renData['is_stereo']

    if 'render_type' not in renData.keys() :
        print 'Render_as information missing. Expected key "render_type"'
        return -1
    renderType = renData['render_type']

    if 'renderer' not in renData.keys() :
        print 'Renderer information missing. Expected key "renderer"'
        return -1
    renderer = renData['renderer']

    if 'char_bg' not in renData.keys() :
        print 'CHAR or BG information missing. Expected key "char_bg"'
        return -1
    charBg = renData['char_bg']

    if 'start_frame' not in renData.keys() :
        print 'Start frame information missing. Expected key "start_frame"'
        return -1
    stFrame = renData['start_frame']

    if 'end_frame' not in renData.keys() :
        print 'End frame information missing. Expected key "end_frame"'
        return -1
    endFrame = renData['end_frame']

    if 'use_frame_range' not in renData.keys() :
        print 'Use frame range information missing. Expected key "use_frame_range"'
        return -1
    useFrameRange = renData['use_frame_range']

    if 'frame_range' not in renData.keys() :
        print 'Frame range information missing. Expected key "frame_range"'
        return -1
    frameRange = renData['frame_range']

    if 'render_engine' not in renData.keys() :
        print 'Render engine information missing. Expected key "render_engine"'
        return -1
    renderEngine = renData['render_engine']

    if 'maya_version' not in renData.keys() :
        print 'Maya version information missing. Expected key "maya_version"'
        return -1
    mayaVersion = renData['maya_version']

    if 'comment' not in renData.keys() :
        print 'Comment information missing. Expected key "comment"'
        return -1
    comment = renData['comment']

    try :
        mm.eval("source \"Z:/REPO/SOURCE/SCRIPTS/PYTHON/LightNPray/lib/MayaAddon/lnp_launchRender.mel\"")
##        sourceString = "source \"" + filePath[:-3] + '.mel\";'
##        mm.eval(sourceString)
    except :
##        print 'Unable to source file', filePath[:-3] + '.mel'
        pass

    try :
##        mm.eval("launchNPray(\""+filePath+"\", {\"persp\"}, \"ScnImg\", \"\", \"Muster\", \"C:/Program Files/Virtual Vertex/Muster 6\",\""+projCode+"\",\""+projCode+"\",\"CHAR\",\""+passType+"\",5, 5, 0, \"\", \"MayaMan\", \"Air\", \"108,105\", \"1\", \"0\",\"test\",\"WS\",\"muster01\",\"WS\",\"savelaunch\",\"r3nd3rN0W\",\"\",\"maya2008\",1)")
        launchString = "launchNPray(\""+filePath+"\", "+cameras+','+"\""+ renderType +"\", \""+ribName+"\", \""+ renderFarm +"\", \""+ \
                       musterPath + "\", \""+projCode+"\", \""+projCode+"\", \"" + charBg + "\", \""+passType+"\" ,\"" + stFrame + "\", \""+ \
                       endFrame + "\", \"" + useFrameRange + "\", \"" + frameRange +"\", \""+ renderer +"\", \""+ renderEngine +"\", \"" + \
                       templateID + "\", \"" + packetSize + "\", \"" + priority + "\", \"" + comment + "\",\"" + smedgeRenpool + "\", \"" + \
                       mustServerName + "\", \"" + mustRenpool + "\", \"" + mustUsername + "\", \"" + mustPassword + "\", \"" + \
                       mayaWrapperPath + "\", \"" + mayaVersion + "\", \"" + saveOrLaunch + "\", \"" + isStereo + "\", \"" + renFile + "\")"
##        print launchString
        mm.eval(launchString)
    except :
        print 'Unable to launch n ready to pray.'
        return -2
    return 0


##launchNPray("D:/ABX_PULSE/AKULMI/ZZP/WORK/SEQ002/SHOT0008/LIGHTING/LIT_ZZP_SEQ002_SHOT0008_TWSN_OCC.ma", {"persp"}, "ScnImg", "TWSN_OCC", "Muster",
##            "c:/Program Files/Virtual Vertex/Muster 6", "ZZP", "ZZP", "CHAR", "GEOM", 5, 5, 0, "", "MayaMan", "Air", "108,105", "1", "0",
##            "test","WS","muster01","WS","savelaunch","r3nd3rN0W","","maya2008",1)


def updatePassFile() :
    try :
        mm.eval("source \"Z:/REPO/SOURCE/SCRIPTS/PYTHON/LightNPray/lib/loadShot.mel\"")
    except :
        print 'Unable to udpate pass scene file'
        return -2
    return 0

def __getCameraString(cameras) :
    retStr = '{"'
    for eachCam in cameras :
        retStr += eachCam + '","'
    retStr = retStr[:-3] + '"}'
    return retStr

