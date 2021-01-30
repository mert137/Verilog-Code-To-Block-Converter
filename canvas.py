# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPolygon
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt


class Canvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 600, 400)

        self.show()
        self.rect_list = []

        init_first_rect = Module()
        self.rect_list.append(init_first_rect)

    # All canvas painting actions are handled here.
    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
        qp.setBrush(br)

        for r in self.rect_list:
            qp.drawRect(QtCore.QRect(r.rect_begin, r.rect_end))  # Draw module rectangle
            qp.drawText((r.rect_begin + r.rect_end) / 2, r.center_text)  # Write the name of module rectangle

            # Draw input ports and their names
            in_order = 0
            out_order = 0
            inout_order = 0
            for i in r.port_list:
                if i.port_type == 'input':
                    i.points = [r.rect_begin + QtCore.QPoint(int(-r.Tri_In_H), int(r.Tri_In_F * in_order)),
                                r.rect_begin + QtCore.QPoint(0, int(r.Tri_In_F / 2 + r.Tri_In_F * in_order)),
                                r.rect_begin + QtCore.QPoint(int(-r.Tri_In_H),
                                                             int(r.Tri_In_F + r.Tri_In_F * in_order))]

                    # Write the port name
                    qp.drawText(r.rect_begin + QtCore.QPoint(5, int(r.Tri_In_F / 2 + r.Tri_In_F * in_order)), i.text)
                    in_order = in_order + 1

                elif i.port_type == 'output':
                    i.points = [r.rect_end + QtCore.QPoint(int(r.Tri_In_H + 1),
                                                           int(-r.Tri_In_F / 2 - r.Tri_In_F * out_order)),
                                r.rect_end + QtCore.QPoint(1, int(-r.Tri_In_F - r.Tri_In_F * out_order)),
                                r.rect_end + QtCore.QPoint(1, int(- r.Tri_In_F * out_order))]

                    # Write the port name
                    qp.drawText(r.rect_end + QtCore.QPoint(int(r.Tri_In_H + 5), int(-r.Tri_In_F / 2 - r.Tri_In_F * out_order)), i.text)
                    out_order = out_order + 1

                elif i.port_type == 'inout':
                    i.points = [QtCore.QPoint(int(r.rect_begin.x() - r.Tri_In_H), int(r.rect_end.y() - r.Tri_In_F - r.Tri_In_F * inout_order)),
                                QtCore.QPoint(int(r.rect_begin.x()), int(r.rect_end.y() - r.Tri_In_F / 2 - r.Tri_In_F * inout_order)),
                                QtCore.QPoint(int(r.rect_begin.x() - r.Tri_In_H), int(r.rect_end.y() - r.Tri_In_F * inout_order)),
                                QtCore.QPoint(int(r.rect_begin.x() - 2 * r.Tri_In_H), int(r.rect_end.y() - r.Tri_In_F / 2 - r.Tri_In_F * inout_order))]

                    # Write the port name
                    qp.drawText(QtCore.QPoint(int(r.rect_begin.x() + 5), int(r.rect_end.y() - r.Tri_In_F / 2 - r.Tri_In_F * inout_order)), i.text)
                    inout_order = inout_order + 1

                polygon = QPolygon(i.points)
                qp.drawPolygon(polygon)

    # When mouse is pressed, the top left corner of the rectangle being drawn is saved
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.rect_list[-1].first_drawn == 0:
                self.rect_list[-1].rect_begin = event.pos()
                self.rect_list[-1].rect_end = event.pos()
                self.update()
        # elif event.button() == Qt.RightButton:

    # When mouse is pressed and moving, the bottom right corner of the rectangle also changes and shown in screen
    def mouseMoveEvent(self, event):
        if self.rect_list[-1].first_drawn == 0:
            self.rect_list[-1].rect_end = event.pos()
            self.update()

    # After mouse has released, the bottom right corner of the rectangle is assigned and rectangle placed in screen
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.rect_list[-1].first_drawn == 0:
                self.rect_list[-1].rect_end = event.pos()
                self.rect_list[-1].first_drawn = 1
                # init_rect = Module()
                # self.rect_list.append(init_rect)
                self.update()

    def contextMenuEvent(self, event):
        for i in self.rect_list:
            if i.rect_begin.x() < event.pos().x() < i.rect_end.x() and i.rect_begin.y() < event.pos().y() < i.rect_end.y():
                contextMenu = QMenu(self)

                # Add Input Port action is used to add input port to both code and block
                inputAction = contextMenu.addAction("Add Input Port")
                # Add Output Port action is used to add output port to both code and block
                outputAction = contextMenu.addAction("Add Output Port")
                # Add Inout Port action is used to add inout port to both code and block
                inoutAction = contextMenu.addAction("Add Inout Port")

                action = contextMenu.exec_(self.mapToGlobal(event.pos()))

                if action == inputAction:
                    self.add_input(i, "input_port_1")
                elif action == outputAction:
                    self.add_output(i, "output_port_1")
                elif action == inoutAction:
                    self.add_inout(i, "inout_port_1")

    def add_input(self, module, text):
        tempClass = Port()
        tempClass.port_type = 'input'
        tempClass.text = text
        module.port_list.append(tempClass)

    def add_output(self, module, text):
        tempClass = Port()
        tempClass.port_type = 'output'
        tempClass.text = text
        module.port_list.append(tempClass)

    def add_inout(self, module, text):
        tempClass = Port()
        tempClass.port_type = 'inout'
        tempClass.text = text
        module.port_list.append(tempClass)


class Port:
    def __init__(self):
        self.points = [QtCore.QPoint()]
        self.polygon = QPolygon(self.points)
        self.text = ''
        self.port_type = 'empty'


class Module:
    def __init__(self):
        self.rect_begin = QtCore.QPoint()   # Module rectangle top left corner
        self.rect_end = QtCore.QPoint()     # Module rectangle bottom right corner
        self.Tri_In_H = 20
        self.Tri_In_F = 2 * self.Tri_In_H
        self.center_text = ''               # Module name in the center of rectangle
        self.first_drawn = 0
        self.port_list = []
