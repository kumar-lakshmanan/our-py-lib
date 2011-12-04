from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from functools import partial
import ConfigParser
from time import strftime
import pickle
import subprocess
import popen2

import os, sys, datetime, time, re, getpass, csv


def getUsername():
        return os.environ.get('USERNAME');

def errorReport(prittyPrint=1):
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


def resizeColumns(tableName):

    tableName.resizeColumnsToContents()

    colCount = tableName.columnCount()
    tableWidth = tableName.width()
    colOldWidths = []
    percentColOldWidth = []
    colNewWidths = []
    totalColOldWidth = 0

    for colNo in xrange(0,colCount):
        vals = tableName.columnWidth(colNo)
        colOldWidths.append(vals)
        totalColOldWidth += vals

    for oldWidth in colOldWidths:
        val = oldWidth * 100.0 / totalColOldWidth
        percentColOldWidth.append(val)

    for c,eachpercentColWidth in enumerate(percentColOldWidth):
        val = eachpercentColWidth * tableWidth / 100.0
        colNewWidths.append(val)

    for c,newWidth in enumerate(colNewWidths):
        tableName.setColumnWidth(c,newWidth)
    tableName.setColumnWidth(c, newWidth-2)

def newschk(forwho,newsfilepath):

    showpopup = str(INIReadValue(newsfilepath,"news","showpopup",False))

    if showpopup=="Yes":
        newsdata = str(INIReadValue(newsfilepath,"news","newsdata",False))
        from ui_news import Ui_Dialog
        uiobj = DialogWindow(Ui_Dialog,forwho,True)
        putString(uiobj[0].textBrowser,newsdata)


def trayagent(forwho,trayclickedfunction):

    """
    trayagent(forwho,trayclickedfunction)

    catch the trayobj i trhough...
    Dont forget to kill your object on Close Event
    use...
    xtools.traykiller()

    """

    tray = QSystemTrayIcon(forwho.windowIcon(), forwho)
    forwho.connect(tray,SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),trayclickedfunction)
    tray.show()
    return tray


def traymessage(tray, messagetitle, message):
    tray.showMessage(messagetitle,message)

def traykiller(tray):
    tray.hide()
    del(tray)


def timeragent(forwho,timeoutfunction,interval):

    """
    timeragentforwho,timeoutfunction,interval)

    catch the timeragent i trhough...
    Dont forget to kill your object on Close Event
    use...
    xtools.timerkiller()

    """

    timerx = QtCore.QTimer()
    timerx.setInterval(interval)
    timerx.stop()

    forwho.connect(timerx,SIGNAL("timeout()"),timeoutfunction)
    return timerx


def timerkiller(timer):
    timer.stop()
    del(timer)


def INIGetSection(inifile, optionValDict) :

    if not os.path.exists(inifile):
        print 'File does not exist'
        return []
    if not len(optionValDict.keys()) :
        print 'No option declared'
        return []
    if not len(optionValDict.values()) :
        print 'No value to match'
        return []

    optionList = optionValDict.keys()
    config = ConfigParser.RawConfigParser()
    config.read(inifile)
    sectionList = config.sections(); parseSection = []
    for section in sectionList :
        addSection = 1
        for option in optionList :
            if not config.has_option(section, option) :
                addSection = 0
                break
        if addSection :
            parseSection.append(section)

    returnList = []
    for section in parseSection :
        addSection = 1
        for option in optionList :
            val = optionValDict[option]
            sectVal = config.get(section, option)
            if not val.upper() == sectVal.upper() :
                addSection = 0
                break
        if addSection :
            returnList.append(section)

    return returnList


def INISetValue(inifile,section,option,value):

    """
    INISetValue(inifile,section,option,value):
    """

    if not os.path.exists(inifile):
        f = open(inifile,"a")
        f.write("")
        f.close()

    if os.path.exists(inifile):
        config = ConfigParser.RawConfigParser()
        config.read(inifile)

        if not config.has_section(section):
            config.add_section(section)
            config.set(section,option,value)
        else:
            config.set(section,option,value)

        configfile = open(inifile, "w")
        config.write(configfile)


def INIReadValue(inifile,section,option,createDefault=False,defaultValue=""):

    """
    INIReadValue(inifile,section,option,createDefault=False,defaultValue=""):
    """


    r = defaultValue

    if os.path.exists(inifile):

        config = ConfigParser.RawConfigParser()
        config.read(inifile)

        if config.has_section(section):
            if config.has_option(section,option):
                r = str(config.get(section,option))
            else:
                if createDefault:
                    INISetValue(inifile,section,option,defaultValue)
        else:
            if createDefault:
                INISetValue(inifile,section,option,defaultValue)

    else:
            if createDefault:
                INISetValue(inifile,section,option,defaultValue)



    return r



def inputDialog(forwho, windowtitle='Input Required!',message='Please Input Some Information: ',default=''):
    """
        inputDialog window

    """
    comments, ok = QInputDialog.getText(forwho, forwho.tr(windowtitle), forwho.tr(message), QLineEdit.Normal, default)
    if ok and not comments.isEmpty():
        return comments
    else:
        return ''

def updaterchk(forwho,latestversionexe):


        """
        Update finder...

        eg:
            xtools.updaterchk(self,"LBR3.exe")

            creates a toolset.ini file near your main executer.
            this contains file link which will be checked for updated version of the same file! If its updated EXE then new UpDATER.bat
            will be created to copy files from folder specified.

        """


        exename = latestversionexe
        updaterfilename = "Updater.bat"

        latestversionexe = INIReadValue("toolset.ini","VersionCheck","latestexepath",True,latestversionexe)

        updatedexe = QDir.convertSeparators(latestversionexe)

        if os.path.exists(updatedexe):

            x = os.stat(updatedexe).st_mtime
            SourceFileTime = time.ctime(x).__str__()

            x = os.stat(sys.argv[0]).st_mtime
            ThisFileTime = time.ctime(x).__str__()
            print "Update Checking.."
            if SourceFileTime != ThisFileTime:
                print "New Update available"

                sourcefile = QtCore.QFileInfo(updatedexe)
                sourcepath = QDir.convertSeparators(sourcefile.path() + QDir.separator () )

                currentfile=QtCore.QFileInfo(sys.argv[0])
                nf=QDir.toNativeSeparators (currentfile.path() + QDir.separator () + updaterfilename)
                fx=open(nf, 'w')
##                k = "taskkill /f /im " + exename + "\n"
##                fx.write(k)
                fx.write("xcopy " + sourcepath + "* /c/e/f/y")
                fx.close()

                messagebox(forwho,"New Update available","It Seems to be your software update is ready! \nTake time and update it. Use Update.bat provided for that! Now you will be running your old version. Close it and update it!")

        else:
            print "Source file not found!"



def stylefiller(parent,skincontrol=None,colorcontrol=None):

    skincontrol.addItems(QtGui.QStyleFactory.keys())
    mycolors = ["Default","Green","Gray","Red","Blue"]
    colorcontrol.addItems(mycolors)
    QtCore.QObject.connect(skincontrol, QtCore.SIGNAL("currentIndexChanged(QString)"), partial(styleapply, parent, skincontrol, colorcontrol))
    QtCore.QObject.connect(colorcontrol, QtCore.SIGNAL("currentIndexChanged(QString)"), partial(styleapply, parent, skincontrol, colorcontrol))

def stylefillerList(parent,skincontrol=None,colorcontrol=None):

    skincontrol.addItems(QtGui.QStyleFactory.keys())
    QtCore.QObject.connect(skincontrol, QtCore.SIGNAL("clicked(QModelIndex)"), partial(styleapply, parent, skincontrol, colorcontrol))
    mycolors = ["Default","Green","Gray","Red","Blue"]
    colorcontrol.addItems(mycolors)
    QtCore.QObject.connect(colorcontrol, QtCore.SIGNAL("clicked(QModelIndex)"), partial(styleapply, parent, skincontrol, colorcontrol))

def styleapply(*args):
    pass

##def styleapply(*args):
##        uis = QtUiSupport.uiCommanCls(0)
##        style = uis.getLabel(args[1])
##        color = uis.getLabel(args[2])
##        if style:
##            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(style))
##            QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
##        if color:
##            applycolors(args[0],color)


def appstyle(whom, stylename = 'Plastique',stylecolor = 'Default'):

    """
                xtools.appstyle(self)
                FOR Changing the Style of your App to Plastique.


                xtools.appstyle(self,'Cleanlooks')
                xtools.appstyle(self,'CDE')
                xtools.appstyle(self,'Windows')

                use this for your different style.



        for iz in QtGui.QStyleFactory.keys():
            print iz

        use above to see all available styles

    """

##        for iz in QtGui.QStyleFactory.keys():
##            print iz

    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(stylename))
    QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
    applycolors(whom,stylecolor)


def applycolors(towhom, color):

    towhom.setStyleSheet("")
    if color == "Green":
        towhom.setStyleSheet("QMainWindow{border-bottom-color: rgb(0, 0, 0);border-color: rgb(57, 105, 126);background-color: qlineargradient(spread:pad, x1:0.505682, y1:0, x2:0.528, y2:1, stop:0 rgba(195, 216, 179, 255), stop:1 rgba(182, 182, 182, 255));}")
    if color == "Gray":
        towhom.setStyleSheet("QMainWindow{background-color: qlineargradient(spread:pad, x1:0.505682, y1:0, x2:0.528, y2:1, stop:0 rgba(216, 216, 216, 255), stop:1 rgba(182, 182, 182, 255));}")
    if color == "Red":
        towhom.setStyleSheet("QMainWindow{background-color: qlineargradient(spread:pad, x1:0.511545, y1:1, x2:0.517, y2:0, stop:0 rgba(216, 169, 169, 255), stop:1 rgba(180, 180, 180, 255));}")
    if color == "Blue":
        towhom.setStyleSheet("QMainWindow{background-color: qlineargradient(spread:pad, x1:0.505682, y1:0, x2:0.528, y2:1, stop:0 rgba(182, 192, 216, 255), stop:1 rgba(185, 185, 185, 255));}")



def saveUIWindowSettings(forwho,companyname,applicationname):

    """
    Saves the  UI Mainwindow and dock settings to registry. And you Restore settings back them!

    """


    QB = QtCore.QByteArray()
    QB = forwho.saveState()

    QS = QtCore.QSettings(companyname,applicationname)
    QS.beginGroup("Win")
    QS.setValue("size",QtCore.QVariant(forwho.size()))
    QS.setValue("pos",QtCore.QVariant(forwho.pos()))
    QS.endGroup()

    QS.beginGroup("All")
    QS.setValue("allstate",QtCore.QVariant(QB))
    QS.endGroup()



def restorUIWindowSettings(forwho,companyname,applicationname):

    QS = QtCore.QSettings(companyname,applicationname)

    QS.beginGroup("Win")
    val = QS.value("size").toSize()
    QS.endGroup()

    if val.height()>-1 and val.width()>-1:
        restore = True
    else:
        restore = False


    if restore:
        QS.beginGroup("All")
        QQ = QtCore.QByteArray()
        QQ = QS.value("allstate").toByteArray()
        forwho.restoreState(QQ)
        QS.endGroup()

        QS.beginGroup("Win")
        forwho.resize(QS.value("size").toSize())
        forwho.move(QS.value("pos").toPoint())
        QS.endGroup()






def saveUISettingAsPreset(fowho,presetfile):

    qb = fowho.saveState()
    winsiz = fowho.size()
    winpos = fowho.pos()
    lst = [qb,winsiz,winpos]
    f=open(presetfile, 'w')
    pickle.dump(lst,f)
    f.close()


def restoreUISettingAsPreset(fowho,presetfile):

    if os.path.exists(presetfile):

        f=open(presetfile, 'r')
        lst = pickle.load(f)
        f.close()

        qb = lst[0]
        winsiz = lst[1]
        winpos = lst[2]

        fowho.restoreState(qb)

        fowho.resize(winsiz)
        fowho.move(winpos)

















def findInArray(array,findtext):

    for its in array:
        if str(its) == str(findtext):
            return True
    return False



def arrayunique(v):
    inarray = v
    for i in xrange(0,inarray.__len__()):
        for j in xrange(i+1,inarray.__len__()):
            if (inarray[i].upper()==inarray[j].upper()):
                inarray.remove(inarray[j])
                i = 0
                j = 0
                break

    return inarray




def unique(v):



    """Return a list of the elements in s, but without duplicates.

    For example, unique([1,2,3,1,2,3]) is some permutation of [1,2,3],
    unique("abcabc") some permutation of ["a", "b", "c"], and
    unique(([1, 2], [2, 3], [1, 2])) some permutation of
    [[2, 3], [1, 2]].

    For best speed, all sequence elements should be hashable.  Then
    unique() will usually work in linear time.

    If not possible, the sequence elements should enjoy a total
    ordering, and if list(s).sort() doesn't raise TypeError it's
    assumed that they do enjoy a total ordering.  Then unique() will
    usually work in O(N*log2(N)) time.

    If that's not possible either, the sequence elements must support
    equality-testing.  Then unique() will usually work in quadratic
    time.
    """

    nstr = "-,-".join(v)
    capsstr = nstr.upper()
    s = capsstr.split("-,-")


    n = len(s)
    if n == 0:
        return []

    # Try using a dict first, as that's the fastest and will usually
    # work.  If it doesn't work, it will usually fail quickly, so it
    # usually doesn't cost much to *try* it.  It requires that all the
    # sequence elements be hashable, and support equality comparison.
    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()

    # We can't hash all the elements.  Second fastest is to sort,
    # which brings the equal elements together; then duplicates are
    # easy to weed out in a single pass.
    # NOTE:  Python's list.sort() was designed to be efficient in the
    # presence of many duplicate elements.  This isn't true of all
    # sort functions in all languages or libraries, so this approach
    # is more effective in Python than it may be elsewhere.
    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]

    # Brute force is all that's left.
    u = []
    for x in s:
        if x not in u:
            u.append(x)


    nstr = "-,-".join(u)
    capsstr = nstr.capitalize()
    x = capsstr.split("-,-")

    return x




def messagebox(towhom,title,message):
    QtGui.QMessageBox.information(towhom, title, message)

def askyesno(towhom,title,message):
    rep = QtGui.QMessageBox.question(towhom, title, message, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    if rep == QtGui.QMessageBox.Yes:
        return 1
    else:
        return 0

def nowuser():
    return getpass.getuser()

def rightClickMenu(controlparent,control,qp,menuarray,rightclickfunction,added_arg):

    """
    controlparent - where the control is placed, usaully self
    control - Into which menu will be generated
    qp - QPoint where menu should popout
    menuarray - Array of menu items
    rightclickfunction - Function to be invoked on menu item clicked
    added_arg - argument to that function

        Inside rightclickfunction() you will receive a tuple with three items
        1 - Menu Label
        2 - Menu Label Index
        3 - added_arg

        eg:
        myutils().rightclickmenus(self,self.textEdit,qp,["KUMAR","TEST"],self.funs,["myarg1","myarg2"])

        def funs(self,t)
                print "Label Clicked is: " + str(t[0])
                print "Label Index is: " + str(t[1])
                print "Added Argument: " + str(t[2])

    """
    if menuarray == []:
        return 0;
    Rmnu = QtGui.QMenu(controlparent)
    for i, itm in enumerate(menuarray):
        newmenuitem = QtGui.QAction(itm, controlparent)
        controlparent.connect(newmenuitem, QtCore.SIGNAL("triggered()"), lambda passarg=(itm,i,added_arg): rightclickfunction(passarg))
        Rmnu.addAction(newmenuitem)

    qp.setY(qp.y() + 0)
    qp.setX(qp.x() + 0)
    Rmnu.exec_(control.mapToGlobal(qp))
    del(Rmnu)


def popUpMenu(callingClassObject,menuRequestingtObject,PopupPoint,menuListString,funcToInvoke,additionalArguments='',iconList = []):

    """
    callingClassObject - where the menuRequestingtObject is placed, usaully self
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
    Rmnu = QtGui.QMenu(callingClassObject)
    for i, itm in enumerate(menuListString):

        newmenuitem = QtGui.QAction(itm, callingClassObject)

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

        callingClassObject.connect(newmenuitem, QtCore.SIGNAL("triggered()"), lambda passarg=(itm,i,additionalArguments,newmenuitem): funcToInvoke(passarg))

        if itm=='':
            Rmnu.addSeparator()
        else:
            Rmnu.addAction(newmenuitem)


    PopupPoint.setY(PopupPoint.y() + 30)
    PopupPoint.setX(PopupPoint.x() + 5)
    Rmnu.exec_(menuRequestingtObject.mapToGlobal(PopupPoint))
    del(Rmnu)




def updateString(olddata,newdata,concater):

    """
    Want to update a string on various options

            thingstoupdate = self.updateString(thingstoupdate,"Status=\""+x+"\""," , ")
    """

    if olddata=="":
        return str(newdata)
    else:
        return str(olddata + concater + newdata)


def smart_bool(s):
    if s is True or s is False:
        return s
    s = str(s).strip().lower()
    return not s in ['false','f','n','0','']

def now( format="yyyy-MM-dd hh:mm:ss", mdate = QtCore.QDateTime.currentDateTime()):
    """
        yyyy-MM-dd hh:mm:ss
    """
    xx=QtGui.QDateTimeEdit(mdate)
    xx.setDisplayFormat(format)
    return xx.text()

def nowdatetime(format = "%Y-%m-%d %H:%M:%S"):
    """
    "%Y-%m-%d %H:%M:%S"
    """
    return strftime(format)











#UI Features


def DialogWindow(UIClass, Parent,Model=True):

    """
        Open new window.... Give me ui class name and parent whom to attach
        returns the [NEW UI Element Collection, WindowHandle]
        -Model is used to set window with First Priority to Close

        eg:

            from AddNewClientUI import Ui_AddNewClientDialog
            cr_ui = xtools.DialogWindow(Ui_AddNewClientDialog,self,True)

            self.connect(cr_ui[0].pushButton_2, QtCore.SIGNAL("clicked()"),lambda passarg=cr_ui: self.fn_addnewclient(passarg))
            self.connect(cr_ui[0].pushButton, QtCore.SIGNAL("clicked()"), lambda passarg=cr_ui: self.fn_addnewclientClose(passarg))



    def fn_addnewclient(self,arg):
        print arg


    def fn_addnewclientClose(self,arg):
        print arg


    """

    Die = QDialog(Parent)
    MyUI = UIClass()
    MyUI.setupUi(Die)
    Die.setModal(Model)
    Die.show()
    return [MyUI,Die]









def treefindInChildList(ParentItem,Label='',MatchExact=1):

    items = []
    for i in xrange(0,ParentItem.childCount()):
        thisParentsChild = ParentItem.child(i)
        thisChildsLabel = getLabelNDataForTreeItem(thisParentsChild)['Label']
        if MatchExact:
            if thisChildsLabel == Label:
                items.append(thisParentsChild)
        else:
            if thisChildsLabel.find(Label)>=0:
                items.append(thisParentsChild)

    return items

def treefindInRootList(TreeName,Label=''):
    items = []
    if TreeName.findItems(Label,QtCore.Qt.MatchExactly,0).__len__()>0:
        for eachFoundItem in TreeName.findItems(Label,QtCore.Qt.MatchExactly,0):
            items.append(eachFoundItem)
    return items


def getLabelNDataForListItem(listItem):
    return {'Label':listItem.text(), 'Data':listItem.data(QtCore.Qt.UserRole).toString()}

def getLabelNDataForTreeItem(treeItem=''):
    if treeItem :
        return {'Label':treeItem.text(0), 'Data':treeItem.data(0,QtCore.Qt.UserRole).toString()}

def getLabelNDataForTableItem(tableItem):
    return {'Label':tableItem.text(), 'Data':tableItem.data(QtCore.Qt.UserRole).toString()}

def getListItemForData(listBox,data):
    for i in xrange(0,listBox.count()):
        if listBox.item(i).data(QtCore.Qt.UserRole).toString() == str(data):
            return listBox.item(i)

def treeGetRootItems(TreeName):
    items = []
    for i in xrange(0,TreeName.topLevelItemCount()):
        item = TreeName.topLevelItem(i)
        items.append(item)
    return items

def treeGetChildItems(Parent):
    items = []
    for i in xrange(0,Parent.childCount()):
        item = Parent.child(i)
        items.append(item)
    return items

def findItemInTree(itemText, treeWidget) :
    rootList = treeGetRootItems(treeWidget); returnList = []
    for i in range(len(rootList)) :
        if str(rootList[i].text(0)) == itemText :
            returnList.append(rootList[i])
        childList = [rootList[i]]; i = 0
        while i < len(childList) :
            itemList = treefindInChildList(childList[i], itemText)
            if len(itemList) :
                returnList.extend(itemList)

            childList.extend(treeGetChildItems(childList[i]))
            i += 1
    return returnList

def getLeafNodes(item, treeWidget) :
    childList = [item]; returnList = []; i = 0
    while i < len(childList) :
        childCount = childList[i].childCount()
        if not childCount :
            returnList.append(childList[i])
        else :
            for j in range(childCount) :
                childList.append(childList[i].child(j))
        i += 1
    return returnList


def arrayIsTextExist(array,findtext,ExactMatch=True):

    if ExactMatch:
        for its in array:
            if str(its) == str(findtext):
                return True
        return False
    else:
        for its in array:
            if str(its).find(findtext)>-1:
                return True
        return False


def osNetworkMapping(driveLetter='Z',mappingPath='D:\\',userName='',passWord=''):

    if os.path.exists(driveLetter+":"):
        if not osNetworkMappingIsMapped(driveLetter,mappingPath):
            osNetworkMappingDisconnect(driveLetter)
        else:
            print "Drive already mapped!"
            return ["Drive already mapped!",1]

    s='net use'

    if userName=='':
        print '!!DirectMounting!!'
        s = 'net use ' + str(driveLetter) + ': "' + str(mappingPath) + '"'

    if userName!='' and passWord=='':
        s = 'net use ' + str(driveLetter) + ': "' + str(mappingPath) + '" ' + '/USER:' + str(userName)

    if userName!='' and passWord!='':
        s = 'net use ' + str(driveLetter) + ': "' + str(mappingPath) + '" ' + str(passWord) + ' /USER:' + str(userName)

    print "Mapping drive..."
    #print "Win Command: " + s
    #z = subprocess.Popen(s,shell=False)
    launchConsole(s)

    if os.path.exists(driveLetter+":"):
        print "Drive mapped successfully!"
        result = 1
    else:
        print "Drive not mapped!"
        result = 0

    return [s,result]

def osNetworkMappingDisconnect(driveLetter='Z'):


    s='net use ' + driveLetter + ': /delete /Y'

    print "Disconnecting map drive..."
    #print "Win Command: " + s
##    info = subprocess.STARTUPINFO()
##    info.wShowWindow = subprocess.SW_HIDE
##    z = subprocess.Popen(s,shell=False,startupinfo=info)
    launchConsole(s)

    if os.path.exists(driveLetter+":"):
        print "Drive not yet disconnected!"
        result = 0
    else:
        print "Drive disconnected!"
        result = 1

    return [s,result]

def isRunningFromNetwork():
    (r,w) = popen2.popen2('net use')

    result = r.readlines()
    r.close()
    w.close()

    return False if len(result)>0 else True

def osNetworkMappingIsMapped(driveLetter='Z',mappedPath='D:\\'):

    mappedPath = os.path.normpath(mappedPath)
    (r,w) = popen2.popen2('net use')

    result = r.readlines()
    r.close()
    w.close()

    for eachLine in result:
        if str(driveLetter+':') in eachLine and str(mappedPath) in eachLine:
            return True

    return False


def launchConsole(command,args=''):

    ##launchConsole('d:\\myeexe\\deghg.exe',['-d','gg'])

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    return subprocess.Popen(command+' '+args,shell=False,startupinfo=startupinfo).wait()

def formattedDateTime(TimeToFormat, SourceFormat='%Y-%m-%d %H:%M:%S', DestiFormat='%b %d, %I:%M %p'):
    dobj = datetime.datetime.strptime(str(TimeToFormat),SourceFormat)
    return (str(dobj.strftime('%b %d, %I:%M %p')))