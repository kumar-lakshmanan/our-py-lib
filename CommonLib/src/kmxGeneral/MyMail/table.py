
from PyQt4 import QtCore, QtGui

class Table():
    """
        Table Supporting Class
    """

    def __init__(self,uiMainObj):
        self.CallingUI = uiMainObj
        self.widget = QtGui.QTableWidget()

    def getItemAt(self, widget, point):
        self.widget = widget
        if point and type(point)==type(QtCore.QPoint()):
            item = self.widget.itemAt(point)
            if item and type(item)==type(QtGui.QTableWidgetItem()):
                return item
        return None

    def format(self, widget, vHeadHide=1, hHeadHide=0, hHeadHeight=10, resizeMode=0, sortingEnabled=0, selectionMode=1, editable=0, alternateRowColor=1, grid=1, cornerButton=0):

        self.widget = widget
        if vHeadHide: self.widget.verticalHeader().hide()
        if hHeadHide: self.widget.horizontalHeader().hide()

        if not selectionMode:
            self.widget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        elif selectionMode==1:
            self.widget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        elif selectionMode==2:
            self.widget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        elif selectionMode==3:
            self.widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        elif selectionMode==4:
            self.widget.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)

        self.widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.setHeaderFormatting(self.widget,resizeMode)
        self.widget.setSortingEnabled(sortingEnabled)
        self.widget.setAlternatingRowColors(alternateRowColor)
        self.widget.setShowGrid(grid)
        self.widget.setCornerButtonEnabled(cornerButton)
        if not editable: self.widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)


    def editorOpen(self, item):
        self.widget = item.tableWidget()
        self.widget.openPersistentEditor(item)

    def editorClose(self, item):
        self.widget = item.tableWidget()
        self.widget.closePersistentEditor(item)

    def initalDesign(self, widget, columnList, extraCol=1):

        self.widget = widget
        self.widget.clear()
        self.widget.setColumnCount(len(columnList)+extraCol)
        for c in xrange(0,len(columnList)+extraCol):
            self.widget.setHorizontalHeaderItem(c,QtGui.QTableWidgetItem())

        for c, eachItem in enumerate(columnList):
            self.widget.horizontalHeaderItem(c).setText(eachItem)

        for eachExtraCol in xrange(len(columnList),len(columnList)+extraCol):
            self.widget.horizontalHeaderItem(eachExtraCol).setText('')

    def setAdditionalData(self,item, Data=None, CodeNumber=1):
        item.setData(32 + int(CodeNumber), QtCore.QVariant(Data))

    def getAdditionalData(self,item, CodeNumber=1):
        '''
            Use following function to convert data
                .toString() - for getting back the string hidden
                .toPyObject() - for getting back the object hidden
        '''
        return item.data(32 + int(CodeNumber))

    def clearTable(self, widget):
        self.widget = widget
        self.widget.setRowCount(0)

    def populateTable(self, widget, listOfList=[], append=0, rowHeight=15, insertAtFirst=False, autoResize=True):
        self.widget = widget
        if not append: self.clearTable(self.widget)
        newRowNo = 0 if insertAtFirst else self.widget.rowCount()
        sortingVal = self.widget.isSortingEnabled()
        self.widget.blockSignals(1)
        self.widget.setSortingEnabled(0)
        ret = []
        for row in xrange(0,len(listOfList)):
            self.widget.insertRow(newRowNo)
            rowItems = []
            for col in xrange(0,self.widget.columnCount()):
                label =listOfList[row][col] if len(listOfList[row])>col else ''
                item = self.createCellItem(label)
                self.widget.setItem(newRowNo, col, item)
                rowItems.append(item)
                if autoResize:
                    self.widget.resizeColumnsToContents()
                    if hasattr(self.widget, 'prResizeMode'):
                        self.setHeaderFormatting(self.widget, self.widget.prResizeMode)
            if rowHeight:
                self.widget.setRowHeight(newRowNo,rowHeight)
            ret.append(rowItems)
        self.widget.blockSignals(0)
        self.widget.setSortingEnabled(sortingVal)
        return ret

    def findRow(self, table, textTofind, returnFirstFound = True, searchInColumnNos=[]):
        self.widget = table

        returnLst = []
        for eachCol in xrange(0,self.widget.columnCount()):
            if eachCol in (searchInColumnNos if searchInColumnNos else [eachCol]):
                for eachRow in xrange(0,self.widget.rowCount()):
                    item = self.widget.item(eachRow,eachCol)
                    label = self.getItemLabel(item)['Label']
                    if label.upper() == textTofind.upper():
                        returnLst.append(eachRow)
                        return returnLst
        return returnLst


    def getSelections(self,tableItemList):
        selectedRows = []
        if len(tableItemList)>0:
            tableName = tableItemList[0].tableWidget()
            ttlcols = tableName.columnCount()

            while len(tableItemList):
                cols = []
                for cnt in xrange(0,ttlcols):
                    if len(tableItemList):
                        cols.append(tableItemList.pop(0))

                selectedRows.append(cols)

        return selectedRows



    def getSelectedTableRowNo(self,tableWidget):
        '''
        Return row numbers
        '''
        tableWidget.blockSignals(1)
        rowCount = tableWidget.rowCount(); returnList = []
        for i in range(rowCount) :
            if tableWidget.item(i, 0).isSelected() :
                returnList.append(i)
        tableWidget.blockSignals(0)
        return returnList

    def getSelectedTableRowItems(self,tableWidget):
        '''
        Return row numbers
        '''
        tableWidget.blockSignals(1)
        colCount = tableWidget.columnCount();
        rowCount = tableWidget.rowCount(); returnList = []
        for r in range(rowCount) :
            ColList = []
            for c in range(colCount-1) :
                if tableWidget.item(r, c).isSelected() :
                    ColList.append(tableWidget.item(r, c))
            if ColList:
                returnList.append(ColList)

        tableWidget.blockSignals(0)
        return returnList

    def clearTable(self, tableWidget):
#        tableWidget = QtGui.QTableWidget()
        self.widget = tableWidget
        self.widget.blockSignals(1)
        self.widget.clearContents()
        self.widget.setRowCount(0)
        self.widget.blockSignals(0)

    def selectRows(self,tableWidget,RowList):
#        tableWidget = QtGui.QTableWidget()
        tableWidget.blockSignals(1)
        c = tableWidget.columnCount()
        for eachRow in RowList:
            for eachCol in xrange(0,c):
                item = tableWidget.item(eachRow,eachCol)
                item.setSelected(1)
        tableWidget.blockSignals(0)

    def closeAllPersistEditor(self,tableWidget):
        tableWidget.blockSignals(1)
        colCount = tableWidget.columnCount()
        rowCount = tableWidget.rowCount()
        for r in range(rowCount) :
            for c in range(colCount-1) :
                tableWidget.closePersistentEditor(tableWidget.item(r, c))
        tableWidget.blockSignals(0)


    def getItemLabel(self,tableItem):
        #return {'Label':tableItem.text(), 'Data':tableItem.data(QtCore.Qt.UserRole).toString()}
        return {'Label':str(tableItem.text()), 'Data':str(tableItem.data(QtCore.Qt.UserRole).toString())}

    def getColumnNoForHeader(self,tableName,HeaderLabel):
        for i in xrange(0,tableName.columnCount()):
            if tableName.horizontalHeaderItem(i).text() == str(HeaderLabel):
                return int(i)
        return -1


    def getColumnNameForNo(self,tableName,columnNo):

        """
           returns column Name for the given column No in a table
        """
        return str(tableName.horizontalHeaderItem(int(columnNo)).text())


    def createCellItem(self,Label='',Data=''):
        itm = QtGui.QTableWidgetItem()
        itm.setText(str(Label))
        itm.setData(QtCore.Qt.UserRole,QtCore.QVariant(str(Data)))
        return itm

    def isExist(self,tableName,string):
        if tableName.findItems(str(string), QtCore.Qt.MatchExactly).__len__()==0:
            return False
        else:
            return True

    def setHeaderFormatting(self,widget,Mode=0):
        '''
            Mode
            0 = User Resize (Last Section Stretched)
            1 = User Resize (All Sections are free) - Default section size is rest
            2 = Auto Resize
        '''
        self.widget = widget
        self.widget.prResizeMode = Mode
        if Mode==0:
            self.widget.resizeColumnsToContents()
            self.widget.horizontalHeader().setStretchLastSection(True)

        if Mode==1:
            self.widget.resizeColumnsToContents()
            self.widget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Interactive)

        if Mode==2:
            self.widget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)





    def resizeColumns(self,tableName,rule=[]):

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

        if not len(rule):
            for c,newWidth in enumerate(colNewWidths):
                tableName.setColumnWidth(c,newWidth-1)
        elif len(rule):
            for c,newWidth in enumerate(colNewWidths):
                if not c in rule:
                    tableName.setColumnWidth(c,newWidth-1)

        tableName.setColumnWidth(colCount,newWidth-3)