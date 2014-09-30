'''
from kmxGeneral import kmxINIConfigReadWrite
from kmxGeneral import kmxTools
from kmxPyQt import kmxQtCommonTools


        self.cfg = kmxINIConfigReadWrite.INIConfig("config.ini")
        self.iconPath = self.cfg.getOption('UserInterface', 'IconPath')
        self.icons = core.icons.iconSetup()
        self.infoStyle = kmxTools.infoStyle()
        self.infoStyle.errorLevel = 2
        self.infoStyle.infoLevel = 0

        self.tls = kmxTools.Tools(self.infoStyle)
        self.qtTools = kmxQtCommonTools.CommonTools(self.win, self.iconPath)

'''
import base64
import configparser
import os


class INIConfig():

    def __init__(self, fileName='', writeOk=True):
        self.iniReady = False
        self.writeable = False

        if os.path.exists(fileName):
            self.configINIFile = fileName
            self.iniReady = True
            self.writeable = writeOk
        else:
            if writeOk:
                self.configINIFile = fileName
                inifile = open(self.configINIFile, "a")
                inifile.write("")
                inifile.close()
                self.iniReady = True
                self.writeable = writeOk

    def getSectionList(self):
        sectionList = []
        if not self.iniReady: return sectionList
        config = configparser.ConfigParser()
        config.read(self.configINIFile)
        sectionList = config.sections()
        sectionList.sort()
        return sectionList

    def getOptionList(self, sectionName=''):
        optionList = []
        if not self.iniReady: return optionList
        config = configparser.ConfigParser()
        config.read(self.configINIFile)
        if config.has_section(sectionName):
            optionList = config.options(sectionName)
        optionList.sort()
        return optionList

    def setSection(self, sectionName):
        if not self.iniReady: return 0
        if not self.writeable: return 0
        if not sectionName: return 0

        config = configparser.ConfigParser()
        config.read(self.configINIFile)

        if not config.has_section(sectionName):
            config.add_section(sectionName)

        configfile = open(self.configINIFile, "w")
        config.write(configfile)

    def setOption(self, sectionName, Option, Value='', encode=0):
        if not self.iniReady: return 0
        if not self.writeable: return 0
        if not sectionName: return 0

        config = configparser.ConfigParser()
        config.read(self.configINIFile)

        if not config.has_section(sectionName):
            config.add_section(sectionName)

        try:
            Val = base64.b64encode(Value) if encode else Value
        except:
            print ('Error! INIB64Encoding...' + str(Value))
            Val = ''

        config.set(sectionName, Option, Val)

        configfile = open(self.configINIFile, "w")
        config.write(configfile)

    def getOption(self, sectionName, Option, defaultValue='', decode=0):
        if not self.iniReady: return 0
        if not sectionName: return 0
        if not Option: return 0

        config = configparser.ConfigParser()
        config.read(self.configINIFile)

        if config.has_section(sectionName):
            if config.has_option(sectionName, Option):
                val = str(config.get(sectionName, Option))
                try:
                    ret = base64.b64decode(val) if decode else val
                except:
                    print ('Error! INIB64Decoding...' + str(val))
                    ret = ''
                return str(ret)
            else:
                self.update(sectionName, Option, decode, defaultValue)
        else:
            self.update(sectionName, Option, decode, defaultValue)
        return 0

    def update(self, sectionName, Option, encode, defaultValue):
        if(self.iniReady and self.writeable):
            if(self.isSectionAvailable(sectionName)):
                self.setOption(sectionName, Option, defaultValue, encode)
            else:
                self.setSection(sectionName)
                self.setOption(sectionName, Option, defaultValue, encode)

    def isSectionAvailable(self, section):
        return section in self.getSectionList()


    def isOptionAvailable(self, sectionName, Option):
        if not self.iniReady: return 0
        if not sectionName: return 0
        if not Option: return 0

        config = configparser.ConfigParser()
        config.read(self.configINIFile)

        if config.has_section(sectionName):
            if config.has_option(sectionName, Option):
                return True
        return False
