from PyQt5 import QtCore, QtGui

class QtConnections():

    def __init__(self, uiMain):
        self.uiMain = uiMain

    def sigConnect(self, sigSender=None, signal='', FunctionToInvoke=None):
        if not sigSender is None and not signal is '' and not FunctionToInvoke is None:
            QtCore.QObject.connect(sigSender,QtCore.SIGNAL(signal),FunctionToInvoke)

    def connectDockAndAction(self, dock, action):
        if dock and action:
            self.sigConnect(action, "toggled(bool)",
                                    lambda vis, dck=dock,
                                           act=action:
                                           self._sigActToggle(vis,dck,act))
            self.sigConnect(dock, "visibilityChanged(bool)",
                                    lambda vis, dck=dock,
                                           act=action:
                                            self._sigDckVisibility(vis,dck,act))

    def _sigActToggle(self,*arg):
        dck = arg[1]
        act = arg[2]
        dck.blockSignals(1)
        act.blockSignals(1)
        dck.setVisible(act.isChecked())
        dck.blockSignals(0)
        act.blockSignals(0)

    def _sigDckVisibility(self,*arg):
        dck = arg[1]
        act = arg[2]
        dck.blockSignals(1)
        act.blockSignals(1)
        act.setChecked(dck.isVisible())
        dck.blockSignals(0)
        act.blockSignals(0)

    def connectToClick(self,Widget, FunctionToInvoke):
        Widget.clicked.connect(FunctionToInvoke)
        
    def connectToDblClick(self,Widget, FunctionToInvoke):
        Widget.doubleClicked.connect(FunctionToInvoke)
        
    def connectToDragDrop(self,Widget, FunctionToInvoke):
        Widget.setAcceptDrops(1)
        Widget.__class__.dragEnterEvent = self.__DragEnterEvent
        Widget.__class__.dragMoveEvent = self.__DragEnterEvent
        Widget.__class__.dropEvent = FunctionToInvoke

    def connectToClose(self, Widget, FunctionToInvoke):
        Widget.__class__.closeEvent = FunctionToInvoke
        #Widget.__class__.closeEvent = lambda Widget, event: Widget.emit(QtCore.SIGNAL('closed(QCloseEvent)'), event)
        #Widget.connect(Widget, QtCore.SIGNAL('closed(QCloseEvent)'), FunctionToInvoke)

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