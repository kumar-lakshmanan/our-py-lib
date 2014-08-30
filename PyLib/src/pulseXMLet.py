import os
import xml.dom.minidom as mini
import xml.etree.ElementTree as xme
em = xme._ElementInterface('','')


class XMLConfig():
    """
        XML Configuration Read/Write Module.
        (Element Tree Based)
    """

    def __init__(self, CONFIG_NAME='Pulse'):
        self.xmlDoc = xme.ElementTree(xme.Element(CONFIG_NAME))
        self.xmlRootNode = self.xmlDoc.getroot()

    def createNode(self,nodeName,parentNode=None):
        if parentNode!=None:
            node = parentNode.makeelement(nodeName,{})
            parentNode.append(node)
        else:
            node = self.xmlRootNode.makeelement(nodeName,{})
            self.xmlRootNode.append(node)
        return node

    def getNode(self,nodeName,parentNode=None):
        node = ''
        if parentNode!=None:
            chList = parentNode.getchildren()
            for eachCh in  chList:
                if nodeName == eachCh.tag:
                    node = eachCh
        else:
            chList = self.xmlRootNode.getchildren()
            for eachCh in  chList:
                if nodeName == eachCh.tag:
                    node = eachCh
        return node

    def removeNode(self,node,parentNode):
        if parentNode!=None:
            parentNode.remove(node)
        else:
            self.xmlRootNode.remove(node)

    def setAttributeVal(self,node,attrName,attrValue=''):
        if attrName not in node.keys():
            node.set(attrName,attrValue)

    def getAttributeVal(self,node,attrName):
        val = ''
        if attrName in node.keys():
            val = node.attrib[attrName]
        return val

    def getNodeValue(self,node):
        return str(node.text).strip() if node.text else ''

    def setNodeValue(self, node, Value):
        node.text = Value

    def getNodeList(self,node=None):
        listOfChildern = 0
        if node!=None:
            listOfChildern = node.getchildren()
        else:
            listOfChildern = self.xmlRootNode.getchildren()
        return listOfChildern

    def getAttributeList(self,node=None):
        return node.keys()

    def removeAttribute(self,node,attrName):
        if attrName in node.keys():
            node.attrib.pop(attrName)

    def getRoot(self):
        return self.xmlDoc.getroot()

    def findChild(self,childName,parentNode):

        if parentNode!=None:
            for eachChild in parentNode.getchildren():
                if eachChild.tag == childName:
                    return eachChild

        return None

    def prettyPrint(self):
        ugly = xme.tostring(self.xmlRootNode)
        return self.uglyToPretty(ugly)

    def uglyToPretty(self,UglyXML=''):
        pretty = mini.parseString(UglyXML).toprettyxml()
        return pretty


    def loadFile(self,fileName,CONFIG_NAME='ABX'):
        if os.path.exists(fileName):
            f = open(fileName,'r')
            stringXML = f.read()
            f.close()
            self.xmlDoc = xme.ElementTree(xme.fromstring(stringXML))
            self.xmlRootNode = self.xmlDoc.getroot()
            return self.xmlDoc
        return 0

    def loadXMLData(self, stringXML):
        try:
            self.xmlDoc = xme.ElementTree(xme.fromstring(stringXML))
        except:
            print 'Unable to Read XML'
            self.xmlDoc = xme.ElementTree(xme.Element('ROOT'))
        self.xmlRootNode = self.xmlDoc.getroot()



    def saveFile(self,fileName):
        f = open(fileName,'w+b')
        ugly = xme.tostring(self.xmlRootNode)
        pretty = mini.parseString(ugly).toprettyxml()
        newFormat = ''
        for eachLine in pretty.split('\n'):
            if eachLine.strip():
                newFormat +=  eachLine + '\n'
        f.write(newFormat)
        f.close()


class KConfig():

    def __init__(self,fileName='', createFile=False, containerName='PULSE', weburl=''):

        """

            Description:
            ------------

            Follow the example...

            This will create XML file and puts default value on demand.
            Read indiviual values,
            Read list of values,
            Update new values


            and also

            You can even pass weburl for reading an XML config (You won't be able to write that xml)


            eg:
            z = KConfig('MYXML.txt',1,'ROOT')
            or
            z = KConfig(weburl = 'ftp://cgapps:thepulse@wiki/LSAM/CONFIG/AppConfig.xml')


        eg:

            z = KConfig('MYXML.txt',1,'ROOT')
            z.KCsetAttrib('SUBROOT1/SBRL1','ATT1','VAL1')
            z.KCsetAttrib('SUBROOT1/SBRL1','ATT2','VAL2')
            z.KCsetAttrib('SUBROOT1/SBRL1','ATT3','VAL3')

            print z.KCgetAttribList('SUBROOT1/SBRL1')

            z.KCsetAttrib('SUBROOT1/SBRL2','ATXT1','VAL1X')
            z.KCsetAttrib('SUBROOT1/SBRL2','ATXT2','VAL2X')
            z.KCsetAttrib('SUBROOT1/SBRL2','ATXT3','VAL3X')

            print z.KCgetAttribList('SUBROOT1/SBRL2')

            z.KCsetAttrib('SUBROOT2/SBR2L1','ATC1','VAL1')
            z.KCsetAttrib('SUBROOT2/SBR2L1','ATC2','VAL3')
            z.KCsetAttrib('SUBROOT2/SBR2L1','ATC3','VAL4')

            z.KCsetAttrib('SUBROOT2/SBR2L1','ATC1','RESETVAL')

            print z.KCprettyPrint()

            z.KCsetAttrib('SUBROOT2/SBR2L1/INSERTED/NODE')

            print z.KCprettyPrint()

            z.KCremoveTag('SUBROOT2/SBR2L1/INSERTED')

            print z.KCprettyPrint()


        """


        if weburl:

            self.xmlReady = False
            self.xmlWriteOk = False
            try:
                hnd = ur.urlopen(weburl)
            except:
                print 'Unable to reach the server! Network busy or No Network at all!'

            strXML = hnd.read()
            hnd.close()

            self.xmls = XMLConfig(containerName)
            self.xmls.loadXMLData(strXML)
            self.xmlReady = True

        else:

            self.xmlReady = False
            self.xmlWriteOk = False
            if os.path.exists(fileName) or createFile:
                self.xmlFileName = fileName
                self.xmls = XMLConfig(containerName)
                self.xmls.loadFile(fileName,containerName)
                self.xmlReady = True
            if createFile:
                self.xmlWriteOk = True
                self.xmlFileName = fileName



    def KCgetTagList(self,nodePath=''):

        if not self.xmlReady: return -1

        nodePath = nodePath.replace('\\','/')
        paths = nodePath.split('/')

        if paths==['']:
            nodeList = [self.xmls.xmlRootNode]
        else:
            res = self.__KCGetLeafNode(paths)
            if res[0]==0:
                nodeList = [res[1]]
            else:
                nodeList = []

        finnodes = []
        for eachNode in nodeList:
            for eachChildNode in eachNode.getchildren():
                finnodes.append(str(eachChildNode.tag))

        return finnodes


    def KCgetAttribList(self,nodePath=''):

        if not self.xmlReady: return -1

        nodePath = nodePath.replace('\\','/')
        paths = nodePath.split('/')

        if paths==['']:
            nodeList = [self.xmls.xmlRootNode]
        else:
            res = self.__KCGetLeafNode(paths)
            if res[0]==0:
                nodeList = [res[1]]
            else:
                nodeList = []

        finList = []
        for eachNode in nodeList:
            for eachAttribute in eachNode.keys():
                finList.append(str(eachAttribute))

        return finList


    def KCgetAttrib(self,nodePath,attribute,Default=None):

        if not self.xmlReady: return -1

        nodePath = nodePath.replace('\\','/')
        paths = nodePath.split('/')

        creatable = 1 if Default else 0

        res = self.__KCGetLeafNode(paths,creatable)
        if res[0]==0:
            lastNode = res[1]
        else:
            return 'Node not found and create node restricted'


        if attribute in self.KCgetAttribList(nodePath):
            val = self.xmls.getAttributeVal(lastNode,attribute)
            return str(val)
        else:
            if creatable:
                self.KCsetAttrib(nodePath,attribute,Default)
                return Default
            else:
                return None

    def KCsetAttrib(self, nodePath, attribute='', value=0):

        if not self.xmlReady: return -1

        nodePath = nodePath.replace('\\','/')
        paths = nodePath.split('/')

        res = self.__KCGetLeafNode(paths,1)
        if res[0]==0:

            if attribute:
                lastNode = res[1]
                self.xmls.setAttributeVal(lastNode,str(attribute),str(value))

            if self.xmlWriteOk:
                self.xmls.saveFile(self.xmlFileName)
            else:
                print 'Not in write mode'
        else:
            print 'Node not found and create node restricted'

    def KCremoveAttrib(self,nodePath,attribute):

        if not self.xmlReady: return -1

        nodePath = nodePath.replace('\\','/')
        paths = nodePath.split('/')

        res = self.__KCGetLeafNode(paths,0)
        if res[0]==0:
            lastNode = res[1]
        else:
            return 'Node not found'

        if attribute in self.KCgetAttribList(nodePath):
            self.xmls.removeAttribute(lastNode,attribute)
            if self.xmlWriteOk:
                self.xmls.saveFile(self.xmlFileName)
            else:
                print 'Not in write mode'

    def KCremoveTag(self,nodePath):

        if not self.xmlReady: return -1

        nodePath = nodePath.replace('\\','/')
        paths = nodePath.split('/')
        res = self.__KCGetLeafNode(paths)

        node = ''
        nodeParent = ''
        if  res[0]==0:
            node = res[1]
            nodeParent = res[2]

            if node!=None and nodeParent!=None and node in nodeParent.getchildren():
                self.xmls.removeNode(node,nodeParent)
                if self.xmlWriteOk:
                    self.xmls.saveFile(self.xmlFileName)
                else:
                    print 'Not in write mode'

    def KCgetTagValue(self, nodePath):


        if not self.xmlReady: return -1

        nodePath = nodePath.replace('\\','/')
        paths = nodePath.split('/')

        if paths==['']:
            nodeList = [self.xmls.xmlRootNode]
        else:
            res = self.__KCGetLeafNode(paths)
            if res[0]==0:
                nodeList = [res[1]]
            else:
                nodeList = []

        finList = []
        for eachNode in nodeList:
            val = self.xmls.getNodeValue(eachNode)
            finList.append(val)

        return finList


    def KCprettyPrint(self):
        return self.xmls.prettyPrint()


    def __KCGetLeafNode(self,paths,writeOk=False):

        if not self.xmlReady: return -1

        parentNode = None
        lastNode = self.xmls.xmlRootNode
        for eachPathNode in paths:
            if self.xmls.findChild(eachPathNode,lastNode)!=None:
                parentNode = lastNode
                lastNode =  self.xmls.getNode(eachPathNode,lastNode)
            else:
                if writeOk:
                    if eachPathNode:
                        newnode = self.xmls.createNode(eachPathNode,lastNode)
                        lastNode = newnode
                        parentNode = lastNode
                    else:
                        return [-1,lastNode,parentNode]
                else:
                    return [-1,lastNode,parentNode]

        return [0,lastNode,parentNode]

















##x  = XMLConfig('USERS')
##file_ = 'D:/XMLS/users.xml'
##x.loadFile(file_)
##node = x.createNode('USER')
##x.setAttributeVal(node, 'NAME', 'aswamy')
##x.saveFile(file_)

##for eachNode in x.getNodeList():
##    print eachNode.tag, x.getAttributeVal(eachNode,'EXT') ,  x.getNodeValue(eachNode)



##
##
##import time
##
##
##import XMLtoOBJ as xm
##
##
##t1 = time.time()

##z = KConfig('D:/MYXMLx.txt',1,'ROOT')
##z.KCsetAttrib('sub/s1')

##z.KCgetAttribList('SUBROOT1/SBRL1')
##z.KCgetAttribList('SUBROOT1/SBRL1')
##z.KCgetAttribList('SUBROOT1/SBRL1')
##z.KCgetAttribList('SUBROOT1/SBRL1')
##z.KCgetAttribList('SUBROOT1/SBRL1')
##z.KCgetAttribList('SUBROOT1/SBRL1')
##z.KCgetAttribList('SUBROOT1/SBRL1')
##z.KCgetAttribList('SUBROOT1/SBRL1')
##print 'Time: ' + str(time.time()-t1)
##
##t1 = time.time()
##zz = xm.getXMLDict('MYXMLx.txt')
##zz['SUBROOT1'][1]['SBRL1'][0].keys()
##zz['SUBROOT1'][1]['SBRL1'][0].keys()
##zz['SUBROOT1'][1]['SBRL1'][0].keys()
##zz['SUBROOT1'][1]['SBRL1'][0].keys()
##zz['SUBROOT1'][1]['SBRL1'][0].keys()
##zz['SUBROOT1'][1]['SBRL1'][0].keys()
##zz['SUBROOT1'][1]['SBRL1'][0].keys()
##zz['SUBROOT1'][1]['SBRL1'][0].keys()
##print 'Time: ' + str(time.time()-t1)


##z.KCsetAttrib('SUBROOT1/SBRL2','ATXT1','VAL1X')
##z.KCsetAttrib('SUBROOT1/SBRL2','ATXT2','VAL2X')
##z.KCsetAttrib('SUBROOT1/SBRL2','ATXT3','VAL3X')
##
##print z.KCgetAttribList('SUBROOT1/SBRL2')
##
##z.KCsetAttrib('SUBROOT2/SBR2L1','ATC1','VAL1')
##z.KCsetAttrib('SUBROOT2/SBR2L1','ATC2','VAL3')
##z.KCsetAttrib('SUBROOT2/SBR2L1','ATC3','VAL4')
##
##z.KCsetAttrib('SUBROOT2/SBR2L1','ATC1','RESETVAL')
##
##print z.KCprettyPrint()
##
##z.KCsetAttrib('SUBROOT2/SBR2L1/INSERTED/NODE')
##
##print z.KCprettyPrint()
##
##z.KCremoveTag('SUBROOT2/SBR2L1/INSERTED')
##
##print z.KCprettyPrint()


##
##xm = XMLConfig('KUMAR')
##xm.loadFile('d:/ZXC.txt')
##print xm.prettyPrint()
##
##print xm.getNode('forme')
####
##zz1 = xm.createNode('NEWNODE')
##xm.createNode('ggg',zz1)
##rm = xm.createNode('forme',zz1)
##xm.createNode('ccc',zz1)
##
##zz2 = xm.createNode('NEWNODE2')
##xm.createNode('ggg',zz2)
##xm.createNode('ssss',zz2)
##xm.createNode('ccc',zz2)
##
###zz1 = xm.createNode('spl1')
##zz3 = xm.createNode('spl2')
###zz3 = xm.createNode('spl3')
##
##xm.setNode(zz3,rm)
##
##print xm.getNode('ssss',zz2)
##x = xm.prettyPrint()
##print x
##xm.saveFile('D:/ZXC.TXT')



##
##
##
##import xml.etree.ElementTree as em
##f = open('D:\NEWXML.xml','r')
##stringXML = f.read()
##print stringXML
##f.close()
##exm = em.ElementTree(em.fromstring(stringXML))
##
##print ex
##
##
