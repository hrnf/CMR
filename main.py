#!/usr/bin/python
import os
from mainwindow import MainWindow

class CMR():
    userdir = os.path.expanduser("~/.CMR")

    if not os.path.exists(userdir):
        os.makedirs(userdir)
        os.makedirs(userdir+"/releases")

    MainWindow.make_list()
    mainwindow = MainWindow()
