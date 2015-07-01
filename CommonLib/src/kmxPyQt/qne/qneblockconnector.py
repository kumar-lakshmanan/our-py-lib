
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QPainterPath, QPen)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsPathItem, QGraphicsTextItem)

class QNEBlockConnector(QGraphicsPathItem):

	def __init__(self, parent):
		super(QNEBlockConnector, self).__init__(parent)
		
		self.radius_ = 4
		self.margin = 3
		
		self.setPen(QPen(Qt.darkRed))
		self.setBrush(Qt.red)
		
		self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
		
		self.m_portFlags = 0
		self.isOutput_ = False
		
		self.m_block = None
		self.m_connections = []


	def __del__(self):
		#print("Del QNEPort %s" % self.name)
		
		for connection in self.m_connections:
		    if connection.port1():
		        connection.port1().removeConnection(connection)
		    if connection.port2():
		        connection.port2().removeConnection(connection)
		    if self.scene():
		        self.scene().removeItem(connection)


	def setIsOutput(self, isOutput):
		self.isOutput_ = isOutput
		
		path = QPainterPath()
		if self.isOutput_:
			path.addEllipse(-2*self.radius_, -self.radius_, 2*self.radius_, 2*self.radius_);
		else:
			path.addEllipse(0, -self.radius_, 2*self.radius_, 2*self.radius_);
		
		self.setPath(path)


	def setNEBlock(self, block):
		self.m_block = block
	
	
	def setPortFlags(self, flags):
		self.m_portFlags = flags
		
		if self.m_portFlags & self.TypePort:
		    font = self.scene().font()
		    font.setItalic(True)
		    self.label.setFont(font)
		    self.setPath(QPainterPath())
		elif self.m_portFlags & self.NamePort:
		    font = self.scene().font()
		    font.setBold(True)
		    self.label.setFont(font)
		    self.setPath(QPainterPath())
	
	
	def setPtr(self, ptr):
		self.m_ptr = ptr
	
	
	def type(self):
		return self.Type
	
	
	def radius(self):
		return self.radius_
	
	
	def portName(self):
		return self.name
	
	
	def isOutput(self):
		return self.isOutput_
	
	
	def block(self):
		return self.m_block
	
	
	def portFlags(self):
		return self.m_portFlags
	
	
	def ptr(self):
		return self.m_ptr;
	
	
	def addConnection(self, connection):
		self.m_connections.append(connection)
	
	
	def removeConnection(self, connection):
		try:
		    self.m_connections.remove(connection)
		except: pass
		
	
	def connections(self):
		return self.m_connections
	
	
	def isConnected(self, other):
		for connection in self.m_connections:
		    if connection.port1() == other or connection.port2() == other:
		        return True
		
		return False
	
	
	def itemChange(self, change, value):
		if change == QGraphicsItem.ItemScenePositionHasChanged:
		    for connection in self.m_connections:
		        connection.updatePosFromPorts()
		        connection.updatePath()
		
		return value
