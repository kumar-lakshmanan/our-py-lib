import os
import maya.cmds as mc
import maya.mel as mel

import sys
qtAppPath = "Z:/REPO/SOURCE/SCRIPTS/PYTHON/LightNPray/lib"
if qtAppPath not in sys.path :
    sys.path.append(qtAppPath)

import launchRender as lr
reload(lr)

import vcLib as vcl
reload(vcl)

import PulseXMLLib as pxml
reload(pxml)

import mayaFuncs as MayaFunc
reload(MayaFunc)




class LNPSetLib() :
    def __init__(self, projectXmlBaseFolder='http://192.168.28.42:81/pulse/beat/projects/') :
        self.status = 0

        self.projectXmlBaseFolder = projectXmlBaseFolder
        if not self.projectXmlBaseFolder.endswith('/') :
            self.projectXmlBaseFolder += '/'

        fileName = self.__getMayaFileName()
        if not fileName.startswith('D:/ABX_PULSE/'+os.getenv('USERNAME').upper()+'/') :
            print 'LNPSetLib.__init__ :- Invalid file location of file', fileName
            return

        fileSplit = fileName.split('/')
        if not len(fileSplit) > 8 :
            print 'LNPSetLib.__init__ :- Invalid file name', fileName
            return

        self.projCode = fileSplit[3]
        self.seqName = fileSplit[4]
        self.shotName = fileSplit[5]

        self.settings = self.__setGlobals()
        data = self.__getXMLSettings()
        stat = self.__overwriteXmlSettings(data)
        self.imageMap = {}
        self.imageMap['TIFF'] = '3'
        self.imageMap['PNG'] = '32'
        self.imageMap['TARGA'] = '19'
        self.imageMap['JPEG'] = '8'

        self.status = 1
        return

    def __overwriteXmlSettings(self, data) :
        if 'Is Stereo' in data.keys() :
            self.settings['project_globals']['is_stereo'] = data['Is Stereo']
            self.settings['scene_settings']['is_stereo'] = data['Is Stereo']

        if 'Resolution' in data.keys() :
            try :
                self.settings['project_globals']['default_resolutions'] = data['Resolution'].split(',')
                self.settings['project_globals']['image_resolution'] = self.settings['project_globals']['default_resolutions'][0]
                self.settings['scene_settings']['image_resolution'] = self.settings['project_globals']['default_resolutions'][0]
            except :
                pass

        if 'Pixel Aspect Ratio' in data.keys() :
            self.settings['project_globals']['pixel_aspect_ratio'] = data['Pixel Aspect Ratio'].split(',')
            try :
                self.settings['scene_settings']['pixel_aspect_ratio'] = self.settings['project_globals']['pixel_aspect_ratio'][0]
            except :
                self.settings['scene_settings']['pixel_aspect_ratio'] = '1.00'
            self.settings['scene_settings']['pixel_aspect_ratio'] = data['Pixel Aspect Ratio']

        if 'Device Aspect Ratio' in data.keys() :
            self.settings['project_globals']['device_aspect_ratio'] = data['Device Aspect Ratio'].split(',')
            try :
                self.settings['scene_settings']['device_aspect_ratio'] = self.settings['project_globals']['device_aspect_ratio'][0]
            except :
                self.settings['scene_settings']['device_aspect_ratio'] = '1.33'

        if 'Renderer' in data.keys() :
            try :
                self.settings['project_globals']['default_renderers'] = data['Renderer'].split(',')
                self.settings['project_globals']['renderer'] = self.settings['project_globals']['default_renderers'][0]
                self.settings['scene_settings']['is_stereo'] = '0'
            except :
                pass

        if 'Maya Version' in data.keys() :
            val = data['Maya Version']
            if not val == None :
                self.settings['project_globals']['maya_version'] = val

        if 'Image Format' in data.keys() :
            val = data['Image Format']
            if not val == None :
                self.settings['project_globals']['image_format'] = val.upper()

        if 'Mayaman template ID' in data.keys() :
            val = data['Mayaman template ID']
            if not val == None :
                self.settings['project_globals']['mayaman_template_id'] = val

        if 'Maya template ID' in data.keys() :
            val = data['Maya template ID']
            if not val == None :
                self.settings['project_globals']['maya_template_id'] = val

        if 'Mental ray template ID' in data.keys() :
            val = data['Mental ray template ID']
            if not val == None :
                self.settings['project_globals']['mental_ray_template_id'] = val

        if 'VRay template ID' in data.keys() :
            val = data['VRay template ID']
            if not val == None :
                self.settings['project_globals']['vray_template_id'] = val

##        self.settings['project_globals']['template_id'] = '1'
        self.setRenderer(self.settings['project_globals']['renderer'])

        return 0
    def __getMayaFileName(self) :
        return str(mc.file(q=True, sn=True))

    def fileName(self, path='') :
        if path == '' :
            path = self.settings['scene_settings']['work_file']
        try :
            fileName = os.path.basename(path)
        except :
            fileName = ''
        return fileName

    def __setGlobals(self) :
        result = {}
        result['project_globals'] = self.__getDefaultProjectSettings()
        result['scene_settings'] = self.__getDefaultSceneSettings()
        return result

    def __getXMLSettings(self) :
        xmlPath = self.projectXmlBaseFolder + self.projCode + '/WORK/XML/PROCESS/project_process.xml'
        xmlTree = pxml.PulseXML()
        stat = xmlTree.setup(xmlPath)
        if stat == -1 :
            return {}
        return self.__getXmlAttributes(xmlTree)

    def __getXmlAttributes(self, xmlTree) :
        result = {}
        attrElems = xmlTree.getChildElements(xmlTree.root_elem, ['attribute'])
        for eachElem in attrElems :
            nameElems = xmlTree.getChildElements(eachElem, ['name'])
            if not len(nameElems) == 1 :
                continue
            valueElems = xmlTree.getChildElements(eachElem, ['value'])
            if not len(valueElems) == 1 :
                continue
            result[nameElems[0].text] = valueElems[0].text
        return result

    def __getDefaultProjectSettings(self) :
        result = {}
        result['maya_version'] = 'MAYA2008'
        result['renderer'] = 'MayaMan'
        result['render_engine'] = 'Air'
        result['is_stereo'] = '1'
        result['image_resolution'] = '1*1'
        result['image_format'] = 'TIFF'
        result['image_depth'] = '8 Bit'
        result['device_aspect_ratio'] = '1.77'
        result['pixel_aspect_ratio'] = '1.00'
        result['default_resolutions'] = ['1*1', '2*2']
        return result

    def __getDefaultSceneSettings(self) :
        result = {}
        result['work_file'] = self.__getMayaFileName()
        result['render_type'] = 'ScnImg'
        result['image_resolution'] = '1920*1480'
        result['resolution_percent'] = '100'
        result['use_frame_range'] = '0'
        result['frame_range'] = ''
        result['start_frame'] = self.__getSceneStartFrame()
        result['end_frame'] = self.__getSceneEndFrame()
        result['is_stereo'] = '0'
        result['camera'] = 'persp'
        result['bit_depth'] = '8 Bit'
        result['char_bg'] = 'CHAR'
        return result

    def getProjectSettings(self) :
        return self.settings['project_globals']

    def getSceneSettings(self) :
        return self.settings['scene_settings']

    def getDefaultRenderTypes(self) :
        return ['ScnImg', 'ScnRibImg', 'RibOnly', 'RibImg']

    def getDefaultResolution(self) :
        return self.settings['project_globals']['default_resolutions']

    def getDefaultDAR(self) :
        return self.settings['project_globals']['device_aspect_ratio']

    def getDefaultPAR(self) :
        return self.settings['project_globals']['pixel_aspect_ratio']

    def getDefaultImageDepths(self) :
        return ['8', '16']

    def getCharBg(self) :
        return ['CHAR', 'BG']

    def getDefaultImageFormats(self) :
        return self.imageMap.keys()

    def getDefaultRenderers(self) :
        return self.settings['project_globals']['default_renderers']

    def getDefaultRenderEngines(self, renderer) :
        if renderer.upper().replace(' ', '') == 'MAYAMAN' :
            return ['Air']
        return []

    def getDefaultStartFrame(self) :
        return self.__getSceneStartFrame()

    def getDefaultEndFrame(self) :
        return self.__getSceneEndFrame()

    def getSceneCameras(self, isStereo=0) :
        if not type(isStereo) == type(1) :
            return []
        if isStereo :
            matchedCam = self.__getStereoCameras('left')
        else:
            matchedCam = self.__getAllCams()
        return matchedCam

    def __getSceneStartFrame(self):
        return str(int(mc.playbackOptions(q=True, min=True)))

    def __getSceneEndFrame(self) :
        return str(int(mc.playbackOptions(q=True, max=True)))

    def __getAllCams(self):
        allSortedCam = []
        cameras = mc.listCameras(p = True)
        for cam in cameras:
            shapeNode = mc.listRelatives(cam, s=True)
            if shapeNode == None :
                continue

            str = "attributeExists \"renderable\"" + " \"" + shapeNode[0]  + "\"" ;
            status = mel.eval(str)
            if status:
                allSortedCam.append(cam)
        return allSortedCam

    def __getStereoCameras(self,searchStr):
        sortedCam = []
        allCams = self.__getAllCams()
        for cam in allCams:
            if cam.lower().find(searchStr.lower()) == -1 :
                continue
            sortedCam.append(cam)
        return sortedCam

    def renderCommit(self, comment, upversion=False) :
        fileName = self.__getMayaFileName()
        stat = self.__saveFile(fileName)
        if stat == -1 :
            print "Unable to save file", fileName
            return -1

        print "Exporting file", fileName
        mf = MayaFunc()
        if mf.status == -1 :
            print "Error initiating 'export maya func' class."
            return -1
        renFile = mf.exportScene(fileName)
        if renFile == '' :
            return -1

        print 'Rendering file', fileName
        if upversion :
            stat = self.__upversionFile(fileName, comment)
        else :
            stat = self.__subversionFile(fileName, comment)
            if stat == -1 :
                return "Unable to do checkin or checkout for", fileName
##                return -1

        if not fileName.lower().endswith(".ma") :
            return ""
        melFileName = os.path.dirname(fileName) + '/DEP/' + os.path.basename(fileName)[:-2] + 'mel'
        try :
            if not os.path.exists(os.path.exists(os.path.dirname(melFileName))) :
                os.makedirs(os.path.dirname(melFileName))
        except :
            print "Unable to make intermediate folders of " + melFileName
            print "Required path " + os.path.dirname(melFileName) + " does not exists."
            return -1

        mf = MayaFunc.LnPSupportFuncs()
        stat = mf.unlockDependencies(melFileName)
##        stat = self.__unlockDependencies(melFileName)
        if stat == -1 :
            return 'Lock check on mel file failed.'
##            return -1
        stat = self.__writeMelRenderFile(melFileName, self.__getMelAttribs())
        if os.path.exists(melFileName) :
            if upversion :
                stat = self.__upversionFile(melFileName, comment)
            else :
                stat = self.__subversionFile(melFileName, comment)
            if stat == -1 :
                return "Unable to do checkin or checkout for", fileName
##                return -1
        else :
            print 'Unable to write mel file for certain render settings.'

##        l = lnpl.LNPLib(self.projCode, self.seqName, self.shotName)
##        return l.render(fileName)
        renData = self.__getRenderData()
        renData['comment'] = comment
        renData['render_file'] = renFile
        stat = lr.launchRocket(fileName, renData)
        if stat == -1 :
            return 'Launch render failed.'
        return 'Render process started successfully.'

    def __unlockDependencies(self, fileName) :
        vl = vcl.vcLib()
        stat = vl.isFileLocked(fileName)
        if stat == 1 :
            return 0
        if stat == 0 :
            stat = vl.CheckOut(fileName)
            if type(stat) == type({}) :
                return 0
        return -1

    def __saveFile(self, fileName) :
        print 'Saving file', fileName
        try :
            tempFile = mc.file(save=True)
        except :
            print 'Unable to save file', fileName
            return -1
        print 'File saved', fileName
        return 0

    def __getMelAttribs(self) :
        result = {}
        format = self.settings['project_globals']['image_format']
        if format in self.imageMap.keys() :
            formatCode = self.imageMap[format]
            result['defaultRenderGlobals.imageFormat'] = str(formatCode)
        result['defaultResolution.deviceAspectRatio'] = self.settings['scene_settings']['device_aspect_ratio']
        result['defaultResolution.pixelAspect'] = self.settings['scene_settings']['pixel_aspect_ratio']
        result['defaultResolution.width'] = self.__getResWidth()
        result['defaultResolution.height'] = self.__getResHeight()
##        try :
##            if self.settings['scene_settings']['image_resolution'] == '1540*2000' :
##                self.settings['scene_settings']['device_aspect_ratio'] = '0.77'
##            elif  self.settings['scene_settings']['image_resolution'] == '2016*1134' :
##                self.settings['scene_settings']['device_aspect_ratio'] = '1.778'
##        except :
##            pass
##        try :
##            result['defaultResolution.deviceAspectRatio'] = str(float(self.__getResWidth())/float(self.__getResHeight()))
##        except :
        result['defaultResolution.deviceAspectRatio'] = self.settings['scene_settings']['device_aspect_ratio']
        return result

    def __getResWidth(self) :
        try :
            width = int(self.settings['scene_settings']['image_resolution'].split('*')[0]) * int(self.settings['scene_settings']['resolution_percent']) / 100.0
        except :
            width = '320'
        return str(int(width))

    def __getResHeight(self) :
        try :
            height = int(self.settings['scene_settings']['image_resolution'].split('*')[1]) * int(self.settings['scene_settings']['resolution_percent']) / 100.0
        except :
            height = '240'
        return str(int(height))

    def __upversionFile(self, fileName, comment) :
        index = fileName.find('/WORK/')
        serverFile = fileName
        if not index == -1 :
            serverFile = 'W:/' + fileName[index+6:]

        print serverFile
        vl = vcl.vcLib()
        if not vl.isFileLocked(fileName) == 1 and os.path.exists(serverFile) :
            print 'Lock check failed for file', fileName
            return -1

        index = fileName.find('/WORK/')
        if index == -1 :
            print 'File', fileName,'should be a work file.'
            return -1

        statDict = vl.CheckIn(fileName, comment, '', False, True, False, True)
        if statDict[fileName] == -1 or statDict[fileName] == 0 :
            return -1
        statDict = vl.CheckOut(fileName)
        if statDict[fileName] == -1 or statDict[fileName] == 0 :
            return -1
        return 0

    def __subversionFile(self, fileName, comment) :
        index = fileName.find('/WORK/')
        serverFile = fileName
        if not index == -1 :
            serverFile = 'W:/' + fileName[index+6:]

        print serverFile
        vl = vcl.vcLib()
        if not vl.isFileLocked(fileName) == 1 and os.path.exists(serverFile) :
            print 'Lock check failed for file', fileName
            return -1

        index = fileName.find('/WORK/')
        if index == -1 :
            print 'File', fileName,'should be a work file.'
            return -1

        statDict = vl.CheckIn(fileName, comment, '', False, False, False, True)
        if statDict[fileName] == -1 or statDict[fileName] == 0 :
            return -1
        statDict = vl.CheckOut(fileName)
        if statDict[fileName] == -1 or statDict[fileName] == 0 :
            return -1
        return 0

    def __writeMelRenderFile(self, melFileName, attribsDict) :
##        print 'Attribs dict is', attribsDict
        backedup = 0
        if os.path.exists(melFileName) :
            backedup = 1
            try :
                os.rename(melFileName, melFileName+'.temp')
            except :
                try :
                    os.remove(melFileName+'.temp')
                    os.rename(melFileName, melFileName+'.temp')
                except :
                    print 'Unable to backup current mel file', melFileName

        fh = file(melFileName, 'w')
        for each in attribsDict.keys() :
            fh.write('setAttr ' + each + ' ' + attribsDict[each] + ';\n')
        fh.close()
        if os.path.exists(melFileName) and os.path.exists(melFileName+'.temp'):
            os.remove(melFileName+'.temp')
        else :
            print 'Unable to write mel file in', melFileName
            if backedup :
                os.rename(melFileName+'.temp', melFileName)
                return melFileName
            return -1
        return 0

    def __getRenderData(self) :
        result = {}
        result['maya_version'] = self.__getMayaVersion()##self.settings['project_globals']['maya_version']
        result['renderer'] = self.settings['project_globals']['renderer']
        result['render_engine'] = self.settings['project_globals']['render_engine']
        result['is_stereo'] = self.settings['scene_settings']['is_stereo']

        result['render_type'] = self.settings['scene_settings']['render_type']
        result['use_frame_range'] = self.settings['scene_settings']['use_frame_range']
        result['frame_range'] = self.settings['scene_settings']['frame_range']
        result['start_frame'] = self.settings['scene_settings']['start_frame']
        result['end_frame'] = self.settings['scene_settings']['end_frame']
        result['camera'] = self.__getRenderCameras()
        result['char_bg'] = self.settings['scene_settings']['char_bg']
        result['template_id'] = self.settings['project_globals']['template_id']
        print result['template_id']
        return result

    def __getMayaVersion(self) :
        mayaVer = mc.about(v=True)
        if not len(mayaVer) > 3 :
            return 'maya2011'
        return 'maya' + mayaver[:4]

    def __getRenderCameras(self) :
        try :
            isStereo = int(self.settings['scene_settings']['is_stereo'])
        except :
            return [ self.settings['scene_settings']['camera'] ]
        if not isStereo :
            return [ self.settings['scene_settings']['camera'] ]

        cam1 = self.settings['scene_settings']['camera']
        searchCam = self.settings['scene_settings']['camera'].lower().replace('left', 'right')
        allCams = self.__getAllCams()
        cam2 = ''
        for eachCam in allCams :
            if not eachCam.lower() == searchCam :
                continue
            cam2 = eachCam
            break
        if cam2 == '' :
            cam2 = cam1
        return [cam1, cam2]

    def ___________settingFuncs(self) :
        return 0

    def setRenderer(self, renderer) :
        try :
            self.settings['project_globals']['renderer'] = renderer
        except :
            print 'Unable to set renderer to', renderer
            return -1

        if renderer.lower().replace(' ', '') == 'mayaman' :
            self.settings['project_globals']['template_id'] = self.settings['project_globals']['mayaman_template_id']
        elif renderer.lower().replace(' ', '') == 'maya' :
            self.settings['project_globals']['template_id'] = self.settings['project_globals']['maya_template_id']
        elif  renderer.lower().replace(' ', '') == 'mentalray' :
            self.settings['project_globals']['template_id'] = self.settings['project_globals']['mental_ray_template_id']
        elif  renderer.lower().replace(' ', '') == 'vray' :
            self.settings['project_globals']['template_id'] = self.settings['project_globals']['vray_template_id']
        else :
            print 'Unknown renderer ' + renderer + '. Could not set template for the renderer.'
        return 0

    def setRenderEngine(self, engine) :
        try :
            self.settings['project_globals']['render_engine'] = engine
        except :
            print 'Unable to set render engine to', engine
            return -1
        return 0

    def setIsStereo(self, isStereo) :
        try :
            self.settings['scene_settings']['is_stereo'] = isStereo
        except :
            print 'Unable to set is stereo value to', isStereo
            return -1
        return 0

    def setRenderType(self, renderType) :
        try :
            self.settings['scene_settings']['render_type'] = renderType
        except :
            print 'Unable to set render type to', renderType
            return -1
        return 0

    def setUseFrameRange(self, use) :
        try :
            self.settings['scene_settings']['use_frame_range'] = use
        except :
            print 'Unable to set use frame range to', use
            return -1
        return 0

    def setFrameRange(self, frameRange) :
        try :
            self.settings['scene_settings']['frame_range'] = frameRange
        except :
            print 'Unable to set frame range to', frameRange
            return -1
        return 0

    def setStartFrame(self, frameNum) :
        try :
            self.settings['scene_settings']['start_frame'] = frameNum
        except :
            print 'Unable to set start frame to', frameNum
            return -1
        return 0

    def setEndFrame(self, frameNum) :
        try :
            self.settings['scene_settings']['end_frame'] = frameNum
        except :
            print 'Unable to set end frame to', frameNum
            return -1
        return 0

    def setCamera(self, camera) :
        try :
            self.settings['scene_settings']['camera'] = camera
        except :
            print 'Unable to set camera to', camera
            return -1
        return 0

    def setCharBg(self, charBg) :
        try :
            self.settings['scene_settings']['char_bg'] = charBg
        except :
            print 'Unable to set char or bg value to', charBg
            return -1
        return 0

    def setImageFormat(self, format) :
        try :
            self.settings['project_globals']['image_format'] = format
        except :
            print 'Unable to set image format to', format
            return -1
        return 0

    def getDeviceAspectRatio(self) :
        return ''

    def setDeviceAspectRatio(self, value) :
##        try :
##            if self.projCode.upper() == 'DOZ' and self.settingsself.settings['scene_settings']['image_resolution'] == '1540*2000' :
##                self.settings['scene_settings']['device_aspect_ratio'] = '0.77'
##                return 0
##            elif self.projCode.upper() == 'DOZ' and self.settingsself.settings['scene_settings']['image_resolution'] == '2016*1134' :
##                self.settings['scene_settings']['device_aspect_ratio'] = '1.778'
##                return 0
##        except :
##            pass

        try :
            self.settings['scene_settings']['device_aspect_ratio'] = value
        except :
            print 'Unable to set device aspect ratio to', value
            return -1
        return 0

    def getPixelAspectRatio(self) :
        return ''

    def setPixelAspectRatio(self, value) :
        try :
            self.settings['scene_settings']['pixel_aspect_ratio'] = value
        except :
            print 'Unable to set pixel aspect ratio to', value
            return -1
        return 0

    def ___________settingFuncsDone(self) :
        return 0



##lps = LNPSetLib()
##print lps.renderCommit('Testing base functions')
