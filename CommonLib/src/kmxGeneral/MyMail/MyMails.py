import sys
import os

##Remove cached custom modules from memory except preloaded IDE modules
if __name__ == '__main__':
    if globals().has_key('InitialModules'):
         for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
            del(sys.modules[CustomModule])
    else:
        InitialModules = sys.modules.keys()


#######Appending Module Search Path########
if __name__ == '__main__':
    currentFolder = os.getcwd()

####Adjust these Parent Folder to reach root folder####
    parentFolder1 = os.path.dirname(currentFolder)
    parentFolder2 = os.path.dirname(parentFolder1)

####Pass parentFolder Level to reach Root folder####
    rootFolder = os.path.dirname(parentFolder2)
    rootFolderParent = os.path.dirname(rootFolder)

####Module Pack folders that will be added to sys search path####
    modulePathList = [
                      rootFolder + '\lib',
                      rootFolder + '\lib\controls',
                      rootFolder + '\ui',
                      rootFolder + '\ui\common',
                      rootFolderParent  + '\UI_DB_lib'
                      'D:\REPO\SOURCE\SCRIPTS\PYTHON\PULSE_GREEN\lib\controls',
                     ]

    for modulePath in modulePathList:
        if modulePath not in sys.path:
            if os.path.exists(modulePath):
                sys.path.append(modulePath)


from PyQt4 import QtCore, QtGui
from MyMailUI import Ui_MainWindow
import emailLister
import table
import qt_common

class MainApplication(QtGui.QMainWindow, Ui_MainWindow):


    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.qtsTable = table.Table(self)
        self.qtsCommon = qt_common.PyQtAppSupport(self,'\\tECH\share\Kumaresan\LSAM_ICONS\ICONS')
        self.ur = 0
        self.tt = 0
        #self.connect(self.tableWidget,QtCore.SIGNAL('itemDoubleClicked(QTableWidgetItem*'),self.mailOpen)
        self.connect(self.tableWidget, QtCore.SIGNAL("itemDoubleClicked(QTableWidgetItem*)"), self.mailOpen)
        self.connect(self.toolButton, QtCore.SIGNAL("clicked()"), self.populate)
        self.populate()

    def mailOpen(self, mailItem):
        r = mailItem.row()
        item = self.tableWidget.item(r,3)
        state = str(self.qtsTable.getItemLabel(item)['Label'])
        url ='http://mail' + str(self.qtsTable.getAdditionalData(item).toString())
        html = ''.join(emailLister.urlData(url))
        self.textBrowser.setHtml(html)
        if state.find('UnRead')>=0:
            self.ur = self.ur - 1
            self.label.setText('Inbox ' + str(self.ur) + '/' + str(self.tt) + '...')

            for eachCol in xrange(0,self.tableWidget.columnCount()):
                item = self.tableWidget.item(r,eachCol)
                f = QtGui.QFont()
                f.setBold(0)
                item.setFont(f)

    def populate(self):
        login = 'lkumaresan'
        password = 'lkumaresan'

        lst = emailLister.listMails(login,password)
        mlst = [[str(mail[3]+'  '), mail[2], mail[0],'UnRead  ' if mail[1] else 'Read'] for mail in lst]
        mlst2 = [[str(mail[3]+'  '), mail[2], mail[0],'UnRead  ' if mail[1] else 'Read', mail[4]] for mail in lst]
        self.qtsTable.initalDesign(self.tableWidget,['Time','Sender','Mail','Status'])
        self.qtsTable.format(self.tableWidget,sortingEnabled=1)
        itms = self.qtsTable.populateTable(self.tableWidget,mlst,rowHeight=17)
        self.ur = 0
        self.tt = 0
        for row,eachRow in enumerate(mlst2):
            self.tt += 1
            if eachRow[3] == 'UnRead  ':
                self.ur += 1
                f = QtGui.QFont()
                f.setBold(1)
                itms[row][0].setFont(f)
                itms[row][1].setFont(f)
                itms[row][2].setFont(f)
                itms[row][3].setFont(f)
            self.qtsTable.setAdditionalData(itms[row][3],str(eachRow[4]))
        self.label.setText('Inbox ' + str(self.ur) + '/' + str(self.tt) + '...')

app = QtGui.QApplication(sys.argv)
ui = MainApplication()
ui.show()
sys.exit(app.exec_())
