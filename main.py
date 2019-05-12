import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QMenuBar
from PySide2.QtCore import Qt, QSize
import interface

__author__ = 'TEOS'
__version__ = '0.0.0'


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.menuBar = QMenuBar(self)

        # flags = Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint
        flags = Qt.FramelessWindowHint

        self.setGeometry(0, 0, 1120, 635)
        self.setMinimumSize(QSize(1120, 635))
        self.setCentralWidget(interface.MainInterface(self, app))
        # self.setWindowFlags(flags)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    root = MainWindow()
    root.show()
    sys.exit(app.exec_())
