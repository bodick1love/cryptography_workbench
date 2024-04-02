from PyQt5.Qt import *
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
import os
import hashlib
import time

from src.modules.Hasher import Hasher


class HasherUI(QWidget):
    def __init__(self, stackedWidget):
        super().__init__()
        uic.loadUi("E:/nulp/3/1/tzi/myApp/src/ui/hash.ui", self)
        self.ValidationErrorText = "Validation Error: The file does not exist."
        self.LimitationErrorText = "Limitation Error: The file size exceeds 5 MB."

        self.stackedWidget = stackedWidget

        self.hasher = Hasher()

        self.valid = True

        self.inputPath.textChanged.connect(self.validate)

        self.chooseFile.clicked.connect(self.openFileDialog)
        self.backButton.clicked.connect(self.goBack)
        self.clearButton.clicked.connect(self.clear)
        self.hashButton.clicked.connect(self.hash)
        self.checkButton.clicked.connect(self.check)

    def hash(self):
        if not self.valid:
            self.showErrorBox(self.ValidationErrorText)
            return
        if os.path.getsize(self.inputPath.text()) > 5 * 2 ** 20:
            self.showErrorBox(self.LimitationErrorText)
            return

        self.clear()
        QCoreApplication.processEvents()  # update graphic interface

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))  # set waiting cursor
        time.sleep(0.5)  # time delay to illustrate new generation

        output1 = self.hasher.hash(Hasher.toByteArray(self.inputPath.text()))
        self.output1.setText(output1)

        with open(self.inputPath.text(), "rb") as file:
            data = file.read()
            output2 = hashlib.md5()
            output2.update(data)
            self.output2.setText(output2.hexdigest())

        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))  # set default cursor
        return output1, output2

    def check(self):
        output1, output2 = self.hash()

        if output1 == self.ownHash.text():
            self.output1.setText("File integrity verified: The hash of the input file matches the expected hash.")
        else:
            self.output1.setText("Hash mismatch: The computed hash does not match the provided hash.")

        if output2 == self.ownHash.text():
            self.output2.setText("File integrity verified: The hash of the input file matches the expected hash.")
        else:
            self.output2.setText("Hash mismatch: The computed hash does not match the provided hash.")

    def validate(self):
        if os.path.isfile(self.inputPath.text()):
            self.valid = True
            self.inputPath.setStyleSheet("")
        else:
            self.valid = False
            self.inputPath.setStyleSheet("border: 2px solid red;")

    def openFileDialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Виберіть файл", "", "All Files (*);;Text Files (*.txt)",
                                                   options=options)
        if file_name:
            self.inputPath.setText(file_name)

    def showErrorBox(self, msg):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setText(msg)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg_box.exec_()

    def clear(self):
        self.output1.setText("")
        self.output2.setText("")

    def goBack(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))