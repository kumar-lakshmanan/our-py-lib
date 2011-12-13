from PyQt4 import QtCore, QtGui

class oplQtConnection():

    def __init__(self, uiMain):
        self.uiMain = uiMain

    def connectToClick(self, widget, FunctionToInvoke):
        widget.__class__.mousePressEvent = lambda widget, event: widget.emit(QtCore.SIGNAL('mousePressEvent(QMouseEvent)'), event)
        self.uiMain.connect(widget, QtCore.SIGNAL('mousePressEvent(QMouseEvent)'), FunctionToInvoke)

    def connectToDragDrop(self, Widget, FunctionToInvoke):
        Widget.__class__.dropEvent = lambda Widget, event: Widget.emit(QtCore.SIGNAL('dropped(QDropEvent)'), event)
        self.uiMain.connect(Widget, QtCore.SIGNAL('dropped(QDropEvent)'), FunctionToInvoke)

    def connectToDragDropEx(self,Widget, FunctionToInvoke):
        Widget.setAcceptDrops(1)
        Widget.__class__.dragEnterEvent = self.__DragEnterEvent
        Widget.__class__.dragMoveEvent = self.__DragEnterEvent
        Widget.__class__.dropEvent = FunctionToInvoke

    def connectToClose(self, Widget, FunctionToInvoke):
        Widget.__class__.closeEvent = lambda Widget, event: Widget.emit(QtCore.SIGNAL('closed(QCloseEvent)'), event)
        Widget.connect(Widget, QtCore.SIGNAL('closed(QCloseEvent)'), FunctionToInvoke)

    def connectToMouseEnter(self, Widget, FunctionToInvoke):
        Widget.__class__.enterEvent = FunctionToInvoke
        Widget.connect(Widget, QtCore.SIGNAL('enterEvent(QEvent)'), FunctionToInvoke)

    def connectToMouseLeave(self, Widget, FunctionToInvoke):
        Widget.__class__.leaveEvent = FunctionToInvoke
        Widget.connect(Widget, QtCore.SIGNAL('leaveEvent(QEvent)'), FunctionToInvoke)

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
        self.uiMain.connect(Widget, QtCore.SIGNAL('customContextMenuRequested(QPoint)'), FunctionToInvoke)

    def enableRightClick(self, Widget):
        Widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def __DragEnterEvent(self, eve):
        eve.accept()

    def connectToTreeClose(self, Widget, FunctionToInvoke):
        self.uiMain.connect(Widget, QtCore.SIGNAL('itemCollapsed(QTreeWidgetItem*)'), FunctionToInvoke)

    def connectToTreeExpand(self, Widget, FunctionToInvoke):
        self.uiMain.connect(Widget, QtCore.SIGNAL('itemExpanded(QTreeWidgetItem*)'), FunctionToInvoke)

    def dropEventInfoEx(self, event):
        files=[]
        if event.mimeData().hasUrls() == True:
            urllist = event.mimeData().urls()
            for url in urllist:
                files.append(
                        str(QtCore.QDir.toNativeSeparators(str(url.toLocalFile()))))
        return files

    def dropEventInfo(self, event, accept=True):
        if accept: event.accept()
        destiWidget = self.uiMain.sender()
        sourceWidget = event.source()
        destiItems = destiWidget.itemAt(event.pos())
        sourceItems = sourceWidget.selectedItems()
        return {'DestiWidget':destiWidget,'SourceWidget':sourceWidget,'DestiItems':destiItems,'SourceItems':sourceItems, 'Event': event}

    def keyEventInfo(self, event):
        if event.key() == QtCore.Qt.Key_Enter:
            return 'Enter'
        if event.key() == QtCore.Qt.Key_Delete:
            return 'Delete'
        else:
            return event.key()