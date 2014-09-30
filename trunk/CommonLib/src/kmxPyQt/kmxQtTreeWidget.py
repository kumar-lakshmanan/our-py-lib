from PyQt5 import QtCore, QtGui, QtWidgets
import os

class TreeWidget(object):

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def createItem(self, Text='', Data=''):
        itm = QtWidgets.QTreeWidgetItem()
        itm.setText(0, str(Text))
        itm.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(str(Data)))
        return itm

    def getRootItems(self, Tree):
        # Tree = QtWidgets.QTreeWidget()
        items = []
        for i in range(0, Tree.topLevelItemCount()):
            item = Tree.topLevelItem(i)
            items.append(item)
        return items

    def addNewRoot(self, treeWidget, item):
        return treeWidget.addTopLevelItem(item)

    def getSelectedItem(self, TreeName, SingleSelection=1, col=0):
        # x = QtGui.QTreeWidget()
        sel = TreeName.selectedItems()

        if SingleSelection:
            if len(sel):
                item = sel[0]
                itemLabel = self.getItemLabel(item, col)['Label']
                itemData = self.getItemLabel(item, col)['Data']
                return {'Item':item, 'Label':itemLabel, 'Data':itemData}
        else:
            if len(sel):
                lst = []
                for eachItem in sel:
                    item = eachItem
                    itemLabel = self.getItemLabel(item, col)['Label']
                    itemData = self.getItemLabel(item, col)['Data']
                    lst.append({'Item':item, 'Label':itemLabel, 'Data':itemData})
                return lst

        return 0

    def getItemLabel(self, item, Col=0):
        if item:
            return {'Label':str(item.text(Col)), 'Data':str(item.data(Col, QtCore.Qt.UserRole)), 'Icon':item.icon(Col), 'Item':item}
        else:
            return {'Label':'', 'Data':'', 'Icon':'', 'Item':''}

