from interface_runner import wgt_form1_general
from interface_runner import wgt_form2_uisettings
import general.tools
import os


class General(object):
    projectName = "Your Project Name"
    author = "LKumaresan"
    location = "c:\kumaresan"
    projectType = "pyqtwindows"  # (pyqtwindows/commandline)
    py2exe = 1


class UISettings(object):
    mainWindowTitle = "This wINYour Project Name"


class ppg(object):

    currentScreenForm = None

    def __init__(self, winHandle=None, ppgFolder="defaultPPGFolder"):
        self.tls = general.tools.basic()

        self.general = General()
        self.UISettings = UISettings()

        self.listOfScreenObjs = []
        self.listOfScreenObjs.append(self.general)
        self.listOfScreenObjs.append(self.UISettings)

        self.mainWindow = winHandle
        self.ppgFolder = ppgFolder
        self._checkPPGFolder()

        self.setCurrentScreen(self.getScreenNameForObject(self.general))

    def clearOldScreen(self):
        if(self.currentScreenName != ""):
            if (self.currentScreenForm is not None):
                self.currentScreenForm.unload()

    def reLoad(self, screenName, avoidShowScreen=False):
        file = self.getScreenFile(screenName)
        if (self.tls.isPathOK(file)):
            if (screenName == 'General'):
                self.general = self.tls.pickleLoadObject(file)
                self.currentScreen = self.general
            elif (screenName == 'UISettings'):
                self.UISettings = self.tls.pickleLoadObject(file)
                self.currentScreen = self.UISettings

        if (not avoidShowScreen):
            self.showScreen()

    def showScreen(self):
        self.clearOldScreen()
        if(self.currentScreenName == "General"):
            self.currentScreenForm = wgt_form1_general.Form(self.mainWindow, self.currentScreen, self)
        if(self.currentScreenName == "UISettings"):
            self.currentScreenForm = wgt_form2_uisettings.Form(self.mainWindow, self.currentScreen, self)
        self.currentScreenForm.populateUI()

    def syncLocalObjWithCurrentScreenObj(self):
        '''
        currentScreenObj may be updated by actual forms and external classes once that is done
        it is good practice to update all localobjs. This fn will do that.
        '''
        if(self.currentScreenName == "General"):
            self.general = self.currentScreen
        if(self.currentScreenName == "UISettings"):
            self.UISettings = self.currentScreen

    def reLoadAll(self):
        for eachScreen in self.listOfScreenObjs:
            self.reLoad(self.getScreenNameForObject(eachScreen), avoidShowScreen=True)

    def saveAllScreens(self):
        for eachScreen in self.listOfScreenObjs:
            file = self.getScreenFileForObj(eachScreen)
            self.tls.pickleSaveObject(eachScreen, file)
        self.saveCurrentScreen()

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

    def _checkPPGFolder(self):
        if(not self.tls.isPathOK(self.ppgFolder)):
            self.tls.makePath(self.ppgFolder)

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

    def __init__(self):
        pass

    def doGenerate(self):
        pass