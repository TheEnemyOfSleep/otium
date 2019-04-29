import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QMenuBar, QStatusBar
from PySide2.QtCore import Qt
from PySide2 import QtGui

import interface

__author__ = 'TEOS'
__version__ = '0.0.0'


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.menuBar = QMenuBar(self)

        # flags = Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint
        flags = Qt.FramelessWindowHint

        self.setCentralWidget(interface.MainInterface(self, app))
        self.setWindowFlags(flags)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    root = MainWindow()
    root.show()
    sys.exit(app.exec_())
