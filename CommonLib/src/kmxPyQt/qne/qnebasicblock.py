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
from PyQt5.QtGui import (QBrush, QColor, QPainter, QPainterPath, QPen, QFontMetrics)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsPathItem, QGraphicsTextItem)

from kmxPyQt.qne.qneport import QNEPort
from kmxPyQt.qne.qneblockconnector import QNEBlockConnector


class QNEBasicBlock(QGraphicsPathItem):

    def __init__(self, Scene, Name):
        super(QNEBasicBlock, self).__init__(None)
        
        self.Name=Name

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemDoesntPropagateOpacityToChildren)
        
        self._color=Qt.green
        self._outlineColor=Qt.darkGreen
        self._textColor=Qt.black
        self._connectorColor=Qt.gray
        self._connectorOutlineColor=Qt.black
        self._selectedColor=Qt.yellow
        self._selectedOutlineColor=Qt.darkYellow
        self._selectedTextColor=Qt.darkRed   

        path = QPainterPath()
        path.addRoundedRect(-50, -15, 100, 30, 5, 5);
                        
        self.setPath(path)
        self.setPen(QPen(self._outlineColor))
        self.setBrush(self._color)
        self.setOpacity(0.9)

        self.horzMargin = 20
        self.vertMargin = 5
        self.width = self.horzMargin
        self.height = self.vertMargin
        
        self.label = QGraphicsTextItem(self)
        self.label.setPlainText(self.Name)             
        self.label.setDefaultTextColor(self._textColor)  
        self.label.setPos(-4-3-self.label.boundingRect().width(), -self.label.boundingRect().height()/2);
        
        self.inputConnector = QNEBlockConnector(self)
        self.inputConnector.setIsOutput(False)
        self.inputConnector.setNEBlock(self)

        fontmetrics = QFontMetrics(Scene.font());
        width = fontmetrics.width(self.Name)
        height = fontmetrics.height()
        if width > self.width - self.horzMargin:
            self.width = width + self.horzMargin
        self.height += height

#         path = QPainterPath()
#         path.addRoundedRect(-self.width/2, -self.height/2, self.width, self.height, 5, 5)
#         self.setPath(path)

        y = -self.height / 2 + self.vertMargin + self.inputConnector.radius()
        self.inputConnector.setPos(self.width/2 + self.inputConnector.radius(), y)
        
        
    def paint(self, painter, option, widget):
        if self.isSelected():
            painter.setPen(QPen(self._selectedOutlineColor))
            painter.setBrush(self._selectedColor)
        else:
            painter.setPen(QPen(self._color))
            painter.setBrush(self._outlineColor)

        painter.drawPath(self.path())
        
        
    def __del__(self):
        #print("Del QNEBlock")

        for port in self.ports():
            for connection in port.connections():
                connection.port1().removeConnection(connection)
                connection.port2().removeConnection(connection)
                self.scene().removeItem(connection)
            self.scene().removeItem(port)


    def addPort(self, name, isOutput = False, flags = 0, ptr = None):
        port = QNEPort(self)
        port.setName(name)
        port.setIsOutput(isOutput)
        port.setNEBlock(self)
        port.setPortFlags(flags)
        port.setPtr(ptr)

        fontmetrics = QFontMetrics(self.scene().font());
        width = fontmetrics.width(name)
        height = fontmetrics.height()
        if width > self.width - self.horzMargin:
            self.width = width + self.horzMargin
        self.height += height

        path = QPainterPath()
        path.addRoundedRect(-self.width/2, -self.height/2, self.width, self.height, 5, 5)
        self.setPath(path)

        y = -self.height / 2 + self.vertMargin + port.radius()
        for port_ in self.childItems():
            if port_.type() != QNEPort.Type:
                continue

            if port_.isOutput():
                port_.setPos(self.width/2 + port.radius(), y)
            else:
                port_.setPos(-self.width/2 - port.radius(), y)
            y += height;

        return port


    def addInputPort(self, name):
        return self.addPort(name, False)


    def addOutputPort(self, name):
        return self.addPort(name, True)


    def addInputPorts(self, names):
        ports=[]
        for name in names:
            ports.append(self.addInputPort(name))
        return ports


    def addOutputPorts(self, names):
        ports=[]
        for name in names:
            ports.append(self.addOutputPort(name))
        return ports

    def ports(self):
        result = []
        for port_ in self.childItems():
            if port_.type() == QNEPort.Type:
                result.append(port_)

        return result
