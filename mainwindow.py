"""
Initialize the main window, containing the manga catalog
"""

import sys
from PyQt5.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.CMS_MW_init()

    def CMS_MW_init(self):
        self.resize(300,300)
        self.move(300,300)
        self.setWindowTitle('Tittle test')
        self.CMS_MW_addButtons()
        self.show()

    def CMS_MW_addButtons(self):
        b = QPushButton('Boton', self)
        b.setToolTip('test')
        b.resize(b.sizeHint())
        b.move(50,50)

    def CMS_centerToScreen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
