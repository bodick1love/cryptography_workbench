from PyQt5 import uic
from PyQt5.QtWidgets import *

from src.widgets.GenUI import GenUI
from src.widgets.HasherUI import HasherUI
from src.widgets.CoderUI import CoderUI
from src.widgets.AsymmetricCoderUI import AsymmetricCoderUI
from src.widgets.SignatureUI import SignatureUI


class HomeUI(QWidget):
    def __init__(self, stackedWidget):
        super(HomeUI, self).__init__()
        uic.loadUi("E:/nulp/3/1/tzi/myApp/src/ui/home.ui", self)
        self.stackedWidget = stackedWidget

        self.gen = None
        self.hasher = None
        self.coder = None
        self.asymmetricCoder = None
        self.signature = None

        self.genButton.clicked.connect(self.setGenUI)
        self.hasherButton.clicked.connect(self.setHasherUI)
        self.coderButton.clicked.connect(self.setCoderUI)
        self.assymetricCoderButton.clicked.connect(self.setAsymmetricCoderUI)
        self.signatureButton.clicked.connect(self.setSignatureUI)

        self.show()

    def setGenUI(self):
        if not self.gen:
            self.gen = GenUI(self.stackedWidget)
            self.stackedWidget.addWidget(self.gen)
        self.stackedWidget.setCurrentWidget(self.gen)

    def setHasherUI(self):
        if not self.hasher:
            self.hasher = HasherUI(self.stackedWidget)
            self.stackedWidget.addWidget(self.hasher)
        self.stackedWidget.setCurrentWidget(self.hasher)

    def setCoderUI(self):
        if not self.coder:
            self.coder = CoderUI(self.stackedWidget)
            self.stackedWidget.addWidget(self.coder)
        self.stackedWidget.setCurrentWidget(self.coder)

    def setAsymmetricCoderUI(self):
        if not self.asymmetricCoder:
            self.asymmetricCoder = AsymmetricCoderUI(self.stackedWidget)
            self.stackedWidget.addWidget(self.asymmetricCoder)
        self.stackedWidget.setCurrentWidget(self.asymmetricCoder)

    def setSignatureUI(self):
        if not self.signature:
            self.signature = SignatureUI(self.stackedWidget)
            self.stackedWidget.addWidget(self.signature)
        self.stackedWidget.setCurrentWidget(self.signature)