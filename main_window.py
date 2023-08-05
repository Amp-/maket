import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSerialPort import QSerialPort,QSerialPortInfo
from PyQt5.QtCore import QIODevice
from pyqtgraph import PlotWidget
import time


open_list = []
close_list = []
portList = []
status = 0
count = 0
stop = 0
baudrate = 9600
serial = QSerialPort()
serial.setBaudRate(baudrate)
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())

cor_x = list(range(100))
cor_y = [0] * 100

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
        self.label_color.setText("Denied")
        self.checkBox_door_status = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_door_status.setGeometry(QtCore.QRect(290, 74, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_door_status.setFont(font)
        self.checkBox_door_status.setObjectName("checkBox_door_status")
        self.checkBox_door_status.clicked.connect(self.checkbox_state_control)
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
        serial.setPortName(self.com_list.currentText())
        serial.open(QIODevice.ReadWrite)

        self.serial_ready_read()
        self.buttonOk.setEnabled(False)
        self.buttonCancel.setEnabled(True)

    def measurement(self):#рассчет экранировки
        global stop
        print(f'Открытая дверь {len(open_list)}')
        print(f'Закрытая дверь {len(close_list)}')
        if len(open_list) == 10 and len(close_list)==10:
            close_list_int = [int(x) for x in close_list] #преобразование списка str->int
            open_list_int = [int(x) for x in open_list]
            random_close_list = random.sample(close_list_int,5)#выбираем 5 случайных чисел из списка
            random_open_list = random.sample(open_list_int, 5)
            close_list_for = sum(random_close_list)/len(random_close_list)#считаем среднее арифмитическое пяти случаных чисел
            open_list_for = sum(random_open_list) / len(random_open_list)
            result = close_list_for - open_list_for #считаем разницу
            if result > 0:#bизменить значение на знаение из стоек
                stop = 1
                self.label_color.setStyleSheet("background-color: green;")
                self.label_color.setText("Allowed")
            else:
                stop = 1
                print(f'Экранировка нарушена')

            print(f'Результат{result}')


    def onRead(self):
        rx = serial.readLine()
        string_rx = str(rx, "UTF-8").strip()
        if (string_rx != 'Empty' and string_rx != 'Fail'):
            if (len(string_rx)) < 5 and stop == 0:
                    self.add_data_in_list(string_rx)

    def add_data_in_list(self,data):
        self.lcd.display(data)
        self.plot_graph(val=data)
        self.measurement()
        if status == 0:
            open_list.append(data)
            if len(open_list) == 11:
                open_list.pop(0)
        if status == 1:
            close_list.append(data)
            if len(close_list) == 11:
                close_list.pop(0)
    def onClose(self):
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

    def checkbox_state_control(self):
        global status, stop
        if self.checkBox_door_status.isChecked():
            self.checkBox_door_status.setText("Открыть дверь")
            close_list.clear()
            status = 1
        else:
            self.checkBox_door_status.setText("Закрыть дверь")
            open_list.clear()
            close_list.clear()
            status = 0
            stop = 0
            self.label_color.setStyleSheet("background-color: red;")
            self.label_color.setText("Denied")



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Макет - 1"))
        self.groupBox.setTitle(_translate("MainWindow", "Приемник"))
        self.buttonOk.setText(_translate("MainWindow", "Ok"))
        self.buttonCancel.setText(_translate("MainWindow", "Cancel"))
        self.label_delay.setText(_translate("MainWindow", "Уровень"))
        self.label_status.setText(_translate("MainWindow", "Статус"))
        self.checkBox_door_status.setText(_translate("MainWindow", "Закрыть дверь"))




