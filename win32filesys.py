
import os
import sys
import shutil
import filecmp
import subprocess as sp

class FileSysHandle(object):

    def fsEexecuteApp(self, currentDir, exe, dontKillMe=0):
        print 'Launching... %s - %s' % (currentDir, exe)

        if not (currentDir.rfind('/')>-1 or currentDir.rfind('\\')>-1):
            currentDir = currentDir + '/'

        if os.path.exists(currentDir + exe):
            cdir = os.path.dirname(currentDir + exe)
            sp.Popen(currentDir + exe, cwd=cdir)
            if not dontKillMe: sys.exit(0)
        else:
            if not dontKillMe: sys.exit(0)

    def fsCopyFolder(self, SrcFolder='', DstFolder=''):
        if self.isExist(SrcFolder) and self.isExist(DstFolder):
            fileList = os.listdir(SrcFolder)
            for eachFile in fileList:
                SrcFile = SrcFolder + '/' + eachFile
                if os.path.isfile(SrcFile):
                    self.fsCopyFile(SrcFile, DstFolder)
                elif os.path.isdir(SrcFile) and not (SrcFile.find('.')>=0):
                    NewDstFolder = DstFolder + '/' + eachFile
                    if not self.isExist(NewDstFolder): os.makedirs(NewDstFolder)
                    self.fsCopyFolder(SrcFile,NewDstFolder)

    def fsDeleteFolder(self,  DstFolder=''):
        if self.isExist(DstFolder):
            print '\nRemoving...', DstFolder

            try:
                shutil.rmtree(DstFolder)
            except:
                print '\n\nError! Removing the folder. Folder might be in use!. Close all files/folders and restart.'

            print '\nCreating new folder...', DstFolder
            try:
                if not self.isExist(DstFolder): os.makedirs(DstFolder)
            except:
                print '\n\nError! Creating the folder. Folder might be in use!. Close all files/folders and restart.'

    def fsMakeFolder(self, path):
        if path and not os.path.exists(path):
            os.makedirs(path)

    def fsCopyFile(self, SrcFile='', DstFolder=''):
        try:
            print '\nCopying ... ' + SrcFile + ' -> ' + DstFolder
            shutil.copy2(SrcFile, DstFolder)
            print 'Copied!' if self.isExist(DstFolder) else 'Unable to Copy!'
        except:
            print '\nProblem Copying...' + SrcFile + '->' + DstFolder

    def isSame(self, file1, file2):
        print '\nComparing...\n1. %s\n2. %s'%(file1,file2)
        result = filecmp.cmp(file1,file2)
        print 'Both are same!\n' if result else 'They are different!\n'
        return result

    def isExist(self, path):
        return os.path.exists(path) if path and path!='' and path!='None' and path!=None else False
