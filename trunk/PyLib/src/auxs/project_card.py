import sys
import os
import console
import PyInterface
from PyQt4 import QtGui


currentFolder = os.getcwd()
parentFolder = os.path.dirname(currentFolder)
modulePathList  =   [
                    os.path.join(currentFolder,'Lib'),
                    os.path.join(currentFolder,'Lib','UI'),
                    os.path.join(currentFolder,'Lib','DB'),
                    'D:/REPO/SOURCE/SCRIPTS/PYTHON/LSAM/SupportLib',
                    'D:/REPO/SOURCE/SCRIPTS/PYTHON/PULSE_GREEN/lib',
                    'D:/REPO/SOURCE/SCRIPTS/PYTHON/Common',
                    'D:/REPO/SOURCE/SCRIPTS/PYTHON/PulseXML',
                    ]

for modulePath in modulePathList:
    modulePath = os.path.normpath(modulePath)
    if modulePath not in sys.path and os.path.exists(modulePath):
        sys.path.append(modulePath)


name = os.getenv('USERNAME').lower()
webBase = 'http://192.168.20.93:85/pulse/beat/projects'


def showCard(arg):
    project = arg[0] if len(arg) else ''
    if project:
        __proInfo(project)
    else:
        print 'NoInfo %s ' % project


def showProjects(arg):
    import projectStruct as projs
    pro = projs.Project('')
    lst = pro.getProjects(name,webBase)

    print
    print 'List of projects:'
    print '-----------------'
    for p in lst: print p
    print
    print 'Total: ' + str(len(lst))
    print


def __proInfo(project):

    import projectStruct as projs
    pro = projs.Project(project)
    pro.doSetDefault(name,webBase)

    print
    print 'Project Name: ' + pro.name
    print 'Web Base: ' + pro.web_base
    print
    print 'FSWorkPath: ' + pro.fs_path_work
    print 'FSLivePath: ' + pro.fs_path_live
    print 'FSOutputPath: ' + pro.fs_path_output
    print 'FSInputPath: ' + pro.fs_path_input
    print
    print 'DBAddress: ' + pro.db_address
    print 'DBPort: ' + pro.db_port
    print 'DBSchema: ' + pro.db_schema
    print 'DBUID: ' + pro.db_uid
    print 'DBPass: ' + pro.db_pass
    print
