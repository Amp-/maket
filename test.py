import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("main_window.py",self)
        self.show()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec()

