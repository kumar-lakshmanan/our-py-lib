from qneblock import QNEBlock
from qneport import QNEPort
from qneconnection import QNEConnection

def readScene(scene):
	sceneBlocks={}
	sceneConnections={}
	for eachItem in scene.items():
		
		#Blocks
		if eachItem.type() == QNEBlock.Type:
			sceneBlocks[eachItem]=[]
			
			#Ports
			ports = eachItem.ports()
			for eachPort in ports:
				sceneBlocks[eachItem].append(eachPort)
				
		#COnnections
		if eachItem.type() == QNEConnection.Type:
			#Connected Ports
			port1 = eachItem.port1()
			port2 = eachItem.port2()
			sceneConnections[eachItem]=(port1,port2)

	sceneData={}
	sceneData['Blocks']=sceneBlocks
	sceneData['Connections']=sceneConnections
	return sceneData


import pprint 
pp = pprint.PrettyPrinter(indent=4)

#Print Info
print("\n\n\n\n\n\n\n\n")
s=readScene(widget.scene)
pp.pprint(s)