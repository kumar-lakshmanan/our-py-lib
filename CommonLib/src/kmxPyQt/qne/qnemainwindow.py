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

from kmxPyQt.qne.qnodeseditor import QNodesEditor
from kmxPyQt.qne.qneblock import QNEBlock
from kmxPyQt.qne.qneport import QNEPort
from kmxPyQt.qne.qneconnection import QNEConnection

class QNEMainWindow(QMainWindow):
    def __init__(self, parent):
        super(QNEMainWindow, self).__init__(parent)

        quitAct = QAction("&Quit", self, shortcut="Ctrl+Q",
            statusTip="Exit the application", triggered=self.close)

        addAct = QAction("&Add", self, statusTip="Add a block", triggered=self.addBlock)

        readAct = QAction("&Read", self, statusTip="Read", triggered=self.readNodes)

        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(addAct)
        fileMenu.addAction(readAct)
        fileMenu.addSeparator()
        fileMenu.addAction(quitAct)

        #self.setMinimumSize(640,480)
        self.setWindowTitle("Node Editor")

        self.scene = QGraphicsScene(self)
        bgcolor = QApplication.palette().color(QPalette.Window)
        self.scene.setBackgroundBrush(QBrush(bgcolor, Qt.SolidPattern))

        self.view = QGraphicsView(self)
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setCentralWidget(self.view)

        self.nodesEditor = QNodesEditor(self)
        self.nodesEditor.install(self.scene)

        block = QNEBlock(None)
        self.scene.addItem(block)
        block.addPort("test", 0, QNEPort.NamePort)
        #block.addPort("TestBlock", 0, QNEPort.TypePort)
        p1 = block.addInputPort("in1");
        block.addInputPort("in2");
        block.addInputPort("in3");
        block.addOutputPort("out1");
        block.addOutputPort("out2");
        block.addOutputPort("out3");


        
        block2 = QNEBlock(None)
        self.scene.addItem(block2)
        block2.addPort("mytest", 0, QNEPort.NamePort)
        #block.addPort("TestBlock", 0, QNEPort.TypePort)
        block2.addInputPort("in1");
        block2.addInputPort("in2");
        block2.addInputPort("in3");
        p2 = block2.addOutputPort("out1");
        
        connection = QNEConnection(None)
        self.scene.addItem(connection)
        
        connection.setPort1(p1)
        connection.setPort2(p2)
        connection.setPos1(block.scenePos())
        connection.setPos2(block2.scenePos())
        connection.updatePath()
        #p1.addConnection(connection)
        
        block = block.clone()
        block.setPos(150,0)

        block = block.clone()
        block.setPos(150,150)
        
        block2.setPos(125,120)
        

    def addBlock(self):
        import random
        import math

        block = QNEBlock(None)

        self.scene.addItem(block)
        names = ["Vin", "Voutsadfasdf", "Imin", "Imax", "mul", "add", "sub", "div", "Conv", "FFT"]
        for i in range(0,math.floor(random.uniform(3,8))):
            block.addPort(random.choice(names), random.random()>0.5)
        block.setPos(self.view.sceneRect().center().toPoint())

    def readNodes(self):
        pass
    
    
    

widget = QNEMainWindow(None)
widget.show()



