from PyQt5.Qt import *
from PyQt5 import uic
from src.modules.AsymmetricCoder import AsymmetricCoder

import time
from datetime import datetime
import os


class AsymmetricCoderUI(QWidget):
    def __init__(self, stackedWidget):
        super().__init__()
        uic.loadUi("E:/nulp/3/1/tzi/myApp/src/ui/asymmetric_coder.ui", self)
        self.stackedWidget = stackedWidget

        self.ConfigurationErrorText = "Configuration file is corrupted or contains errors."
        self.FilePathErrorText = "Validation Error: The file does not exist."
        self.FileWeightErrorText = "Limitation Error: The file size exceeds 5 MB."
        self.TypeErrorText = "Type Error: Provided file isn't rsa code."

        args = [61, 53]
        self.my_coder = AsymmetricCoder(*args)

        self.path_validation = True

        self.edit_path.textChanged.connect(self.validate_path)
        self.fileButton.clicked.connect(self.openFileDialog)
        self.encryptButton.clicked.connect(lambda: self.processFile(self.encryptButton))
        self.decryptButton.clicked.connect(lambda: self.processFile(self.decryptButton))
        self.backButton.clicked.connect(self.goBack)

    def processFile(self, button):
        if not self.path_validation:
            self.showMessageBox(self.FilePathErrorText)
            return

        path = self.edit_path.text()
        if os.path.getsize(path) > 5 * 2**20:
            self.showMessageBox(self.FileWeightErrorText)
            return

        QCoreApplication.processEvents()  # update graphic interface
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))  # set waiting cursor
        time.sleep(0.2)  # time delay to illustrate new generation

        input_file = open(path, 'rb')
        file_content = input_file.read()

        o_f = "E:/nulp/3/1/tzi/myApp/output/"
        dt = datetime.now()  # using timestamp to give unique name to each file
        ending = dt.strftime("%d-%m-%Y-%H-%M-%S")

        if button == self.encryptButton:
            o_f += "asymmetric_code-"
            cipher = self.my_coder.encryption(file_content)
            binary_cipher = b''.join(x.to_bytes(4, 'big') for x in cipher)
            extension = os.path.splitext(path)[1]
            extension_len = len(extension)
            output = b'\rsa-code' + extension_len.to_bytes(1, byteorder="big") + extension.encode() + binary_cipher
            extension = ".bin"
        else:
            o_f += "asymmetric_decode-"
            if len(file_content) < 8 or file_content[:8] != b'\rsa-code':
                self.showMessageBox(self.TypeErrorText)
                QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
                return
            extension_len = int.from_bytes(file_content[8:9], byteorder="big")
            extension = file_content[9:9+extension_len].decode()
            byte_cipher = file_content[9+extension_len:]
            cipher = [int.from_bytes(byte_cipher[i:i+4], 'big') for i in range(0, len(byte_cipher), 4)]
            output = self.my_coder.decryption(cipher)

        with open(o_f + ending + extension, 'wb') as output_file:
            output_file.write(output)

        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

        self.showMessageBox("Output saved into " + o_f + ending + extension, "Success")

    def validate_path(self):
        path = self.edit_path.text()
        if os.path.exists(path):
            self.path_validation = True
            self.edit_path.setStyleSheet("")
        else:
            self.path_validation = False
            self.edit_path.setStyleSheet("border: 2px solid red;")

    def showMessageBox(self, msg, title="Error", icon=QMessageBox.Information):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.setIcon(icon)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg_box.exec_()

    def openFileDialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Виберіть файл", "", "All Files (*);;Text Files (*.txt)",
                                                   options=options)
        if file_name:
            self.edit_path.setText(file_name)

    def goBack(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))