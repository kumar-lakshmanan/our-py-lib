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
            self.FilePathAlone = str(FS.path())
            self.FileNameAlone = str(os.path.basename(path).replace('.'+FS.suffix(),''))
            self.FileExtAlone = str(FS.suffix())
            self.FileName = str(os.path.basename(path))
            self.File = str(FS.filePath())
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



class fileSystem():

    def __init__(self, SearchList):
        '''
        Pass a list of SearchList and use the functions to search the files/folders with Ext Rules for files.
        '''

        self.SearchList = SearchList
        self.ruleExtFilters = []
        self.ruleNameFilters = []
        self.ruleDefined = ['NOHIDDEN']


    def getFileList(self):

        FileList = []

        self.SearchList = list(set(self.SearchList))

        for eachSearchPath in self.SearchList:
            if os.path.exists(eachSearchPath):
                fileList = os.listdir(eachSearchPath)
                for eachFile in fileList:
                    fileName = os.path.join(eachSearchPath,eachFolder)
                    cfile = fileInfo(fileName)


                    if cfile.IsFile:

                        #ExtFilter
                        ExtFilter = False
                        for eachExtFilter in self.ruleExtFilters:
                            if cfile.FileExtAlone == eachExtFilter.upper():
                                ExtFilter = True

                        #NameRule
                        NameFilter = False
                        for eachNameFilter in self.ruleNameFilters:
                            if cfile.FileNameAlone == eachNameFilter.upper():
                                NameFilter = True

                        if str(eachFile).find('.')==0:
                            NameFilter = True

                        #DefinedRule
                        DefineFilter = False
                        if 'NOHIDDEN' in self.ruleDefined:
                            if cfile.IsHidden:
                                DefineFilter = True


                        if not NameFilter and not ExtFilter and not DefineFilter:
                            FileList.append(cfile)


        return FileList


    def getFolderList(self):

        FolderList = []

        self.SearchList = list(set(self.SearchList))

        for eachSearchPath in self.SearchList:
            if os.path.exists(eachSearchPath):
                folderList = os.listdir(eachSearchPath)
                for eachFolder in folderList:
                    folderPath = os.path.join(eachSearchPath,eachFolder)
                    cfolder = fileInfo(folderPath)

                    if cfolder.IsDir:

                        #NameRule
                        NameFilter = False
                        for eachNameFilter in self.ruleNameFilters:
                            if cfolder.FileNameAlone == eachNameFilter.upper():
                                NameFilter = True

                        if str(eachFolder).find('.')==0:
                            NameFilter = True


                        #DefinedRule
                        DefineFilter = False
                        if 'NOHIDDEN' in self.ruleDefined:
                            if cfolder.IsHidden:
                                DefineFilter = True


                        if not NameFilter and not DefineFilter:
                            FolderList.append(cfolder)

        return FolderList


    def getAllFilesUnderFolders(self,foldersList) :

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
                SkipThisFile = False
                print fullFile
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

                    #ExtFilter
                    ExtFilter = len(self.ruleExtFilters)>1
                    for eachExtFilter in self.ruleExtFilters:
                        if cfile.FileExtAlone.upper() == eachExtFilter.upper():
                            ExtFilter = False

                    #NameRule
                    NameFilter = len(self.ruleNameFilters)>1
                    for eachNameFilter in self.ruleNameFilters:
                        if cfile.FileNameAlone.upper() == eachNameFilter.upper():
                            NameFilter = False

                    #DefinedRule
                    DefineFilter = len(self.ruleDefined)>1
                    if 'NOHIDDEN' in self.ruleDefined:
                        if cfile.IsHidden:
                            DefineFilter = False

                    SkipThisFile =  (
                                    ExtFilter
                                    or NameFilter
                                    or DefineFilter
                                    or ConstantFilter
                                    )

                if SkipThisFile: continue

                if os.path.isfile(fullFile) :
                    returnDict[fileName] = fullFile
                else :
                    newfoldersList.append(fullFile)

        if not newfoldersList :
            return returnDict

        newDict = self.getAllFilesUnderFolders(newfoldersList)
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

    def getChildPaths(self,foldersList) :
        returnList = []
        for checkPath in foldersList :
            toAdd = 1
            for folderPath in foldersList :
                if not os.path.exists(folderPath) :
                    continue
                if checkPath == folderPath :
                    continue
                if folderPath.startswith(checkPath) :
                    toAdd = 0
                    break

            if not os.path.exists(checkPath):
                toAdd = 0

            if toAdd :
                returnList.append(checkPath)



        return returnList



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
    lst = ["M:\\"]
    f = fileSystem(lst)
    f.ruleExtFilters = ["MP3","AMR"]
    result = f.getAllFilesUnderFolders(lst)
    for each in result:
        print each

if __name__ == "__main__":
    doMain()


