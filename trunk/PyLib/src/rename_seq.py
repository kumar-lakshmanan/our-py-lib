__author__ = 'lkumaresan'

import os
import shutil

def doRename(arg):
    if len(arg)==3:
        filePath = arg[0] if len(arg)>0 else ''
        oldName = arg[1] if len(arg)>1 else ''
        newName = arg[2] if len(arg)>2 else ''
        filePath = os.path.normpath(filePath)

        if not os.path.exists(filePath):
            print '%s does not exist!' % filePath
            dispInfo()
            return 0

        if not os.path.isdir(filePath):
            print '%s is not a valid path!' % filePath
            dispInfo()
            return 0

        if filePath and oldName and newName and os.path.exists(filePath) and os.path.isdir(filePath):
            files = os.listdir(filePath)
            for eachFileName in files:
                oldFile = os.path.join(filePath,eachFileName)
                if os.path.isdir(oldFile):
                    doRename([oldFile, oldName, newName])
                else:
                    if oldName in eachFileName:
                        newFileName = eachFileName.replace(oldName, newName)
                        newFile = os.path.join(filePath,newFileName)
                        if os.path.exists(oldFile):
                            if not os.path.exists(newFile):
                                print 'Renaming... %s -> %s' % (oldFile, newFileName)
                                try:
                                    shutil.move(oldFile,newFile)
                                except:
                                    print 'Error renameing the file! Might be in use!'
                                print 'Done!' if os.path.exists(newFile) else 'Problem Renaming!'
                            else:
                                print '%s already exists!' % newFile
                    else:
                        print '%s not found in %s' % (oldName,oldFile)
        else:
            print 'Invalid input!'
    else:
        dispInfo()

def dispInfo():
        print '\n\nInvalid Input for renaming.\n\n'
        print '\nInput Format:\n'
        print '\nRenameSeq "D:\SOMEPATH" OLDNAME NEWNAME\n\n\n'
        print '\nEg Files:\n'
        print '\nD:\SOMEPATH\OLDNAME.000.EXT'
        print '\nD:\SOMEPATH\OLDNAME.001.EXT'
        print '\nD:\SOMEPATH\OLDNAME.002.EXT'
        print '\nD:\SOMEPATH\OLDNAME.003.EXT'
        print '\n\n'


