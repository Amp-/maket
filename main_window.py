import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSerialPort import QSerialPort,QSerialPortInfo
from PyQt5.QtCore import QIODevice
from pyqtgraph import PlotWidget

serial = QSerialPort()#инициализауия com
serial.setBaudRate(9600)#инициализауия com
portList = []
ports = QSerialPortInfo().availablePorts() #список доспутных портов
for port in ports:
    portList.append(port.portName())

cor_x = list(range(100))
cor_y = [0] * 100
count = 0
class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(682, 660)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 641, 151))
        self.groupBox.setObjectName("groupBox")
        self.com_list = QtWidgets.QComboBox(self.groupBox)
        self.com_list.setGeometry(QtCore.QRect(12, 32, 86, 25))
        self.com_list.setObjectName("com_list")
        self.com_list.addItems(portList)
        self.buttonOk = QtWidgets.QPushButton(self.groupBox)
        self.buttonOk.setGeometry(QtCore.QRect(104, 32, 80, 25))
        self.buttonOk.setObjectName("buttonOk")
        self.buttonOk.clicked.connect(self.opnet_serial)
        self.buttonCancel = QtWidgets.QPushButton(self.groupBox)
        self.buttonCancel.setGeometry(QtCore.QRect(190, 32, 80, 25))
        self.buttonCancel.setObjectName("buttonCancel")
        self.buttonCancel.setEnabled(False)
        self.buttonCancel.clicked.connect(self.onClose)
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(16, 68, 111, 61))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_delay = QtWidgets.QLabel(self.widget)
        self.label_delay.setObjectName("label_delay")
        self.verticalLayout.addWidget(self.label_delay)
        self.label_status = QtWidgets.QLabel(self.widget)
        self.label_status.setObjectName("label_status")
        self.verticalLayout.addWidget(self.label_status)
        self.widget1 = QtWidgets.QWidget(self.groupBox)
        self.widget1.setGeometry(QtCore.QRect(149, 68, 121, 61))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lcd = QtWidgets.QLCDNumber(self.widget1)
        self.lcd.setFrameShape(QtWidgets.QFrame.Panel)
        self.lcd.setObjectName("lcd")
        self.verticalLayout_2.addWidget(self.lcd)
        self.label_color = QtWidgets.QLabel(self.widget1)
        self.label_color.setFrameShape(QtWidgets.QFrame.Box)
        self.label_color.setText("")
        self.label_color.setObjectName("label_color")
        self.verticalLayout_2.addWidget(self.label_color)
        self.label_color.setStyleSheet("background-color: red;")
        self.graph = PlotWidget(self.centralwidget)
        self.graph.setGeometry(QtCore.QRect(10, 190, 641, 381))
        self.graph.setObjectName("graph")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 682, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)



        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def opnet_serial(self):
        serial.setPortName(self.com_list.currentText()) #установить имя порта из списка выбранного значения com_list
        serial.open(QIODevice.ReadWrite) #открыть порт для чтения/записи
        self.serial_ready_read()
        self.buttonOk.setEnabled(False)#кнопки Ok Cancle
        self.buttonCancel.setEnabled(True)#кнопки Ok Cancle


    def onRead(self):# переписать на чтение в другом потоке
        rx = serial.readLine()
        string_rx = str(rx, "UTF-8").strip()
        if (string_rx != 'Empty' and string_rx != 'Fail'):
            if (len(string_rx)) < 5:
                self.change_color(string_rx)
                self.plot_graph(val=string_rx)
                self.lcd.display(string_rx)

    def onClose(self):# нужна ли вообще данная функция
        serial.close()

    def plot_graph(self,val):
        global cor_y, cor_x
        cor_y = cor_y[1:]
        cor_y.append(int(val))
        self.graph.clear()
        self.graph.plot(cor_x, cor_y,pen='blue')
    def serial_ready_read(self):
        if serial.isOpen():
            serial.readyRead.connect(lambda : self.onRead())

    def change_color(self,t):
        if (t != 'Empty' and t != 'Fail'):
            if(int(t)==632):
                self.label_color.setStyleSheet("background-color: green;")
                self.label_color.setText("Allowed")
            if(int(t)==634):
                self.label_color.setStyleSheet("background-color: red;")
                self.label_color.setText("Denied")

    def measurement(self):
        pass


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Макет - 1"))
        self.groupBox.setTitle(_translate("MainWindow", "Приемник"))
        self.buttonOk.setText(_translate("MainWindow", "Ok"))
        self.buttonCancel.setText(_translate("MainWindow", "Cancel"))
        self.label_delay.setText(_translate("MainWindow", "Уровень"))
        self.label_status.setText(_translate("MainWindow", "Статус"))





