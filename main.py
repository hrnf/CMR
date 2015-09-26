#!/usr/bin/python3
# -*- coding: utf-8 -*-

from mainwindow import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
