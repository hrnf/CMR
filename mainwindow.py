"""
Initialize the main window, containing the manga catalog
"""

import sys
from PyQt5.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.CMR_MW_init()

    def CMR_MW_init(self):
        canvas = QGraphicsView()
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addwidget(okButton)
        buttonsLayout.addwidget(cancelButton)

        mainLayout = QVBoxLayout()
        mainLayout.addStretch(1)
        mainLayout.addWidget(canvas)
        mainLayout.addLayout(buttonsLayout)

        self.setLayout(mainLayout)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Community\'s Manga Reader')
        self.show()

    def CMR_centerToScreen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
