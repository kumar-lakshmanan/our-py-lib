#-------------------------------------------------------------------------------
# Name:        QtTable
# Purpose:
#
# Author:      AIAA
#
# Created:     10-11-2011
# Copyright:   (c) AIAA 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
import sip

class oplQtTable():

    """
        Following functions are ment for handling Qt Table Component.
    """

    def __init__(self,uiMain):
        self.uiMain = uiMain
        self.widget = QtGui.QTableWidget()  #Dummy Object to get properties of
                                            # table component.


    def initializing(self, widget, columnNames, extraCol=1):

        self.widget = widget
        self.widget.clear()
        self.widget.setColumnCount(len(columnNames)+extraCol)
        for c in xrange(0,len(columnNames)+extraCol):
            self.widget.setHorizontalHeaderItem(c,QtGui.QTableWidgetItem())

        for c, eachItem in enumerate(columnNames):
            self.widget.horizontalHeaderItem(c).setText(str(eachItem))

        for eachExtraCol in xrange(len(columnNames),len(columnNames)+extraCol):
            self.widget.horizontalHeaderItem(eachExtraCol).setText('')

    def formatting(self, widget,
                          vertHeadHide=1,
                          horzHeadHide=0,
                          hHeadHeight=10,
                          sortingEnabled=0,
                          alternateRowColor=1,
                          grid=1,
                          selectMode=1,
                          resizeMode=0,
                          editable=0,
                          cornerButton=0 ):

        self.widget = widget
        if vertHeadHide: self.widget.verticalHeader().hide()
        if horzHeadHide: self.widget.horizontalHeader().hide()

        if not selectMode:
            self.widget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        elif selectMode==1:
            self.widget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        elif selectMode==2:
            self.widget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        elif selectMode==3:
            self.widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        elif selectMode==4:
            self.widget.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)

        self.widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.headFormatting(self.widget,resizeMode)
        self.widget.setSortingEnabled(sortingEnabled)
        self.widget.setAlternatingRowColors(alternateRowColor)
        self.widget.setShowGrid(grid)
        self.widget.setCornerButtonEnabled(cornerButton)
        if not editable:
            self.widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)


    def clear(self, widget):
        self.widget = widget
        self.widget.blockSignals(1)
        self.widget.clearContents()
        self.widget.setRowCount(0)
        self.widget.blockSignals(0)

    def headFormatting(self,widget,Mode=0):

        self.widget = widget
        self.widget.prResizeMode = Mode
        if Mode==0:
            self.widget.resizeColumnsToContents()
            self.widget.horizontalHeader().setStretchLastSection(True)

        if Mode==1:
            self.widget.resizeColumnsToContents()
            self.widget.horizontalHeader().setResizeMode(
                                            QtGui.QHeaderView.Interactive)

        if Mode==2:
            self.widget.horizontalHeader().setResizeMode(
                                            QtGui.QHeaderView.Stretch)


    def resizeColumns(self,table,rule=[]):

        table.resizeColumnsToContents()

        colCount = table.columnCount()
        tableWidth = table.width()
        colOldWidths = []
        percentColOldWidth = []
        colNewWidths = []
        totalColOldWidth = 0

        for colNo in xrange(0,colCount):
            vals = table.columnWidth(colNo)
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
                table.setColumnWidth(c,newWidth-1)
        elif len(rule):
            for c,newWidth in enumerate(colNewWidths):
                if not c in rule:
                    table.setColumnWidth(c,newWidth-1)

        table.setColumnWidth(colCount,newWidth-3)

    def createItem(self,Text='',Data=''):
        itm = QtGui.QTableWidgetItem()
        itm.setText(str(Text))
        itm.setData(QtCore.Qt.UserRole,QtCore.QVariant(str(Data)))
        return itm

    def addRow(self, widget,
                     rowData=[],
                     append=0,
                     rowHeight=15,
                     insertAtFirst=False,
                     allowEmpty=False):
        self.widget = widget
        if not append: self.clearTable(self.widget)
        sortingVal = self.widget.isSortingEnabled()
        self.widget.blockSignals(1)
        self.widget.setSortingEnabled(0)
        newRowNo = 0 if insertAtFirst else self.widget.rowCount()
        self.widget.insertRow(newRowNo)
        rowItems = []
        for col in xrange(0,len(rowData)):
            txt = rowData[col] if len(rowData)>col else ''
            if txt or allowEmpty:
                txt,data = (txt[0],txt[1]) if type(txt)==type(()) else (txt,'')
                if type(data)==type(()):
                    item = self.createItem(str(txt),str(len(data)))
                    for i in xrange(len(data)):
                        self.setAdditionalData(item,data[i])
                else:
                    item = self.createItem(str(txt),data)
                self.widget.setItem(newRowNo, col, item)
                rowItems.append(item)
        if rowHeight:
            self.widget.setRowHeight(newRowNo,rowHeight)

        self.widget.blockSignals(0)
        self.widget.setSortingEnabled(sortingVal)
        return rowItems

    def removeRow(self, widget, rowNo):
        self.widget.removeRow(rowNo)


    def findRow(self, widget, textTofind, returnFirstFound = True, searchInColumnNos=[]):
        self.widget = widget

        returnLst = []
        for eachCol in xrange(0,self.widget.columnCount()):
            if eachCol in (searchInColumnNos if searchInColumnNos else [eachCol]):
                for eachRow in xrange(0,self.widget.rowCount()):
                    item = self.widget.item(eachRow,eachCol)
                    txt = self.getItemText(item)['Text']
                    if txt.upper() == textTofind.upper():
                        returnLst.append(eachRow)
                        return returnLst
        return returnLst

    def selectRows(self, widget, rowNos=[], offset=0):
        widget.blockSignals(1)
        c = widget.columnCount()
        for row in rowNos:
            for col in xrange(0,c):
                item = widget.item(row+offset,col)
                item.setSelected(1) if item else None
        widget.blockSignals(0)

    def setItemText(self, item, Text='', Data=''):
        if Text:
            item.setText(str(Text))
        if Data:
            item.setData(QtCore.Qt.UserRole,QtCore.QVariant(str(Data)))

    def getItemText(self, item):
        return {
                'Text':str(item.text()),
                'Data':str(item.data(QtCore.Qt.UserRole).toString())
               }

    def setTag(self, item, tagName='tag', value=None):
        setattr(item, str(tagName), value)

    def getTag(self, item, tagName='tag'):
        tagName = str(tagName)
        if hasattr(item, tagName):
            return getattr(item, tagName)
        else:
            return None

    def setData(self, item, datas=[], spot=34):
        datas = list(datas)
        datas.insert(0,len(datas))
        for i,data in enumerate(datas):
            item.setData(spot + int(i), QtCore.QVariant(data))

    def getData(self, item, spot=34):
        length = item.data(spot).toInt()
        length = int(length[0]) if length[1] else 0
        data = []
        for i in xrange(length+1):
            data.append(str(item.data(spot + i).toString()))
        if data:
            data.remove(data[0])
        return data

    def getItemAt(self, widget, point):
        self.widget = widget
        if point and type(point)==type(QtCore.QPoint()):
            item = self.widget.itemAt(point)
            if item and type(item)==type(QtGui.QTableWidgetItem()):
                return item
        return None

    def getSelectedRowNo(self,widget):
        widget.blockSignals(1)
        rowCount = widget.rowCount(); returnList = []
        for i in range(rowCount) :
            if widget.item(i, 0).isSelected() :
                returnList.append(i)
        widget.blockSignals(0)
        return returnList

    def getSelectedItems(self,widget):
        widget.blockSignals(1)
        colCount = widget.columnCount();
        rowCount = widget.rowCount(); returnList = []
        for r in range(rowCount) :
            ColList = []
            for c in range(colCount-1) :
                if widget.item(r, c) and widget.item(r, c).isSelected() :
                    ColList.append(widget.item(r, c))
            if ColList:
                returnList.append(ColList)

        widget.blockSignals(0)
        return returnList

    def getItemsText(self, items, format='Text'):
        res = []
        if type(items)==type([]):
            for row in items:
                if type(row)==type([]):
                    r1 = []
                    for col in row:
                        txt = self.getItemText(col)[format]
                        r1.append(txt)
                    res.append(r1)
                else:
                    txt = self.getItemText(row)[format]
                    res.append(txt)
        return res

    def getHeaderColNo(self, table, headerText):
        for i in xrange(0,table.columnCount()):
            if table.horizontalHeaderItem(i).text() == str(Text):
                return int(i)
        return -1

    def getColHeader(self,table,colNo):
        return str(table.horizontalHeaderItem(int(colNo)).text())

    def isItemExist(self, item):
        return not sip.isdeleted(item)

    def isTextExist(self, table, string):
        if table.findItems(str(string), QtCore.Qt.MatchExactly).__len__()==0:
            return False
        else:
            return True

    def openPersEditor(self, item):
        self.widget = item.tableWidget()
        self.widget.openPersistentEditor(item)

    def closePersEditor(self, item):
        self.widget = item.tableWidget()
        self.widget.closePersistentEditor(item)

    def closeAllPersEditor(self,table):
        table.blockSignals(1)
        colCount = table.columnCount()
        rowCount = table.rowCount()
        for r in range(rowCount) :
            for c in range(colCount-1) :
                tableWidget.closePersistentEditor(table.item(r, c))
        table.blockSignals(0)

    def populateContent(self,
                            widget,
                            listOfList=[],
                            append=0,
                            rowHeight=15,
                            insertAtFirst=False,
                            progressBar=None):

        self.widget = widget
        if not append: self.clearTable(self.widget)
        sortingVal = self.widget.isSortingEnabled()
        self.widget.blockSignals(1)
        self.widget.setSortingEnabled(0)
        ret = []

        ttlRows = len(listOfList)
        if progressBar: progressBar.setMaximum(ttlRows)
        for row in xrange(0,ttlRows):
            newRowNo = 0 if insertAtFirst else self.widget.rowCount()
            self.widget.insertRow(newRowNo)
            rowItems = []

            for col in xrange(0,self.widget.columnCount()):
                txt =listOfList[row][col] if len(listOfList[row])>col else ''
                txt,data = (txt[0],txt[1]) if type(txt)==type(()) else (txt,'')
                item = self.createItem(txt,data)
                self.widget.setItem(newRowNo, col, item)
                rowItems.append(item)

            self.__progCallBack(progressBar, row, ttlRows)

            if rowHeight:
                self.widget.setRowHeight(newRowNo,rowHeight)
            ret.append(rowItems)

        self.widget.blockSignals(0)
        self.widget.setSortingEnabled(sortingVal)
        return ret

    def __progCallBack(self, progressBar, currentVal, totalVal):
        if not progressBar: return
        progressBar.setValue(currentVal)
        QtGui.QApplication.processEvents()

