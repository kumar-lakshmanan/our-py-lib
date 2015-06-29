import os
import maya.cmds as mc


class MayaFuncs() :
    def __init__(self, renExt='mb', renFileType='mayaBinary') :
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
        try :
            return str(mc.file(q=True, sceneName=True))
        except :
            print "MayaFuncs.getSceneName :- Error finding scene name."
        return ''

    def __getSceneDetails(self, sceneName='') :
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
        if sceneName == '' :
            sceneName = self.getSceneName()
        try :
            return mc.file(self.__getRenderSceneLocal(sceneName), type=self.renFileType, ea=True, op="v=0", )
        except :
            print "MayaFuncs.exportScene :- Error exporting file."
        return ''



if __name__ == "__main__" :
    mf = MayaFuncs()
##    print mf.getSceneName()
##    print mf.getRenderFileLocal(mf.getSceneName())
    print mf.exportScene()
