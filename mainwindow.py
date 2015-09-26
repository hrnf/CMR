"""
Initialize the main window, containing the manga catalog
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.CMR_MW_init()

    def CMR_MW_init(self):
        # Instantiate central widget for layouts
        self.setCentralWidget(QWidget())

        # Define widgets
        canvas = QGraphicsView()
        nameLabel = QLabel('Name:')
        nameField = QLineEdit()
        okButton = QPushButton('Ok')

        # Define actions and toolbar
        searchAction = QAction('Show SearchBox', self)
        searchAction.setShortcut('Alt+1')

        self.toolbar = QToolBar('Toolbar')
        self.toolbar.addAction(searchAction)

        # Define searchbox
        searchBox = QGridLayout()
        searchBox.addWidget(nameLabel, 0, 0)
        searchBox.addWidget(nameField, 0, 1)
        searchBox.addWidget(okButton, 1, 1)

        # Insert searchbox and canvas into main layout
        mainBox = QHBoxLayout(self.centralWidget())
        mainBox.insertLayout(0, searchBox)
        mainBox.insertWidget(1, canvas, 1)

        # Set window
        self.setGeometry(300, 300, 700, 400)
        self.setWindowTitle('Community\'s Manga Reader')
        self.show()

    def CMR_centerToScreen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
