#-------------------------------------------------------------------------------
# Name:        Config class content Read/Write
#
# Author:      lkumaresan
#
# Created:     14/10/2010
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
import random
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


class DisplayStrings():

    def __init__(self):

        self.lnpLibInitSuccess = 'Initialized LNP Successfullyz!'
        self.lnpLibAddPassTypeSuccess = 'Added Passtype Successfully!'
        self.lnpLibRemovePassTypeSuccess = 'Removed Passtype Successfully!'
        self.lnpLibAddPassSuccess = 'Added Pass Successfully!'
        self.lnpLibRemovePassSuccess = 'Removed Pass Successfully!'
        self.lnpLibAddAOVSuccess = 'Added AOV Successfully!'
        self.lnpLibRemoveAOVSuccess = 'Removed AOV Successfully!'
        self.lnpLibAddPassSceneSuccess = 'Added PassScene Successfully!'
        self.lnpLibRemovePassSceneSuccess = 'Removed PassScene Successfully!'
        self.lnpLibAddPassSceneAssetSuccess = 'Added PassScene Assets Successfully!'
        self.lnpLibRemovePassSceneAssetSuccess = 'Removed PassScene Assets Successfully!'
        self.lnpLibBuildStartConfirm= 'Are you sure to build scene files?'
        self.lnpLibBuildFilesSuccessfull= 'Files created successfully! Refresh and Check SAM for new files!'
        self.lnpLibBuildFilesFail = 'File build failed! Check error console for more information!'
        self.lnpLibSaveSuccess = 'Render pass info xml updated successfully!'
        self.lnpLibInvalidInputs = 'Action Cancelled/Missed few input(s) for this action, Check the inputs and try again...'
        self.lnpLibInvalidAction = 'Invalid action. Check the selection(s) and try again!'
        self.lnpLibInvalidDragDrop = 'Invalid action: Drag&Drop Asset RN Node to PassSceneName and Make sure its not already added!'
        self.lnpLibCheckConsole = 'Check error console for more information!'
        self.lnpLibInitFailed = 'Problem Initializing LNP Lib. Check error console for more information!'
        self.lnpLibNotInitalized = 'LNP not inialized. Check error console for more information!'
        self.lnpLibGetSeqFail = 'Problem retriving seqence info. Check error console for more information!'
        self.lnpLibGetShotFail = 'Problem retriving shot info. Check error console for more information!'
        self.lnpLibGetPassTypeFail = 'Problem retriving pass type info. Check error console for more information!'
        self.lnpLibGetPassFail = 'Problem retriving pass info. Check error console for more information!'
        self.lnpLibGetAOVFail = 'Problem retriving aov info. Check error console for more information!'
        self.lnpLibGetPassSceneAssetFail = 'Problem retriving pass scene assest info. Check error console for more information!'
        self.lnpLibGetRenderFilesFail = 'Problem retriving render files info. Check error console for more information!'
        self.lnpLibGetWorkFilesFail = 'Problem retriving work files info. Check error console for more information!'
        self.lnpLibGetPassSceneFail = 'Problem retriving pass scene info. Check error console for more information!'
        self.lnpLibGetAssetsFail = 'Problem retriving pass scene info. Check error console for more information!'
        self.lnpLibGetGlobalsFail = 'Problem retriving global available list. Check error console for more information!'
        self.lnpLibAddPassTypeFail = 'Problem adding passtype. Check error console for more information!'
        self.lnpLibRemovePassTypeFail = 'Problem removing passtype. Check error console for more information!'
        self.lnpLibAddPassFail = 'Problem adding pass. Check error console for more information!'
        self.lnpLibRemovePassFail = 'Problem removing pass. Check error console for more information!'
        self.lnpLibAddAOVFail = 'Problem adding AOV. Check error console for more information!'
        self.lnpLibRemoveAOVFail = 'Problem removing AOV. Check error console for more information!'
        self.lnpLibAddPassSceneFail = 'Problem adding pass scene. Check error console for more information!'
        self.lnpLibRemovePassSceneFail = 'Problem removing pass scene. Check error console for more information!'
        self.lnpLibAddPassSceneAssetFail = 'Problem adding pass scene asset. Check error console for more information!'
        self.lnpLibRemovePassSceneAssetFail = 'Problem removing pass scene asset. Check error console for more information!'
        self.lnpLibSaveFail = 'Unable to save render pass info xml. Check error console for more information!'
        self.lnpLibRemindSave = 'You have made some changes, Please! Save before closing application.'
        self.lnpLibConfirmSave = 'Are sure you want to save the changes?'
        self.lnpLibNothingToSave = 'You have made no changes to save!'
        self.lnpLibDeleteConfirm = 'Are you sure you want delete following item?'
        self.lnpLoadingShots = 'Loading shot infos...'


class Icons():

    def __init__(self):

        self.AppLogo = 'PulseLogoWithText.png'
        self.Home = 'home.png'
        self.GenericPlus = 'highlighter--plus.png'
        self.GenericMinus = 'highlighter--minus.png'
        self.GenericLoad = 'folder-horizontal-open.png'
        self.GenericSave = 'save.png'
        self.ImageSet = 'camera-black.png'
        self.GenericCancel = 'cross-small.png'
        self.Process = 'application-monitor.png'
        self.AssetType = 'grp.png'
        self.Attributes = 'application-tree.png'
        self.NewProject = 'application-image.png'
        self.Sync = 'databases-relation.png'
        self.Online = 'universal.png'
        self.Inbox = 'mails.png'
        self.InstantMessage = 'smiley.png'
        self.WorldClock = 'alarm-clock.png'
        self.Folder = 'folder-horizontal-open.png'
        self.File = 'notebook.png'
        self.Project = 'point.png'
        self.Server = 'servers-network.png'
        self.ProjectStructure = 'node.png'
        self.AssetDefinition = 'notebook--plus.png'
        self.Flag = 'tick-button.png'
        self.GlobalProjectStructure = 'ruler--plus.png'
        self.DefaultProject = 'newProject.png'
        self.System = 'node.png'
        self.User = 'users.png'
        self.Software = 'node.png'
        self.TeamStructure = 'node.png'
        self.UserDefinition = 'user.png'
        self.BookMark = 'bookmark.png'
        self.Status = 'stamp.png'
        self.Revert = 'arrow-repeat.png'
        self.Sequences = 'color-adjustment-red.png'
        self.Search = 'magnifier.png'
        self.Up = 'arrow-090.png'
        self.Down = 'arrow-270.png'

        self.PassDefinition = 'layers-stack.png'
        self.BuildFiles = 'maps-stack.png'
        self.RenderFiles = 'pictures-stack.png'

        self.Logs =  'application-text.png'
        self.Quit =  'slash.png'
        self.Render_Settings = 'server--pencil.png'
        self.Seq_N_Shots = 'ui-paginator.png'


class AppInfos():

    def __init__(self):

        self.ShortName = 'LNP'
        self.FullName = 'Pulse - Light N Pray'
        self.AppName = 'LNP'
        self.ReleaseLog = 'ReleaseLog.xml'
        self.PyServer = 'Z:/REPO/PulseServer/PyServer/PyServer.exe'

        self.DataFolder = 'data'
        self.LayoutFile = 'data/LastUsedLayout.lyt'
        self.IconPath = 'Z:/REPO/CONFIG/BASEICONS/splIcons'
        self.TemplatePath = 'Z:/repo/source/scripts/python/LightNPray/templates'

        self.WebBasePath = 'http://192.168.20.93:85/pulse/beat/projects'
        self.CommonFileServerUid = 'cgapps'
        self.enc_CommonFileServerPass = 'thepulse'


class LasedUsedInfos():

    def __init__(self):

        self.Theme = 'CleanLooks'
        self.Layout= 'data/Custom.lyt'
        self.LastPage= 'PASSDEFINITION'