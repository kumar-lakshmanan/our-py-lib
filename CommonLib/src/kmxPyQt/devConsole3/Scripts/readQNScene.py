from qneblock import QNEBlock
from qneport import QNEPort
from qneconnection import QNEConnection

class QNESaveLoadScene:
	
	refList=[]
	
	def __init__(self, scene):
		self.currentScene = scene
		
	def _findTagNameForObj(self,obj):
		for each in refList:
			#print(each)
			if obj==each[1]:
				return each[0]
				
	def _findObjForTagName(self,tagName):
		for each in refList:
			#print(each)
			if tagName==each[0]:
				return each[1]
		
	def _getTagName(self,unit,counter):
		return unit + str(counter).zfill(5)
		
	def getSceneData(self, scene):
		sceneData={}
		sceneBlocks={}
		sceneConnections={}
		blockCounter=0
		portCounter=0
		connCounter=0
		refList=[]
		for eachItem in scene.items():		
			#Blocks
			if eachItem.type() == QNEBlock.Type:
				blockCounter+=1
				nextBlockTag=_getTagName('block',blockCounter)
				sceneBlocks[nextBlockTag]=[]
				sceneBlocks[nextBlockTag].append((eachItem.pos().x(),eachItem.pos().y()))
				refList.append((nextBlockTag,eachItem))
				#Ports
				ports = eachItem.ports()
				for eachPort in ports:
					portTag={}
					portCounter+=1
					nextPortTag=_getTagName('port',portCounter)
					refList.append((nextPortTag,eachPort))
					portName = eachPort.portName()
					portIsOutput = eachPort.isOutput()
					portFlags = eachPort.portFlags()
					portTag[nextPortTag]={'portName':portName, 'portIsOutput':portIsOutput, 'portFlags':portFlags }
					sceneBlocks[nextBlockTag].append(portTag)
			#Connections
			if eachItem.type() == QNEConnection.Type:
				connCounter+=1
				nextConnTag=_getTagName('conn',connCounter)
				port1 = eachItem.port1()
				port1Block = port1.block()
				port2 = eachItem.port2()
				port2Block = port2.block()
				conn={}
				conn['port1']=(findTagNameForObj(port1Block), findTagNameForObj(port1))
				conn['port2']=(findTagNameForObj(port2Block), findTagNameForObj(port2))
				sceneConnections[nextConnTag]=conn
				
		sceneData['blocks']=sceneBlocks
		sceneData['connection']=sceneConnections
		return sceneData
		
	def setSceneData(self,scene,data):
		

import pprint 
pp = pprint.PrettyPrinter(indent=4)

#Print Info
print("\n\n\n\n\n\n\n\n")
s=readScene(widget.scene)
#pp.pprint(s)

import pickle
with open('mydata.txt', 'wb') as handle:
	pickle.dump(s, handle)
	
with open('mydata.txt', 'rb') as handle:
	backData=pickle.load(handle)
	
pp.pprint(backData)