import sys
import os
import shutil
import filecmp
import popen2
import subprocess as sp
import commandLine

class registryRead():

    def __init__(self,Path,Key):
        #reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop

        self.Path = ''
        self.KeyName = ''
        self.KeyType = ''
        self.DataValue = ''
        self.__Result = ''

        if Path and Key:
            if self.__RRregAvailable():
                self.Path = Path
                self.KeyName = Key
                self.KeyType = ''
                self.DataValue = ''
                if not self.__RRreadReg(self.Path,self.KeyName):
                    print '\nRegistryReadError!', self.__Result[0] if len(self.__Result)>=1 else self
            else:
                print '\nRegistryReadError!','Registry Reader Not Found!'


    def __RRreadReg(self,Path,Key):

        cmd = 'reg query "' + Path + '" /v ' + Key
        cmdLine = commandLine.commandLineParser(cmd)
        self.__Result = cmdLine.executeCommand(1)

        if len(self.__Result)==2:
            if len(self.__Result[1])==3:
                self.KeyName = self.__Result[1][0]
                self.KeyType = self.__Result[1][1]
                self.DataValue = self.__Result[1][2]
                return True

        return False

    def __RRregAvailable(self):

        try:
            regRes = popen2.popen4('reg')[0].readlines()
            return True if regRes[0]=='ERROR: Invalid syntax.\n' and regRes[1]=='Type "REG /?" for usage.\n' else False
        except:
            return False



##
rr = registryRead('HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders','Desktop')
print rr.KeyName
print rr.KeyType
print rr.DataValue


