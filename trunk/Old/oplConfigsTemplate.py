#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      AIAA
#
# Created:     14-12-2011
# Copyright:   (c) AIAA 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import configobj
import oplPyUtilities

class settings():
    def __init__(self):
        self.appName="Render Assistant"
        self.iconPath="F:/Kumaresan/Dev/Python/lra/res/icons"
        self.load="dd"
        self.bos=["f","SDf","fs"]

class Configs(settings):
    def __init__(self, file="settings.ini", autoLoad=True):
        settings.__init__(self)
        self._muti = oplPyUtilities.oplPyUtilities()
        self._cfg = configobj.ConfigObj(file)
        if autoLoad: self.loadSettings()

    def loadSettings(self):
        attribs = self._muti.getAttributes(self)
        for eachAttrib in attribs:
            if (self._cfg.dict().has_key(eachAttrib[0])):
                setattr(self,eachAttrib[0],self._cfg[eachAttrib[0]])
            else:
                self._cfg[eachAttrib[0]]=getattr(self,eachAttrib[0])
                self._cfg.write()

    def saveSettings(self):
        attribs = self._muti.getAttributes(self)
        for eachAttrib in attribs:
            self._cfg[eachAttrib[0]]=getattr(self,eachAttrib[0])
        self._cfg.write()

if '__main__' == __name__:
    cfg = Configs()
    #cfg.appName="newName"
    #cfg.saveSettings()
    print cfg.bos

