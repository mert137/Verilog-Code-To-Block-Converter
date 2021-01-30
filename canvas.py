# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPolygon
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt

class Canvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 600, 400)

        self.in_order = 0
        self.out_order = 0
        self.inout_order = 0

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
            for i in r.port_list:
                if i.port_type == 'input':
                    i.points = [r.rect_begin + QtCore.QPoint(int(-r.Tri_In_H), int(r.Tri_In_F * i.in_order)),
                                r.rect_begin + QtCore.QPoint(0, int(r.Tri_In_F / 2 + r.Tri_In_F * i.in_order)),
                                r.rect_begin + QtCore.QPoint(int(-r.Tri_In_H),
                                                             int(r.Tri_In_F + r.Tri_In_F * i.in_order))]
                    qp.drawText(r.rect_begin + QtCore.QPoint(int(-r.Tri_In_H), int(r.Tri_In_F * i.in_order)),
                                i.text)  # Write the port name
                elif i.port_type == 'output':
                    i.points = [r.rect_end + QtCore.QPoint(int(r.Tri_In_H),
                                                           int(-r.Tri_In_F / 2 - r.Tri_In_F * i.out_order)),
                                r.rect_end + QtCore.QPoint(0, int(-r.Tri_In_F - r.Tri_In_F * i.out_order)),
                                r.rect_end + QtCore.QPoint(0, int(- r.Tri_In_F * i.out_order))]
                    qp.drawText(r.rect_end + QtCore.QPoint(int(r.Tri_In_H),
                                                           int(-r.Tri_In_F / 2 - r.Tri_In_F * i.out_order)),
                                i.text)  # Write the port name
                elif i.port_type == 'inout':
                    i.points = [r.rect_begin + QtCore.QPoint(int(-r.Tri_In_H), int(r.Tri_In_F * i.inout_order)),
                                r.rect_begin + QtCore.QPoint(0, int(r.Tri_In_F / 2 + r.Tri_In_F * i.inout_order)),
                                r.rect_begin + QtCore.QPoint(int(-r.Tri_In_H),
                                                             int(r.Tri_In_F + r.Tri_In_F * i.inout_order)),
                                r.rect_begin + QtCore.QPoint(int(-2 * r.Tri_In_H),
                                                             int(r.Tri_In_F / 2 + r.Tri_In_F * i.inout_order))]
                    qp.drawText(r.rect_begin + QtCore.QPoint(int(-r.Tri_In_H), int(r.Tri_In_F * i.inout_order)),
                                i.text)  # Write the port name
                i.set_polygon()
                qp.drawPolygon(i.polygon)

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
        contextMenu = QMenu(self)

        # Add Input Port action is used to add input port to both code and block
        inputAction = contextMenu.addAction("Add Input Port")
        # Add Output Port action is used to add output port to both code and block
        outputAction = contextMenu.addAction("Add Output Port")
        # Add Inout Port action is used to add inout port to both code and block
        inoutAction = contextMenu.addAction("Add Inout Port")

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        if action == inputAction:
            self.draw_input(self.rect_list[-1], "input_port_1")
        elif action == outputAction:
            self.draw_output(self.rect_list[-1], "output_port_1")
        elif action == inoutAction:
            self.draw_inout(self.rect_list[-1], "inout_port_1")

    def draw_input(self, module, text):
        tempClass = Port()
        tempClass.port_type = 'input'
        tempClass.points = \
            [
                module.rect_begin + QtCore.QPoint(int(-module.Tri_In_H), int(module.Tri_In_F * tempClass.in_order)),
                module.rect_begin + QtCore.QPoint(0, int(module.Tri_In_F / 2 + module.Tri_In_F * tempClass.in_order)),
                module.rect_begin + QtCore.QPoint(int(-module.Tri_In_H),
                                                  int(module.Tri_In_F + module.Tri_In_F * tempClass.in_order))
            ]
        tempClass.set_polygon()
        tempClass.text = text
        tempClass.in_order = self.in_order
        self.in_order = self.in_order + 1
        module.port_list.append(tempClass)

    def draw_output(self, module, text):
        tempClass = Port()
        tempClass.port_type = 'output'
        tempClass.points = \
            [
                module.rect_end + QtCore.QPoint(int(module.Tri_In_H),
                                                int(-module.Tri_In_F / 2 - module.Tri_In_F * tempClass.out_order)),
                module.rect_end + QtCore.QPoint(0, int(-module.Tri_In_F - module.Tri_In_F * tempClass.out_order)),
                module.rect_end + QtCore.QPoint(0, int(- module.Tri_In_F * tempClass.out_order))
            ]
        tempClass.set_polygon()
        tempClass.text = text
        tempClass.out_order = self.out_order
        self.out_order = self.out_order + 1
        module.port_list.append(tempClass)

    def draw_inout(self, module, text):
        tempClass = Port()
        tempClass.port_type = 'inout'
        tempClass.points = \
            [
                module.rect_begin + QtCore.QPoint(int(-module.Tri_In_H), int(module.Tri_In_F * tempClass.in_order)),
                module.rect_begin + QtCore.QPoint(0, int(module.Tri_In_F / 2 + module.Tri_In_F * tempClass.in_order)),
                module.rect_begin + QtCore.QPoint(int(-module.Tri_In_H),
                                                  int(module.Tri_In_F + module.Tri_In_F * tempClass.in_order)),
                module.rect_begin + QtCore.QPoint(int(-2 * module.Tri_In_H),
                                                  int(module.Tri_In_F / 2 + module.Tri_In_F * tempClass.in_order))
            ]
        tempClass.set_polygon()
        tempClass.text = text
        tempClass.inout_order =  self.in_order   # self.inout_order
        self.in_order = self.in_order + 1        # self.inout_order = self.inout_order + 1
        module.port_list.append(tempClass)


class Port:
    def __init__(self):
        self.points = [QtCore.QPoint()]
        self.polygon = QPolygon(self.points)
        self.text = ''
        self.in_order = 0
        self.out_order = 0
        self.inout_order = 0
        self.set_polygon()
        self.port_type = 'empty'

    def set_polygon(self):
        self.polygon = QPolygon(self.points)


class Module:
    def __init__(self):
        self.rect_begin = QtCore.QPoint()  # Module rectangle top left corner
        self.rect_end = QtCore.QPoint()  # Module rectangle bottom right corner
        self.Tri_In_H = 20
        self.Tri_In_F = 2 * self.Tri_In_H
        self.center_text = ''  # Module name in the center of rectangle
        self.first_drawn = 0
        self.port_list = []
