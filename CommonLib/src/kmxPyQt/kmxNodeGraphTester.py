import importlib

from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QPainter, QBrush, QPalette)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QWidget, QGraphicsScene, QGraphicsView)

from kmxPyQt.kmxNodeGraph import kmxNodeGraphSystem as kgs
importlib.reload(kgs)
import sys

class TesterWindow(QMainWindow):
	def __init__(self, parent):
		super(TesterWindow, self).__init__(parent)
		self.setWindowTitle("TesterWindow")

		self.scene = QGraphicsScene(self)
		self.view = QGraphicsView(self)
		self.view.setScene(self.scene)
		self.view.setRenderHint(QPainter.Antialiasing)
		self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
		self.setCentralWidget(self.view)
		self.view.setAcceptDrops(1)

		self.kgs=kgs.KMXNodeGraphSystem(self, self.view, self.scene)
		self.kgs.readyTheScene()
		
		b1 = self.kgs.addNodeFn("a")
		b2 = self.kgs.addNodeFn("b")
		#b2 = self.kgs.addNodeFn("abcdedcccsdsdw")
		
		#self.kgs.connect(b1,b2)
		
		#self.kgs.connectToNodeStart(b1)
		#self.kgs.connectToNodeEnd(b1)
		
	def saveScene(self):
		self.kgs.saveScene("filea")		

	def loadScene(self):		
		self.kgs.loadScene("filea")					


