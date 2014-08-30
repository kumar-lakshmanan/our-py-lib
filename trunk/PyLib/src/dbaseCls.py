#from pysqlite2 import dbapi2 as sqlite
import MySQLdb
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import xtools

class openDbase:

    connection=object
    cursor=object

    getQry = ""
    getHeadings = ""
    getGrid = ""

    pFilterstring = ""
    pSortstring = ""
    pBoldifyRow = 0
    pBoldifyRow_coltocheck = 0
    pBoldifyRow_colvalue = ""
    pColorizeColumns = 0

    __scrolvalHor = 0
    __scrolvalVal = 0

    __scrolRow = 0
    __scrolCol = 0



    def __init__(self,Database,IP="127.0.0.1",UserID="root",Password="root",PortID=3306):

        try:
            self.connection = MySQLdb.connect (host=IP, port=PortID, user=UserID, passwd=Password, db=Database)
            self.cursor = self.connection.cursor()

        except MySQLdb.Error, e:
            xtools.messagebox(None,"Problem COnnecting to Database...","Error %d: %s" % (e.args[0], e.args[1]))



    def doGridPopulate(self,grid,header,qry):

        self.__scrolvalVal = grid.verticalScrollBar().value()
        self.__scrolvalHor = grid.horizontalScrollBar().value()

        try:
            self.__scrolCol = grid.column(grid.selectedItems()[0])
            self.__scrolRow = grid.row(grid.selectedItems()[0])
        except :
            pass


        self.getGrid = grid
        self.getHeadings = header
        self.getQry = qry

        if self.pFilterstring!="":
            qry = qry + " WHERE " + self.pFilterstring

        if self.pSortstring!="":
            qry = qry + " ORDER BY " + self.pSortstring

        datas = self.doSelQuery(qry)

        self.__filGrid(grid,header,datas)


        grid.verticalScrollBar().setValue(self.__scrolvalVal)
        grid.horizontalScrollBar().setValue(self.__scrolvalHor)

        grid.selectRow(self.__scrolRow)
        grid.selectColumn(self.__scrolCol)

        grid.setFocus()

    def doGetCount(self,qry):
        v = 0
        v=self.doSelQuery(qry).__len__()
        return v

    def doExeQuery(self,qry):
        self.cursor.execute(str(qry))
        self.connection.commit()

    def doCloseMydb(self):
        try:
            self.cursor.close()
        except  AttributeError, x:
            print x


    def doSelQuery(self,qry):
        outp = []

        try:
            self.cursor.execute(qry)
            for s in self.cursor:
                outp.append(s)

        except MySQLdb.Error, e:
            print "\n" + qry
            print "Error %d: %s" % (e.args[0], e.args[1])
        except AttributeError, x:
            print x
            xtools.messagebox(None,"Network Problem","Please! Check your Network Connection.  This machine is unable to reach the Database. \nAsk your admin to check the connection with database machine.\nNow Launching the software interface without database!")



        return outp




    def __filGrid(self,xtable,headings,array):

            xtable.clearContents()
            xtable.setRowCount(array.__len__())

            xtable.setColumnCount(headings.__len__())
            for headno in xrange(0, headings.__len__()):
                item = QTableWidgetItem()
                xtable.setHorizontalHeaderItem(headno, item)
                xtable.horizontalHeaderItem(headno).setText(headings[headno])

            r = 0
            c = 0

            for row in array:
                c = 0

                #Row processor
                if str(row[self.pBoldifyRow_coltocheck]) == self.pBoldifyRow_colvalue:
                    rowbold = 1
                else:
                    rowbold = 0

                for col in xrange(0,row.__len__()):
                    newitem = QTableWidgetItem(str(row[col]))

                    if rowbold and self.pBoldifyRow:
                        f1 = QFont()
                        f1.setWeight(75)
                        newitem.setFont(f1)

                    if self.pColorizeColumns:
                        self.__CellColorize(str(row[col]), newitem)

                    xtable.setItem(r, c, newitem)
                    xtable.setRowHeight(r,17)
                    c = c + 1
                r = r + 1


            xtable.scrollToTop()
            xtable.scrollToBottom()
            xtable.scrollToTop()


    def __CellColorize(self, Data, Item):

        if Data == "Problem":
            Item.setBackgroundColor (QColor(0,0,0,255))
            Item.setTextColor(QColor(Qt.red))

        elif Data == "Cancel":
            Item.setBackgroundColor (QColor(100,100,100,80))
            Item.setTextColor(QColor(Qt.black))


        elif Data == "Ready":
            Item.setBackgroundColor (QColor(255,0,0,255))
            Item.setTextColor(QColor(Qt.yellow))

        elif Data == "Pause":
            Item.setBackgroundColor (QColor(255,0,255,50))
            Item.setTextColor(QColor(Qt.black))

        elif Data == "Hold":
            Item.setBackgroundColor (QColor(255,255,0,255))
            Item.setTextColor(QColor(Qt.red))

        elif Data == "Completed":
            Item.setBackgroundColor (QColor(0,255,0,255))
            Item.setTextColor(QColor(Qt.blue))

        elif Data == "InMuster":
            Item.setBackgroundColor (QColor(0,0,255,255))
            Item.setTextColor(QColor(Qt.yellow))

        elif Data == "Rendering":
            Item.setBackgroundColor (QColor(0,0,255,124))
            Item.setTextColor(QColor(Qt.yellow))

        else:
            Item.setBackgroundColor (QColor(Qt.white))
            Item.setTextColor(QColor(Qt.black))
