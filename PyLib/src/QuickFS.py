from PyQt4 import QtCore, QtGui
import os
import sys
import datetime
import commandLine
import popen2

class UNCAccess():

    def __init__(self):
        self.cmd = commandLine

    def allPath(self):
        command = 'net use'
        cmd = self.cmd.commandLineParser(command)
        res = cmd.executeCommand()
        return res

    def mountPath(self, unc, mountDrive, userId='', password=''):
        if os.path.exists(mountDrive): return [['Drive in use: ' + mountDrive]]
        unc = os.path.normpath(unc)
        command='net use'

        if userId=='':
            command = 'net use ' + str(mountDrive) + ' "' + str(unc) + '"'

        if userId!='' and password=='':
            command = 'net use ' + str(mountDrive) + ' "' + str(unc) + '" ' + '/USER:' + str(userId)

        if userId!='' and password!='':
            command = 'net use ' + str(mountDrive) + ' "' + str(unc) + '" ' + str(password) + ' /USER:' + str(userId)

        cmd = self.cmd.commandLineParser(command)
        res = cmd.executeCommand()

        return res

    def accessPath(self, unc, userId='', password=''):

        if self.isPathAvailable(unc): return [['UNC Available: ' + unc]]

        command='net use'
        unc = os.path.normpath(unc)
        if userId=='':
            command = 'net use  "' + str(unc) + '"'

        if userId!='' and password=='':
            command = 'net use  "' + str(unc) + '" ' + '/USER:' + str(userId)

        if userId!='' and password!='':
            command = 'net use  "' + str(unc) + '" ' + str(password) + ' /USER:' + str(userId)

        cmd = self.cmd.commandLineParser(command)
        res = cmd.executeCommand()

        return res


    def removePath(self, unc):
        unc = os.path.normpath(unc)
        command = 'net use ' + unc + ' /delete /Y'
        cmd = self.cmd.commandLineParser(command)
        res = cmd.executeCommand()
        return res

    def dismountDrive(self, mountDrive):
        command = 'net use ' + mountDrive + ' /delete /Y'
        cmd = self.cmd.commandLineParser(command)
        res = cmd.executeCommand()
        return res

    def isPathAvailable(self,  unc='//tech/share'):
        unc = os.path.normpath(unc)
        command = 'net use'
        cmd = self.cmd.commandLineParser(command)
        res = cmd.executeCommand()

        for line in res:
            uncFound = 0
            connected = 1
            for word in line:
                if word.__contains__(unc): uncFound = 1
                if word.__contains__('Disconnected'): connected = 0
            if uncFound and connected:
                return True
        return False


    def isMounted(self, mountDrive='Z:', unc='//tech/share'):
        unc = os.path.normpath(unc)
        command = 'net use'
        cmd = self.cmd.commandLineParser(command)
        res = cmd.executeCommand()

        for line in res:
            mountFound = 0
            uncFound = 0
            for word in line:
                if word == mountDrive: mountFound = 1
                if word == unc: uncFound = 1
            if mountFound and uncFound:
                return True
        return False


    def isRunningFromUNC(self):
        (r,w) = popen2.popen2('net use')

        result = r.readlines()
        r.close()
        w.close()

        return False if len(result)>0 else True

    def isInResult(self, result, lookFor='The password or user name is invalid'):
        for line in result:
            for word in line:
                if word.__contains__(lookFor):
                    return True
        return False


class fileValidate():

    def __init__(self, fileName):
        self.fs = fileInfo(fileName)

    def isValid(self, fileSys):
        fileSys = fileInfo(fileName)

        #No Space Allowed:
        if fileSys.FileNameAlone.find(' '):
            pass

        #No More then one dot. Only at the beginning
        if fileSys.FileNameAlone.find('.'):
            pass







class fileInfo():

    def __init__(self,path=''):
        path = os.path.normpath(path)
        if os.path.exists(str(path)) and path!='':
            FS = QtCore.QFileInfo(path)
            self.Exists = FS.exists()
            self.IsFile = FS.isFile()
            self.IsDir = FS.isDir()
            self.IsHidden = FS.isHidden()
            self.Size = FS.size()
            self.LastModifiedDate = FS.lastModified()
            self.FormattedLastModifiedDate = str(formatOut().dateFormat(FS.lastModified()))
            self.FormattedSize = str(formatOut().fileSizeFormatting(FS.size()))
            self.FilePathAlone = str(FS.path().toAscii())
            self.FileNameAlone = str(os.path.basename(path).replace('.'+FS.suffix(),''))
            self.FileExtAlone = str(FS.suffix().toAscii())
            self.FileName = str(os.path.basename(path))
            self.File = str(FS.filePath().toAscii())
            self.FS = FS
            self.PathType = 'LINUX'
        else:
            self.Exists = 0
            self.IsFile = 0
            self.IsDir = 0
            self.Size = 0
            self.LastModifiedDate = 0
            self.FormattedLastModifiedDate = 0
            self.FormattedSize = 0
            self.FilePathAlone = 0
            self.FileNameAlone = 0
            self.FileExtAlone = 0
            self.FileName =  0
            self.File = 0
            self.FS = None
            self.PathType = 'LINUX'


class fileInfoWin():

    def __init__(self,path=None):

        FS = QtCore.QFileInfo(path)

        self.Exists = FS.exists()
        self.IsFile = FS.isFile()
        self.IsDir = FS.isDir()
        self.IsHidden = FS.isHidden()
        self.Size = FS.size()
        self.LastModifiedDate = FS.lastModified()
        self.FormattedLastModifiedDate = str(formatOut().dateFormat(FS.lastModified()))
        self.FormattedSize = str(formatOut().fileSizeFormatting(FS.size()))
        self.FilePathAlone = str(FS.path()).replace('/','\\')
        self.FileNameAlone = str(os.path.basename(path).replace('.'+FS.suffix(),''))
        self.FileExtAlone = str(FS.suffix())
        self.FileName =  str(os.path.basename(path))
        self.File = str(FS.filePath()).replace('/','\\')
        self.FS = FS
        self.PathType = 'WINDOWS'



class fileSearch():

    def __init__(self):
        '''
        Pass a list of SearchPaths and use the functions to search the files/folders with Ext Rules for files.
        '''

        self.SearchPaths = []
        self.ruleExtFilters = []
        self.ruleNameFilters = []
        self.callBackFn = None
        #self.ruleDefined = ['NOHIDDEN']

    def doSearch(self):
        if (len(self.SearchPaths)>0):
            return self._coreGetAllFilesUnderFolders(self.SearchPaths)
        else:
            print "No search path given"
        return {}

    def _coreGetAllFilesUnderFolders(self,foldersList) :

        returnDict = {}; newfoldersList = []
        for folderPath in foldersList :
            if not os.path.exists(folderPath) :
                continue
            try :
                filesList = os.listdir(folderPath)
            except :
                return {}

            for fileName in filesList :
                #Filters
                fullFile = os.path.join(folderPath,fileName)
                #print fullFile
                cfile = fileInfo(fullFile)
                if cfile.IsFile:
                    #-All filter should be deactivated (false) to proceed adding that file to list.
                    #-Filters are off - If no rule is given
                    #-If Filter is activated by giving some rules (len>1). Search loop should
                    # set it back to false. else that filter will remain activated for filtering.

                    #ConstantFilters
                    ConstantFilter = (
                                        cfile.FileName.startswith('.') or
                                        cfile.FileName.upper() == 'THUMBS.DB'
                                     )

                    if ConstantFilter: continue

                    #ExtFilter
                    ExtFilter = len(self.ruleExtFilters)>0
                    for eachExtFilter in self.ruleExtFilters:
                        if cfile.FileExtAlone.upper() == eachExtFilter.upper():
                            ExtFilter = False

                    if ExtFilter: continue

                    #NameRule
                    NameFilter = len(self.ruleNameFilters)>0
                    for eachNameFilter in self.ruleNameFilters:
                        if cfile.FileNameAlone.upper() == eachNameFilter.upper():
                            NameFilter = False

                    if NameFilter: continue

##                    #DefinedRule
##                    DefinedFilter = len(self.ruleDefined)>0
##                    if 'NOHIDDEN' in self.ruleDefined:
##                        if cfile.IsHidden:
##                            DefinedFilter = False
##
##                    if DefinedFilter: continue

                if self.callBackFn:
                    self.callBackFn(fullFile)

                if os.path.isfile(fullFile) :
                    returnDict[fileName] = fullFile
                else :
                    newfoldersList.append(fullFile)

        if not newfoldersList :
            return returnDict

        newDict = self._coreGetAllFilesUnderFolders(newfoldersList)
        for newFileName in newDict.keys() :
            newFilePath = newDict[newFileName]
            if newFileName in returnDict.keys() :
                found = 0
                while not found :
                    newFileName += "_dup"
                    if newFileName not in returnDict.keys() :
                        found = 1
            returnDict[newFileName] = newFilePath

        return returnDict


class formatOut():

    def fileSizeFormatting(self,fileSizeInBytes):

        if float(fileSizeInBytes)/1024/1024>=1:
            fileSize = float(fileSizeInBytes)/1024/1024
            fileSize = '%(#)G'%{'#':fileSize}
            fileSize = str(fileSize) + str(' MB')
        else:
            fileSize = float(fileSizeInBytes)/1024
            fileSize = '%(#)G'%{'#':fileSize}
            fileSize = str(fileSize) + str(' KB')

        return fileSize

    def dateFormat(self,qtdate):

        DATE = str(qtdate.date().day()).zfill(2)
        MONTH = str(qtdate.date().month()).zfill(2)
        YEAR = str(qtdate.date().year()).zfill(4)

        return str(str(DATE) +'/'+ str(MONTH) +'/' + str(YEAR))

    def dateFormatGeneral(self,TimeToFormat, SourceFormat='%Y-%m-%d %H:%M:%S', DestiFormat='%b %d, %I:%M %p'):
        dobj = datetime.datetime.strptime(str(TimeToFormat),SourceFormat)
        return (str(dobj.strftime('%b %d, %I:%M %p')))


def doMain():
    fs = fileSearch()
    fs.SearchPaths = ["M:\\"]
    fs.ruleExtFilters = ["mp3"]
    result = fs.doSearch()
    for each in result:
        print result[each]

if __name__ == "__main__":
    doMain()


