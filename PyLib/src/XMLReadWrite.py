import os
import xml.dom.minidom as mini
#import xml.etree.ElementTree as xme
import lxml.etree as xme



class XMLRW():
    """
        XML ReadWrite
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
        else:
            node.set(attrName,attrValue)


    def getAttributeVal(self,node,attrName):
        val = ''
        if attrName in node.keys():
            val = node.attrib[attrName]
        return val

    def isAttributeExist(self, node, attrName):
        return node in self.getAttributeList(node)

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
        try:
            f = open(fileName,'w')
            ugly = xme.tostring(self.xmlRootNode)
            pretty = mini.parseString(ugly).toprettyxml()
            newFormat = ''
            for eachLine in pretty.split('\n'):
                if eachLine.strip():
                    newFormat +=  eachLine + '\n'
            f.write(newFormat)
            f.close()
        except:
            print 'Writing file'