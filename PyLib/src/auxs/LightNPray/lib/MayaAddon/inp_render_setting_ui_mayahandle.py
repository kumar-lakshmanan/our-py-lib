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


import os, sys, time, pickle

newQt = 1
try :
    import maya.OpenMayaUI as mui
    x = mui.MQtUtil()
except :
    newQt = 0
    pass

try :
    temp = dir(QtCore)
    temp = []
except :
    import maya.cmds as mc

    if newQt :
        qtPath = "Z:/REPO/SOURCE/APPS/pyqt/maya2011"
        dbPath = "Z:/REPO/SOURCE/APPS/Py2_6Apps/MySQL/64bit"
    else :
        if mc.about(is64=True) :
            qtPath = 'Z:/REPO/SOURCE/APPS/pyqt/64Bit'
            dbPath = "Z:/REPO/SOURCE/SCRIPTS/PYTHON/SqlWrapperLibrary/64bit"
        else :
            qtPath = "Z:/REPO/SOURCE/APPS/pyqt/32Bit"
            dbPath = "Z:/REPO/SOURCE/SCRIPTS/PYTHON/SqlWrapperLibrary/32bit"

    if qtPath not in sys.path :
        sys.path.append(qtPath)

    if not dbPath in sys.path:
        sys.path.append(dbPath)


offline = 0
onlineModulePathList =  [
                        'Z:/REPO/SOURCE/SCRIPTS/PYTHON/LightNPray/lib',
                        'Z:/REPO/SOURCE/SCRIPTS/PYTHON/LightNPray/lib/MayaAddon',
                        'Z:/REPO/SOURCE/SCRIPTS/PYTHON/PulseXML'
                        ]
offlineModulePathList = [
                        'D:/REPO/SOURCE/SCRIPTS/PYTHON/LightNPray/lib',
                        'D:/REPO/SOURCE/SCRIPTS/PYTHON/LightNPray/lib/MayaAddon',
                        'D:/REPO/SOURCE/SCRIPTS/PYTHON/PulseXML'
                        ]

modulePathList = offlineModulePathList if offline else onlineModulePathList
for modulePath in modulePathList:
    if modulePath not in sys.path:
        sys.path.append(modulePath)


import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pumpThread as pump
import sip

#Application Lib
import inp_render_setting_ui as irsu
reload(irsu)

##import lnpLib as lnp
##reload(lnp)

import lnpSettingsLib as lnps
reload(lnps)

import renderConfirm_ui as renCon
reload(renCon)

class RenderConfirm(QtGui.QDialog, renCon.Ui_Dialog) :
    def __init__(self, prnt) :
        if prnt == '':
            QtGui.QDialog.__init__(self)
        else:
            QtGui.QDialog.__init__(self, prnt)

        self.setupUi(self)
        self.comment = ''
        self.updateRevision = 0
        self.status = 0
        self.connect(self.versionPB, QtCore.SIGNAL('clicked()'), self.versionCheckIn)
        self.connect(self.revisionPB, QtCore.SIGNAL('clicked()'), self.revisionCheckIn)
        try :
            print 'Hiding group box'
            self.groupBox_6.setVisible(0)
        except :
            print "Unable to hide aspect ratio grp box"
        return

    def versionCheckIn(self) :
        self.comment = str(self.commentTE.toPlainText())
        if self.comment.strip().replace(' ', '') == '' :
            return -1
        self.updateRevision = 0
        self.status = 1
        self.close()
        return 0

    def revisionCheckIn(self) :
        self.comment = str(self.commentTE.toPlainText())
        if self.comment.strip().replace(' ', '') == '' :
            return -1
        self.updateRevision = 1
        self.status = 1
        self.close()
        return 0


class LNPRenderSetting(QtGui.QDialog, irsu.Ui_Form, lnps.LNPSetLib):

    def __init__(self, prnt):
        if prnt == '':
            QtGui.QDialog.__init__(self)
        else:
            QtGui.QDialog.__init__(self, prnt)

        self.setupUi(self)

        lnps.LNPSetLib.__init__(self)
        if not self.status :
            self.statusbar.showMessage("Unable to initialize settings.")
            return

        stat = self.sigConnection()
##        stat = self.settingsTabChanged(0)
        self.__setup()
        return

    def sigConnection(self):
        self.connect(self.renderButton, QtCore.SIGNAL('clicked()'),self.doRender)
##        self.connect(self.updateFileButton, QtCore.SIGNAL('clicked()'),self.doUpdate)
##        self.connect(self.settingsTab, QtCore.SIGNAL('currentChanged(int)'), self.settingsTabChanged)
        self.connect(self.isFrameRangeChkB, QtCore.SIGNAL('stateChanged(int)'), self.useFrameRangeChecked)
        self.connect(self.isStereoChkB, QtCore.SIGNAL('stateChanged(int)'), self.refreshCameraList)
        self.connect(self.sceneResCB, QtCore.SIGNAL('currentIndexChanged(int)'), self.sceneResChanged)
        self.connect(self.darCB, QtCore.SIGNAL('currentIndexChanged(int)'), self.darChanged)
        self.connect(self.parCB, QtCore.SIGNAL('currentIndexChanged(int)'), self.parChanged)
        self.connect(self.percentRenderSB, QtCore.SIGNAL('valueChanged(int)'), self.sceneResChanged)
## Edit signal slot connections
        self.connect(self.imageFormatCB, QtCore.SIGNAL('currentIndexChanged(const QString &)'), self.imageFormatChanged)
        self.connect(self.rendererCB, QtCore.SIGNAL('currentIndexChanged(const QString &)'), self.projRendererChanged)
        self.connect(self.renderEngineCB, QtCore.SIGNAL('currentIndexChanged(const QString &)'), self.renderEngineChanged)

        self.connect(self.renderTypeCB, QtCore.SIGNAL('currentIndexChanged(const QString &)'), self.renderTypeChanged)
        self.connect(self.charBgCB, QtCore.SIGNAL('currentIndexChanged(const QString &)'), self.charBgChanged)
        self.connect(self.frameRangeLE, QtCore.SIGNAL('textChanged(const QString &)'), self.frameRangeChanged)
        self.connect(self.startFrameSB, QtCore.SIGNAL('valueChanged(int)'), self.startFrameChanged)
        self.connect(self.endFrameSB, QtCore.SIGNAL('valueChanged(int)'), self.endFrameChanged)
        self.connect(self.isStereoChkB, QtCore.SIGNAL('stateChanged(int)'), self.isStereoRender)
        self.connect(self.cameraCB, QtCore.SIGNAL('currentIndexChanged(const QString &)'), self.cameraChanged)
        return 0

    def doRender(self):
        rc = RenderConfirm(self)
        rc.exec_()
        if not rc.status :
            return -1
##        print rc.comment, rc.updateRevision
        message = self.renderCommit(rc.comment.replace("#", "HASH"), rc.updateRevision)
        self.statusbar.showMessage(message, 10000)
        return 0
##        filePath = str(mc.file(q=True, sn=True))
##        fileName = os.path.basename(filePath)
##        fileSplit = fileName.split('_')
##        if len(fileSplit) < 6 :
##            return -1
##        projCode = fileSplit[1]
##        seqName = fileSplit[2]
##        l = lnp.LNPLib(projCode, seqName)
##        return l.render(filePath)


##    def doUpdate(self):
##        filePath = str(mc.file(q=True, sn=True))
##        fileName = os.path.basename(filePath)
##        fileSplit = fileName.split('_')
##        if len(fileSplit) < 6 :
##            return -1
##        projCode = fileSplit[1]
##        seqName = fileSplit[2]
##        l = lnp.LNPLib(projCode, seqName)
##        return l.updatePassFile()

    def __setup(self) :
        stat = self.__setProjectGlobals()
        stat = self.__setSceneSettings()
        return 0

    def projRendererChanged(self, renderer) :
        self.setRenderer(str(renderer))
##        self.settings['project_globals']['renderer'] = renderer
        defVal = self.getDefaultRenderEngines(str(renderer))
        stat = self.__loadComboBox(self.renderEngineCB, defVal)
        val = self.settings['project_globals']['render_engine']
        if not val in defVal :
##            self.renderEngineCB.addItem(val)
            if self.renderEngineCB.count() :
               self.renderEngineCB.setCurrentIndex(0)
        else :
            index = defVal.index(val)
            self.renderEngineCB.setCurrentIndex(index)

        renderEngine = str(self.renderEngineCB.currentText())
        self.settings['project_globals']['render_engine'] = renderEngine
        print self.settings['project_globals']['template_id']
        return 0

    def renderEngineChanged(self, engine) :
        self.settings['project_globals']['render_engine'] = str(engine)
        return 0

    def imageFormatChanged(self, format) :
        self.settings['project_globals']['image_format'] = str(format)
        return 0

##    def notEditableCheckBox(self, state) :
##        checkBox = self.sender()
##        checkBox.blockSignals(1)
##        if state :
##            checkBox.setCheckState(QtCore.Qt.Unchecked)
##        else :
##            checkBox.setCheckState(QtCore.Qt.Checked)
##        checkBox.blockSignals(0)
##        return 0

    def renderTypeChanged(self, type_) :
        self.settings['scene_settings']['render_type'] = str(type_)
        return 0

    def charBgChanged(self, val) :
        self.settings['scene_settings']['char_bg'] = str(val)
        return 0

    def useFrameRangeChecked(self, val) :
        if not val :
            self.settings['scene_settings']['use_frame_range'] = '0'
            self.frameRangeLE.setEnabled(0)
            self.startFrameSB.setEnabled(1)
            self.endFrameSB.setEnabled(1)
        else :
            self.settings['scene_settings']['use_frame_range'] = '1'
            self.frameRangeLE.setEnabled(1)
            self.startFrameSB.setEnabled(0)
            self.endFrameSB.setEnabled(0)
        return 0

    def frameRangeChanged(self, text) :
        self.settings['scene_settings']['frame_range'] = str(text)
        return 0

    def startFrameChanged(self, value) :
        self.settings['scene_settings']['start_frame'] = str(value)
        return 0

    def endFrameChanged(self, value) :
        self.settings['scene_settings']['end_frame'] = str(value)
        return 0

    def isStereoRender(self, state) :
        if state :
            self.settings['scene_settings']['is_stereo'] = '1'
        else :
            self.settings['scene_settings']['is_stereo'] = '0'
        return 0

    def cameraChanged(self, camera) :
        self.settings['scene_settings']['camera'] = str(camera)
        return 0

    def refreshCameraList(self, val) :
        defVal = self.getSceneCameras(val)
        stat = self.__loadComboBox(self.cameraCB, defVal)
        self.settings['scene_settings']['camera'] = str(self.cameraCB.currentText())
        return 0

    def sceneResChanged(self, val) :
        self.settings['scene_settings']['image_resolution'] = str(self.sceneResCB.currentText())
        self.settings['scene_settings']['resolution_percent'] = str(self.percentRenderSB.value())
##        return self.updateCurrentRezLabel()
        return 0

    def darChanged(self, val) :
        return self.setDeviceAspectRatio(str(self.darCB.currentText()))

    def parChanged(self, val) :
        return self.setPixelAspectRatio(str(self.parCB.currentText()))

##    def updateCurrentRezLabel(self) :
##        rezText = str(self.sceneResCB.currentText())
##        index = rezText.find('*')
##        if index == -1 or not len(rezText.split('*')) == 2 :
##            self.curntRezLabel.setText('-- ERROR --')
##            return -1
##        rezSplit = rezText.split('*')
##        try :
##            width = int(rezSplit[0]); height = int(rezSplit[1])
##            renCent = int(self.percentRenderSB.value()) / 100.0
##        except :
##            self.curntRezLabel.setText('-- ERROR --')
##            return -1
##        renderWidth = int(width * renCent)
##        renderHeight = int(height * renCent)
##        self.curntRezLabel.setText(str(renderWidth) + '*' + str(renderHeight))
##        return 0

    def __setProjectGlobals(self) :
        stat = self.mayaVersionLE.setText(self.settings['project_globals']['maya_version'])

        defVal = self.getDefaultRenderers()
        stat = self.__loadComboBox(self.rendererCB, defVal)
        val = self.settings['project_globals']['renderer']
        if not val in defVal :
            self.rendererCB.addItem(val)
        else :
            index = defVal.index(val)
            self.rendererCB.setCurrentIndex(index)

        defVal = self.getDefaultRenderEngines(self.settings['project_globals']['renderer'])
        stat = self.__loadComboBox(self.renderEngineCB, defVal)
        val = self.settings['project_globals']['render_engine']
        if not val in defVal :
            if self.renderEngineCB.count() :
                self.renderEngineCB.setCurrentIndex(index)
        else :
            index = defVal.index(val)
            self.renderEngineCB.setCurrentIndex(index)

        try :
            val = int(self.settings['project_globals']['is_stereo'])
        except :
            val = -1

        if not val == -1 :
            if val :
                stat = self.isStereoPrjChkB.setCheckState(QtCore.Qt.Checked)
            else :
                stat = self.isStereoPrjChkB.setCheckState(QtCore.Qt.Unchecked)
        else :
            print 'Unable to find if project is a stereo'
        self.isStereoPrjChkB.setEnabled(0)

        defVal = self.getDefaultResolution()
        stat = self.__loadComboBox(self.resolutionPrjCB, defVal)
        val = self.settings['project_globals']['image_resolution']
        if not val in defVal :
            self.resolutionPrjCB.addItem(val)
        else :
            index = defVal.index(val)
            self.resolutionPrjCB.setCurrentIndex(index)
        self.resolutionPrjCB.setEnabled(0)

        defVal = self.getDefaultImageFormats()
        stat = self.__loadComboBox(self.imageFormatCB, defVal)
        val = self.settings['project_globals']['image_format']
        if not val in defVal :
            self.imageFormatCB.addItem(val)
        else :
            index = defVal.index(val)
            self.imageFormatCB.setCurrentIndex(index)

        defVal = self.getDefaultImageDepths()
        stat = self.__loadComboBox(self.imageDepthCB, defVal)
        val = self.settings['project_globals']['image_depth']
        if not val in defVal :
            self.imageDepthCB.addItem(val)
        else :
            index = defVal.index(val)
            self.imageDepthCB.setCurrentIndex(index)
        self.imageDepthCB.setEnabled(0)

##        try :
##            val = float(self.settings['scene_settings']['device_aspect_ratio'])
##        except :
##            val = 0
##        self.deviceDSB.setValue(val)
##        self.deviceDSB.setEnabled(0)
##
##        try :
##            val = float(self.settings['scene_settings']['pixel_aspect_ratio'])
##        except :
##            val = 0
##        self.pixelDSB.setValue(val)
##        self.pixelDSB.setEnabled(0)
        return 0

    def __setSceneSettings(self) :
        stat = self.workFileLE.setText( self.fileName() )

        defVal = self.getDefaultRenderTypes()
        stat = self.__loadComboBox(self.renderTypeCB, defVal)
        val = self.settings['scene_settings']['render_type']
        if not val in defVal :
##            self.renderTypeCB.addItem(val)
            print 'Unkown render type', val
        else :
            index = defVal.index(val)
            self.renderTypeCB.setCurrentIndex(index)

        defVal = self.getDefaultDAR()
        stat = self.__loadComboBox(self.darCB, defVal)
        val = self.settings['scene_settings']['device_aspect_ratio']
        if not val in defVal :
            print 'Unkown device aspect ratio', val
        else :
            index = defVal.index(val)
            self.darCB.setCurrentIndex(index)

        defVal = self.getDefaultPAR()
        stat = self.__loadComboBox(self.parCB, defVal)
        val = self.settings['scene_settings']['pixel_aspect_ratio']
        if not val in defVal :
            print 'Unkown pixel aspect ratio', val
        else :
            index = defVal.index(val)
            self.parCB.setCurrentIndex(index)

        defVal = self.getCharBg()
        stat = self.__loadComboBox(self.charBgCB, defVal)
        val = self.settings['scene_settings']['char_bg']
        if not val in defVal :
            print 'Unkown render as value', val
        else :
            index = defVal.index(val)
            self.charBgCB.setCurrentIndex(index)

        defVal = self.getDefaultResolution()
        stat = self.__loadComboBox(self.sceneResCB, defVal)
        val = self.settings['scene_settings']['image_resolution']
        if not val in defVal :
            print 'Unkown resolution', val
        else :
            index = defVal.index(val)
            self.sceneResCB.setCurrentIndex(index)
##        stat = self.updateCurrentRezLabel()

        try :
            val = int(self.settings['scene_settings']['use_frame_range'])
        except :
            val = 0
        if val :
            self.isFrameRangeChkB.setCheckState(QtCore.Qt.Checked)
        else :
            self.isFrameRangeChkB.setCheckState(QtCore.Qt.Unchecked)

        try :
            val = int(self.getDefaultStartFrame())
        except :
            val = 1001
        self.startFrameSB.setValue(val)

        try :
            val = int(self.getDefaultEndFrame())
        except :
            val = 1101
        self.endFrameSB.setValue(val)

        try :
            val = int(self.settings['scene_settings']['is_stereo'])
        except :
            val = 0
        if val :
            self.isStereoChkB.setCheckState(QtCore.Qt.Checked)
        else :
            self.isStereoChkB.setCheckState(QtCore.Qt.Unchecked)

        defVal = self.getSceneCameras(val)
        stat = self.__loadComboBox(self.cameraCB, defVal)
        val = self.settings['scene_settings']['camera']
        if val not in defVal :
            print 'Unknown camera in settings', val
        else :
            index = defVal.index(val)
            self.cameraCB.setCurrentIndex(index)

        return 0

    def __clearComboBox(self, cb) :
        cb.blockSignals(1)
        cb.clear()
        cb.blockSignals(0)
        return 0

    def __loadComboBox(self, cb, data) :
        if not type(data) == type([]) :
            return -1
        cb.blockSignals(1)
        cb.clear()
        for eachVal in data :
            cb.addItem(eachVal)
        cb.blockSignals(0)




def getMayaWindow() :
    try :
        ptr = mui.MQtUtil.mainWindow()
        return sip.wrapinstance(long(ptr), QtCore.QObject)
    except :
        pass

    return ''

parentWindow = getMayaWindow()
if parentWindow == '' :
    try :
        pump.initializePumpThread()
        qapp = QtGui.QApplication(sys.argv)
    except :
        print 'Pump thread failed.'
        pass

ui = LNPRenderSetting(parentWindow)
ui.show()
