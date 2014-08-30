from PyQt4 import QtCore, QtGui
from controls import qt_common

class ComboBox():
    """
        Tree Supporting Class
    """

    def __init__(self,uiMainObj):
        self.CallingUI = uiMainObj
        self.uiComman = qt_common.PyQtAppSupport(uiMainObj)
        self.widget = QtGui.QComboBox()

    def populateList(self, widget, listToAdd=[], append=0):

        self.widget = widget
        if not append: self.widget.clear()
        for each in listToAdd:
            self.addText(self.widget, each)

    def getAllText(self, widget):

        self.widget = widget
        items = []
        for inx in xrange(0, self.widget.count()-1):
            items.append(self.widget.itemText(inx))
        return items

    def addText(self, widget, Label='', Data='', Icon=''):

        self.widget = widget
        if Icon:
            self.widget.addItem(Icon, str(Label), QtCore.QVariant(str(Data)))
        else:
            self.widget.addItem(str(Label), QtCore.QVariant(str(Data)))

