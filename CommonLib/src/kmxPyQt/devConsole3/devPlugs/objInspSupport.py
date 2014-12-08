import inspect
import types

from PyQt5 import QtGui, QtCore, QtWidgets


def objInsp_popList(prn, plgName, data):

    obj = prn.qplug.getPlugObjFor(plgName, 'name')
    prn = obj.obj

    members = inspect.getmembers(data)
    prn.treeWidget.clear()
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

        prn.item = QtGui.QTreeWidgetItem()
        prn.item.setText(0, mem)
        prn.item.setText(1, tp)
        setattr(prn.item, 'dx', eachMember[1])
        prn.treeWidget.addTopLevelItem(prn.item)

# code:objInsp_popList(<<arg>>)
