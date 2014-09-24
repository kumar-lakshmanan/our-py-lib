from interface_runner import wgt_form1_general, wgt_form3_py2exe
from interface_runner import wgt_form2_uisettings
import general.tools
import os
from PyQt5 import QtCore
import shutil


class General(object):
    projectName = "Your Project Name"
    author = "LKumaresan"
    location = "c:\kumaresan"
    projectType = "pyqtwindows"  # (pyqtwindows/commandline)


class UISettings(object):
    mainWindowTitle = "MainWindow"


class Py2Exe(object):
    isEnabled = True
    appName = "mainapp"
    description = "app created by template"
    company_name = "kumaresan studio"
    copyrights = "kumar"
    version = "1.0.0"
    owner = "kumaresan"

class ppg(object):

    currentScreenForm = None

    def __init__(self, winHandle=None, ppgFolder="defaultPPGFolder"):
        if(winHandle is None): return  # For Fake Objs
        self.infoStyle = general.tools.infoStyle()
        self.infoStyle.errorLevel = 2
        self.infoStyle.infoLevel = 0
        self.tls = general.tools.basic(self.infoStyle)

        self.general = General()
        self.UISettings = UISettings()
        self.py2exe = Py2Exe()

        self.listOfScreenObjs = []
        self.listOfScreenObjs.append(self.general)
        self.listOfScreenObjs.append(self.UISettings)
        self.listOfScreenObjs.append(self.py2exe)

        self.mainWindow = winHandle
        self.projFolder = ppgFolder
        self.ppgFolder = ppgFolder
        self._doBasicSetup()

        self.setCurrentScreen(self.getScreenNameForObject(self.general))

    def _setProjFolder(self):
        self.general.projectName = os.path.basename(self.projFolder)
        self.general.location = os.path.join(self.projFolder)

    def _doBasicSetup(self):
        self._setProjFolder()
        self.ppgFolder = os.path.join(self.ppgFolder, "_ppg_")
        if(not self.tls.isPathOK(self.ppgFolder)):
            self.tls.makePath(self.ppgFolder)

    def clearOldScreen(self):
        if(self.currentScreenName != ""):
            if (self.currentScreenForm is not None):
                self.currentScreenForm.unload()

    def reLoad(self, screenName, avoidShowScreen=False):
        file = self.getScreenFile(screenName)
        if (self.tls.isPathOK(file)):
            if (screenName == 'General'):
                self.general = self.tls.pickleLoadObject(file)
                self._setProjFolder()
                self.currentScreen = self.general
            elif (screenName == 'UISettings'):
                self.UISettings = self.tls.pickleLoadObject(file)
                self.currentScreen = self.UISettings
            elif (screenName == 'Py2Exe'):
                self.py2exe = self.tls.pickleLoadObject(file)
                self.currentScreen = self.py2exe

        if (not avoidShowScreen):
            self.showScreen()

    def syncLocalObjWithCurrentScreenObj(self):
        '''
        currentScreenObj may be updated by actual forms and external classes once that is done
        it is good practice to update all localobjs. This fn will do that.
        '''
        if(self.currentScreenName == "General"):
            self.general = self.currentScreen
        if(self.currentScreenName == "UISettings"):
            self.UISettings = self.currentScreen
        if(self.currentScreenName == "Py2Exe"):
            self.py2exe = self.currentScreen

    def showScreen(self):
        self.clearOldScreen()
        if(self.currentScreenName == "General"):
            self.currentScreenForm = wgt_form1_general.Form(self.mainWindow, self.currentScreen, self)
        if(self.currentScreenName == "UISettings"):
            self.currentScreenForm = wgt_form2_uisettings.Form(self.mainWindow, self.currentScreen, self)
        if(self.currentScreenName == "Py2Exe"):
            self.currentScreenForm = wgt_form3_py2exe.Form(self.mainWindow, self.currentScreen, self)

        self.currentScreenForm.populateUI()

    def reLoadAll(self):
        for eachScreen in self.listOfScreenObjs:
            self.reLoad(self.getScreenNameForObject(eachScreen), avoidShowScreen=True)

#     def saveAllScreens(self):
#         for eachScreen in self.listOfScreenObjs:
#             file = self.getScreenFileForObj(eachScreen)
#             self.tls.pickleSaveObject(eachScreen, file)
#         self.saveCurrentScreen()

    def saveCurrentScreen(self):
        self.currentScreen = self.currentScreenForm.getUpdatedUIValues()
        self.syncLocalObjWithCurrentScreenObj()
        file = self.getScreenFile(self.currentScreenName)
        self.tls.pickleSaveObject(self.currentScreen, file)

    def getObjectForScreenName(self, screenName):
        for eachScreen in self.listOfScreenObjs:
            if(screenName == self.getScreenNameForObject(eachScreen)):
                return eachScreen
        return None

    def getScreenNameForObject(self, obj):
        return obj.__class__.__name__

    def getScreenFile(self, screenName):
        return os.path.join(self.ppgFolder, screenName)

    def getScreenFileForObj(self, obj):
        name = self.getScreenNameForObject(obj)
        return self.getScreenFile(name)

    def getListOfScreenNames(self):
        lst = []
        for eachScreen in self.listOfScreenObjs:
            lst.append(self.getScreenNameForObject(eachScreen))
        return lst

    def setCurrentScreen(self, screenName):
        self.currentScreen = self.getObjectForScreenName(screenName)
        self.currentScreenName = screenName
        self.reLoad(self.currentScreenName)


class ppgGenerator(object):

    def __init__(self, ppgObj):
        self.ppg = ppg(None)
        self.ppg = ppgObj
        self.infoStyle = general.tools.infoStyle()
        self.infoStyle.errorLevel = 2
        self.infoStyle.infoLevel = 0
        self.tls = general.tools.basic(self.infoStyle)

    def doGenerate(self):
        src = os.path.abspath(os.path.curdir)
        src = os.path.join(src, 'BaseCodes')
        if (self.ppg.general.projectType == 'pyqtwindows'):
            src = os.path.join(src, 'SampleQtApp')
        else:
            src = os.path.join(src, 'SamplePyApp')

        dst = self.ppg.general.location

        self._doReadyFileList(src, dst)

        # py2exe
        if(self.ppg.py2exe.isEnabled):
            self._doCopyPy2Exe()

    def _doCopyPy2Exe(self):
        py2exesrc = os.path.abspath(os.path.curdir)
        py2exesrc = os.path.join(py2exesrc, 'BaseCodes', 'py2exeTemplate')

        src = os.path.join(py2exesrc, 'py2exeTemplate.py')
        dst = self.ppg.general.location
        dstPath = os.path.join(dst, 'src', 'core')
        dst = os.path.join(dstPath, 'build_' + self.ppg.general.projectName + '.py')
        buildDir = os.path.join(dstPath, self.ppg.general.projectName + "_bin")
        if(not os.path.exists(buildDir)):
            os.makedirs(buildDir)

        self._doCopyFile(src, dst)

        if (self.ppg.general.projectType == 'pyqtwindows'):
            src = os.path.join(py2exesrc, 'qt.conf')
            dst = os.path.join(buildDir, 'qt.conf')
            self._doCopyFile(src, dst)

            src = os.path.join(py2exesrc, 'plugins')
            buildDir = os.path.join(buildDir, 'plugins')
            if(not os.path.exists(buildDir)):
                os.makedirs(buildDir)
            for (path, dirs, files) in os.walk(src):
                for file in files:
                    srcFile = os.path.join(path, file)
                    dstFile = srcFile.replace(src, buildDir)
                    self._doCopyFile(srcFile, dstFile)

    def _doReadyFileList(self, src, dst):
        for (path, dirs, files) in os.walk(src):
            for file in files:
                srcFile = os.path.join(path, file)
                dstFile = srcFile.replace(src, dst)
                self._doFilters(srcFile, dstFile)

    def _doFilters(self, src, dst):
        srcFile = QtCore.QFileInfo(src)
        dstFile = QtCore.QFileInfo(dst)

        ignoreList = ['__pycache__']

        ignore = False
        for eachIgnoreItem in ignoreList:
            if eachIgnoreItem in srcFile.absoluteFilePath():
                ignore = True

        if (not ignore):
            self._doCopyFile(src, dst)

    def _doCopyFile(self, src, dst):
        srcFile = QtCore.QFileInfo(src)
        dstFile = QtCore.QFileInfo(dst)

        dstFileLoc = dstFile.absolutePath()
        if (not os.path.exists(dstFileLoc)):
            os.makedirs(dstFileLoc)
        src, dst = srcFile.absoluteFilePath(), dstFile.absoluteFilePath()
        shutil.copy(src, dst)
        self.tls.info("\n\nCopied...\n{}\nto\n{}".format(src, dst))

        if(os.path.exists(dstFile.absoluteFilePath())):
            self._doProcessFile(dstFile.absoluteFilePath())

    def _doProcessFile(self, dst):
        dstFile = QtCore.QFileInfo(dst)
        fl = dstFile.absoluteFilePath()
        path = dstFile.absolutePath()
        name = dstFile.baseName()

        if(".project" in fl):
            self._doReplaceParameter(fl, "[[PROJECTNAME]]", self.ppg.general.projectName)

        if("SampleQtApp" in fl or "SamplePyApp" in fl):
            self._doReplaceParameter(fl, "[[PROJECTNAME]]", self.ppg.general.projectName)
            self._doReplaceParameter(fl, "[[AUTHOR]]", self.ppg.general.author)
            self._doReplaceParameter(fl, "[[DATETIME]]", self.tls.getDateTime("%b %d, %Y %a - %H:%M:%S"))
            self._doRenameFiles(fl, self.ppg.general.projectName)

        if("win_main.py" in fl):
            self._doReplaceParameter(fl, "[[AUTHOR]]", self.ppg.general.author)
            self._doReplaceParameter(fl, "[[DATETIME]]", self.tls.getDateTime("%b %d, %Y %a - %H:%M:%S"))
            self._doReplaceParameter(fl, "[[WINDOWTITLE]]", self.ppg.UISettings.mainWindowTitle)

        if("win_main.ui" in fl):
            self._doReplaceParameter(fl, "[[WINDOWTITLE]]", self.ppg.UISettings.mainWindowTitle)

        if("build_" + self.ppg.general.projectName in fl):
            self._doReplaceParameter(fl, "[[AUTHOR]]", self.ppg.general.author)
            self._doReplaceParameter(fl, "[[DATETIME]]", self.tls.getDateTime("%b %d, %Y %a - %H:%M:%S"))
            self._doReplaceParameter(fl, "[[PROJECTNAME]]", self.ppg.general.projectName)
            self._doReplaceParameter(fl, "[[APPNAME]]", self.ppg.py2exe.appName)
            self._doReplaceParameter(fl, "[[DESCRIPTION]]", self.ppg.py2exe.description)
            self._doReplaceParameter(fl, "[[COMPANY]]", self.ppg.py2exe.company_name)
            self._doReplaceParameter(fl, "[[COPYRIGHTS]]", self.ppg.py2exe.copyrights)
            self._doReplaceParameter(fl, "[[VERSION]]", self.ppg.py2exe.version)
            if(self.ppg.general.projectType == 'pyqtwindows'):
                self._doReplaceParameter(fl, "[[COMMANDLINE]]", "False")
            else:
                self._doReplaceParameter(fl, "[[COMMANDLINE]]", "True")


    def _doReplaceParameter(self, fileName, findParameter, replaceWithParameter):
        f = open(fileName, mode='r')
        matter = f.read()
        f.close()
        matter = matter.replace(findParameter, replaceWithParameter, 100000)

        f = open(fileName, mode='w')
        f.write(matter)
        f.close()
        self.tls.info("Updated " + fileName)

    def _doRenameFiles(self, srcFileName, newName):
        srcFile = QtCore.QFileInfo(srcFileName)
        fl = srcFile.absoluteFilePath()
        path = srcFile.absolutePath()
        fileName, fileExtension = os.path.splitext(fl)
        newFile = os.path.join(path, newName)
        newFile += fileExtension
        if(os.path.exists(newFile)):
            os.remove(newFile)
        os.renames(fl, newFile)
        self.tls.info("Rename: " + newFile)


if __name__ == '__main__':
    pass


