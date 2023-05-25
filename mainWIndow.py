from PyQt5 import QtCore, QtGui, QtWidgets, uic


class MainWIndow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWIndow,self).__init__()
        uic.loadUi("./Main.ui", self)