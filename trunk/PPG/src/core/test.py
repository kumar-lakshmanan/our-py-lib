'''
Created on Oct 7, 2014

@author: Mukundan
'''

import inspect
import sys

from PyQt5 import QtWidgets

obj = QtWidgets
app = QtWidgets.QApplication([])
lt = QtWidgets.QListWidget()
lt.setWindowTitle(obj.__name__)
for each in inspect.getmembers(obj):
    itm = QtWidgets.QListWidgetItem()
    itm.setText(str(each))
    lt.addItem(itm)
lt.show()
sys.exit(app.exec_())

