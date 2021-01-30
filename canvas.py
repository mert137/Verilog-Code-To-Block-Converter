# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPolygon
from PyQt5.QtWidgets import QMenu,  QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt


class Canvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 600, 400)

        self.show()
        self.rect_list = []
        self.code_string = ""

        init_first_rect = Module()
        self.rect_list.append(init_first_rect)

        self.intersect_module = 1

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
            for i in r.in_port_list:
                i.points = [r.rect_begin + QtCore.QPoint(int(-r.Tri_In_H), int(r.Tri_In_F * in_order)),
                            r.rect_begin + QtCore.QPoint(0, int(r.Tri_In_F / 2 + r.Tri_In_F * in_order)),
                            r.rect_begin + QtCore.QPoint(int(-r.Tri_In_H),
                                                         int(r.Tri_In_F + r.Tri_In_F * in_order))]

                # Write the port name
                qp.drawText(r.rect_begin + QtCore.QPoint(5, int(r.Tri_In_F / 2 + r.Tri_In_F * in_order)), i.text)
                in_order = in_order + 1

                polygon = QPolygon(i.points)
                qp.drawPolygon(polygon)

            for i in r.inout_port_list:
                i.points = [QtCore.QPoint(int(r.rect_begin.x() - r.Tri_In_H), int(r.rect_end.y() - r.Tri_In_F - r.Tri_In_F * inout_order)),
                            QtCore.QPoint(int(r.rect_begin.x()), int(r.rect_end.y() - r.Tri_In_F / 2 - r.Tri_In_F * inout_order)),
                            QtCore.QPoint(int(r.rect_begin.x() - r.Tri_In_H), int(r.rect_end.y() - r.Tri_In_F * inout_order)),
                            QtCore.QPoint(int(r.rect_begin.x() - 2 * r.Tri_In_H), int(r.rect_end.y() - r.Tri_In_F / 2 - r.Tri_In_F * inout_order))]

                # Write the port name
                qp.drawText(QtCore.QPoint(int(r.rect_begin.x() + 5), int(r.rect_end.y() - r.Tri_In_F / 2 - r.Tri_In_F * inout_order)), i.text)
                inout_order = inout_order + 1

                polygon = QPolygon(i.points)
                qp.drawPolygon(polygon)

            for i in r.out_port_list:
                i.points = [r.rect_end + QtCore.QPoint(int(r.Tri_In_H + 1),
                                                       int(r.Tri_In_F / 2 - (r.rect_end.y() - r.rect_begin.y()) + r.Tri_In_F * out_order)),
                            r.rect_end + QtCore.QPoint(1, int(-(r.rect_end.y() - r.rect_begin.y()) + r.Tri_In_F * out_order)),
                            r.rect_end + QtCore.QPoint(1, int(r.Tri_In_F - (r.rect_end.y() - r.rect_begin.y()) + r.Tri_In_F * out_order))]

                # Write the port name
                qp.drawText(r.rect_end + QtCore.QPoint(int(r.Tri_In_H + 5), int(-(r.rect_end.y() - r.rect_begin.y()) + r.Tri_In_F / 2 + r.Tri_In_F * out_order)), i.text)
                out_order = out_order + 1

                polygon = QPolygon(i.points)
                qp.drawPolygon(polygon)


    # When mouse is pressed, the top left corner of the rectangle being drawn is saved
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.rect_list[-1].first_drawn == 0:
                for i in self.rect_list:
                    if i.rect_begin.x() < event.pos().x() < i.rect_end.x() and i.rect_begin.y() < event.pos().y() < i.rect_end.y():
                        self.intersect_module = 0
                if self.intersect_module == 1:
                    self.rect_list[-1].rect_begin = event.pos()
                    self.rect_list[-1].rect_end = event.pos()
                    self.update()
        # elif event.button() == Qt.RightButton:

    # When mouse is pressed and moving, the bottom right corner of the rectangle also changes and shown in screen
    def mouseMoveEvent(self, event):
        if self.rect_list[-1].first_drawn == 0:
            for i in self.rect_list:
                if i.rect_begin.x() < event.pos().x() < i.rect_end.x() and i.rect_begin.y() < event.pos().y() < i.rect_end.y():
                    self.intersect_module = 0
            if self.intersect_module == 1:
                self.rect_list[-1].rect_end = event.pos()
                self.update()

    # After mouse has released, the bottom right corner of the rectangle is assigned and rectangle placed in screen
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.rect_list[-1].first_drawn == 0:
                for i in self.rect_list:
                    if i.rect_begin.x() < event.pos().x() < i.rect_end.x() and i.rect_begin.y() < event.pos().y() < i.rect_end.y():
                        self.intersect_module = 0
                if self.intersect_module == 1:
                    self.rect_list[-1].rect_end = event.pos()
                    self.rect_list[-1].first_drawn = 1
                    self.update()
            self.intersect_module = 1

    def contextMenuEvent(self, event):
        empty_area = 1
        for i in self.rect_list:
            if i.rect_begin.x() < event.pos().x() < i.rect_end.x() and i.rect_begin.y() < event.pos().y() < i.rect_end.y():
                empty_area = 0
                contextMenu = QMenu(self)

                # Add Input Port action is used to add input port to both code and block
                portAction = contextMenu.addAction("Add Port")
                renameAction = contextMenu.addAction("Rename Module")

                action = contextMenu.exec_(self.mapToGlobal(event.pos()))

                if action == portAction:
                    self.myshow = InputDialog(i)
                    self.myshow.setWindowTitle("Add Port")
                    self.myshow.show()
                elif action == renameAction:
                    self.myshow = Rename(i)
                    self.myshow.setWindowTitle("Rename Module")
                    self.myshow.show()

        if empty_area == 1:
            contextMenu = QMenu(self)

            # Add Input Port action is used to add input port to both code and block
            addModuleAction = contextMenu.addAction("Add Module")

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))
            if action == addModuleAction:
                tempModule = Module()
                tempModule.center_text = 'case_block'
                self.rect_list.append(tempModule)

    def add_input(self, module, text):
        tempClass = Port()
        tempClass.port_type = 'input'
        tempClass.text = text
        module.in_port_list.append(tempClass)
        module.update()

    def add_output(self, module, text):
        tempClass = Port()
        tempClass.port_type = 'output'
        tempClass.text = text
        module.out_port_list.append(tempClass)
        module.update()

    def add_inout(self, module, text):
        tempClass = Port()
        tempClass.port_type = 'inout'
        tempClass.text = text
        module.inout_port_list.append(tempClass)
        module.update()

    def update_code(self):
        self.code_string = ""
        for i in self.rect_list:
            for j in i.module_string_list:
                self.code_string = self.code_string + j


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
        self.in_port_list = []
        self.out_port_list = []
        self.inout_port_list = []
        self.module_string_list = []

    def update_string(self):
        self.module_string_list = []
        self.module_string_list.append("module ")
        self.module_string_list.append(self.center_text )
        self.module_string_list.append("(" + "\n")

        for j in self.in_port_list:
            self.module_string_list.append("input ")
            self.module_string_list.append(j.text + ",\n")

        for j in self.out_port_list:
            self.module_string_list.append("output ")
            self.module_string_list.append(j.text + ",\n")

        for j in self.inout_port_list:
            self.module_string_list.append("inout ")
            self.module_string_list.append(j.text + ",\n")

        self.module_string_list.append(");" + "\n")
        self.module_string_list.append("endmodule" + "\n\n")

    def update(self):
        temp_left = self.Tri_In_F
        temp_right = self.Tri_In_F
        if self.Tri_In_F * (len(self.in_port_list) + len(self.inout_port_list)) + 1 >= self.rect_end.y() - self.rect_begin.y():
            temp_left = int((self.rect_end.y() - self.rect_begin.y()) / ((len(self.in_port_list) + len(self.inout_port_list)) + 1))

        if self.Tri_In_F * len(self.out_port_list) + 1 >= self.rect_end.y() - self.rect_begin.y():
            temp_right = int((self.rect_end.y() - self.rect_begin.y()) / (len(self.out_port_list) + 1))

        self.Tri_In_F = min(temp_left, temp_right)
        self.Tri_In_H = int(self.Tri_In_F / 2)
        self.update_string()

class Rename(QtWidgets.QWidget):
    def __init__(self, module):
        super(Rename, self).__init__()

        self.module = module

        self.nametextbox = QtWidgets.QLineEdit(self)
        self.setButton = QPushButton('Okay', self)
        self.setButton.clicked.connect(self.okay_button)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.nametextbox,   0, 0)
        mainLayout.addWidget(self.setButton,     0, 1)

        mainLayout.setRowMinimumHeight(2, 40)
        mainLayout.setRowStretch(3, 1)
        mainLayout.setColumnMinimumWidth(1, 200)
        mainLayout.setSpacing(5)

        self.setLayout(mainLayout)

    def okay_button(self):
        self.module.center_text = self.nametextbox.text()
        self.module.update()
        self.close()


class InputDialog(QtWidgets.QWidget):
    def __init__(self, module):
        super(InputDialog, self).__init__()

        self.port = Port()
        self.module = module

        label1 = QLabel("Signal Type")
        label2 = QLabel("Port Name")
        label3 = QLabel("Signal Length")

        self.port_type = "input"
        self.combo_box = QtWidgets.QComboBox(self)              # creating a combo box widget
        self.combo_box.setGeometry(200, 150, 150, 30)           # setting geometry of combo box
        self.combo_box.addItems(["Input", "Output", "Inout"])   # adding list of items to combo box
        self.combo_box.activated.connect(self.determine_type)   # adding action to combo box

        self.nametextbox = QtWidgets.QLineEdit(self)
        self.veclentextbox = QtWidgets.QLineEdit(self)

        self.setButton = QPushButton('Add', self)
        self.setButton.clicked.connect(self.add_port)


        mainLayout = QGridLayout()
        mainLayout.addWidget(label1,             0, 0)
        mainLayout.addWidget(label2,             0, 1)
        mainLayout.addWidget(label3,             0, 2)

        mainLayout.addWidget(self.combo_box,     1, 0)
        mainLayout.addWidget(self.nametextbox,   1, 1)
        mainLayout.addWidget(self.veclentextbox, 1, 2)

        mainLayout.addWidget(self.setButton,     2, 2)

        mainLayout.setRowMinimumHeight(2, 40)
        mainLayout.setRowStretch(3, 1)
        mainLayout.setColumnMinimumWidth(1, 200)
        mainLayout.setSpacing(5)

        self.setLayout(mainLayout)

    def add_port(self):
        self.port.port_type = self.port_type
        self.port.text = self.nametextbox.text() + "(" + self.veclentextbox.text() + " downto 0" + ")"
        if self.port_type == "output":
            self.module.out_port_list.append(self.port)
        elif self.port_type == "input":
            self.module.in_port_list.append(self.port)
        else:
            self.module.inout_port_list.append(self.port)
        self.module.update()
        self.close()

    def determine_type(self):
        if str(self.combo_box.currentText()) == "Input":
            self.port_type = 'input'
        elif str(self.combo_box.currentText()) == "Output":
            self.port_type = 'output'
        elif str(self.combo_box.currentText()) == "Inout":
            self.port_type = 'inout'
