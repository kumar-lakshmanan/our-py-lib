from PyQt4 import QtCore, QtGui

class DroppableListWidget(QtGui.QListWidget):

    def __init__(self, parent = None):
        QtGui.QListWidget.__init__(self)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        event.acceptProposedAction()


class DroppableTableWidget(QtGui.QTableWidget):

    def __init__(self, parent = None):
        QtGui.QTableWidget.__init__(self)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        event.acceptProposedAction()



class DroppableLineEdit(QtGui.QLineEdit):

    def __init__(self, parent = None):
        QtGui.QLineEdit.__init__(self)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        event.acceptProposedAction()


