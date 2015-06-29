from PyQt4 import QtCore, QtGui

class List():

    """
        List Supporting Class
    """

    def __init__(self,uiMainObj):
        self.CallingUI = uiMainObj
        self.widget = QtGui.QListWidget()
        self.item = QtGui.QListWidgetItem()


    def format(self, widget, alternateRowColor=1 ):

        self.widget = widget
        self.widget.setAlternatingRowColors(alternateRowColor)

    def getAllItem(self, widget):

        self.widget = widget
        items = []
        for inx in xrange(0, self.widget.count()):
            items.append(self.widget.item(inx))
        return items

    def getAllText(self, widget):

        self.widget = widget
        items = []
        for inx in xrange(0, self.widget.count()-1):
            item = self.widget.itemFromIndex(inx)
            items.append(self.getItemLabel(item)['Label'])
        return items


    def populateList(self, widget, listToAdd=[], append=0):
        self.widget = widget
        if not append: self.widget.clear()
        ret = []
        for each in listToAdd:
            if type(each)==type(()):
                item = self.addListItem(self.widget, str(each[0]),str(each[1]))
            else:
                item = self.addListItem(self.widget, str(each))
            ret.append(item)
        return ret

    def getItemAt(self, widget, point):
        self.widget = widget
        if point and type(point)==type(QtCore.QPoint()):
            item = self.widget.itemAt(point)
            if item and type(item)==type(QtGui.QListWidgetItem()):
                return item
        return None


    def getItemLabel(self,listItem,DataCode=32):
        return {'Label':str(listItem.text() if listItem else ''), 'Data':str(listItem.data(DataCode).toString() if listItem else '')}

    def isExist(self, listWidget, searchText, mode=1):
        result = listWidget.findItems(searchText,QtCore.Qt.MatchCaseSensitive)
        return True if result else False

    def addListItem(self,listBox,Label,Data='',DataCode=32,Checkable=False,CheckState=QtCore.Qt.Unchecked):

        itm = QtGui.QListWidgetItem()
        itm.setText(Label)
        itm.setData(DataCode,QtCore.QVariant(Data))
        if Checkable:
            itm.setCheckState(CheckState)
        listBox.addItem(itm)
        return itm

    def setAdditionalData(self, itm, roleCode=33, Data=''):
        itm.setData(roleCode,QtCore.QVariant(Data))

    def getAdditionalData(self, itm, roleCode=33):
        return itm.data(roleCode).toString()

    def clearSelections(self,listBox):
        for i in xrange(0,listBox.count()):
            listBox.setItemSelected(listBox.item(i),0)

    def getSelectedItem(self, widget):
        self.widget = widget
        return self.widget.selectedItems()

    def getSelectedItemLabel(self, widget, get='Label'):
        self.widget = widget
        if len(self.widget.selectedItems()):
            itm = self.widget.selectedItems()[0]
            return self.getItemLabel(itm)[get]

    def getItems(self, widget, label=''):
        self.widget = widget
        return self.widget.findItems(str(label),QtCore.Qt.MatchExactly)

    def selectItem(self, widget, itemList=[], pointList=[], clearPrevious=1):

        self.widget = widget

        if clearPrevious:
            self.clearSelections(widget)

        if itemList:
            if type(itemList) == type([]):
                for item in itemList:
                    self.widget.setItemSelected(item, 1)
                    self.widget.setCurrentItem(item)
            else:
                self.widget.setItemSelected(itemList, 1)
                self.widget.setCurrentItem(itemList)
        if pointList:
            if type(pointList) == type([]):
                for point in pointList:
                    self.widget.setItemSelected(self.getItemAt(self.widget, point) , 1)
                    self.widget.setCurrentItem(self.getItemAt(self.widget, point))
            else:
                self.widget.setItemSelected(self.getItemAt(self.widget, pointList), 1)
                self.widget.setCurrentItem(self.getItemAt(self.widget, pointList))

    def removeListItem(self,listBox, Label):

        lstOfItem = listBox.findItems(str(Label),QtCore.Qt.MatchExactly)
        if len(lstOfItem):
            row = listBox.row(lstOfItem[0])
            listBox.takeItem(row)