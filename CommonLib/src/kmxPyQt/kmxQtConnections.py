from PyQt5 import QtCore, QtGui, QtWidgets

# class MyEventFilter(QObject):
#    def eventFilter(self, receiver, event):
#       if(event.type() == QEvent.KeyPress):
#     QMessageBox.information(None,"Filtered Key Press Event!!",
#                      "You Pressed: "+ event.text())
#     return True
#       else:      
#        #Call Base Class Method to Continue Normal Event Processing
#        return super(MyEventFilter,self).eventFilter(receiver, event)
   
class QtConnections():

    def __init__(self, uiMain):
        self.uiMain = uiMain
        self.eventConnection = []

    def installEventHandler(self):
        self.uiMain.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.uiMain.installEventFilter(self.uiMain)
        self.uiMain.__class__.eventFilter = self.eventFilter

    def testEventNames(self, obj, event):
        eventName = self._getEventName(QtCore.QEvent, event.type())
        eventNo = int(event.type())
        print("Testing Event: ", str(obj), str(eventNo), eventName)
        
    def eventFilter(self, obj, event):
        #Use this for testing the event Name
        #self.testEventNames(obj, event)
        
        currentEvent = event
        currentEventObject = obj        
        currentEventName = self._getEventName(QtCore.QEvent, event.type())
        currentEventNo = int(event.type())

        for eachEntry in self.eventConnection:
            if (currentEventObject in eachEntry and currentEventName in eachEntry):
                eachEntry[2](currentEvent, currentEventObject, currentEventName)
                
        currentEvent.accept()

        app = QtWidgets.QApplication.instance() 
        app.processEvents()
        #app.notify(obj, event)
        return super(type(self.uiMain),self.uiMain).eventFilter(obj, event)

    def addEventConnection(self, obj, eventName, fnToInvoke):
        entry = (obj, eventName, fnToInvoke)
        if (not entry in self.eventConnection):
            self.eventConnection.append(entry)
        
    def _getTheEventEntry(self, obj, eventName):
        for each in self.eventConnection:
            if (obj in each and eventName in each):
                return each
        return None

    def _getEventName(self, base, value):
        """Convert a Qt Enum value to its key as a string.
    
        Args:
            base: The object the enum is in, e.g. QFrame.
            value: The value to get.
    
        Return:
            The key associated with the value as a string, or None.
        """
        klass = value.__class__
        try:
            idx = klass.staticMetaObject.indexOfEnumerator(klass.__name__)
        except AttributeError:
            idx = -1
        if idx != -1:
            return klass.staticMetaObject.enumerator(idx).valueToKey(value)
        else:
            for name, obj in vars(base).items():
                if isinstance(obj, klass) and obj == value:
                    return name
            return None
        
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

    def connectToFocusChange(self, Widget, FunctionToInvoke):
        app = QtWidgets.QApplication.instance()        
        app.__class__.focusChanged = FunctionToInvoke
        app.focusChanged = FunctionToInvoke

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
        


# class MyWidget(QtGui.QWidget):
# 
#     def __init__(self, parent = None):
#         super(MyWidget, self).__init__(parent)
#         self.installEventFilter(self)
# 
#     def eventFilter(self, object, event):
#         if event.type() == QtCore.QEvent.WindowActivate:
#             print "widget window has gained focus"
#         elif event.type()== QtCore.QEvent.WindowDeactivate:
#             print "widget window has lost focus"
#         elif event.type()== QtCore.QEvent.FocusIn:
#             print "widget has gained keyboard focus"
#         elif event.type()== QtCore.QEvent.FocusOut:
#             print "widget has lost keyboard focus"
        