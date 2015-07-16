from kmxPyQt.qne.qnodeseditor import QNodesEditor
from kmxPyQt.qne import qneblock
from kmxPyQt.qne.qneport import QNEPort
from kmxPyQt.qne import qneconnection

from kmxPyQt.kmxNodeGraph.kmxNodeBlock import kmxNodeBlock
import importlib
importlib.reload(qneblock)

from PyQt5.QtCore import (Qt)
import pickle
import argparse

class KMXNodeGraphSystem():
	def __init__(self, parent, view, scene):
		self.win = parent
		self.view = view
		self.scene = scene
		self.ne = None

	def restScene(self):
		self.nodes=[]
		self.nodesCounter=0
		
		self.nodeColor = Qt.green
		self.nodeTextColor = Qt.blue
		
		self.nodeSelectedColor = Qt.yellow
		self.nodeSelectedTextColor = Qt.blue	
		
		self.sysNodeColor = Qt.blue
		self.sysNodeTextColor = Qt.yellow
		
		self.sysNodeSelectedColor = Qt.yellow
		self.sysNodeSelectedTextColor = Qt.red
				
		self.scene.clear()
	
	def sceneData(self):
		nodeBlock = kmxNodeBlock()	
			
		blocks=[]
		conn=[]			
		for eachItem in self.scene.items():
			if eachItem.type() == qneblock.QNEBlock.Type:
				#print("BlockNode: "+str(eachItem.kmxNodeBlock.nodeTag))
				nodeBlock = eachItem.kmxNodeBlock
				nodeTag = nodeBlock.nodeTag
				nodeName = nodeBlock.Name
				nodeModule = nodeBlock.Module
				xpos = nodeBlock.Node.pos().x()			
				ypos = nodeBlock.Node.pos().y()
				variables = eachItem.getVariables()
				blocks.append((nodeTag, nodeName, nodeModule, xpos, ypos,variables))
			if eachItem.type() == qneconnection.QNEConnection.Type:				
				#print("Connection: "+str(eachItem)) 
				port1 = eachItem.port1()				
				port2 = eachItem.port2()
				port1Block = port1.block()								
				port2Block = port2.block()				
				port1NodeBlock = port1Block.kmxNodeBlock
				port2NodeBlock = port2Block.kmxNodeBlock
				if(not port1.isOutput()):
					#print(port2NodeBlock.Name, port1NodeBlock.Name)
					conn.append((port2NodeBlock.nodeTag, port1NodeBlock.nodeTag))
				else:				
					#print(port1NodeBlock.Name, port2NodeBlock.Name)
					conn.append((port1NodeBlock.nodeTag, port2NodeBlock.nodeTag))
				#print((port1NodeBlock.nodeTag, port2NodeBlock.nodeTag))

						
		data={}
		data['blocks']=blocks
		data['conn']=conn
		data['counter']=self.nodesCounter			
		return data
					
	def saveScene(self,fileName):
		data=self.sceneData()
		with open(fileName, 'wb') as handle:
			pickle.dump(data, handle)		

	def loadScene(self,fileName):
		with open(fileName, 'rb') as handle:
			data=pickle.load(handle)
					
		blocks=data['blocks']
		conn=data['conn']
		counter=data['counter']
		self.restScene()


		for eachBlock in blocks:
			nodeTag=eachBlock[0]
			nodeName=eachBlock[1]
			nodeModule=eachBlock[2]
			xpos=eachBlock[3]
			ypos=eachBlock[4]
			variableLst=eachBlock[5]
			if (nodeName=='Start'):
				self._addNodeStart()
				self.startNode.setPos(xpos,ypos)
				self.startNode.kmxNodeBlock.additionalTags=nodeTag
				#self.startNode.setVariables(variableLst)
			elif (nodeName=='End'):
				self._addNodeEnd()
				self.endNode.setPos(xpos,ypos)
				self.endNode.kmxNodeBlock.additionalTags=nodeTag
				#self.startNode.setVariables(variableLst)
			else:
				nd = self.addNodeFn(nodeName,nodeModule,variableLst)
				nd.nodeTag=nodeTag
				nd.additionalTags=nodeTag
				nd.Node.setPos(xpos,ypos)
				
		self.nodesCounter=counter							
		for eachConn in conn:
			node1AdditionalTag = eachConn[0]
			node2AdditionalTag = eachConn[1]
			node1 = self.getNodeByAdditionalTag(node1AdditionalTag)
			node2 = self.getNodeByAdditionalTag(node2AdditionalTag)
			#print(node1.Name, node2.Name)
			#print(node1.outPort, node2.inPort)
			self.connectNodes(node1, node2)

				
	def _getnodeTag(self):
		self.nodesCounter+=1
		return self._getNodeTagCore(self.nodesCounter)
	
	def _getNodeTagCore(self, number):
		return "node" + str(number).zfill(5)
		
	def readyTheScene(self):
		#Graph handler
		
		self.restScene()		
		self.ne = QNodesEditor(self.win)
		self.ne.install(self.scene)	
		
# 		print(self.ne.callBackBlockSelected)
# 		self.ne.callBackConnAdded = self.connectionAdded
# 		self.ne.callBackConnRemoved = self.connectionRemoved

# 		self.ne.callBackBlockRemoved = self.blockRemoved
# 		self.ne.callBackBlockSelected = self.blockSelected
# 		self.ne.callBackBlockDeSelected = self.blockDeSelected			

		self._addNodeStart()
		self._addNodeEnd()

	def connectFnConnectionAdded(self, fn):
 		self.ne.callBackConnAdded = fn

	def connectFnConnectionRemoved(self, fn):
 		self.ne.callBackConnRemoved = fn 		
 			
	def connectFnNodeSelected(self, fn):
 		self.ne.callBackBlockSelected = fn

	def connectFnNodeDeSelected(self, fn):
 		self.ne.callBackBlockDeSelected = fn
 		 		
	def connectFnNodeRemoved(self, fn):
 		self.ne.callBackBlockRemoved = fn

	def _addNodeStart(self):
		self.startNode=qneblock.QNEBlock(None)
		self.startNode.nodeColor =  self.sysNodeColor
		self.startNode.nodeTextColor =  self.sysNodeTextColor
		self.startNode.nodeSelectedColor =  self.sysNodeSelectedColor
		self.startNode.nodeSelectedTextColor =  self.sysNodeSelectedTextColor		

		self.scene.addItem(self.startNode)
		self.startNode.addPort('Start', 0, QNEPort.NamePort)		
		port = self.startNode.addOutputPort('');
		self.startNodePort = port 
		
		newNode = kmxNodeBlock()
		newNode.nodeTag = 'Start'
		newNode.Name = 'Start'
		newNode.Node = self.startNode
		newNode.inPort = None
		newNode.outPort = self.startNodePort
		newNode.additionalTags=''
		self.startNode.kmxNodeBlock=newNode
		self.nodes.append(newNode)
		return newNode		
		
	def _addNodeEnd(self):
		self.endNode=qneblock.QNEBlock(None)
		self.endNode.nodeColor =  self.sysNodeColor
		self.endNode.nodeTextColor =  self.sysNodeTextColor
		self.endNode.nodeSelectedColor =  self.sysNodeSelectedColor
		self.endNode.nodeSelectedTextColor =  self.sysNodeSelectedTextColor		
		
		self.scene.addItem(self.endNode)
		self.endNode.addPort('End', 0, QNEPort.NamePort)		
		port = self.endNode.addInputPort('');
		self.endNode.setPos(160,0)
		self.endNodePort = port	
		
		newNode = kmxNodeBlock()
		newNode.nodeTag = 'End'
		newNode.Name = 'End'
		newNode.Node = self.endNode
		newNode.inPort = self.endNodePort
		newNode.outPort = None
		newNode.additionalTags=''
		self.endNode.kmxNodeBlock=newNode
		self.nodes.append(newNode)
		return newNode			
		
	def addNodeFn(self,name, module='', variableLst=[]):
		
		if (name=="Start" or name=="End"):
			print("You can't have your nodes with name - Start or End")
			return
		
		nodeTag = self._getnodeTag()
		
		node = qneblock.QNEBlock(None)
		node.setVariables(variableLst)

		node.nodeColor =  self.nodeColor
		node.nodeTextColor =  self.nodeTextColor
		node.nodeSelectedColor =  self.nodeSelectedColor
		node.nodeSelectedTextColor =  self.nodeSelectedTextColor		
				
		self.scene.addItem(node)
		node.addPort(name, 0, QNEPort.NamePort)
		inPort = node.addInputPort("")
		outPort = node.addOutputPort("")
		
		node.setPos(self.view.sceneRect().center().toPoint())
		
		newNode = kmxNodeBlock()
		newNode.nodeTag = nodeTag
		newNode.Name = name
		newNode.Node = node
		newNode.inPort = inPort
		newNode.outPort = outPort
		newNode.additionalTags=''
		newNode.Module = module
		newNode.setVariables(variableLst)
		node.kmxNodeBlock=newNode
		self.nodes.append(newNode)
		return newNode
		
	def getNodeByTag(self, tag):
		for each in self.nodes:
			if(tag == each.nodeTag):
				return each
			
	def getNodeByName(self, name):
		for each in self.nodes:
			if(name == each.Name):
				return each
	
	def getNodeByAdditionalTag(self, additionalTags):
		for each in self.nodes:
			if(each.additionalTags==additionalTags):
				return each			
	
	def connectToNodeStart(self, node):		
		inPort = node.inPort
		outPort = self.startNodePort
		block1 = self.startNode		
		block2 = node.Node
		self._doConnect(inPort, outPort, block1, block2)		
		
	def connectToNodeEnd(self, node):		
		inPort = self.endNodePort
		outPort = node.outPort
		block1 = node.Node		
		block2 = self.endNode
		self._doConnect(inPort, outPort, block1, block2)	

	def connectNodes(self, node1, node2):		
		inPort = node2.inPort
		outPort = node1.outPort		
		block1 = node1.Node		
		block2 = node2.Node
		self._doConnect(inPort, outPort, block1, block2)
		
	def _doConnect(self,inPort,outPort,block1,block2):
		conn = qneconnection.QNEConnection(None)
		self.scene.addItem(conn)
		conn.setPort1(inPort)
		conn.setPort2(outPort)
		conn.setPos1(block1.scenePos())
		conn.setPos2(block2.scenePos())
		inPort.addConnection(conn)
		conn.updatePosFromPorts()
		conn.updatePath()			

	def connectionAdded(self, *args):
		print("connAdd"+ str(args))

	def connectionRemoved(self, *args):
		print("removConn"+ str(args))	
		
	def blockRemoved(self, *args):
		print("removBlock"+ str(args))
		
	def blockSelected(self, *args):		
		print("selected " + str(args))	
		
	def blockDeSelected(self, *args):
		print("Deselected " + str(args))