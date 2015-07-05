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
from PyQt5.QtGui import (QBrush, QColor, QPainter, QPainterPath, QPen,
    QFontMetrics)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsPathItem)


from kmxPyQt.qne import qneport
from kmxPyQt.kmxNodeGraph.kmxNodeBlock import kmxNodeBlock


class QNEBlock(QGraphicsPathItem):
    (Type) = (QGraphicsItem.UserType +3)

    def __init__(self, parent):
        super(QNEBlock, self).__init__(parent)

        path = QPainterPath()
        path.addRoundedRect(-50, -15, 100, 30, 5, 5);
        #path.addRoundedRect(-50, -15, 100, 30, 5, 5);

        self.kmxNodeBlock = kmxNodeBlock()
        
        self.nodeColor = Qt.green
        self.nodeTextColor = Qt.blue
        
        self.nodeSelectedColor = Qt.yellow
        self.nodeSelectedTextColor = Qt.blue    
        
        
        self.setPath(path)
        self.setPen(QPen(Qt.darkGreen))
        self.setBrush(self.nodeColor)
        self.setOpacity(0.9)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemDoesntPropagateOpacityToChildren)

        self.horzMargin = 60
        self.vertMargin = 25
        self.width = self.horzMargin
        self.height = self.vertMargin
        


    def __del__(self):
        #print("Del QNEBlock")

        for port in self.ports():
            for connection in port.connections():
                connection.port1().removeConnection(connection)
                connection.port2().removeConnection(connection)
                self.scene().removeItem(connection)
            self.scene().removeItem(port)


    def paint(self, painter, option, widget):
        if self.isSelected():
            painter.setPen(QPen(Qt.darkGreen))
            painter.setBrush(self.nodeSelectedColor)
            for each in self.ports():
                if (each.portName()):
                    each.label.setDefaultTextColor(self.nodeSelectedTextColor)
        else:
            painter.setPen(QPen(Qt.darkGreen))
            painter.setBrush(self.nodeColor)
            for each in self.ports():
                if (each.portName()):
                    each.label.setDefaultTextColor(self.nodeTextColor)
                                                   
        painter.drawPath(self.path())


    def addPort(self, name, isOutput = False, flags = 0, ptr = None):
        port = qneport.QNEPort(self)
        port.textColor=self.nodeTextColor
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
        if(flags):
            self.height += height

        path = QPainterPath()
        path.addRoundedRect(-self.width/2, -8, self.width, self.height, 5, 5)        
        self.setPath(path)

        y = -self.height / 2 + self.vertMargin + port.radius()
        for port_ in self.childItems():
            if port_.type() != qneport.QNEPort.Type:
                continue

            if port_.isOutput():
                port_.setPos(self.width/2 + port.radius(), y)
            else:
                if(port_.portName()):
                    width = fontmetrics.width(port_.portName())                     
                    port_.setPos(-((self.width/4)+(width/4)), y)
                else:
                    port_.setPos(-self.width/2 - port.radius(), y)
                    
            if(flags):                    
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


    def clone(self):
        block = QNEBlock(None)
        self.scene().addItem(block)

        for port_ in self.childItems():
            block.addPort(port_.portName(), port_.isOutput(), port_.portFlags(), port_.ptr())

        return block


    def ports(self):
        result = []
        for port_ in self.childItems():
            if port_.type() == qneport.QNEPort.Type:
                result.append(port_)

        return result

    def type(self):
        return self.Type
