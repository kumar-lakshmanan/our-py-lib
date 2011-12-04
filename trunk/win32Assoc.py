import os
import shutil
import filecmp
import popen2
import subprocess as sp
import sys

from win32exec import win32Execute

class win32Association():

    def __init__(self):
        cmdParse = commandLineParser('assoc', Splitter='=')
        self.EXT_APPNAME = cmdParse.executeCommand()

        cmdParse = commandLineParser('ftype', Splitter='=')
        self.APPNAME_PATH = cmdParse.executeCommand()

    def getAssociation(self, ext):

        APPNAME = ''
        for each in self.EXT_APPNAME:
            if str(each[0]).upper() == str(ext).upper():
                APPNAME = str(each[1])

        for each in self.APPNAME_PATH:
            if str(each[0]).upper() == str(APPNAME).upper():
                return str(each[1])

        return ''

    def getSubprocessCommand(self, association, filename):

        if association and filename:
            x = association
            x = x.replace('%1',filename)
            return 'cmd /c "'+x+'"'
        else:
            return ''

    def openByDefault(self, fileName):
        print 'Detect and Launching default application!'
        if os.path.exists(fileName):
            ext = str(os.path.splitext(fileName)[1])
            asso = self.getAssociation(ext)
            command = self.getSubprocessCommand(asso, fileName)
            if command:
                sp.Popen(command)
                return 1
            else:
                return 0
        else:
            print fileName,' Not found!'
        return 0

if __name__ == '__main__':
    f = win32Association()
    f.openByDefault('')