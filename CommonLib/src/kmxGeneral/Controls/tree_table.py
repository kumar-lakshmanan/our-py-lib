from PyQt4 import QtCore, QtGui
from controls import qt_common

class TreeTable():
    """
        Tree Supporting Class
    """

    def __init__(self,uiMainObj):
        self.CallingUI = uiMainObj
        self.uiComman = qt_common.PyQtAppSupport(uiMainObj)
        self.widgetItem = QtGui.QTreeWidgetItem()

    def initalDesign(self, widget, columnList, extraCol=1):

        self.widget = widget
        self.widget.clear()
        self.widget.setColumnCount(len(columnList)+extraCol)

        for c, eachItem in enumerate(columnList):
            self.widget.headerItem().setText(c,eachItem)

        for eachExtraCol in xrange(len(columnList),len(columnList)+extraCol):
            self.widget.headerItem().setText(eachExtraCol,'')


    #Todo Merge functions
    def format(self, widget, alternateRowColor=1 ):
        self.widget = widget
        self.widget.setAlternatingRowColors(alternateRowColor)

    def formatTree(self, widget, sortingEnabled=0, selectionMode=1, editable=0, alternateRowColor=1):
        self.widget = widget

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
        self.widget.setSortingEnabled(sortingEnabled)
        self.widget.setAlternatingRowColors(alternateRowColor)
        if not editable: self.widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.widget.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.widget.header().setMovable(1)

    def getItemAt(self, widget, point):
        self.widget = widget
        if point and type(point)==type(QtCore.QPoint()):
            item = self.widget.itemAt(point)
            if item and type(item)==type(QtGui.QTreeWidgetItem()):
                return item
        return None

    def populateTree(self, widget, dataDict={}, append=0):

        self.widget = widget
        if not append:
            self.removeAll(widget)
        for eachRoot in dataDict:
            if type(dataDict[eachRoot]) == type({}):
                newRoot = self.addRootItem(self.widget, str(eachRoot))
                self.populateTreeChildren(self.widget, newRoot, dataDict[eachRoot])
            else:
                childItem = self.addRootItem(self.widget, str(eachRoot))

    def populateTreeChildren(self, widget, parentItem, childDict):

        self.widget = widget
        for eachChild in childDict:
            if type(childDict[eachChild]) == type({}):
                newRoot = self.addChildItem(self.widget, parentItem, str(eachChild))
                self.populateTreeChildren(self.widget, newRoot, childDict[eachChild])
            else:
                childItem = self.addChildItem(self.widget, parentItem, str(eachChild))

    def removeAll(self,TreeName):
        for eachRoot in self.getRootItems(TreeName):
            inx = TreeName.indexOfTopLevelItem(eachRoot)
            TreeName.takeTopLevelItem(inx)

    def removeChildItem(self,ChildItem):
        ChildItem.parent().removeChild(ChildItem)

    def removeRootItem(self,RootItem):
        tree = RootItem.treeWidget()
        inx = tree.indexOfTopLevelItem(RootItem)
        tree.takeTopLevelItem(inx)

    def setItemLabel(self,item,Label,Data='',Col=0):
        item.setText(Col, Label)
        item.setData(Col, QtCore.Qt.UserRole, QtCore.QVariant(str(Data)))

    def setAdditionalData(self,item, Data='', CodeNumber=33, Col=0):
        item.setData(Col, int(CodeNumber), QtCore.QVariant(Data))

    def getAdditionalData(self,item, CodeNumber=33, Col=0):
        return item.data(Col, int(CodeNumber))

    def getItemLabel(self,item, Col=0):
        return {'Label':item.text(Col), 'Data':item.data(Col,QtCore.Qt.UserRole).toString(), 'Icon':item.icon(Col)}

    def getSelectedItem(self,TreeName, SingleSelection=1):
        #x = QtGui.QTreeWidget()
        sel = TreeName.selectedItems()

        if SingleSelection:
            if len(sel):
                item = sel[0]
                itemLabel = self.getItemLabel(item)['Label']
                itemData  = self.getItemLabel(item)['Data']
                return {'Item':item,'Label':itemLabel,'Data':itemData}
        else:
            if len(sel):
                lst = []
                for eachItem in sel:
                    item = eachItem
                    itemLabel = self.getItemLabel(item)['Label']
                    itemData  = self.getItemLabel(item)['Data']
                    lst.append({'Item':item,'Label':itemLabel,'Data':itemData})
                return lst

        return 0

    def getRootItems(self,TreeName):
        items = []
        for i in xrange(0,TreeName.topLevelItemCount()):
            item = TreeName.topLevelItem(i)
            items.append(item)
        return items

    def getChildItems(self,Parent):
        items = []
        for i in xrange(0,Parent.childCount()):
            item = Parent.child(i)
            items.append(item)
        return items

    def addRootItem(self,TreeName,Label,Data='',DataAsToolTip=1,Col=0):
        itm = QtGui.QTreeWidgetItem()
        self.setItemLabel(itm,Label,Data,Col)
        if DataAsToolTip:
            itm.setToolTip(Col,str(Data))
        TreeName.addTopLevelItem(itm)
        return itm

    def addRootItemAt(self,TreeName,Index,Label,Data='',DataAsToolTip=1,Col=0):
        itm = QtGui.QTreeWidgetItem()
        self.setItemLabel(itm,str(Label),str(Data),Col)
        if DataAsToolTip:
            itm.setToolTip(Col,str(Data))
        TreeName.insertTopLevelItem(Index,itm)
        return itm


    def addRootItems(self,TreeName,Label=[],Data=[],DataAsToolTip=1):
        itm = QtGui.QTreeWidgetItem()

        for Col, eachLabel in enumerate(Label):
            self.setItemLabel(itm, eachLabel, Data[Col] if len(Data)>Col else '', Col)
            if DataAsToolTip:
                itm.setToolTip(Col,str(Data))

        TreeName.addTopLevelItem(itm)
        return itm

    def createItem(self, Label, Data='', Col=0):
        itm = QtGui.QTreeWidgetItem()
        self.setItemLabel(itm,Label,Data,Col)
        return itm

    def addChildItem(self,TreeName,ParentItem,Label,Data='',Icon=None,Col=0):
        itm = QtGui.QTreeWidgetItem()
        font = QtGui.QFont()
        font.setBold(0)
        self.setItemLabel(itm,Label,Data,Col)
        ParentItem.addChild(itm)
        itm.setFont(Col,font)
        if Icon:
            itm.setIcon(Icon)
        return itm

    def addChildItems(self,TreeName,ParentItem,Label=[],Data=[],Icon=None):
        itm = QtGui.QTreeWidgetItem()
        font = QtGui.QFont()
        font.setBold(0)
        for Col, eachLabel in enumerate(Label):
            self.setItemLabel(itm,eachLabel,Data,Col)
            itm.setFont(Col,font)
            if Icon:
                itm.setIcon(Icon)
        ParentItem.addChild(itm)
        return itm

    def formatItem(self,Item, Bold=0,Italics=0, Color=QtCore.Qt.red, Col=0):

        font = QtGui.QFont()
        font.setBold(Bold)
        font.setItalic(Italics)
        Item.setTextColor(Col,Color)
        Item.setFont(Col,font)

    def isGivenItemAChild(self,item):
        #To Guess whtr given item is one level child... Its Parent's type must be TreeWidItem Class and It Should not have any childs
        if str(type(item.parent()))=="<class 'PyQt4.QtGui.QTreeWidgetItem'>" and item.childCount()==0:
            return True
        else:
            return False

    def isGivenItemARoot(self,item,Col=0):
        #TODO: MUST SEARCH ON OTHER COLUMNS TOO
        tree = item.treeWidget()
        if tree:
            for i in xrange(0,tree.topLevelItemCount()):

                rootItem = tree.topLevelItem(i)
                rootLabel = self.uiComman.getLabelNDataForTreeItem(rootItem,Col)['Label']
                rootData = self.uiComman.getLabelNDataForTreeItem(rootItem,Col)['Data']
                givenLabel = self.uiComman.getLabelNDataForTreeItem(item,Col)['Label']
                givenData = self.uiComman.getLabelNDataForTreeItem(item,Col)['Data']

                if (rootLabel == givenLabel) and (rootData==givenData):
                    return True

        return False

    def isChildExistInParent(self,Parent,Label='',Data='',Col=0):
        for i in xrange(0,Parent.childCount()):
            thisParentsChild = Parent.child(i)
            thisChildsLabel = self.uiComman.getLabelNDataForTreeItem(thisParentsChild,Col)['Label']
            thisChildsData = self.uiComman.getLabelNDataForTreeItem(thisParentsChild,Col)['Data']
            if thisChildsLabel == Label:
                #If some data is given and its not matching then return o
                if Data<>'' and thisChildsData<>Data:
                    return 0
                else:
                    return 1
        return 0


    def isRootExist(self,TreeName,Label='',Data='',Col=0):

        if TreeName.findItems(Label,QtCore.Qt.MatchExactly,0).__len__()>0:
            for i in xrange(0,TreeName.topLevelItemCount()):
                thisRoot = TreeName.topLevelItem(i)
                thisRootsLabel = self.uiComman.getLabelNDataForTreeItem(thisRoot,Col)['Label']
                if thisRootsLabel == Label:
                    #If some data is given and its not matching then return o
                    if Data<>'' and thisRootsData <> Data:
                        return 0
                    else:
                        return 1
        return 0

    def getItemLevelNo(self,item):
        c = 0
        nowParent = item.parent()
        while nowParent:
            nowParent = nowParent.parent()
            c+=1
        return c

    def findInChildren(self,ParentItem,Label='',Col=0):
        #TODO: MUST SEARCH OTHER COLUMNS TOO... SEARCHS ONLY SPECIFIED COL
        items = []
        for i in xrange(0,ParentItem.childCount()):
            thisParentsChild = ParentItem.child(i)
            thisChildsLabel = self.uiComman.getLabelNDataForTreeItem(thisParentsChild,Col)['Label']
            if thisChildsLabel == Label:
                items.append(thisParentsChild)
        return items

    def findInRoots(self,TreeName,Label=''):
        items = []
        if TreeName.findItems(Label,QtCore.Qt.MatchExactly,0).__len__()>0:
            for eachFoundItem in TreeName.findItems(Label,QtCore.Qt.MatchExactly,0):
                items.append(eachFoundItem)
        return items

    def searchSelectLabelInTree(self,TreeName,Col=0):
        #TODO: Must search all columns
        self.treeOpenClose(TreeName,1)
        Search = str(self.uiComman.showInputBox('Search in the list','Enter the text to search in the list...'))

        founditems = []

        #Tre = QtGui.QTreeWidget()
        TreeName.expandAll

        item = TreeName.topLevelItem(0)
        while item:
            text = str(self.uiComman.getLabelNDataForTreeItem(item,Col)['Label'])
            if text.find(Search)>=0:
                founditems.append(item)
            item = TreeName.itemBelow(item)

        for eachitem in founditems:
            eachitem.setSelected(1)

        if founditems.__len__()==0:
            self.uiComman.showInformationBox('Not found','Search text not found in the list, Try with some partial characters.')

    def treeOpenClose(self,TreeName,Expand=1):
        if Expand:
            TreeName.expandAll()
        else:
            TreeName.collapseAll()



    def selectItem(self, widget, itemList=[], pointList=[],clearPrevious=1):

        self.widget = widget
        if clearPrevious:
            self.widget.clearSelection()

        if pointList:
            if type(pointList) == type([]):
                for eachPoint in pointList:
                    self.widget.setCurrentItem(self.widget.itemAt(eachPoint))
                    self.widget.setItemSelected(self.widget.itemAt(eachPoint),1)
            else:
                self.widget.setCurrentItem(self.widget.itemAt(pointList))
                self.widget.setItemSelected(self.widget.itemAt(pointList),1)

        if itemList:
            if type(itemList) == type([]):
                for eachItem in itemList:
                    self.widget.setCurrentItem(eachItem)
                    self.widget.setItemSelected(eachItem,1)
            else:
                self.widget.setCurrentItem(itemList)
                self.widget.setItemSelected(itemList,1)

    def findItemInTree(itemText, treeWidget) :
        rootList = self.getRootItems(treeWidget);
        returnList = []
        for i in range(len(rootList)) :
            childList = [rootList[i]]; i = 0
            while i < len(childList) :
                itemList = self.findInChildrenList(childList[i], itemText)
                if len(itemList) :
                    returnList.extend(itemList)
                childList.extend(self.getChildItems(childList[i]))
                i += 1
        return returnList


    def resizeColumns(self,treeName):

        colCount = treeName.columnCount()
        tableWidth = treeName.width()
        colOldWidths = []
        percentColOldWidth = []
        colNewWidths = []
        totalColOldWidth = 0

        for colNo in xrange(0,colCount):
            treeName.resizeColumnToContents(colNo)

##        for colNo in xrange(0,colCount):
##            vals = treeName.columnWidth(colNo)
##            colOldWidths.append(vals)
##            totalColOldWidth += vals
##
##        for oldWidth in colOldWidths:
##            val = oldWidth * 100.0 / totalColOldWidth
##            percentColOldWidth.append(val)
##
##        for c,eachpercentColWidth in enumerate(percentColOldWidth):
##            val = eachpercentColWidth * tableWidth / 100.0
##            colNewWidths.append(val)
##
##        for c,newWidth in enumerate(colNewWidths):
##            treeName.setColumnWidth(c,newWidth)
##

    def getHierarchyList(self,item,get='Label'):
        ParentExist = True
        PathItm = item
        HirItems = []
        HirItems.append(self.getItemLabel(item)[get])
        while(ParentExist):
            PathItm = PathItm.parent()
            ParentExist = True if PathItm else False
            if PathItm : HirItems.append(self.getItemLabel(PathItm)[get])
        HirItems.reverse()
        return HirItems


    def labelCount(self,treeName,Prefix='Total=',Col=0):
        count = len(self.getRootItems(treeName))
        if count>0:
            treeName.headerItem().setText(Col,str(Prefix) + ' (' + str(count) + ')')
        else:
            treeName.headerItem().setText(Col,str(Prefix))


    def getAllItems(self, TreeName, CallBackFunction=None):

        rootList = self.getRootItems(TreeName)

        AllItems = []
        CurrentItems=[]
        for eachRoot in rootList:
            AllItems.append(eachRoot)
            rootItems = self.__getItems(eachRoot, CurrentItems, CallBackFunction=CallBackFunction)
            self.__appendToList(AllItems, rootItems)

        return AllItems

    def editorOpen(self, treeItem, Col=1):
        tree = treeItem.treeWidget()
        tree.openPersistentEditor(treeItem, Col)

    def editorClose(self, treeItem, Col=1):
        tree = treeItem.treeWidget()
        tree.closePersistentEditor (treeItem, Col)

    def __getItems(self, Parent, CurrentItems=[], CallBackFunction=None):
        Childrens = self.getChildItems(Parent)
        if len(Childrens):
            for eachChild in Childrens:
                CurrentItems.append(eachChild)
                if CallBackFunction: CallBackFunction(eachChild)
                ChildItems = self.__getItems(eachChild, CurrentItems, CallBackFunction)
                self.__appendToList(CurrentItems, ChildItems)

        return CurrentItems


    def __appendToList(self, MainList=[], AdditionalList=[]):
        if MainList != AdditionalList:
            for eachAddition in AdditionalList:
                if eachAddition not in MainList:
                    MainList.append(eachAddition)


    def addHir(self, destiWidget, destiItem, sourceWidget, sourceItemList):
        self.widget = destiWidget
        for eachSourceItem in sourceItemList:
            Label = str(self.getItemLabel(eachSourceItem)['Label'])
            Data = str(self.getItemLabel(eachSourceItem)['Data'])
            if not destiItem:
                newroot = self.addRootItem(self.widget, Label, Data)
                destiItem = newroot
            else:
                destiItem = self.addChildItem(self.widget, destiItem, Label, Data)

            newchildrens = self.getChildItems(eachSourceItem)
            if len(newchildrens):
                self.__addHir(self.widget, destiItem, newchildrens)

    def __addHir(self, widget, parent, childrens):
        self.widget = widget
        for eachChild in childrens:
            Label = str(self.getItemLabel(eachChild)['Label'])
            Data = str(self.getItemLabel(eachChild)['Data'])
            newparent = self.addChildItem(self.widget, parent, Label, Data)
            newchildrens = self.getChildItems(eachChild)
            if len(newchildrens):
                self.__addHir(self.widget, newparent, newchildrens)
