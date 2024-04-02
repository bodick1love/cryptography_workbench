import os

from PyQt5.Qt import *
from PyQt5 import uic

from datetime import datetime
import time

from src.modules.Generator import Generator


class GenUI(QWidget):
    def __init__(self, stackedWidget):
        super().__init__()
        uic.loadUi("E:/nulp/3/1/tzi/myApp/src/ui/gen.ui", self)
        self.ValidationErrorText = "Input Value Error: The provided input cannot be processed due to its format. " \
                                   "Please check the input and try again."
        self.LimitationErrorText = "Please ensure that the value of this parameter meets the specified requirements."
        self.ConfigurationErrorText = "Configuration file is corrupted or contains errors."

        self.stackedWidget = stackedWidget

        m, a, c, x0 = ["2^14 - 1", "6^5", "5", "32"]
        if os.path.exists("E:/nulp/3/1/tzi/myApp/input/gen_input.txt"):
            with open("E:/nulp/3/1/tzi/myApp/input/gen_input.txt", "r") as input_file:
                lines = [line.strip() for line in input_file.readlines()]
            m, a, c, x0 = lines
        else:
            self.showErrorBox(self.ConfigurationErrorText)

        lines = [line.replace("^", "**") for line in lines]
        args = ["2**14 - 1", "6**5", "5", "32"]
        try:
            args = list(map(eval, lines))
        except Exception as error:
            self.showErrorBox(self.ConfigurationErrorText)

        self.my_gen = Generator(args[0], args[1], args[2], args[3])

        self.validation_states = {
            self.edit_m: True,
            self.edit_a: True,
            self.edit_c: True,
            self.edit_x0: True,
            self.edit_n: True
        }

        self.edit_m.setText(m)
        self.edit_a.setText(a)
        self.edit_c.setText(c)
        self.edit_x0.setText(x0)

        self.edit_m.textChanged.connect(lambda: self.validate(self.edit_m))  # validate on changing
        self.edit_a.textChanged.connect(lambda: self.validate(self.edit_a))
        self.edit_c.textChanged.connect(lambda: self.validate(self.edit_c))
        self.edit_x0.textChanged.connect(lambda: self.validate(self.edit_x0))

        self.edit_n.setText("1000")
        self.edit_n.textChanged.connect(lambda: self.validate(self.edit_n))

        self.generateButton.clicked.connect(self.generate)
        self.clearButton.clicked.connect(self.output.clear)
        self.backButton.clicked.connect(self.goBack)

        self.line_setters = {
            self.edit_m: self.my_gen.setM,
            self.edit_a: self.my_gen.setA,
            self.edit_c: self.my_gen.setC,
            self.edit_x0: self.my_gen.setX0
        }

    def generate(self):
        self.output.clear()
        QCoreApplication.processEvents()    # update graphic interface
        if any(value is False for value in self.validation_states.values()):  # validation block
            self.showErrorBox(self.ValidationErrorText)
            return

        n = eval(self.edit_n.text())    # limitation block
        if not 1 < n < 10**6:
            self.showErrorBox(self.LimitationErrorText)
            return

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))  # set waiting cursor
        time.sleep(0.5)  # time delay to illustrate new generation

        x = self.my_gen.generate(n)
        T = Generator.countT(x)
        output = " ".join(map(str, x))
        output += "\nPeriod: " + str(T)
        self.output.setText(output)

        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))     # set default cursor

        if self.checkBox.isChecked():
            dt = datetime.now()  # using timestamp to give unique name to each file
            ending = dt.strftime("%d-%m-%Y-%H-%M-%S")
            output_file = open("output/gen-" + ending + ".txt", "w")
            output_file.write(output)

    def validate(self, input_field):
        text = input_field.text().replace("^", "**")
        try:
            val = eval(text)
            if input_field in self.line_setters:
                setter = self.line_setters[input_field]
                setter(val)
            self.validation_states[input_field] = True
            input_field.setStyleSheet("")
            return True
        except (SyntaxError, NameError, TypeError):
            self.validation_states[input_field] = False
            input_field.setStyleSheet("border: 2px solid red;")
            return False

    def showErrorBox(self, msg):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setText(msg)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg_box.exec_()

    def goBack(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))