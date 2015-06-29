import os
import sys

modulesPath = ['Z:/REPO/SOURCE/SCRIPTS/PYTHON/COMMON']
for eachMod in modulesPath :
    if eachMod not in sys.path :
        sys.path.append(eachMod)

import vcLib as vcl
reload(vcl)

import csftp as ftp
reload(ftp)

status = 0
try :
    import maya.cmds as mc
except :
    status = -1


class MayaFuncs() :
    def __init__(self, renExt='mb', renFileType='mayaBinary') :
        self.status = status
        if self.status == -1 :
            print "Unable to import maya's cmds module. Unable to continue."
            return
        if renExt.startswith(".") :
            renExt = renExt[1:]
        self.renExt = renExt

        if renFileType == '' :
            if self.renExt.lower() == 'mb' :
                self.renFileType = 'mayaBinary'
            elif self.renExt.lower() == 'ma' :
                self.renFileType = 'mayaAscii'
        else :
            self.renFileType = renFileType
        return

    def getSceneName(self) :
        if self.status == -1 :
            return ''
        try :
            return str(mc.file(q=True, sceneName=True))
        except :
            print "MayaFuncs.getSceneName :- Error finding scene name."
        return ''

    def __getSceneDetails(self, sceneName='') :
        if self.status == -1 :
            return ''
        if sceneName == '' :
            sceneName = self.getSceneName()
        data = {}; sceneName = sceneName.replace("\\", '/')
        pathSplit = sceneName.split('/')
        crntString = pathSplit[0].upper()+'/'+pathSplit[1].upper()+'/'+pathSplit[2].upper()+'/'
        checkString = "D:/ABX_PULSE/" + os.getenv("USERNAME").upper() + '/'
        if not checkString == crntString :
            print "MayaFuncs.__getSceneDetails :- Invalid scene file. Is not from local or does not belong to the domain user."
            return data
        if len(pathSplit) < 9 :
            print "MayaFuncs.__getSceneDetails :- Insufficient details in scene path."
            return data
        data['project_name'] = pathSplit[3]
        data['repo'] = pathSplit[4]
        data['asset_type'] = pathSplit[5]
        data['asset'] = pathSplit[6]
        data['process'] = pathSplit[7]
        data['file_name'] = pathSplit[-1]
        return data

    def __getRenderSceneLocal(self, sceneName) :
        if self.status == -1 :
            return ''
        if sceneName == '' :
            print 'MayaFuncs.__getRenderSceneLocal :- Expected scene name.'
            return ''
        sceneData = self.__getSceneDetails(sceneName)
        if sceneData == {} :
            return ''
        if not sceneData['file_name'].lower().endswith('.ma') and not sceneData['file_name'].lower().endswith('.mb') :
            print "MayaFuncs.__getRenderSceneLocal :- Invalid file type."
            return ''
        renFileName = "D:/ABX_PULSE/" + os.getenv("USERNAME").upper() + '/'
        renFileName += sceneData['project_name'] + '/LIVE/'
        renFileName += sceneData['asset_type'].upper() + '/' + sceneData['asset'].upper()
        renFileName += '/RENDER/' + sceneData['process'] + '/FILES/' + sceneData['file_name'][:-3] + '.' + self.renExt
        return renFileName

    def exportScene(self, sceneName='') :
        if self.status == -1 :
            return ''
        if sceneName == '' :
            sceneName = self.getSceneName()
        renFile = self.__getRenderSceneLocal(sceneName)
        dirName = os.path.dirname(renFile)
        try :
            if not os.path.exists(dirName) :
                os.makedirs(dirName)
        except :
            print "Unable to create intermediate directories for render file on local."
            print dirName + " directory not available."
            return ''
        try :
            return mc.file(renFile, type=self.renFileType, ea=True, op="v=0", )
        except :
            print "MayaFuncs.exportScene :- Error exporting file."
        return ''


class LnPSupportFuncs() :

    def unlockDependencies(self, filename) :
        vl = vcl.vcLib()
        projName=vl.getProjectName(filename)
        vl.ftpInit(projName)
        ftpHandle=vl.ftpHandle
        ServerPath = vl.toServerPath(filename)
        ftpCurrDir = vl.rootFld
##        print ftpCurrDir
        if not ftpCurrDir == '/':
            ServerPath = ftpCurrDir+ServerPath
        fileNameBs = os.path.basename(filename)
        LockPath = os.path.dirname(ServerPath)+'/.LOCK/'+fileNameBs+'/'
        if os.path.exists('W:/'+LockPath.split('/WORK/')[1]):
            listOfFiles=os.listdir('W:/'+LockPath.split('/WORK/')[1])
            for files in listOfFiles:
                if ftp.fileTestHidden(ftpHandle, (LockPath+files)):
                    stat = ftp.deleteFile(ftpHandle, LockPath+files)
            vl.ftpClose()

        try :
            stat = vl.CheckOut(filename)
            if type(stat) == type({}) :
                return 0
        except :
            print filename, "checkout failed"
            return -1
        return -1



if __name__ == "__main__" :
##    mf = MayaFuncs()
##    if mf.status == -1 :
##        print "Module can only be used inside maya."
##    print mf.getSceneName()
##    print mf.getRenderFileLocal(mf.getSceneName())
##    print mf.exportScene()

    lsf = LnPSupportFuncs()
    print lsf.unlockDependencies("D:/ABX_PULSE/SINGHP/DOZ/WORK/SQ370ANIMTEST/SC0050/LIGHTING/TESTLNP/LIT_DOZ_SQ370ANIMTEST_SC0050_TESTLNP_GEOM.mel")
