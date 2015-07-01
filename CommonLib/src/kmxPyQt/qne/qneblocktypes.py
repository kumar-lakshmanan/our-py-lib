
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QPainterPath, QPen,
    QFontMetrics)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsPathItem)

from kmxPyQt.qne.qnebasicblock import QNEBasicBlock

class QNBlockStart(QNEBasicBlock):
    (Type) = (QGraphicsItem.UserType + 0)

    def __init__(self):
        super(QNEBasicBlock, self).__init__(None)
        
        #Style
        self._color
        self._outlineColor
        self._textColor
        self._connectorColor
        self._connectorOutlineColor
        self._selectedColor
        self._selectedOutlineColor
        self._selectedTextColor
        
        self._name="Start"


class QNEBasicBlock(QGraphicsPathItem):
    (Type) = (QGraphicsItem.UserType +3)

    def __init__(self, name, tag):
        super(QNEBasicBlock, self).__init__(None)

        path = QPainterPath()
        path.addRoundedRect(-50, -15, 100, 30, 5, 5);
        self.setPath(path)
        self.setPen(QPen(Qt.darkGreen))
        self.setBrush(Qt.green)
        self.setOpacity(0.9)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemDoesntPropagateOpacityToChildren)

        self.horzMargin = 20
        self.vertMargin = 5
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
            painter.setPen(QPen(Qt.darkYellow))
            painter.setBrush(Qt.yellow)
        else:
            painter.setPen(QPen(Qt.darkGreen))
            painter.setBrush(Qt.green)

        painter.drawPath(self.path())


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

    def type(self):
        return self.Type
