import sys
import os

##Remove cached custom modules from memory except preloaded IDE modules
# if __name__ == '__main__':
#     if globals().has_key('InitialModules'):
#          for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
#             del(sys.modules[CustomModule])
#     else:
#         InitialModules = sys.modules.keys()


#######Appending Module Search Path########
if __name__ == '__main__':
    currentFolder = os.getcwd()

####Adjust these Parent Folder to reach root folder####
    parentFolder1 = os.path.dirname(currentFolder)
    parentFolder2 = os.path.dirname(parentFolder1)

####Pass parentFolder Level to reach Root folder####
    rootFolder = currentFolder
    rootFolderParent = os.path.dirname(rootFolder)

####Module Pack folders that will be added to sys search path####
    modulePathList = [
                      #rootFolder + '\lib',
                      #rootFolder + '\lib\controls',
                      #rootFolder + '\ui',
                      #rootFolder + '\ui\common',
                      #rootFolderParent  + '\UI_DB_lib',
                      'C:\Python25\Lib\site-packages\eric4',
                      'C:\Python25\Lib\site-packages\eric4\Graphics'
                     ]

    for modulePath in modulePathList:
        if modulePath not in sys.path:
            sys.path.append(modulePath)

import PackageDiagram
from PyQt4 import QtCore,QtGui

if __name__ == '__main__':
    if len(sys.argv)>0:
        Path = sys.argv[1]
        app = QtGui.QApplication(sys.argv)
        mywin = QtGui.QMainWindow()
        win = PackageDiagram.PackageDiagram(Path,mywin)
        win.show()
        exitcode = app.exec_()
        sys.exit(exitcode)

