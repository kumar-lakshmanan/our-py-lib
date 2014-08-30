from PyQt4 import QtCore, QtGui

class CustomItemDelegate(QtGui.QStyledItemDelegate):
    '''

    Overridden Item Delegate (For TableWidget!)
    For providing table cell editing feature, Editing triggered on double clicking cells and editor is closed on editFinished!

    Input:
        parentTableWidget = TableWidget
        openFunciton = FunctionToInvokedBeforeOpeningEditor
        closeFunction = FunctionToInvokedBeforeClosingEditor

    Use:
        Create custom item delegate object with required arguments.
            1.parentTableWidget = TableWidget
            2.openFunciton = FunctionToInvokedBeforeOpeningEditor
            4.closeFunction = FunctionToInvokedBeforeClosingEditor

        these funcions will be invoked and three arguments will be passed to them... they are...
        - 1. Current CustomItemDelegateObj
        - 2. Table that is connected
        - 3. Table Item widget that is affected by the editor


        Editor will OPEN only if Current CustomItemDelegate Object's following flags are set to true

            i.e
            Function which is invoked before opening the editor should do this...
                CustomItemDelegateObj.editProceed = True


            Refer example!



    Eg:

    class myClass():


        def initalConnect(self)
            CustomItemDelegate(self.myTableWidget, self.openCellEditor, self.closeCellEditor)


        def openCellEditor(self, cid, tbl, itm):

            print 'Table: ', tbl
            print 'Cell Item: ', itm

            if self.myConditionForOpen:
                cid.editProceed = True
            else:
                cid.editProceed = False


        def closeCellEditor(self, cid, tbl, itm):

            print 'Table: ', tbl
            print 'Cell Item: ', itm


    '''



    def __init__(self, parentTableWidget, openFunction, closeFunction):
        QtGui.QStyledItemDelegate.__init__(self, parentTableWidget)
        self.tbl = parentTableWidget
        self.tbl.setItemDelegate(self)
        self.closeFunction = closeFunction
        self.openFunction = openFunction
        self.editProceed = False
        self.connect(self.tbl, QtCore.SIGNAL('itemDoubleClicked(QTableWidgetItem*)'), self.editorOpen)
        self.tbl.__class__.keyReleaseEvent = self.__keyPress

    def __keyPress(self, event):

        if event.key() == QtCore.Qt.Key_Tab or event.key() == QtCore.Qt.Key_Shift or event.key() == 16777218:
            event.ignore()
            self.tbl.setFocus()
            self.editorClose()
        else:
            event.accept()

    def editorOpen(self, *arg):
        self.openFunction(self, self.tbl, arg[0])
        if self.editProceed:
           self.tbl.editItem(arg[0])
           #self.tbl.openPersistentEditor(arg[0])

    def createEditor(self, *arg):
        self.editor = QtGui.QLineEdit(arg[0])
        self.mdl = arg[2]
        self.itm = self.tbl.itemFromIndex(self.mdl)
        self.connect(self.editor, QtCore.SIGNAL('editingFinished()'), self.editorClose)
        return self.editor

    def editorClose(self, *arg):
        if self.itm:
            try:
                self.itm.setText(self.editor.text())
                self.closeFunction(self, self.tbl, self.itm)
                self.editProceed = False
                del(self)
            except:
                print 'Invalid key action!'


class Override():
    '''
    over rides widget Signal and connect custom functions to it
    '''

    def __init__(self, CallingUI):
        self.CallingUI = CallingUI

    def genConnectToolButton(self, Widget, FunctionToInvoke):
        self.CallingUI.connect(Widget, QtCore.SIGNAL('triggered(bool)'), FunctionToInvoke)

    def connectToClick(self, widget, FunctionToInvoke):
        widget.__class__.mousePressEvent = lambda widget, event: widget.emit(QtCore.SIGNAL('mousePressEvent(QMouseEvent)'), event)
        self.CallingUI.connect(widget, QtCore.SIGNAL('mousePressEvent(QMouseEvent)'), FunctionToInvoke)

    def connectToDragDrop(self, Widget, FunctionToInvoke):
        Widget.__class__.dropEvent = lambda Widget, event: Widget.emit(QtCore.SIGNAL('dropped(QDropEvent)'), event)
        self.CallingUI.connect(Widget, QtCore.SIGNAL('dropped(QDropEvent)'), FunctionToInvoke)

    def connectToClose(self, Widget, FunctionToInvoke):
        Widget.__class__.closeEvent = lambda Widget, event: Widget.emit(QtCore.SIGNAL('closed(QCloseEvent)'), event)
        Widget.connect(Widget, QtCore.SIGNAL('closed(QCloseEvent)'), FunctionToInvoke)

    def connectToMouseEnter(self, Widget, FunctionToInvoke):
        Widget.__class__.enterEvent = FunctionToInvoke
        Widget.connect(Widget, QtCore.SIGNAL('enterEvent(QEvent)'), FunctionToInvoke)

    def connectToMouseLeave(self, Widget, FunctionToInvoke):
        Widget.__class__.leaveEvent = FunctionToInvoke
        Widget.connect(Widget, QtCore.SIGNAL('leaveEvent(QEvent)'), FunctionToInvoke)

    def connectToTableCellEditor(self, Widget, OpenFunction, CloseFunction):
        '''
        Please Refer CustomItemDelegate Class Info before using this function!
        '''
        return CustomItemDelegate(Widget, OpenFunction, CloseFunction)


    def connectToDropEvent(self,Widget, FunctionToInvoke):
        Widget.setAcceptDrops(1)
        Widget.__class__.dragEnterEvent = self.__DragEnterEvent
        Widget.__class__.dragMoveEvent = self.__DragEnterEvent
        Widget.__class__.dropEvent = FunctionToInvoke

    def connectToDropEventItems(self, Widget, FunctionToInvoke):
        Widget.__class__.dropEvent = FunctionToInvoke

    def connectToKeyPress(self, Widget, FunctionToInvoke):
        Widget.__class__.keyReleaseEvent = FunctionToInvoke

    def connectToFocusOut(self, Widget, FunctionToInvoke):
        Widget.__class__.focusOutEvent = FunctionToInvoke

    def connectToCloseEditor(self, Widget, FunctionToInvoke):
        Widget.__class__.closeEditor = FunctionToInvoke

    def connectToResize(self, Widget, FunctionToInvoke):
        Widget.__class__.resizeEvent = FunctionToInvoke

    def connectToRightClick(self, Widget, FunctionToInvoke):
        self.enableRightClick(Widget)
        self.CallingUI.connect(Widget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), FunctionToInvoke)

    def enableRightClick(self, Widget):
        Widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def __DragEnterEvent(self, eve):
        eve.accept()

    def connectToTreeClose(self, Widget, FunctionToInvoke):
        self.CallingUI.connect(Widget, QtCore.SIGNAL('itemCollapsed(QTreeWidgetItem*)'), FunctionToInvoke)

    def connectToTreeExpand(self, Widget, FunctionToInvoke):
        self.CallingUI.connect(Widget, QtCore.SIGNAL('itemExpanded(QTreeWidgetItem*)'), FunctionToInvoke)

    def dropEventInfo(self, event, accept=True):

        if accept: event.accept()

        destiWidget = self.CallingUI.sender()
        sourceWidget = event.source()
        destiItems = destiWidget.itemAt(event.pos())
        sourceItems = sourceWidget.selectedItems()
#        colno = destiItems.currentColumn() if type(destiWidget) == type(QtGui.QTreeWidget()) else -1

        return {'DestiWidget':destiWidget,'SourceWidget':sourceWidget,'DestiItems':destiItems,'SourceItems':sourceItems, 'Event': event}

    def keyEventInfo(self, event):
        if event.key() == QtCore.Qt.Key_Enter:
            return 'Enter'
        if event.key() == QtCore.Qt.Key_Delete:
            return 'Delete'
        else:
            return event.key()