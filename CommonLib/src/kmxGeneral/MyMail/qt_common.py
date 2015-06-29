from PyQt4 import QtCore, QtGui
import os
import sys
import pickle
from functools import partial
from time import strftime

class PyQtAppSupport():
    """
        Comman functions for handling most of the ItemWidgets and BASE ui
    """

    def __init__(self, CallingUI=None, iconPath=None, defaultIcon=None):
        self.CallingUI = CallingUI
        self.IconPath = iconPath
        self.DefaultIcon = defaultIcon

    def waitDialog(self, winHeading='Please wait...', label='Please wait...Processing!', textStyle = None, w=350, h=100, model=False, noClose=True, keyPressFunction=None):

        '''

        def closeMyDialog(window,Eve):
            if Eve.key() == QtCore.Qt.Key_Escape:
                window.close()

        di = PyQtAppSupport().waitDialog(model=False, keyPressFunction=closeMyDialog)

        '''


        dia = QtGui.QDialog()

        if noClose:
            dia.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint)
            #dia.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTitleHint)

        dia.resize(w,h)
        LABEL = QtGui.QLabel()
        LABEL.setFrameStyle(QtGui.QFrame.Panel|QtGui.QFrame.Sunken)
        LABEL.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter)
        grd = QtGui.QGridLayout(dia)
        grd.addWidget(LABEL)
        dia.setWindowTitle(winHeading)
        if textStyle: LABEL.setFont(textStyle)
        LABEL.setText(label)
        dia.label = LABEL
        if keyPressFunction:
            dia.__class__.keyReleaseEvent = keyPressFunction
        QtGui.QApplication.processEvents()
        dia.exec_() if model else dia.show()
        QtGui.QApplication.processEvents()
        return dia

    def mouseLock(self):
        self.CallingUI.grabMouse(QtCore.Qt.WaitCursor)

    def mouseRelease(self):
        self.CallingUI.releaseMouse()

    def keyboardLock(self):
        self.CallingUI.grabKeyboard()

    def keyboardRelease(self):
        self.CallingUI.releaseKeyboard()

    def getFile(self,Title='Select a file to open...',FileName='YourFile',FileType='All Files (*);;Excel Files (*.xls);;Text Files (*.txt)'):
        fileName = QtGui.QFileDialog.getOpenFileName(self.CallingUI, str(Title), FileName, str(FileType))
        if not fileName.isEmpty():
            return str(fileName)
        return ''

    def toolBarEmpty (self, toolBar):

        toolBar = QtGui.QToolBar()
        for eachAction in toolBar.actions:
            toolBar.removeAction(eachAction)


    def toolBarAddButton(self, toolBar, buttonLabel, functionToInvoke, Checkable=False, Icon=None,AlterIcon=None):

        #toolBar = QtGui.QToolBar()
        action = QtGui.QAction(self.CallingUI)
        action.setCheckable(Checkable)
        action.setText(str(buttonLabel))
        toolBar.addAction(action)
        self.CallingUI.connect(action, QtCore.SIGNAL('triggered()'), functionToInvoke)

        if Icon:
            self.setIconForItem(action,Icon,OptionalIcon=AlterIcon)
        return action


    def formatToolButton(self, widget, text='', textIconStyleMode=2, autoRise=0):

        if textIconStyleMode==0:
            widget.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        if textIconStyleMode==1:
            widget.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        if textIconStyleMode==2:
            widget.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        if textIconStyleMode==3:
            widget.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        widget.setAutoRaise(autoRise)

        if text:
            widget.setText(str(text))
        if text=='RAMUK':
            widget.setText('')

    def uiLayoutSave(self,presetfile='Temp.lyt'):

        dirname = os.path.dirname(presetfile)
        if dirname!='' and not os.path.exists(dirname):
            os.makedirs(dirname)

        qb = self.CallingUI.saveState()
        winsiz = self.CallingUI.size()
        winpos = self.CallingUI.pos()
        lst = [qb,winsiz,winpos]
        f=open(presetfile, 'w')
        pickle.dump(lst,f)
        f.close()

    def uiLayoutRestore(self,presetfile='Temp.lyt'):

        if os.path.exists(presetfile):
            f=open(presetfile, 'r')
            lst = pickle.load(f)
            f.close()
            qb = lst[0]
            winsiz = lst[1]
            winpos = lst[2]
            self.CallingUI.restoreState(qb)
            self.CallingUI.resize(winsiz)
            self.CallingUI.move(winpos)

    def getSkinList(self):
        return [str(each) for each in QtGui.QStyleFactory.keys()]

    def setSkinList(self,ListName):
        ListName.addItems(QtGui.QStyleFactory.keys())

    def setSkin(self,SkinName='windows'):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(SkinName))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())

    def getIconForLabel(self,iconname='NoIcon.png',alternateIcon='NoIcon.png'):
        """
        Returns the path of ICONNAME found on 'iconPath'. Else
        """
        if os.path.exists(self.IconPath+'/'+iconname) and os.path.isfile(self.IconPath+'/'+iconname):
            return self.IconPath+'/'+iconname
        elif os.path.exists(self.IconPath+'/'+alternateIcon) and os.path.isfile(self.IconPath+'/'+alternateIcon):
            return self.IconPath+'/'+alternateIcon
        elif os.path.exists(self.IconPath+'/'+self.DefaultIcon) and os.path.isfile(self.IconPath+'/'+self.DefaultIcon):
            return self.IconPath+'/'+self.DefaultIcon
        else:
            print "Error!","No Icon found for: " + iconname
            return None

    def getIcon(self,iconName, OptionalIcon=''):


        #print itemType

        icon = QtGui.QIcon()
        pxmap = None

        if OptionalIcon:
            if self.getIconForLabel(iconName,OptionalIcon):
                icon.addPixmap(QtGui.QPixmap(self.getIconForLabel(iconName,OptionalIcon)), QtGui.QIcon.Normal, QtGui.QIcon.On)
                pxmap = QtGui.QPixmap(self.getIconForLabel(iconName,OptionalIcon))
        else:
            if self.getIconForLabel(iconName):
                icon.addPixmap(QtGui.QPixmap(self.getIconForLabel(iconName)), QtGui.QIcon.Normal, QtGui.QIcon.On)
                pxmap = QtGui.QPixmap(self.getIconForLabel(iconName))
        return icon

    def setIconForItem(self,item,iconName,Window=0,Col=0, comboBoxIndex=0,OptionalIcon='',thisImage=''):

        itemType = type(item)

        #print itemType


        icon = QtGui.QIcon()
        pxmap = None

        if thisImage:
                if os.path.exists(thisImage):
                    icon.addPixmap(QtGui.QPixmap(thisImage), QtGui.QIcon.Normal, QtGui.QIcon.On)
                    pxmap = QtGui.QPixmap(thisImage)
        else:
            if OptionalIcon:
                if self.getIconForLabel(iconName,OptionalIcon):
                    icon.addPixmap(QtGui.QPixmap(self.getIconForLabel(iconName,OptionalIcon)), QtGui.QIcon.Normal, QtGui.QIcon.On)
                    pxmap = QtGui.QPixmap(self.getIconForLabel(iconName,OptionalIcon))
            else:
                if self.getIconForLabel(iconName):
                    icon.addPixmap(QtGui.QPixmap(self.getIconForLabel(iconName)), QtGui.QIcon.Normal, QtGui.QIcon.On)
                    pxmap = QtGui.QPixmap(self.getIconForLabel(iconName))

        if Window:
            item.setWindowIcon(icon)

        if itemType == type(QtGui.QPushButton()):
            item.setIcon(icon)

        if itemType == type(QtGui.QToolButton()):
            item.setIcon(icon)

        if itemType == type(QtGui.QWidget()):
            tabWidget = item.parentWidget().parentWidget()
            if type(tabWidget)==type(QtGui.QTabWidget()):
                index = tabWidget.indexOf(item)
                tabWidget.setTabIcon(index,icon)

        if itemType == type(QtGui.QTreeWidgetItem()):
            item.setIcon(Col,icon)

        if itemType == type(QtGui.QTableWidgetItem()):
            item.setIcon(icon)

        if itemType == type(QtGui.QListWidgetItem()):
            item.setIcon(icon)

        if itemType == type(QtGui.QAction(None)):
            item.setIcon(icon)

        if itemType == type(QtGui.QLabel()):
            if pxmap<>None:
                item.setPixmap(pxmap)

        if itemType == type(QtGui.QComboBox()):
            item.setItemIcon (comboBoxIndex, icon)


    def setFontForItem(self,item,bold=0,italic=0,underline=0,strike=0,size=8,Col=0,TextColor=''):
        f = QtGui.QFont()
        f.setBold(bold)
        f.setUnderline(underline)
        f.setItalic(italic)
        f.setStrikeOut(strike)
        f.setPointSize(int(size))

        if TextColor:
            if type(item)==type(QtGui.QTreeWidgetItem()):
                item.setTextColor(Col,TextColor)
            else:
                item.setTextColor(TextColor)

        if type(item)==type(QtGui.QTreeWidgetItem()):
            item.setFont(Col,f)
        else:
            item.setFont(f)
        return f


    def setLayoutList(self,ListName,LayoutFolder):

        if os.path.exists(LayoutFolder):
            files = os.listdir(LayoutFolder)
            for eachFile in files:
                lytfile = LayoutFolder + '/' + eachFile
                if os.path.isfile(lytfile) and str(os.path.splitext(eachFile)[1]).upper() == '.LYT':
                    ListName.addItem(eachFile)


    def errorReport(self, prittyPrint=1):
        try:
            TrackStack = sys.exc_traceback
            ErrorReport = []
            while TrackStack:
            	FileName = TrackStack.tb_frame.f_code.co_filename
            	FunctionName = TrackStack.tb_frame.f_code.co_name
            	ErrorLine =TrackStack.tb_lineno
            	TrackStack = TrackStack.tb_next
            	ErrorReport.append([FileName,FunctionName,ErrorLine])

            ErrorReport.append([sys.exc_info()[0],sys.exc_info()[1],0])

            if prittyPrint:
                ErrorInfo=''
                for eachErrorLevel in ErrorReport:
                    ErrorInfo+= '\nFile: "' + str(eachErrorLevel[0]) + '", line ' + str(eachErrorLevel[2]) + ', in ' + str(eachErrorLevel[1])
                return ErrorInfo
            else:
                return ErrorReport

        except:
            return 'Problem Preparing Error Report'


    def errorReportAdvance(self):

        Ret = {}
        ErrorReport = []
        try:
            TrackStack = sys.exc_traceback
            while TrackStack:
            	FileName = TrackStack.tb_frame.f_code.co_filename
            	FunctionName = TrackStack.tb_frame.f_code.co_name
            	ErrorLine =TrackStack.tb_lineno
            	TrackStack = TrackStack.tb_next
            	ErrorReport.append([FileName,FunctionName,ErrorLine])
            ErrorReport.append([sys.exc_info()[0],sys.exc_info()[1],0])
            Ret['Result'] = 1
        except:
            Ret['Result'] = 0

        Ret['ErrorInfo'] = ErrorReport

        return Ret

    def setDockOption(self,AnimateDock=1, ForceTabbedDock=1, AutoTabHeadOrientation=1, Lock=False):


        #Dock Options setting value on main window
        dkop = QtGui.QMainWindow.DockOptions()

        dkop = dkop.__or__(QtGui.QMainWindow.AllowTabbedDocks)
        dkop = dkop.__or__(QtGui.QMainWindow.AllowNestedDocks)

        if AnimateDock:
            dkop = dkop.__or__(QtGui.QMainWindow.AnimatedDocks)

        if ForceTabbedDock:
            dkop = dkop.__or__(QtGui.QMainWindow.ForceTabbedDocks)

        if AutoTabHeadOrientation:
            dkop = dkop.__or__(QtGui.QMainWindow.VerticalTabs)

        self.CallingUI.setDockOptions(dkop)



        #Dock Feature setting value on each Dock
        dkFeature = QtGui.QDockWidget.DockWidgetFeatures()

        if Lock:
            dkFeature = dkFeature.__or__(QtGui.QDockWidget.NoDockWidgetFeatures)
        else:
            dkFeature = dkFeature.__or__(QtGui.QDockWidget.DockWidgetMovable)
            dkFeature = dkFeature.__or__(QtGui.QDockWidget.DockWidgetFloatable)
            dkFeature = dkFeature.__or__(QtGui.QDockWidget.DockWidgetClosable)

        for eachObj in self.CallingUI.children():
            if type(eachObj) == type(QtGui.QDockWidget()):
                eachObj.setFeatures(dkFeature)



    def winLock(self,lock):
        if lock:
            self.CallingUI.statusbar.showMessage('Just a moment...')
        else:
            self.CallingUI.statusbar.showMessage('')

        self.CallingUI.setEnabled(not lock)


    def getLabelNDataForListItem(self,listItem):
        return {'Label':listItem.text(), 'Data':listItem.data(QtCore.Qt.UserRole).toString()}

    def getLabelNDataForTreeItem(self,treeItem,Col=0):
        return {'Label':treeItem.text(Col), 'Data':treeItem.data(Col,QtCore.Qt.UserRole).toString()}

    def getLabelNDataForTableItem(self,tableItem):
        return {'Label':tableItem.text(), 'Data':tableItem.data(QtCore.Qt.UserRole).toString()}

    def getListItemForData(self,listBox,data):
        for i in xrange(0,listBox.count()):
            if listBox.item(i).data(QtCore.Qt.UserRole).toString() == str(data):
                return listBox.item(i)

    def getCommandLine(self,mode='',needValue=1,Simple=False):

        if Simple:
            if len(sys.argv)>1:
                res = ''
                for cnt in xrange(1,len(sys.argv)):
                    res += sys.argv[cnt]
                return res
            else:
                return 0

        if not needValue:
            if len(sys.argv)>1:
                for eachCommand in sys.argv:
                    if str(eachCommand).upper().strip() == str(mode).upper().strip():
                        return 1
                return 0


        commandLines = []
        if len(sys.argv)>1:
            for eachCommand in sys.argv:
                cmdline = eachCommand.split('=')
                if len(cmdline)==2:
                    commandLines.append(str(eachCommand).upper().strip())


        for eachCommands in commandLines:
            if str(mode+'=').upper().strip() in eachCommands.upper().strip():
                val = eachCommands.split('=')[1]
                return val.upper()
        return 0



    def getLabel(self,control,ignoredisabled=False):

        """
        Give any control... Get the string from

            x = self.getLabel(self.listWidget_2)
            if str(x)!=str(None):
                thingstoupdate = self.updateString(thingstoupdate,"Status=\""+x+"\""," , ")
        """


        if str(type(control)) == "<class 'PyQt4.QtGui.QListWidget'>"  and control.selectedItems().__len__()>0 and ( ignoredisabled or control.isEnabled()):
            return control.selectedItems()[0].text()

        if str(type(control)) == "<class 'PyQt4.QtGui.QComboBox'>"  and control.currentText()!="" and ( ignoredisabled or control.isEnabled()):
            return control.currentText()

        if str(type(control)) == "<class 'PyQt4.QtGui.QDateTimeEdit'>"  and ( ignoredisabled or control.isEnabled()):
                return now("yyyy-MM-dd hh:mm:ss",control.dateTime())

        if str(type(control)) == "<class 'PyQt4.QtGui.QTimeEdit'>"  and ( ignoredisabled or control.isEnabled()):
                return now("hh:mm",control.time())

        if str(type(control)) == "<class 'PyQt4.QtGui.QLineEdit'>"  and control.text()!="" and ( ignoredisabled or control.isEnabled() ):
                return control.text()

        if str(type(control)) == "<class 'PyQt4.QtGui.QTextEdit'>"  and control.toPlainText()!="" and ( ignoredisabled or control.isEnabled()):
                return control.toPlainText()

        if str(type(control)) == "<class 'PyQt4.QtGui.QCalendarWidget'>"  and ( ignoredisabled or control.isEnabled()):
                return now("yyyy-MM-dd",control.selectedDate())

        if str(type(control)) == "<class 'PyQt4.QtGui.QTabWidget'>"  and ( ignoredisabled or control.isEnabled()):
                return control.currentIndex()

        if str(type(control)) == "<class 'PyQt4.QtGui.QDockWidget'>"  and ( ignoredisabled or control.isEnabled()):
                return control.isVisible()

        if str(type(control)) == "<class 'PyQt4.QtGui.QSpinBox'>"  and ( ignoredisabled or control.isEnabled()):
               return control.value()

        if str(type(control)) == "<class 'PyQt4.QtGui.QLabel'>"  and ( ignoredisabled or control.isEnabled()):
               return control.text()

        if str(type(control)) == "<class 'PyQt4.QtGui.QTextBrowser'>" and (control.isEnabled() or ignoredisabled):
                return control.toPlainText()

        if str(type(control)) == "<class 'PyQt4.QtGui.QPlainTextEdit'>" and (control.isEnabled() or ignoredisabled):
                return control.toPlainText()

        if str(type(control)) == "<class 'PyQt4.QtGui.QDateEdit'>" and (control.isEnabled() or ignoredisabled):
                return control.date()

        if str(type(control)) == "<class 'PyQt4.QtGui.QCheckBox'>" and (control.isEnabled() or ignoredisabled):
                return control.isChecked()

        return None


    def setLabel(self,control,Strx,ignoredisabled=False):

        if str(type(control)) == "<class 'PyQt4.QtGui.QListWidget'>" and (control.isEnabled() or ignoredisabled):
            d = control.findItems(str(Strx) , QtCore.Qt.MatchContains)
            if d.__len__()>0:
                control.setItemSelected(d[0],True)
            else:
                d = control.findItems(str("None"), QtCore.Qt.MatchContains)
                if d.__len__()>0:
                    control.setItemSelected(d[0],True)


        if str(type(control)) == "<class 'PyQt4.QtGui.QComboBox'>" and (control.isEnabled() or ignoredisabled):
            d = control.findText(str(Strx))
            if d>-1:
                control.setCurrentIndex(d)
            else:
                d = control.findText(str("None"))
                if d>-1:
                    control.setCurrentIndex(d)


        if str(type(control)) == "<class 'PyQt4.QtGui.QLineEdit'>" and (control.isEnabled() or ignoredisabled):
                control.setText(str(Strx))

        if str(type(control)) == "<class 'PyQt4.QtGui.QSpinBox'>" and (control.isEnabled() or ignoredisabled):
            if str(Strx)!="None":
                control.setValue(int(Strx))

        if str(type(control)) == "<class 'PyQt4.QtGui.QGroupBox'>" and (control.isEnabled() or ignoredisabled):
                control.setChecked(bool(Strx))

        if str(type(control)) == "<class 'PyQt4.QtGui.QCheckBox'>" and (control.isEnabled() or ignoredisabled):
                control.setChecked(bool(Strx))

        if str(type(control)) == "<class 'PyQt4.QtGui.QCheckBox'>" and (control.isEnabled() or ignoredisabled):
                control.setChecked(bool(Strx))

        if str(type(control)) == "<class 'PyQt4.QtGui.QTabWidget'>" and (control.isEnabled() or ignoredisabled):
                control.setCurrentIndex(int(Strx))

        if str(type(control)) == "<class 'PyQt4.QtGui.QDockWidget'>" and (control.isEnabled() or ignoredisabled):
                control.setVisible(smart_bool(Strx))

        if str(type(control)) == "<class 'PyQt4.QtGui.QDateTimeEdit'>" and (control.isEnabled() or ignoredisabled):
                control.setDateTime(Strx)

        if str(type(control)) == "<class 'PyQt4.QtGui.QDateEdit'>" and (control.isEnabled() or ignoredisabled):
                control.setDate(Strx)

        if str(type(control)) == "<class 'PyQt4.QtGui.QTimeEdit'>" and (control.isEnabled() or ignoredisabled):
                control.setTime(Strx)

        if str(type(control)) == "<class 'PyQt4.QtGui.QTextEdit'>" and (control.isEnabled() or ignoredisabled):
                control.setPlainText(Strx)

        if str(type(control)) == "<class 'PyQt4.QtGui.QLabel'>" and (control.isEnabled() or ignoredisabled):
                control.setText(Strx)

        if str(type(control)) == "<class 'PyQt4.QtGui.QTextBrowser'>" and (control.isEnabled() or ignoredisabled):
                control.setText(Strx)

        if str(type(control)) == "<class 'PyQt4.QtGui.QCheckBox'>" and (control.isEnabled() or ignoredisabled):
                return control.setChecked(bool(Strx))

    def showInformationBox(self,Title='Information',Message='Information'):
        QtGui.QMessageBox.information(self.CallingUI,Title,Message)

    def showInputBox(self,Title='Information',Message='Information',DefaultValue=''):
        comments, ok = QtGui.QInputDialog.getText(self.CallingUI, str(Title), str(Message), QtGui.QLineEdit.Normal, DefaultValue)
        if ok and not comments.isEmpty():
            return comments
        else:
            return ''

    def showYesNoBox(self,Title='Information',Message='Information'):
        rep = QtGui.QMessageBox.question(self.CallingUI, Title, Message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if rep == QtGui.QMessageBox.Yes:
            return 1
        else:
            return 0

    def showYesNoCancelBox(self,Title='Information',Message='Information'):
        rep = QtGui.QMessageBox.question(self.CallingUI, Title, Message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)
        if rep == QtGui.QMessageBox.Yes:
            return 1
        elif rep == QtGui.QMessageBox.No:
            return 0
        elif rep == QtGui.QMessageBox.Cancel:
            return -1

    def splitterMove(self,splitter,mainObj,mainObjsPercentage=65):
        '''
            Must be used inside showEvent(self,eve)
        '''

        if splitter.orientation()==2:
            val = mainObjsPercentage * mainObj.height()/100
        else:
            val = mainObjsPercentage * mainObj.width()/100

        splitter.moveSplitter(val, splitter.indexOf(mainObj))

    def underConstruction(self,Info='This feature is still under construction.'):
        self.showInformationBox('Sorry!',Info)


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
        Rmnu = QtGui.QMenu(self.CallingUI)
        for i, itm in enumerate(menuListString):

            newmenuitem = QtGui.QAction(itm, self.CallingUI)

            if len(itm)>1 and itm[0]=='|':
                itm = itm[1:len(itm)]
                newmenuitem.setEnabled(False)
                newmenuitem.setText(itm)

            if itm != '':
                if len(iconList)>1 and len(iconList)>i:
                    if iconList[i]<>None:
                        icon = QtGui.QIcon()
                        icon.addPixmap(QtGui.QPixmap(iconList[i]), QtGui.QIcon.Normal, QtGui.QIcon.On)
                        newmenuitem.setIcon(icon)

            self.CallingUI.connect(newmenuitem, QtCore.SIGNAL("triggered()"), lambda passarg=(itm,i,additionalArguments,newmenuitem): funcToInvoke(passarg))

            if itm=='':
                Rmnu.addSeparator()
            else:
                Rmnu.addAction(newmenuitem)


        PopupPoint.setY(PopupPoint.y() + 30)
        PopupPoint.setX(PopupPoint.x() + 5)
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

        Rmnu =  QtGui.QMenu(CallingUI)

        Rmnu.setTearOffEnabled(False)

        for cnt, eachItem in enumerate(listOfItem):
            if type(eachItem)==type([]):
                Menu = self.menuCreator(eachItem[1:], CallingUI, AdditionalArgument, FunctionToInvoke, cnt, Level+1)
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

                newmenuitem = QtGui.QAction(Label, CallingUI)
                if len(eachItem)>1 and Label[0]=='|':
                    Label = Label[1:len(Label)]
                    newmenuitem.setEnabled(False)
                    newmenuitem.setText(Label)

                if IconPath:
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(IconPath), QtGui.QIcon.Normal, QtGui.QIcon.On)
                    newmenuitem.setIcon(icon)

                CallingUI.connect(newmenuitem, QtCore.SIGNAL("triggered()"), lambda passarg=(Label,Level,ParentID,cnt,AdditionalArgument,newmenuitem): FunctionToInvoke(passarg))

                if Label=='':
                    Rmnu.addSeparator()

                else:
                    Rmnu.addAction(newmenuitem)
        return Rmnu

    def getDataTime(self,format = "%Y-%m-%d %H:%M:%S"):
        """
        "%Y-%m-%d %H:%M:%S"
        """
        return strftime(format)

##    def getSplDataTime(self, format = "%Y-%m-%d %H:%M:%S", Year=0,Month=0,Date=0,Hour=0,Min=0,Sec=0):
##        """
##        "%Y-%m-%d %H:%M:%S"
##        """
##        import datetime
##        sp_year = int(strftime('%y')) if not Year else Year
##        sp_month = int(strftime('%m')) if not Month else Month
##        sp_date = int(strftime('%d'))  if not Date else Date
##        sp_hour = int(strftime('%H')) if not Hour else Hour
##        sp_min = int(strftime('%M')) if not Min else Min
##        sp_sec = int(strftime('%S')) if not Sec else Sec
##        timetuple = datetime.datetime(sp_year,sp_month,sp_date,sp_hour,sp_min,sp_sec).timetuple()
##        return strftime(format,timetuple)


    def getSplDataTime(self, format = "%Y-%m-%d %H:%M:%S", Year=0,Month=0,Date=0,Hour=0,Min=0,Sec=0):
        """
        "%Y-%m-%d %H:%M:%S"
        """
        import datetime
        sp_year = int(strftime('%y'))+Year
        sp_month = int(strftime('%m'))+(Month if int(strftime('%m'))+Month>=12 else (int(strftime('%m'))+Month)-12)
        sp_date = int(strftime('%d'))+(Date if int(strftime('%d'))+Date>=30 else (int(strftime('%d'))+Date)-30)
        sp_hour = int(strftime('%H'))+(Hour if int(strftime('%H'))+Hour>=12 else (int(strftime('%H'))+Hour)-12)
        sp_min = int(strftime('%M'))+(Min if int(strftime('%M'))+Min>=59 else (int(strftime('%M'))+Min)-59)
        sp_sec = int(strftime('%S'))+(Sec if int(strftime('%S'))+Sec>=59 else (int(strftime('%S'))+Sec)-59)

        sp_month =  sp_month * -1 if sp_month<0 else sp_month
        sp_date =  sp_date * -1 if sp_date<0 else sp_date
        sp_month =  sp_month * -1 if sp_month<0 else sp_month
        sp_hour =  sp_hour * -1 if sp_hour<0 else sp_hour
        sp_min =  sp_min * -1 if sp_min<0 else sp_min
        sp_sec =  sp_sec * -1 if sp_sec<0 else sp_sec

        timetuple = datetime.datetime(sp_year,sp_month,sp_date,sp_hour,sp_min,sp_sec).timetuple()
        return strftime(format,timetuple)

    def statusMessage(self, message='Ready!'):
        self.CallingUI.statusbar.showMessage(str(message),0)


