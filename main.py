import sys
import traceback

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMenuBar, QAction, QHBoxLayout, QTabWidget, QTextEdit

from canvas import Canvas, Module

title = "GUI PROJECT"

# Explaın the flow of the code
# Explaın the purpose of each class
# Example: MaınWındow class: Thıs class has so and so components and ıt's prımary objectıve ıs ...


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
        # Explaın WHY do we add tabs?
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
        self.canvas.rect_list = []

        for line in lines:
            x = [s.strip() for s in line.split(' ')]
            if 'module' in x:
                tempModule = Module()
                tempModule.rect_begin = QtCore.QPoint(100, 100)
                tempModule.rect_end = QtCore.QPoint(200, 200)
                tempModule.center_text = x[1]
                self.canvas.rect_list.append(tempModule)
            if 'input' in x:
                self.canvas.draw_input(self.canvas.rect_list[-1], x[1])
            if 'output' in x:
                self.canvas.draw_output(self.canvas.rect_list[-1], x[1])
            if 'inout' in x:
                self.canvas.draw_inout(self.canvas.rect_list[-1], x[1])

    def generate_code(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    w = MainWindow()
    w.showMaximized()

    sys.exit(app.exec_())
