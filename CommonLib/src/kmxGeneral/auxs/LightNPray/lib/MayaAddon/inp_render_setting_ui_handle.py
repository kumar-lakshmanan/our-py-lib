#-------------------------------------------------------------------------------
# Name:        Render Setting UI Handle
#
# Author:      lkumaresan
#
# Created:     28/10/2010
# Copyright:   (c) lkumaresan 2010
# Licence:     Personal
#
# Description:
#
#
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python




import os
import sys

##Remove cached custom modules from memory except preloaded IDE modules
if __name__ == '__main__':
    if globals().has_key('InitialModules'):
         for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
            del(sys.modules[CustomModule])
    else:
        InitialModules = sys.modules.keys()



#Global Lib
import time
import base64
from PyQt4 import QtCore, QtGui

#Application Lib
from inp_render_setting_ui import Ui_Form


class LNPRenderSetting(QtGui.QDialog, Ui_Form):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ui = LNPRenderSetting()
    ui.show()
    sys.exit(app.exec_())