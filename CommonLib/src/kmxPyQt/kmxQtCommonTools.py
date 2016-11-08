'''
Created on Sep 6, 2014

@author: Mukundan
'''

'''
Usage:

from kmxGeneral import kmxINIConfigReadWrite
from kmxGeneral import kmxTools
from kmxPyQt import kmxQtCommonTools


        self.cfg = kmxINIConfigReadWrite.INIConfig("config.ini")
        self.iconPath = self.cfg.getOption('UserInterface', 'IconPath')
        self.icons = core.icons.iconSetup()
        self.infoStyle = kmxTools.infoStyle()
        self.infoStyle.errorLevel = 2
        self.infoStyle.infoLevel = 0

        self.tls = kmxTools.Tools(self.infoStyle)
        self.qtTools = kmxQtCommonTools.CommonTools(self.win, self.iconPath)

'''

import os

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from kmxGeneral import kmxINIConfigReadWrite
from kmxGeneral import kmxTools
import pickle
import html2text


class iconSetup():
    
    def __init__(self, parent, isRCBased=1, iconBasePath='', iconPrefix=':/fatcow/32x32/'):
        '''
        iconStyle = 1 - Imported RC based icons
        iconStyle = 0 - Absolute Path based icons        
        '''
        self.parent = parent
        self.isRCBased = isRCBased
        self.iconBasePath = iconBasePath
        self.iconPrefix = iconPrefix
        
    def getIconString(self, iconName):
        if self.isRCBased:
            ret = self.iconPrefix + iconName
        else:
            ret = self.iconBasePath + iconName
        return ret
    
    def setIcon(self, item, iconName, size=32):
        itemType = type(item)
        icon = self._getIcon(iconName, size)        
        if itemType == type(QtWidgets.QAction(None)):
            item.setIcon(icon)
            #item.setIconSize(self.getSize(size))
    def getIcon(self,iconName,size=32):
        return self._getIcon(iconName, size)
    
    def getSize(self, size):
        if(size==16):
            return QtCore.QSize(16, 16) 
        if(size==32):
            return QtCore.QSize(32, 32)    

    def _getIcon(self, iconName, size=16):
        if (iconName):
            icon = QtGui.QIcon()
            pixMap = QtGui.QPixmap(self.getIconString(iconName))
            s = self.getSize(size)
            pixMap.scaled(s)        
            icon.addPixmap(pixMap, QtGui.QIcon.Normal, QtGui.QIcon.Off)
            return icon
        return None
    
class CommonTools(object):
    '''
    classdocs
    '''
    def __init__(self, parentWindow, iconPath=None):
        '''
        Constructor
        '''
        self.CallingUI = parentWindow
        self.IconPath = iconPath
        self.defaultIcon = "NoIcon.png"
        self.infoStyle = kmxTools.infoStyle()
        self.ttls = kmxTools.Tools(self.infoStyle)
        if self.IconPath is None:
            self.cfg = kmxINIConfigReadWrite.INIConfig("config.ini", writeOk=False)
            if(self.cfg.iniReady):
                self.iconPath = self.cfg.getOption('UserInterface', 'IconPath')
            else:
                self.IconPath = "../icons/"

    def html2Text(self, data):
        h = html2text.HTML2Text()
        #h.ignore_links = True
        return h.handle(data)
        
    
    def setIconByObj(self, itm2Icon):
        # print (itm2Icon.__name__)
        pass

    def getIconString(self, iconName='NoIcon.png', alternateIcon='NoIcon.png'):
        """
        Returns the path of ICONNAME found on 'iconPath'. Else
        """
        try:
            if os.path.exists(self.IconPath + '/' + iconName) and os.path.isfile(self.IconPath + '/' + iconName):
                return self.IconPath + '/' + iconName
            elif os.path.exists(self.IconPath + '/' + alternateIcon) and os.path.isfile(self.IconPath + '/' + alternateIcon):
                return self.IconPath + '/' + alternateIcon
            elif os.path.exists(self.IconPath + '/' + self.DefaultIcon) and os.path.isfile(self.IconPath + '/' + self.DefaultIcon):
                return self.IconPath + '/' + self.DefaultIcon
            else:
                print ("Error! No Icon found for: " + iconName)
                return None
        except:
            print ("Error! No Icon found for: " + iconName)
            return None

    def getIcon(self, iconName, alternate='', random=False):
            icon = QtGui.QIcon()
            pxmap = None

            if(random):
                iconName = "/04/16/" + str(self.ttls.getRandom(50, 10)) + ".png"

            if alternate:
                iconString = self.getIconString(iconName, alternate)
                if iconString:
                    icon.addPixmap(QtGui.QPixmap(iconString), QtGui.QIcon.Normal, QtGui.QIcon.On)
                    pxmap = QtGui.QPixmap(iconString)
            else:
                iconString = self.getIconString(iconName)
                if iconString:
                    icon.addPixmap(QtGui.QPixmap(iconString), QtGui.QIcon.Normal, QtGui.QIcon.On)
                    pxmap = QtGui.QPixmap(iconString)

            return icon

    def setIconForItem(self, item, iconName, isWindow=0, Col=0, comboBoxIndex=0, OptionalIcon='', thisImage='', clear=0, random=False):
        itemType = type(item)
        # print itemType
        icon = QtGui.QIcon()
        pxmap = None

        if thisImage:
                if os.path.exists(thisImage):
                    icon.addPixmap(QtGui.QPixmap(thisImage), QtGui.QIcon.Normal, QtGui.QIcon.On)
                    pxmap = QtGui.QPixmap(thisImage)
        else:
            icon = self.getIcon(iconName, OptionalIcon, random)

        if clear:
                icon = QtGui.QIcon()
                pxmap = QtGui.QPixmap()

        if isWindow:
            item.setWindowIcon(icon)

        if itemType == type(QtWidgets.QPushButton()):
            item.setIcon(icon)

        if itemType == type(QtWidgets.QToolButton()):
            item.setIcon(icon)

        if itemType == type(QtWidgets.QWidget()):
            tabWidget = item.parentWidget().parentWidget()
            if type(tabWidget) == type(QtWidgets.QTabWidget()):
                index = tabWidget.indexOf(item)
                tabWidget.setTabIcon(index, icon)

        if itemType == type(QtWidgets.QTreeWidgetItem()):
            item.setIcon(Col, icon)

        if itemType == type(QtWidgets.QTableWidgetItem()):
            item.setIcon(icon)

        if itemType == type(QtWidgets.QListWidgetItem()):
            item.setIcon(icon)

        if itemType == type(QtWidgets.QAction(None)):
            item.setIcon(icon)

        if itemType == type(QtWidgets.QLabel()):
            if (pxmap is not None):
                item.setPixmap(pxmap)

        if itemType == type(QtWidgets.QComboBox()):
            item.setItemIcon (comboBoxIndex, icon)


    def getValue(self, control):
        val = ""
        if (type(control) == QtWidgets.QLineEdit):
            val = control.text()
        elif (type(control) == QtWidgets.QLabel):
            val = control.text()
        return str(val)

    def setValue(self, control, value):
        if (type(control) == QtWidgets.QLineEdit):
            control.setText(str(value))
        elif (type(control) == QtWidgets.QLabel):
            control.setText(str(value))

    def applyStyle(self, style='Fusion'):
        # ['Windows', 'WindowsXP', 'WindowsVista', 'Fusion']
        # Use this ... getStyleList()
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create(style))
        QtWidgets.QApplication.setPalette(QtWidgets.QApplication.style().standardPalette())

    def getStyleList(self):
        return QtWidgets.QStyleFactory.keys()

    def showInputBox(self, Title='Information', Message='Information', DefaultValue=''):
        comments, ok = QtWidgets.QInputDialog.getText(self.CallingUI, str(Title), str(Message), QtWidgets.QLineEdit.Normal, DefaultValue)
        if ok:
            return comments
        else:
            return ''

    def getFile(self, Title='Select a file to open...', FileName='Select File', FileType='All Files (*);;Excel Files (*.xls);;Text Files (*.txt)'):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self.CallingUI, str(Title), FileName, str(FileType))
        if(fileName[0] == ""): return ""
        return fileName[0]

    def getFileToSave(self, Title='Select a file to save...', FileName='Select File', FileType='All Files (*);;Excel Files (*.xls);;Text Files (*.txt)'):
        fileName = QtWidgets.QFileDialog.getSaveFileName(self.CallingUI, str(Title), FileName, str(FileType))
        if(fileName[0] == ""): return ""
        return fileName[0]
    
    def getFolder(self, Title='Select a directory...'):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self.CallingUI, str(Title))
        if(folder == ""): return ""
        return folder

    def showYesNoBox(self, Title='Information', Message='Information'):
        ret = QtWidgets.QMessageBox.question(self.CallingUI, Title, Message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        return ret == QtWidgets.QMessageBox.Yes

    def showInfoBox(self, Title='Information', Message='Information'):
        QtWidgets.QMessageBox.information(self.CallingUI, Title, Message)

    def connectToRightClick(self, Widget, FunctionToInvoke):
        self.enableRightClick(Widget)
        #self.CallingUI.connect(Widget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), FunctionToInvoke)
        Widget.customContextMenuRequested.connect(FunctionToInvoke)
        #QtWidgets

    def enableRightClick(self, Widget):
        Widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def quickSave(self, data, fileName):
        with open(fileName, 'wb') as handle:
            pickle.dump(data, handle)        

    def quickLoad(self, fileName):
        if os.path.exists(fileName):
            with open(fileName, 'rb') as handle:
                lst=pickle.load(handle)
            return lst  
        
    def uiLayoutSave(self, layoutFile='layout.lyt', additionalObjToSaveStates=None, saveThisList=[]):
        dirname = os.path.dirname(layoutFile)
        if dirname!='' and not os.path.exists(dirname):
            os.makedirs(dirname)

        win={}
        win['state']=self.CallingUI.saveState()
        win['size']=self.CallingUI.size()
        win['pos']=self.CallingUI.pos()
        
        additionalObjs=[]
        if additionalObjToSaveStates:
            for each in additionalObjToSaveStates:
                splt={}
                splt['state']=each.saveState()
                additionalObjs.append(splt)

        data={}
        data['win']=win
        data['added']=additionalObjs
        data['mylist']=saveThisList
        
        with open(layoutFile, 'wb') as handle:
            pickle.dump(data, handle)


    def uiLayoutRestore(self,layoutFile='layout.lyt',additionalObjToRestoreStates=None):
        if os.path.exists(layoutFile):
            with open(layoutFile, 'rb') as handle:
                data=pickle.load(handle)            
                
            win=data['win']               
            self.CallingUI.restoreState(win['state'])
            self.CallingUI.resize(win['size'])
            self.CallingUI.move(win['pos'])
            
            dcksObj = []
            sptsObj = []
            for each in self.CallingUI.children():
                if isinstance(each,QtWidgets.QDockWidget):
                    dcksObj.append(each)
                elif isinstance(each,QtWidgets.QSplitter):
                    sptsObj.append(each)
            
#             dcks=data['dcks']
#             for cnt, each in enumerate(range(len(dcksObj),0,-1)):
#                 dcksObj[cnt].resize(dcks[cnt]['size'])
#                 dcksObj[cnt].move(dcks[cnt]['pos'])

            added=data['added']
            if additionalObjToRestoreStates:
                for cnt, each in enumerate(range(0,len(additionalObjToRestoreStates))):
                    additionalObjToRestoreStates[cnt].restoreState(added[cnt]['state'])
        
            return data['mylist']
        return None

    def popUpMenu(self, menuRequestingtObject, PopupPoint, menuListString, funcToInvoke, additionalArguments='', iconList = []):

        """
        self.CallingUI - where the menuRequestingtObject is placed, usaully self
        menuRequestingtObject - Into which menu will be generated
        PopupPoint - QPoint where menu should popout
        menuListString - Array of menu items
        funcToInvoke - Function to be invoked on menu item clicked
        additionalArguments - argument to that function

            Inside funcToInvoke() you will receive a tuple with three items
            1 - Menu Label
            2 - Menu Label Index
            3 - added_arg

            eg:
            myutils().popUpMenu(self,self.textEdit,PopupPoint,["KUMAR","TEST"],self.funs,["myarg1","myarg2"])

            def funs(self,t)
                    print "Label Clicked is: " + str(t[0])
                    print "Label Index is: " + str(t[1])
                    print "Added Argument: " + str(t[2])

        """
        if menuListString == []:
            return 0;
        Rmnu = QtWidgets.QMenu(self.CallingUI)
        for i, itm in enumerate(menuListString):

            newmenuitem = QtWidgets.QAction(itm, self.CallingUI)
            #newmenuitem

            if len(itm)>1 and itm[0]=='|':
                itm = itm[1:len(itm)]
                newmenuitem.setEnabled(False)
                newmenuitem.setText(itm)
                #var = QtCore.QVariant()



            if itm != '':
                if len(iconList)>1 and len(iconList)>i:
                    if iconList[i]!=None:
                        icon = QtGui.QIcon()
                        icon.addPixmap(QtGui.QPixmap(iconList[i]), QtGui.QIcon.Normal, QtGui.QIcon.On)
                        newmenuitem.setIcon(icon)

            #self.CallingUI.connect(newmenuitem, QtCore.SIGNAL("triggered()"), lambda passarg=(itm,i,additionalArguments,newmenuitem): funcToInvoke(passarg))
            newmenuitem.triggered.connect(lambda passarg=([itm,i,additionalArguments,newmenuitem]): funcToInvoke(passarg))
            newmenuitem.setData(PopupPoint)

            if itm=='':
                Rmnu.addSeparator()
            else:
                Rmnu.addAction(newmenuitem)


        PopupPoint.setY(PopupPoint.y())
        PopupPoint.setX(PopupPoint.x())
        Rmnu.exec_(menuRequestingtObject.mapToGlobal(PopupPoint))
        del(Rmnu)



    def popUpMenuAdv(self, MenuList, MenuRequestingObject, MenuStartPoint, FunctionToBeInvoked, AdditionalArgument=[], popupOffset=QtCore.QPoint(0,0)):

        """

        popup a menu for a given object and point

        menu = [{'m1':'iconPath'},{'m2':''},[{'m3':''},{'m31':''},[{'m32':''},{'m321':''},{'m322':''}],{'m33':''}],{'m4':''},{'m5':''},[{'m6':''},{'m61':''},{'m62':''}],'m7']
        or
        menu = ['m1','m2',['m3','m31',['m32','m321','m322'],'m33'],'m4','m5',['m6','m61','m62'],'m7']

        m1
        m2
        m3-->m31
        m4   m32-->m321
        m5   m33   m322
        m6
        m7

        eg:

        self.uic = QtUiSupport.uiComman(self)
        self.uif = QtUiSupport.visualFormat('//tech/share/PULSE_SANDBOX/GLOBAL_SETTINGS/BASEICONS/splIcons')

        ic1 = self.uif.getIconForLabel('photo-album.png')
        ic2 = self.uif.getIconForLabel('shortcut.png')

        menu = [{'m1':ic1},{'m2':ic2},[{'m3':ic3},{'m31':ic4},[{'m32':ic5},{'m321':ic6},{'m322':ic7}],{'m33':ic8}],{'m4':ic9},{'m5':ic0},[{'m6':ic11},{'m61':ic12},{'m62':ic13}],{'m7':ic14}]

        self.uic.popUpMenuAdv(menu,self.pushButton,qpoint,self.myOptFun,'addedArgument')

        Your Function will be invoked and following values will be passed through the single argument.

            RETURN VALUE (Single Tuple):
            ('MENULABEL', 1, 2, 0, 'addedArgument', <PyQt4.QtGui.QAction object at 0x045B9030>)

            MENULABEL = Menu Label
            1 = Menu Level No (0 - Main Menu, 1 - First Level Submenu, 2 - Second Level Submenu....)
            2 = Parent ID - Index of the parent item, In parent's level
            0 = ItemIndex - Index of item, In its level
            addedArgument = Addition Arguments which was added on menu creation.
            QACTION - Action is the item sending the signal.

        See UISUPPORT.menuCreator function for additional info!

        """

        if type(MenuStartPoint)==type(QtCore.QPoint()):
            PopupPoint = MenuStartPoint
        else:
            PopupPoint = QtCore.QPoint(-3,-5)

        Rmnu = self.menuCreator(MenuList, self.CallingUI, AdditionalArgument, FunctionToBeInvoked)
        PopupPoint.setY(PopupPoint.y() + popupOffset.y())
        PopupPoint.setX(PopupPoint.x() + popupOffset.x())
        Rmnu.exec_(MenuRequestingObject.mapToGlobal(PopupPoint))
        del(Rmnu)

    def menuCreator(self, listOfItem, CallingUI, AdditionalArgument, FunctionToInvoke, ParentID=0, Level=0):

        '''
        Do you want menu?
        Give me listOfMenuItem and function to be invoked, and additional args that are to be passed to that functoin... .

        Results a menu which can be used
            * for popup as context menu
            * ui main menu
            * toolbutton popup menu

        Your Function will be invoked and following values will be passed through the single argument.

            RETURN VALUE (Single Tuple):
            ('MENULABEL', 1, 2, 0, 'addedArgument', <PyQt4.QtGui.QAction object at 0x045B9030>)

            MENULABEL = Menu Label
            1 = Menu Level No (0 - Main Menu, 1 - First Level Submenu, 2 - Second Level Submenu....)
            2 = Parent ID - Index of the parent item, In parent's level
            0 = ItemIndex - Index of item, In its level
            addedArgument = Addition Arguments which was added on menu creation.
            QACTION - Action is the item sending the signal.


        Eg:

        ic1 = 'D:\DD\DD\DOWNICON.png'
        ic2 = 'D:\DD\DD\DOWNICON.png'
        .
        .
        .

        menu = [{'mx1':ic1},{'mxx2':ic2},{'kzzzz':ic4},[{'mcccccc3z':ic3},{'mzxczxczcx31':ic4},[{'xzczcm32':ic5},{'sdfsdfm321':ic6},{'m3ffffs22':ic7}],{'msdfsdf33':ic8}],{'mxcvxcv4':ic9},{'ewrwerwerm5':ic0},[{'mrrrwe6':ic11},{'m61':ic12},{'m62':ic13}],{'m7':ic14}]
        mnu = UISUPPORT.menuCreator(menu, self, 'ADDEDARG', self.mySplMenuFunction)

        self.toolButton.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        self.toolButton.setMenu(mnu)



        See UISUPPORT.popUpMenuAdv function for additional info!

        '''

        Rmnu =  QtWidgets.QMenu(self.CallingUI)

        Rmnu.setTearOffEnabled(False)

        for cnt, eachItem in enumerate(listOfItem):
            if type(eachItem)==type([]):
                Menu = self.menuCreator(eachItem[1:], self.CallingUI, AdditionalArgument, FunctionToInvoke, cnt, Level+1)
                if type(eachItem[0])==type({}):
                    Menu.setTitle(eachItem[0].keys()[0])
                else:
                    Menu.setTitle(str(eachItem[0]))
                Rmnu.addMenu(Menu)
            else:
                itemDict = eachItem

                if type(itemDict)==type({}):
                    Label = itemDict.keys()[0]
                    IconPath = itemDict.values()[0]
                else:
                    Label = str(itemDict)
                    IconPath = ''

                newmenuitem = QtWidgets.QAction(Label, self.CallingUI)
                if len(eachItem)>1 and Label[0]=='|':
                    Label = Label[1:len(Label)]
                    newmenuitem.setEnabled(False)
                    newmenuitem.setText(Label)

                if IconPath:
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(IconPath), QtGui.QIcon.Normal, QtGui.QIcon.On)
                    newmenuitem.setIcon(icon)

                newmenuitem.triggered.connect(lambda passarg=(Label,Level,ParentID,cnt,AdditionalArgument,newmenuitem): FunctionToInvoke(passarg))

                if Label=='':
                    Rmnu.addSeparator()

                else:
                    Rmnu.addAction(newmenuitem)
        return Rmnu
