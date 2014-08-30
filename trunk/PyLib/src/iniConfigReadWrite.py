import ConfigParser
import os
import base64

class INIConfig():

    def __init__(self,fileName='',writeOk=False):

        self.iniReady=False
        self.writeable=False

        if os.path.exists(fileName):
            self.configINIFile = fileName
            self.iniReady=True
            self.writeable=writeOk
        else:
            if writeOk:
                self.configINIFile=fileName
                inifile = open(self.configINIFile,"a")
                inifile.write("")
                inifile.close()
                self.iniReady=True
                self.writeable=writeOk

    def getSectionList(self):
        sectionList = []
        if not self.iniReady: return sectionList
        config = ConfigParser.RawConfigParser()
        config.read(self.configINIFile)
        sectionList = config.sections()
        sectionList.sort()
        return sectionList

    def getOptionList(self,sectionName=''):
        optionList = []
        if not self.iniReady: return optionList
        config = ConfigParser.RawConfigParser()
        config.read(self.configINIFile)
        if config.has_section(sectionName):
            optionList = config.options(sectionName)
        optionList.sort()
        return optionList

    def setSection(self,sectionName):

        if not self.iniReady: return 0
        if not self.writeable: return 0
        if not sectionName: return 0

        config = ConfigParser.RawConfigParser()
        config.read(self.configINIFile)

        if not config.has_section(sectionName):
            config.add_section(sectionName)

        configfile = open(self.configINIFile, "w")
        config.write(configfile)

    def setOption(self,sectionName,Option,Value='',encode=0):

        if not self.iniReady: return 0
        if not self.writeable: return 0
        if not sectionName: return 0
        if not Option: return 0

        config = ConfigParser.RawConfigParser()
        config.read(self.configINIFile)

        if not config.has_section(sectionName):
            config.add_section(sectionName)

        try:
            Val = base64.b64encode(Value) if encode else Value
        except:
            print 'Error! INIB64Encoding...' + str(Value)
            Val = ''

        config.set(sectionName,Option,Val)

        configfile = open(self.configINIFile, "w")
        config.write(configfile)

    def getOption(self,sectionName,Option,decode=0):

        if not self.iniReady: return 0
        if not sectionName: return 0
        if not Option: return 0

        config = ConfigParser.RawConfigParser()
        config.read(self.configINIFile)

        if config.has_section(sectionName):
            if config.has_option(sectionName,Option):
                val = str(config.get(sectionName,Option))
                try:
                    ret = base64.b64decode(val) if decode else val
                except:
                    print 'Error! INIB64Decoding...' + str(val)
                    ret = ''

                return str(ret)

        return 0

    def isOptionAvailable(self, section, Option):

        if not self.iniReady: return 0
        if not section: return 0
        if not Option: return 0

        config = ConfigParser.RawConfigParser()
        config.read(self.configINIFile)

        if config.has_section(section):
            if config.has_option(section,Option):
                return True

        return False
