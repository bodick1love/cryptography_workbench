from PyQt5.QtWidgets import *
import sys

from src.widgets.HomeUI import HomeUI


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 700)
        self.setWindowTitle("Information security ToolKit")

        self.stackedWidget = QStackedWidget(self)
        self.home_ui = HomeUI(self.stackedWidget)

        self.stackedWidget.addWidget(self.home_ui)
        self.setCentralWidget(self.stackedWidget)
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()