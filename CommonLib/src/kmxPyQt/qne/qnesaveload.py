from kmxPyQt.qne.qneblock import QNEBlock
from kmxPyQt.qne.qneport import QNEPort
from kmxPyQt.qne.qneconnection import QNEConnection
import pickle
import pprint 

class QNESaveLoadScene:
	refList=[]
	
	def __init__(self, scene):
		self.currentScene = scene
		
	def _findTagNameForObj(self,obj):
		for each in self.refList:
			#print(each)
			if obj==each[1]:
				return each[0]
				
	def _findObjForTagName(self,tagName):
		for each in self.refList:
			#print(each)
			if tagName==each[0]:
				return each[1]
		
	def _getTagName(self,unit,counter):
		return unit + str(counter).zfill(5)
		
	def printScene(self):
		data = self.getSceneData()
		pprint.pprint(data)
	
	def printFileData(self,fileName):
		with open(fileName, 'rb') as handle:
			data=pickle.load(handle)
		pprint.pprint(data)
	
	def getSceneData(self):
		sceneData={}
		sceneBlocks={}
		sceneConnections={}
		blockCounter=0
		portCounter=0
		connCounter=0
		self.refList=[]
		for eachItem in self.currentScene.items():		
			#Blocks
			if eachItem.type() == QNEBlock.Type:
				blockCounter+=1
				nextBlockTag=self._getTagName('block',blockCounter)
				sceneBlocks[nextBlockTag]=[]
				sceneBlocks[nextBlockTag].append((eachItem.pos().x(),eachItem.pos().y()))
				self.refList.append((nextBlockTag,eachItem))
				#Ports
				ports = eachItem.ports()
				for eachPort in ports:
					portTag={}
					portCounter+=1
					nextPortTag=self._getTagName('port',portCounter)
					self.refList.append((nextPortTag,eachPort))
					portName = eachPort.portName()
					portIsOutput = eachPort.isOutput()
					portFlags = eachPort.portFlags()
					portTag[nextPortTag]={'portName':portName, 'portIsOutput':portIsOutput, 'portFlags':portFlags }
					sceneBlocks[nextBlockTag].append(portTag)
			#Connections
			if eachItem.type() == QNEConnection.Type:
				connCounter+=1
				nextConnTag=self._getTagName('conn',connCounter)
				port1 = eachItem.port1()
				port1Block = port1.block()
				port2 = eachItem.port2()
				port2Block = port2.block()
				conn={}
				conn['port1']=(self._findTagNameForObj(port1Block), self._findTagNameForObj(port1))
				conn['port2']=(self._findTagNameForObj(port2Block), self._findTagNameForObj(port2))
				sceneConnections[nextConnTag]=conn
				
		sceneData['blocks']=sceneBlocks
		sceneData['connection']=sceneConnections
		return sceneData
		
	def setSceneData(self,data):
		self.clearScene()
		self.refList=[]
		blocks = data['blocks']
		connection = data['connection']
		for eachBlock in blocks:
			block = QNEBlock(None)
			self.currentScene.addItem(block)
			self.refList.append((eachBlock,block))
			pos = blocks[eachBlock][0]
			block.setPos(pos[0],pos[1])
			for eachPortCnt in range(1,len(blocks[eachBlock])):
				port = blocks[eachBlock][eachPortCnt]
				portTagName=list(port.keys())[0]
				portContent=port[portTagName]
				portName=portContent['portName']
				portIsOutput=portContent['portIsOutput']
				portFlags=portContent['portFlags']
				portObj = block.addPort(portName,portIsOutput,portFlags)
				self.refList.append((portTagName,portObj))
				
		for eachConn in connection:
			connContent=connection[eachConn]
			port1Data = connContent['port1']
			port2Data = connContent['port2']
			
			conn = QNEConnection(None)
			self.currentScene.addItem(conn)
			p1Block=self._findObjForTagName(port1Data[0])
			p2Block=self._findObjForTagName(port2Data[0])
			p1=self._findObjForTagName(port1Data[1])
			p2=self._findObjForTagName(port2Data[1])
			conn.setPort1(p1)
			conn.setPort2(p2)
			conn.setPos1(p1Block.scenePos())
			conn.setPos2(p2Block.scenePos())
			p1.addConnection(conn)
			conn.updatePosFromPorts()
			conn.updatePath()
	
	def saveScene(self,fileName):
		data = self.getSceneData()
		with open(fileName, 'wb') as handle:
			pickle.dump(data, handle)
			
	def loadScene(self,fileName):
		with open(fileName, 'rb') as handle:
			data=pickle.load(handle)
		self.setSceneData(data)
		
	def clearScene(self):
		self.currentScene.clear()

#fileName="testFile.txt"
#qls = QNESaveLoadScene(widget.scene)
#qls.printFileData(fileName)
#qls.loadScene(fileName)
#qls.saveScene(fileName)
#qls.clearScene()
