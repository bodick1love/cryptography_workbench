from PyQt5.Qt import *
from PyQt5 import uic
from src.modules.Signature import Signer

import os
import time
from datetime import datetime


class SignatureUI(QWidget):
    def __init__(self, stackedWidget):
        super().__init__()
        uic.loadUi("E:/nulp/3/1/tzi/myApp/src/ui/signature.ui", self)
        self.stackedWidget = stackedWidget

        self.FilePathErrorText = "Validation Error: One of provided file paths isn't correct."

        key_path = "E:/nulp/3/1/tzi/myApp/keys/key.pem"
        if not os.path.exists(key_path):
            key = Signer.generateKey()
            file = open(key_path, "wb")
            file.write(key.export_key())
            file.close()

        self.my_signer = Signer(key_path)

        self.pathValidation = {
            self.keyPath: True,
            self.filePath: True,
            self.signaturePath: True
        }

        self.keyPath.textChanged.connect(lambda: self.validatePath(self.keyPath))
        self.filePath.textChanged.connect(lambda: self.validatePath(self.filePath))
        self.signaturePath.textChanged.connect(lambda: self.validatePath(self.signaturePath))

        self.keyPath.textChanged.connect(self.changeKey)

        self.fileDialogButton1.clicked.connect(lambda: self.openFileDialog(self.fileDialogButton1))
        self.fileDialogButton2.clicked.connect(lambda: self.openFileDialog(self.fileDialogButton2))
        self.fileDialogButton3.clicked.connect(lambda: self.openFileDialog(self.fileDialogButton3))

        self.signMessageButton.clicked.connect(self.signMessage)
        self.signButton.clicked.connect(self.sign)
        self.verifyButton.clicked.connect(self.verify)
        self.generateButton.clicked.connect(self.generateKey)
        self.saveButton.clicked.connect(self.save)
        self.clearButton.clicked.connect(self.output.clear)
        self.backButton.clicked.connect(self.goBack)

    def signMessage(self):
        msg = self.message.text().encode()
        result = self.my_signer.sign(msg)

        self.output.setText(str(result))

    def sign(self):
        if False in self.pathValidation.values():
            self.showMessageBox(self.FilePathErrorText)
            return

        QCoreApplication.processEvents()  # update graphic interface
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))  # set waiting cursor
        time.sleep(0.2)  # time delay to illustrate new generation

        file = open(self.filePath.text(), "rb")
        data = file.read()
        file.close()

        signature = self.my_signer.sign(data)

        dt = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        file_path = f"E:/nulp/3/1/tzi/myApp/output/signed-{dt}.bin"
        with open(file_path, "wb") as file:
            file.write(signature)
            file.close()

        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
        self.showMessageBox(f"Signature saved into {file_path}", "Info")

    def verify(self):
        if False in self.pathValidation.values():
            self.showMessageBox(self.FilePathErrorText)
            return

        QCoreApplication.processEvents()  # update graphic interface
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))  # set waiting cursor
        time.sleep(0.2)  # time delay to illustrate new generation

        file = open(self.filePath.text(), "rb")
        data = file.read()
        file.close()

        signature_path = self.signaturePath.text()
        signature = open(signature_path, "rb").read()

        verified = self.my_signer.verify(data, signature)

        output = "File verified successfully." if verified else "File verification failed."
        self.output.setText(output)

        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

    def generateKey(self):
        QCoreApplication.processEvents()  # update graphic interface
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))  # set waiting cursor

        key = self.my_signer.generateKey()
        dt = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        file_path = f"E:/nulp/3/1/tzi/myApp/keys/key-{dt}.pem"
        with open(file_path, "wb") as file:
            file.write(key.export_key())
            file.close()

        QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

        self.showMessageBox(f"Key saved into {file_path}", title="Info")

    def save(self):
        output = self.output.toPlainText()
        dt = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        file_path = f"E:/nulp/3/1/tzi/myApp/output/signature_output-{dt}.txt"
        with open(file_path, "w") as file:
            file.write(output)
            file.close()
        self.showMessageBox(f"Output saved into {file_path}", title="Info")

    def validatePath(self, lineEdit):
        file_path = lineEdit.text()
        if not os.path.exists(file_path):
            self.pathValidation[lineEdit] = False
            lineEdit.setStyleSheet("border: 2px solid red;")
        else:
            self.pathValidation[lineEdit] = True
            lineEdit.setStyleSheet("")

    def changeKey(self):
        key_path = self.keyPath.text()
        try:
            self.my_signer.setKey(key_path)
        except ValueError:
            self.showMessageBox("Provided file isn't suitable.", "Error")

    def openFileDialog(self, button):
        matchingLine = {
            self.fileDialogButton1: self.keyPath,
            self.fileDialogButton2: self.filePath,
            self.fileDialogButton3: self.signaturePath,
        }

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Виберіть файл", "", "All Files (*);;Text Files (*.txt)",
                                                   options=options)
        if file_name:
           matchingLine[button].setText(file_name)

    def showMessageBox(self, msg, title="Error", icon=QMessageBox.Information):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.setIcon(icon)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg_box.exec_()

    def goBack(self):
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))