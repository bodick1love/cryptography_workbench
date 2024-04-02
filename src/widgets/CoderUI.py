from PyQt5.Qt import *
from PyQt5 import uic
from src.modules.Coder import Coder
from src.modules.Hasher import Hasher

import time
import json
from datetime import datetime
import os


class CoderUI(QWidget):
    def __init__(self, stackedWidget):
        super().__init__()
        uic.loadUi("E:/nulp/3/1/tzi/myApp/src/ui/coder.ui", self)
        self.stackedWidget = stackedWidget
        self.ValidationErrorText = "Input Value Error: The provided input cannot be processed due to its format. " \
                                   "Please check the input and try again."
        self.LimitationErrorText = "Please ensure that the values of parameters meet the specified requirements."
        self.ConfigurationErrorText = "Configuration file is corrupted or contains errors."
        self.FilePathError = "Validation Error: The file does not exist."
        self.FileWeightError = "Limitation Error: The file size exceeds 5 MB."

        self.path_validation = True
        self.validation_states = {
            self.edit_w: True,
            self.edit_r: True,
            self.edit_b: True,
            self.edit_key: True
        }
        self.limitation_states = {
            self.edit_w: True,
            self.edit_r: True,
            self.edit_b: True
        }
        self.limitation_range = {
            self.edit_w: [16, 32, 64],
            self.edit_r: [i for i in range(255)],
            self.edit_b: [i for i in range(33)]
        }

        args = [32, 8, 16]
        if os.path.exists("E:/nulp/3/1/tzi/myApp/input/symmetric_code.json"):
            inp = open("E:/nulp/3/1/tzi/myApp/input/symmetric_code.json")
            data = json.load(inp)
            args[0] = data["w"]
            args[1] = data["r"]
            args[2] = data["b"]
        else:
            self.showMessageBox(self.ConfigurationErrorText)

        self.my_hasher = Hasher()

        key = bytearray(self.edit_key.text().encode())
        hashed_key = self.my_hasher.hash(key)
        key = bytes.fromhex(hashed_key)
        self.my_coder = Coder(key, args[0], args[1], args[2])

        self.edit_w.setText(str(args[0]))
        self.edit_r.setText(str(args[1]))
        self.edit_b.setText(str(args[2]))

        self.edit_w.textChanged.connect(lambda: self.validateParam(self.edit_w))
        self.edit_r.textChanged.connect(lambda: self.validateParam(self.edit_r))
        self.edit_b.textChanged.connect(lambda: self.validateParam(self.edit_b))

        self.edit_path.textChanged.connect(self.validatePath)
        self.edit_key.textChanged.connect(self.setKey)

        self.backButton.clicked.connect(self.goBack)
        self.fileButton.clicked.connect(self.openFileDialog)
        self.codeButton.clicked.connect(lambda: self.processFile(self.codeButton))
        self.decodeButton.clicked.connect(lambda: self.processFile(self.decodeButton))

        self.line_setters = {
            self.edit_w: self.my_coder.setW,
            self.edit_r: self.my_coder.setR,
            self.edit_b: self.my_coder.setB
        }

    def processFile(self, button):
        if False in self.validation_states.values():
            self.showMessageBox(self.ValidationErrorText)
            return
        elif False in self.limitation_states.values():
            self.showMessageBox(self.LimitationErrorText)
            return
        elif not self.path_validation:
            self.showMessageBox(self.FilePathError)
            return
        elif os.path.getsize(self.edit_path.text()) > 5 * 2 ** 20:
            self.showMessageBox(self.FileWeightError)
            return

        QCoreApplication.processEvents()  # update graphic interface
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))  # set waiting cursor
        time.sleep(0.2)  # time delay to illustrate new generation

        o_f = "E:/nulp/3/1/tzi/myApp/output/"
        dt = datetime.now()  # using timestamp to give unique name to each file
        ending = dt.strftime("%d-%m-%Y-%H-%M-%S")

        if button == self.codeButton:
            o_f += "code-"
            self.my_coder.encryptFile(self.edit_path.text(), o_f + ending + ".txt")
        elif button == self.decodeButton:
            o_f += "decode-"
            self.my_coder.decryptFile(self.edit_path.text(), o_f + ending + ".txt")

        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

        self.showMessageBox("Output saved into " + o_f + ending, "Success")

    def setKey(self):
        try:
            key = bytearray(self.edit_key.text().encode())
            self.validation_states[self.edit_key] = True

            h_key = bytes.fromhex(self.my_hasher.hash(key))
            key = h_key
            if int(self.edit_b.text()) >= 16:
                hh_key = bytes.fromhex(self.my_hasher.hash(bytearray(h_key)))
                key = hh_key + h_key
            self.my_coder.setK(key)

        except ValueError:
            self.validation_states[self.edit_key] = False

    def validateParam(self, lineEdit):
        param = lineEdit.text()
        try:
            param = eval(param)
            self.validation_states[lineEdit] = True

            # Check limitation
            self.limitation_states[lineEdit] = True if param in self.limitation_range[lineEdit] else False
            if not self.limitation_states[lineEdit]:
                raise ValueError

            if lineEdit == self.edit_b:     # Ensure that len(key) feets
                self.setKey()

            setter = self.line_setters[lineEdit]
            setter(param)
            lineEdit.setStyleSheet("")

        except (SyntaxError, NameError, TypeError, ValueError):
            self.validation_states[lineEdit] = False
            lineEdit.setStyleSheet("border: 2px solid red;")
            return False

    def validatePath(self):
        if os.path.isfile(self.edit_path.text()):
            self.path_validation = True
            self.edit_path.setStyleSheet("")
        else:
            self.path_validation = False
            self.edit_path.setStyleSheet("border: 2px solid red;")

    def openFileDialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Виберіть файл", "", "All Files (*);;Text Files (*.txt)",
                                                   options=options)
        if file_name:
            self.edit_path.setText(file_name)

    def showMessageBox(self, msg, title="Error", icon=QMessageBox.Information):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.setIcon(icon)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg_box.exec_()

    def goBack(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))