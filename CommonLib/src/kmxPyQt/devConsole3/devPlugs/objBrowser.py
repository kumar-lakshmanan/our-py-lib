#For DevConsole
import inspect
import os

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class objBrowser(QDialog):

    def __init__(self, parent=None):

        self.parent = parent
        self.uiName = "objBrowser.ui"
        super(objBrowser, self).__init__(parent)
#        super(objBrowser, self).__init__(parent, self.uiName)
        print ("Loaded!")

#         self.lineEdit.returnPressed.connect(self.inputReturn)
#         self.treeWidget.itemClicked.connect(self.itemClicked)
#         self.treeWidget.itemDoubleClicked.connect(self.itemDblClicked)

        self.cwd = os.getcwd()
        self.setupUI(self.uiName)
        self.scriptContent = self.readScript('objInspSupport.py')
        print(self.scriptContent)
        self.show()

    def setupUI(self, uiFile):
        prepath = os.path.abspath(os.curdir)
        prepath = os.path.join(prepath, "devPlugs")
        uiFile = os.path.join(prepath, uiFile)
        loadUi(uiFile, self)
        self.setWindowTitle(self.__class__.__name__)

    def uiPreparation(self):
        pass

    def uiConnection(self):
        pass

    def inputReturn(self):
        self.objInspectSpl()

    def itemDblClicked(self, *arg):
        self.objInspectDblClick(arg)

    def itemClicked(self, *arg):
        self.objInspectClick(arg)

    def objInspectSpl(self):
        val = str(self.lineEdit.text())
        members = inspect.getmembers(eval(val))
        self.treeWidget.clear()
        for eachMember in members:
            obj = eachMember[1]
            mem = eachMember[0]
            tp = 'None'
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                tp = 'Fn'
            elif inspect.isbuiltin(obj):
                tp = 'BuiltIn'
            elif inspect.isclass(obj):
                tp = 'Class'
            elif inspect.ismodule(obj):
                tp = 'Module'
            elif inspect.iscode(obj):
                tp = 'Code'
    #         elif type(obj) is types.InstanceType:
    #             tp = 'UserType'
            elif (type(obj) is type(1) or
                    type(obj) is type('') or
                    type(obj) is type([]) or
                    type(obj) is type(()) or
                    type(obj) is type({})
                  ):
                tp = 'Variable'
            elif type(obj) is type(None):
                tp = 'None'
            else:
                tp = 'None'

            self.item = QtWidgets.QTreeWidgetItem()
            self.item.setText(0, mem)
            self.item.setText(1, tp)
            setattr(self.item, 'dx', eachMember[1])
            self.treeWidget.addTopLevelItem(self.item)

    def objInspectClick(self, *arg):
        arg = arg[0]
        if len(arg) > 0:
            itm = arg[0]

            nam = str(itm.text(0))
            tp = str(itm.text(1))
            obj = getattr(itm, 'dx')

            try:
                doc = inspect.getdoc(obj)
                comments = inspect.getcomments(obj)
                if inspect.isfunction(obj) or inspect.ismethod(obj):
                    args = inspect.getargspec(obj)
                    arginfo = inspect.formatargspec(args)
                else:
                    args = 'Not Available'
                    arginfo = 'Not Available'
            except:
                args = ''
                arginfo = ''
                doc = obj.__doc__
                comments = ''

# #            mems=''
# #            try:
# #                for i in inspect.getmembers(obj):
# #                    mems = mems+'\n%s - %s' % (i[0],i[1])
# #            except:
# #                pass

            info = ''
            info += '\nName: %s' % (str(nam))
            info += '\nType: %s' % (str(tp))
            info += '\nInfo: %s' % (str(obj))
            info += '\nArgs: %s' % (str(arginfo))
            info += '\n\nDoc: %s\n\n' % (str(doc))
            info += '\nComments: %s\n\n' % (str(comments))
            # info += '\n\n\nMembers: %s\n\n' % (str(mems))

            self.textBrowser.setText(info)

    def objInspectDblClick(self, *arg):
        arg = arg[0]
        if len(arg) > 0:
            itm = sitm = arg[0]

            nam = str(itm.text(0))
            tp = str(itm.text(1))
            obj = getattr(itm, 'dx')

            self.objInsp_In_popList(itm, obj)

    def objInsp_In_popList(self, item, data):
        prn = self

        members = inspect.getmembers(data)

        for i in range(0, item.childCount()):
            ch = item.child(i)
            item.removeChild(ch)

        for eachMember in members:
            obj = eachMember[1]
            mem = eachMember[0]
            tp = 'None'
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                tp = 'Fn'
            elif inspect.isbuiltin(obj):
                tp = 'BuiltIn'
            elif inspect.isclass(obj):
                tp = 'Class'
            elif inspect.ismodule(obj):
                tp = 'Module'
            elif inspect.iscode(obj):
                tp = 'Code'
#             elif type(obj) isinstance(obj, class_or_type_or_tuple) types.InstanceType:
#                 tp = 'UserType'
            elif (type(obj) is type(1) or
                    type(obj) is type('') or
                    type(obj) is type([]) or
                    type(obj) is type(()) or
                    type(obj) is type({})
                  ):
                tp = 'Variable'
            elif type(obj) is type(None):
                tp = 'None'
            else:
                tp = 'None'

            prn.item = QtWidgets.QTreeWidgetItem()
            prn.item.setText(0, mem)
            prn.item.setText(1, tp)
            setattr(prn.item, 'dx', eachMember[1])
            item.addChild(prn.item)


    def readScript(self, fileName):
        data = ''
        ff = os.path.join(self.cwd, fileName)
        if os.path.exists(ff):
            f = open(ff, 'r')
            data = f.read()
            f.close()
        return data


# if '__main__' == __name__:
#
#     try:
#         sip.delete(app)
#     except:
#         try:
#             del(app)
#         except:
#             pass
#
#     inst = QtGui.QApplication.instance()
#     if inst:
#         inst.exit()
#         inst.quit()
#         del(inst)
#
#
#     app = QtGui.QApplication(sys.argv)
#     ui = objBrowserPlug()
#     ui.show()
#     z = app.exec_()
#     del(app)
#     sys.exit(z)
