#-------------------------------------------------------------------------------
# Name:        PulseLightNPray - Application Entry Point
#
# Author:      lkumaresan
#
# Created:     21/10/2010
# Copyright:   (c) lkumaresan 2010
# Licence:     Personal
#
# Description:
#       LIGHT N PRAY - STANDALONE, SAM ADDON, MAYA ADDON
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

#######Appending Module Search Path########
if __name__ == '__main__':
    currentFolder = os.getcwd()
    parentFolder = os.path.dirname(currentFolder)

####Module Pack folders that will be added to sys search path####
    modulePathList = [
                        currentFolder,
                        parentFolder,
                        parentFolder + '/UI_DB_lib',
                        parentFolder + '/PulseXML',
                        parentFolder + '/Common',
                        'Z:/REPO/PulseServer/Library/Common'
                     ]

    for modulePath in modulePathList:
        modulePath = os.path.normpath(modulePath)
        if modulePath not in sys.path and os.path.exists(modulePath):
            sys.path.append(modulePath)

from PyQt4 import QtCore, QtGui

#Global Lib
import time
import base64
from ui.winLightNPray import lnp_data
from lib import configs
from lib import shared
import version_client

class Application():

    def __init__(self, arguments):
        UPDATECONFIG=1
        self.App = QtGui.QApplication(arguments)
        if UPDATECONFIG:
            self.Config = configs.AppConfigs('data/setting.ini',0)
            self.Config.UpdateAllConfigValues()
        else:
            self.Config = configs.AppConfigs('data/setting.ini')
        self.Common = shared.AppShared()
        self.MainUIHandle = lnp_data.LightNPrayData(self)
        self.svc = version_client.VersionClient(self.MainUIHandle.ui, self.Config.AppInfo.AppName, self.Config.AppInfo.ReleaseLog, self.Config.AppInfo.PyServer)

    def Start(self):
        if self.svc: self.svc.doUpdateCheck()
        self.MainUIHandle.initalize()
        self.MainUIHandle.showUI()
        return self.App.exec_()

if __name__ == '__main__':
    main = Application(sys.argv)
    exitCode = main.Start()
    del(main)
    sys.exit(exitCode)