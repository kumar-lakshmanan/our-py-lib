#!/usr/bin/python3

# Copyright (c) 2014, ALDO HOEBEN
# Copyright (c) 2012, STANISLAW ADASZEWSKI
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of STANISLAW ADASZEWSKI nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL STANISLAW ADASZEWSKI BE LIABLE FOR ANY
#DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QPainter, QBrush, QPalette)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QWidget,
    QGraphicsScene, QGraphicsView)

from Scripts.qne.qnodeseditor import QNodesEditor
from Scripts.qne.qneblock import QNEBlock
from Scripts.qne.qnesysblock import QNESysBlock
from Scripts.qne.qneport import QNEPort
import myscript
import inspect

class funs():
	
	def __init__(self):
		self.fns=[]
		
	def getListOfFns(self):
		self.fns=[]
		members = inspect.getmembers(myscript)
		for eachMember in members:
			obj = eachMember[1]
			mem = eachMember[0]
			if inspect.isfunction(obj) or inspect.ismethod(obj):
				self.fns.append((obj,mem))
		return self.fns
	
	def getArguments(self, fnName):
		for each in self.fns:
			if each[1]==fnName:
				args = inspect.getargspec(each[0])[0]
		return args

class QNEMainWindow(QMainWindow):
	def __init__(self, parent):
		super(QNEMainWindow, self).__init__(parent)
		fileMenu = self.menuBar().addMenu("&File")

		quitAct = QAction("&Quit", self, shortcut="Ctrl+Q",  statusTip="Exit the application", triggered=self.close)

		self.fnCls = funs()
		lst = self.fnCls.getListOfFns()
		for each in lst:
			fnAct = QAction(each[1], self, triggered=self.addFn)
			fileMenu.addAction(fnAct)
			
		fileMenu.addSeparator()
		fileMenu.addAction(quitAct)

		self.setWindowTitle("PyFn")

		self.scene = QGraphicsScene(self)
		bgcolor = QApplication.palette().color(QPalette.Window)
		self.scene.setBackgroundBrush(QBrush(bgcolor, Qt.SolidPattern))

		self.view = QGraphicsView(self)
		self.view.setScene(self.scene)
		self.view.setRenderHint(QPainter.Antialiasing)
		self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
		self.setCentralWidget(self.view)
		self.view.setAcceptDrops(1)

		self.nodesEditor = QNodesEditor(self)
		self.nodesEditor.callBack = self.dropAdd
		self.nodesEditor.install(self.scene)

		
		s=QNESysBlock(None)
		self.scene.addItem(s)
		s.addPort('Start', 0, QNEPort.NamePort)		
		s.addOutputPort('');

		s=QNESysBlock(None)
		self.scene.addItem(s)
		s.addPort('End', 0, QNEPort.NamePort)		
		s.addInputPort('');
		s.setPos(160,0)

	def dropAdd(self, eve):
		sourceWidget = eve.source()
		sourceItems = sourceWidget.selectedItems()[0]		
		self.addFnBlock(sourceItems.text(0), eve.scenePos().x(), eve.scenePos().y())
		

	def addFn(self):
		actingButton = self.sender()
		self.addFnBlock(actingButton.text())

	def addFnBlock(self, fnName, xpos=10, ypos=10):
		fn=fnName
		args=self.fnCls.getArguments(fn)
		block = QNEBlock(None)
		self.scene.addItem(block)
		block.addPort(fn, 0, QNEPort.NamePort)
		block.addInputPort("")
		for eachArg in args:
			block.addInputPort(eachArg)
		block.addOutputPort("return");
		block.setPos(xpos,ypos)		

