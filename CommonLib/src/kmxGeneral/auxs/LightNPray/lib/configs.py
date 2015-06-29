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

#Custom Lib
import iniConfigReadWrite as ini

#Special
from LightNPray.lib.config_infos import Icons
from LightNPray.lib.config_infos import AppInfos
from LightNPray.lib.config_infos import LasedUsedInfos
from LightNPray.lib.config_infos import DisplayStrings

class AppConfigs():

    def __init__(self, settingsFile='data/setting.ini', loadConfigFile=1):

        self.Icon = Icons()
        self.AppInfo = AppInfos()
        self.LastUsed = LasedUsedInfos()
        self.Strings = DisplayStrings()

        if settingsFile:
            self.__config = ConfigReadWrite(self.__configObjs(), settingsFile) if loadConfigFile else None
            if self.__config: self.__config.loadSettings()
        else:
            self.__config = None
        self.__settingsFile = settingsFile

    def SettingsFile(self):
        return self.__settingsFile

    def __configObjs(self):
        cObjs = []
        for attr in self.__dict__:
            if not attr.find('_')==0:
                cObjs.append(getattr(self,attr))
        return cObjs

    def UpdateConfigValues(self, obj):
        if self.__config:
            self.__config._checkAndUpdateNewAttribute(obj, 1)

    def UpdateAllConfigValues(self):
        if not self.__config:
            self.__config = ConfigReadWrite(self.__configObjs(), self.__settingsFile)

        for eachClass in self.__configObjs():
            self.__config._checkAndUpdateNewAttribute(eachClass, 1)
        self.__config.loadSettings()


class ConfigReadWrite():

    def __init__(self, settingsClasses=[], settingsFile='data/setting.ini'):

        self.ready=False

        if os.path.exists(settingsFile):
            self.appconfig = settingsFile
        else:
            path = os.path.dirname(settingsFile)
            if not os.path.exists(path):
                os.makedirs(path)
            file(settingsFile,'w').close()
            self.appconfig = settingsFile

        self.settingsClasses = settingsClasses
        self.iniHandle = ini.INIConfig(settingsFile,True)

        for eachClasses in self.settingsClasses:
            self._checkAndUpdateNewAttribute(eachClasses)

        self.ready=True


    def loadSettings(self):

        if self.ready:
            for eachClasses in self.settingsClasses:
                cls = eachClasses
                clsName = str(cls.__class__.__name__)
                clsAttr = cls.__dict__
                for eachAttr in clsAttr:
                    value = self.iniHandle.getOption(clsName,eachAttr)
                    value = self._coreEncodeDecode(eachAttr,value,0)
                    if value!=0:
                        value = int(value) if value.isdigit() else str(value)
                        actualAttr = self._getActualKey(eachAttr, clsAttr)
                        if hasattr(cls,actualAttr):
                            setattr(cls,actualAttr,value)

    def _checkAndUpdateNewAttribute(self, ClassName, updateValues = 0):

        clsName = str(ClassName.__class__.__name__)
        clsAttr = ClassName.__dict__
        encAttr = self._encodeDecode(clsAttr)
        encAttr = self._dictCaseConvert(encAttr)

        settingList = [each.upper() for each in self.iniHandle.getOptionList(clsName)]

        for eachClsAttr in encAttr:
            saved = False
            if not eachClsAttr in settingList:
                actualAttr = self._getActualKey(eachClsAttr, clsAttr).upper()
                if type(encAttr[actualAttr]) == type('') or type(encAttr[actualAttr]) == type(0):
                    self.iniHandle.setOption(clsName,actualAttr,encAttr[actualAttr])
                    saved = True
                elif type(encAttr[actualAttr]) == type(bool):
                    self.iniHandle.setOption(clsName,actualAttr,1 if encAttr[actualAttr] else 0)
                    saved = True

            if updateValues:
                if eachClsAttr in settingList and not saved:
                    oldVal = str(self.iniHandle.getOption(clsName,eachClsAttr)).upper()
                    curVal = str(encAttr[eachClsAttr]).upper()
                    actualAttr = self._getActualKey(eachClsAttr, clsAttr)
                    if oldVal != curVal:
                        self.iniHandle.setOption(clsName,actualAttr,encAttr[eachClsAttr])

    def _encodeDecode(self, attrs, encode = 1):

        dictx = {}
        for att in attrs:
            actVal = str(attrs[att])
            dictx[att] = self._coreEncodeDecode(att,actVal,1)

        return dictx


    def _coreEncodeDecode(self, attr, value, encode=1):

        if attr.lower().find('enc_') == 0:
            try:
                val = base64.b64encode(value) if encode else base64.b64decode(value)
            except:
                val = value
        else:
            val = value

        return val


    def _dictCaseConvert(self, dicts):
        newDicts = {}
        for eachKey in dicts:
            newDicts[eachKey.upper()] = dicts[eachKey]
        return newDicts

    def _getActualKey(self, key, dicts):
        for eachKey in dicts:
            if eachKey.upper() == key.upper():
                return eachKey