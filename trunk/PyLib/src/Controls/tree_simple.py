from PyQt4 import QtCore, QtGui
from Controls import qt_common

class TreeSimple():
    """
        Tree Supporting Class
    """

    def __init__(self,uiMainObj):
        self.CallingUI = uiMainObj
        self.uiComman = qt_common.PyQtAppSupport(uiMainObj)
        self.widget = QtGui.QTreeWidget()

    def getCollapseStates(self, widget):
        self.widget = widget
        itr = self.allItems(self.widget)
        states = {}
        for itm in itr:
            states[str(itm)] = itm.isExpanded()
        return states

    def setCollapseStates(self, widget, statesDct):
        self.widget = widget
        itr = self.allItems(self.widget)
        for itm in itr:
            itm.setExpanded(bool(statesDct[str(itm)]))

    def allItems(self, tree):
        return self.__treeAllItems(tree)

    def __treeNotHidden(self, Tree):
        items = QtGui.QTreeWidgetItemIterator(Tree, QtGui.QTreeWidgetItemIterator.NotHidden)
        return self.__treeIteratorList(items)

    def __treeAllItems(self, Tree):
        items = QtGui.QTreeWidgetItemIterator(Tree, QtGui.QTreeWidgetItemIterator.All)
        return self.__treeIteratorList(items)

    def __treeIteratorList(self, TreeIterator):
        TreeItems = []
        while TreeIterator.value():
            TreeItems.append(TreeIterator.value())
            TreeIterator+=1
        return TreeItems

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

        self.widget.header().setResizeMode(QtGui.QHeaderView.Fixed)
        self.widget.header().setMovable(0)

    def getItemAt(self, widget, point):
        self.widget = widget
        if point and type(point)==type(QtCore.QPoint()):
            item = self.widget.itemAt(point)
            if item and type(item)==type(QtGui.QTreeWidgetItem()):
                return item
        return None

    def editorOpen(self, treeItem, Col=1):
        tree = treeItem.treeWidget()
        tree.openPersistentEditor(treeItem, Col)

    def editorClose(self, treeItem, Col=1):
        tree = treeItem.treeWidget()
        tree.closePersistentEditor (treeItem, Col)

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
                childItem = self.addChildItem(self.widget, parentItem, str(eachChild), str(childDict[eachChild]))


    def populateTreeTable(self, widget, dataDictLst={}):

        '''
        DATA
             = {'CHARACTERS':
                            [{'QORAXX': [{'CLOTH': [{}, val1, val2, val3],
                                         'HAIR': [{},  val1, val2, val3],
                                         'MODEL': [{},  val1, val2, val3],
                                         'RIG': [{},  val1, val2, val3],
                                         'SHADE': [{},  val1, val2, val3],},
                                        0],
                             'SAMXXX': [{'CLOTH': [{},  val1, val2, val3],,
                                         'HAIR': [{},  val1, val2, val3],,
                                         'MODEL': [{},  val1, val2, val3],,
                                         'RIG': [{},  val1, val2, val3],,
                                         'SHADE': [{},  val1, val2, val3],},
                                        0],
                             'VORA': [{'CLOTH': [{},  val1, val2, val3],,
                                       'HAIR': [{},  val1, val2, val3],,
                                       'MODEL': [{},  val1, val2, val3],,
                                       'RIG': [{},  val1, val2, val3],,
                                       'SHADE': [{},  val1, val2, val3],},
                                      -1]}
                }

        '''

        self.widget = widget
        columnCount = self.widget.columnCount()
        for eachRoot in dataDictLst:
            if type(dataDictLst[eachRoot]) == type([]) and len(dataDictLst[eachRoot])>0:
                Columns = dataDictLst[eachRoot]
                MainColumn = Columns[0]
                OtherColumns =  Columns[1:]
                if MainColumn != {} :#May Extend more
                    newRoot = self.addRootItem(self.widget, str(eachRoot))
                    for cnt, eachColumn in enumerate(OtherColumns):
                        if columnCount>=cnt+1:
                            newRoot.setText(cnt+1, str(eachColumn))
                    self.subPopulateTreeChildren(self.widget, newRoot, MainColumn)
                else:
                    childItem = self.addRootItem(self.widget, str(eachRoot))
                    for cnt, eachColumn in enumerate(OtherColumns):
                        if columnCount>=cnt+1:
                            childItem.setText(cnt+1, str(eachColumn))

    def populateTreeTableChildren(self, widget, parentItem, childDict):

        self.widget = widget
        columnCount = self.widget.columnCount()
        for eachChild in childDict:
            if type(childDict[eachChild]) == type([]) and len(childDict[eachChild])>0:
                Columns = childDict[eachChild]
                MainColumn = Columns[0]
                OtherColumns =  Columns[1:]
                if MainColumn != {}: #May Extend more
                    newRoot = self.addChildItem(self.widget, parentItem, str(eachChild))
                    for cnt, eachColumn in enumerate(OtherColumns):
                        if columnCount>=cnt+1:
                            newRoot.setText(cnt+1, str(eachColumn))
                    self.populateTreeTableChildren(self.widget, newRoot, MainColumn)
                else: #Finish
                    childItem = self.addChildItem(self.widget, parentItem, str(eachChild))
                    for cnt, eachColumn in enumerate(OtherColumns):
                        if columnCount>=cnt+1:
                            childItem.setText(cnt+1, str(eachColumn))


    def removeAll(self,TreeName):
        for eachRoot in self.getRootItems(TreeName):
            inx = TreeName.indexOfTopLevelItem(eachRoot)
            TreeName.takeTopLevelItem(inx)

    def removeChildItem(self,ChildItem):
        ChildItem.parent().removeChild(ChildItem) if ChildItem and ChildItem.parent() else ''

    def removeRootItem(self,RootItem):
        tree = RootItem.treeWidget()
        inx = tree.indexOfTopLevelItem(RootItem)
        tree.takeTopLevelItem(inx)

    def setItemLabel(self,item,Label,Data='',Col=0):
        item.setText(Col, Label)
        item.setData(Col, QtCore.Qt.UserRole, QtCore.QVariant(str(Data)))

    def sortColumn(self, widget, order=1, Col=0):
        widget.sortItems(Col, QtCore.Qt.AscendingOrder) if order==1 else widget.sortItems(Col, QtCore.Qt.DescendingOrder)

    def setHiddenData(self,item, Data=None, CodeNumber=1, Col=0):
        item.setData(Col, 32 + int(CodeNumber), QtCore.QVariant(Data))

    def getHiddenData(self,item, CodeNumber=1, Col=0):
        return item.data(Col, 32 + int(CodeNumber)).toPyObject()

    def setAdditionalData(self,item, Data=None, CodeNumber=1, Col=0):
        item.setData(Col, 32 + int(CodeNumber), QtCore.QVariant(Data))

    def getAdditionalData(self,item, CodeNumber=1, Col=0):
        '''
            Use following function to convert data
                .toString() - for getting back the string hidden
                .toPyObject() - for getting back the object hidden
        '''
        return item.data(Col, 32 + int(CodeNumber))

    def getItemLabel(self,item,Col=0):
        if item:
            return {'Label':str(item.text(Col)), 'Data':str(item.data(Col,QtCore.Qt.UserRole).toString()), 'Icon':item.icon(Col), 'Item':item}
        else:
            return {'Label':'', 'Data':'', 'Icon':'','Item':''}

    def getSelectedItem(self,TreeName, SingleSelection=1, col=0):
        #x = QtGui.QTreeWidget()
        sel = TreeName.selectedItems()

        if SingleSelection:
            if len(sel):
                item = sel[0]
                itemLabel = self.getItemLabel(item,col)['Label']
                itemData  = self.getItemLabel(item,col)['Data']
                return {'Item':item,'Label':itemLabel,'Data':itemData}
        else:
            if len(sel):
                lst = []
                for eachItem in sel:
                    item = eachItem
                    itemLabel = self.getItemLabel(item,col)['Label']
                    itemData  = self.getItemLabel(item,col)['Data']
                    lst.append({'Item':item,'Label':itemLabel,'Data':itemData})
                return lst

        return 0

    def getRootItems(self,TreeName):
        items = []
        for i in xrange(0,TreeName.topLevelItemCount()):
            item = TreeName.topLevelItem(i)
            items.append(item)
        return items

    def getRootItemFor(self, TreeName, Item):
        foundRoot = False
        while not foundRoot:
            miParent = Item.parent()
            if not isinstance(miParent,QtGui.QTreeWidgetItem):
                root = Item
                foundRoot = True
            else:
                Item = miParent
        return root

    def getLeafItemFor(self, TreeName, Item):
        #Item = QtGui.QTreeWidgetItem()
        if self.isGivenItemAChild(Item):
            return [Item]
        else:
            moreleafs = []
            for cnt in range(Item.childCount()):
                newChild = Item.child(cnt)
                newList = self.getLeafItemFor(TreeName, newChild)
                if newList: moreleafs = moreleafs + newList
            return moreleafs

    def getChildItems(self,Parent):
        items = []
        for i in xrange(0,Parent.childCount()):
            item = Parent.child(i)
            items.append(item)
        return items

    def createItem(self,Label,Data,Col=0):
        itm = QtGui.QTreeWidgetItem()
        self.setItemLabel(itm,Label,Data,Col)
        return itm

    def addRootItem(self,TreeName,Label,Data='',DataAsToolTip=1,Col=0):
        itm = QtGui.QTreeWidgetItem()
        self.setItemLabel(itm,Label,Data,Col)
        if DataAsToolTip:
            itm.setToolTip(0,str(Data))
        TreeName.addTopLevelItem(itm)
        return itm

    def addChildItem(self,TreeName,ParentItem,Label,Data='',Col=0,Icon=None):
        itm = QtGui.QTreeWidgetItem()
        font = QtGui.QFont()
        font.setBold(0)
        self.setItemLabel(itm,Label,Data,Col)
        ParentItem.addChild(itm)
        itm.setFont(Col,font)
        if Icon:
            itm.setIcon(Icon)
        return itm


    def formatItem(self,Item,Bold=0,Italics=0,Color=QtCore.Qt.red,Col=0):
        itm = QtGui.QTreeWidgetItem()
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

    def isGivenItemARoot(self,item):

        tree = item.treeWidget()
        if tree:
            for i in xrange(0,tree.topLevelItemCount()):

                rootItem = tree.topLevelItem(i)
                rootLabel = self.uiComman.getLabelNDataForTreeItem(rootItem)['Label']
                rootData = self.uiComman.getLabelNDataForTreeItem(rootItem)['Data']
                givenLabel = self.uiComman.getLabelNDataForTreeItem(item)['Label']
                givenData = self.uiComman.getLabelNDataForTreeItem(item)['Data']

                if (rootLabel == givenLabel) and (rootData==givenData):
                    return True

        return False

    def isChildExistInParent(self,Parent,Label='',Data=''):

        for i in xrange(0,Parent.childCount()):
            thisParentsChild = Parent.child(i)
            thisChildsLabel = str(self.uiComman.getLabelNDataForTreeItem(thisParentsChild)['Label'])
            thisChildsData = str(self.uiComman.getLabelNDataForTreeItem(thisParentsChild)['Data'])
            if thisChildsLabel == Label:
                #If some data is given and its not matching then return o
                if Data<>'' and thisChildsData<>Data:
                    return 0
                else:
                    return 1
        return 0


    def isRootExist(self,TreeName,Label='',Data=''):

        if TreeName.findItems(Label,QtCore.Qt.MatchExactly,0).__len__()>0:
            for i in xrange(0,TreeName.topLevelItemCount()):
                thisRoot = TreeName.topLevelItem(i)
                thisRootsLabel = self.uiComman.getLabelNDataForTreeItem(thisRoot)['Label']
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

    def findInChildren(self,ParentItem,Label=''):
        items = []
        for i in xrange(0,ParentItem.childCount()):
            thisParentsChild = ParentItem.child(i)
            thisChildsLabel = self.uiComman.getLabelNDataForTreeItem(thisParentsChild)['Label']
            if thisChildsLabel == Label:
                items.append(thisParentsChild)
        return items

    def findInRoots(self,TreeName,Label=''):
        items = []
        if TreeName.findItems(Label,QtCore.Qt.MatchExactly,0).__len__()>0:
            for eachFoundItem in TreeName.findItems(Label,QtCore.Qt.MatchExactly,0):
                items.append(eachFoundItem)
        return items

    def searchSelectLabelInTree(self,TreeName):

        self.treeOpenClose(TreeName,1)
        Search = str(self.uiComman.showInputBox('Search in the list','Enter the text to search in the list...'))

        founditems = []

        #Tre = QtGui.QTreeWidget()
        TreeName.expandAll

        item = TreeName.topLevelItem(0)
        while item:
            text = str(self.uiComman.getLabelNDataForTreeItem(item)['Label'])
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

    def findItemInTree(self, itemText, treeWidget) :
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

    def findInChildrenList(self,ParentItem,Label=''):
        items = []
        for i in xrange(0,ParentItem.childCount()):
            thisParentsChild = ParentItem.child(i)
            thisChildsLabel = self.uiComman.getLabelNDataForTreeItem(thisParentsChild)['Label']
            if thisChildsLabel == Label:
                items.append(thisParentsChild)
        return items


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



    def labelCount(self,treeName,Prefix='Total='):
        count = len(self.getRootItems(treeName))
        if count>0:
            treeName.headerItem().setText(0,str(Prefix) + ' (' + str(count) + ')')
        else:
            treeName.headerItem().setText(0,str(Prefix))


    def getAncestorsHierarchy(self,item,get='Label'):
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

    def getChildrenHierarchy(self, item, get='Label'):
        #item = QtGui.QTreeWidgetItem()
        #item.child
        ChildExist = True
        cPathItm = item
        HirItems = []
        HirItems.append(self.getItemLabel(item)[get])
        while(ChildExist):
            PathItm = self.getChildItems(cPathItm)
            ParentExist = True if len(PathItm) else False
            for eachChild in PathItm:
                if eachChild : HirItems.append(self.getItemLabel(eachChild)[get])
                cPathItm = self.getChildItems(eachChild)

        HirItems.reverse()
        return HirItems

    def getAllChildren(self, parent, get='Label', Children = [], includeParent = False, expandedOnly=False):
        child = self.getChildItems(parent)
        if includeParent:
            info = self.getItemLabel(parent)[get]
            Children.append(info)
        for each in child:
            childrenOfChildren = (self.getChildItems(each) if each.isExpanded() else []) if expandedOnly else self.getChildItems(each)
            if len(childrenOfChildren):
                Children = self.getAllChildren(each, get, Children, True, expandedOnly)
            else:
                info = self.getItemLabel(each)[get]
                Children.append(info)

        return Children



    def getAllItems(self, TreeName, CallBackFunction=None):

        rootList = self.getRootItems(TreeName)

        AllItems = []
        CurrentItems=[]
        for eachRoot in rootList:
            AllItems.append(eachRoot)
            rootItems = self.__getItems(eachRoot, CurrentItems, CallBackFunction=CallBackFunction)
            self.__appendToList(AllItems, rootItems)

        return AllItems


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