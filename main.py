import sys
import traceback
import re

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMenuBar, QAction, QHBoxLayout, QTabWidget, QTextEdit

from canvas import Canvas, Module

title = "GUI PROJECT"

# : MaınWındow class: Thıs class has so and so components and ıt's prımary objectıve is designing a GUI based application.


# purpose of each class creates the main window.
class MainWindow(QWidget):
    def __init__(self):
        try:
            super().__init__()
            self.setupUI()
        except Exception as e:
            print(e)
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)

    def setupUI(self):
        self.canvas = Canvas()

        self.setWindowTitle(title)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)

        tabLayout = QVBoxLayout()
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Add tabs
        # This tabs add code editor and rtl design.
        self.tabs.addTab(self.tab1, "Code Editor")
        self.tabs.addTab(self.tab2, "RTL Design")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.textEdit = QTextEdit()
        self.tab1.layout.addWidget(self.textEdit)
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(self.canvas, 16)
        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        tabLayout.addWidget(self.tabs)

        menubar = QMenuBar()
        mainLayout.addWidget(menubar)

        # Under file menu, Save action is used to save block design and written code
        saveAction = QAction("&Save...", self)
        saveAction.triggered.connect(self.save)

        # Under file menu, Load action is used to load block design or written code
        loadAction = QAction("&Load...", self)
        loadAction.triggered.connect(self.load)

        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(saveAction)
        fileMenu.addAction(loadAction)

        # Under Generate menu, Generate Block action is used to compile code and generate block
        generateBlockAction = QAction("&Generate Block...", self)
        generateBlockAction.triggered.connect(self.generate_block)

        # Under Generate menu, Generate Code action is used to compile block and generate code
        generateCodeAction = QAction("&Generate Code...", self)
        generateCodeAction.triggered.connect(self.generate_code)

        generateMenu = menubar.addMenu("&Generate")
        generateMenu.addAction(generateBlockAction)
        generateMenu.addAction(generateCodeAction)

        appLayout = QHBoxLayout()
        appLayout.setContentsMargins(10, 0, 10, 10)

        appLayout.addLayout(tabLayout, 10)
        mainLayout.addLayout(appLayout, 1)
        self.setLayout(mainLayout)

    def save(self):
        pass

    def load(self):
        pass

    def draw_block(self):
        pass

    def generate_block(self):
        my_text = self.textEdit.toPlainText()
        lines = my_text.splitlines()
        if "" in lines:
            lines.remove("")
        self.canvas.rect_list = []
        temp_rect_list = []

        i = -1

        forbidden_module_names = ["input", "output", "inout", "module", "endmodule", ""]
        while i != len(lines) - 1:
            if self.canvas.error == 1:
                print('error')
                break
            i = i + 1

            result = re.split(r'\Amodule ', lines[i])       # Split start
            if "" in result:
                result.remove("")
                result = re.split('(?:\(|\040\()\Z', result[0])       # Split end
                if "" in result:
                    result.remove("")
                    if not (re.search('\W', result[0]) or (result[0] not in self.canvas.forbidden_module_names)):  # Search for non-word character
                        tempModule = Module()
                        tempModule.rect_begin = QtCore.QPoint(100, 100)
                        tempModule.rect_end = QtCore.QPoint(300, 300)
                        tempModule.center_text = result[0]
                        temp_rect_list.append(tempModule)
                        forbidden_module_names.append(tempModule.center_text)
                        while 1:
                            if self.canvas.error == 1:
                                print('error')
                                break
                            i = i + 1
                            result = re.split('(,|\);)\Z', lines[i])
                            while "" in result:
                                result.remove("")
                            if result[-1] != ');':
                                result = re.split('\A(?:input |output |inout )', result[0])
                                if "" in result:
                                    result.remove("")
                                    if not (re.search('\W', result[0]) or result[0] == ""):  # Search for non-word character
                                        x = [s.strip() for s in lines[i].split(' ')]
                                        if 'input' == x[0]:
                                            if result[0] not in tempModule.forbidden_words:
                                                self.canvas.add_input(temp_rect_list[-1], result[0])
                                            else:
                                                print('error')
                                                self.canvas.error = 1
                                                break
                                        elif 'output' == x[0]:
                                            if result[0] not in tempModule.forbidden_words:
                                                self.canvas.add_output(temp_rect_list[-1], result[0])
                                            else:
                                                print('error')
                                                self.canvas.error = 1
                                                break
                                        elif 'inout' == x[0]:
                                            if result[0] not in tempModule.forbidden_words:
                                                self.canvas.add_inout(temp_rect_list[-1], result[0])
                                            else:
                                                print('error')
                                                self.canvas.error = 1
                                                break
                                        else:
                                            print('error')
                                            self.canvas.error = 1
                                            break
                                    else:
                                        self.canvas.error = 1
                            else:
                                i = i + 1
                                x = [s.strip() for s in lines[i].split(' ')]
                                if 'endmodule' == x[0]:
                                    temp_rect_list[-1].update()
                                    break
                                else:
                                    print('error')
                                    self.canvas.error = 1
                                    break

                            if self.canvas.error == 1:
                                print('error')
                                self.canvas.error = 1
                                break
                    else:
                        print("error")
                        self.canvas.error = 1
                        break
                else:
                    print("error")
                    self.canvas.error = 1
                    break
            else:
                print("error")
                self.canvas.error = 1
                break
        if self.canvas.error == 0:
            for i in temp_rect_list:
                self.canvas.rect_list.append(i)
            self.canvas.forbidden_module_names = forbidden_module_names.copy()
        else:
            self.canvas.error = 0

    def generate_code(self):
        self.canvas.update_code()
        self.textEdit.setText(self.canvas.code_string)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    w = MainWindow()
    w.showMaximized()

    sys.exit(app.exec_())
