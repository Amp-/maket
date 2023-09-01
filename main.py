"""

"""

import os
import random
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets, QtSerialPort
from Communication import Com


baudRate=9600
portName = "/dev/ttyACM0"
portList = Com.com_list()
open_list = []
close_list = []
status = 0
count = 0
stop = 0

pg.mkQApp()

## Define main window class from template
path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, 'Main_1.ui')
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)

com = Com(baudRate=baudRate, portName=portName, serialPort=QtSerialPort.QSerialPort())
class MainWindow(TemplateBaseClass):
    def __init__(self):
        TemplateBaseClass.__init__(self)
        # Create the main window
        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        self.ui.buttonOk.clicked.connect(self.on_toggled)
        self.ui.buttonCancel.clicked.connect(self.close)
        self.ui.com_list.addItems(portList)
        self.serial = com.serial
        self.serial.readyRead.connect(lambda: self.parse())
        self.ui.checkBox_door_status.clicked.connect(self.checkbox_state_control)
        self.output_te = []
        self.show()

    def parse(self):
            data = com.read()
            if len(data) <= 4 and stop==0:
                self.output_te.append(int(data))
                self.ui.graph.plot(self.output_te)
                self.add_data_in_list(data)

    def on_toggled(self, checked):
        self.ui.buttonOk.setText("Disconnect" if checked else "Connect")
        self.serial.setPortName(self.ui.com_list.currentText())
        com.togle()

    def close(self):
        com.close()

    def measurement(self):  # рассчет экранировки
        global stop
        print(f'Открытая дверь {len(open_list)}')
        print(f'Закрытая дверь {len(close_list)}')
        if len(open_list) == 10 and len(close_list) == 10:
            close_list_int = [int(x) for x in close_list]  # преобразование списка str->int
            open_list_int = [int(x) for x in open_list]
            random_close_list = random.sample(close_list_int, 5)  # выбираем 5 случайных чисел из списка
            random_open_list = random.sample(open_list_int, 5)
            close_list_for = sum(random_close_list) / len(
                random_close_list)  # считаем среднее арифмитическое пяти случаных чисел
            open_list_for = sum(random_open_list) / len(random_open_list)
            result = close_list_for - open_list_for  # считаем разницу
            if result > 0:  # bизменить значение на знаение из стоек
                stop = 1
                self.ui.label_color.setStyleSheet("background-color: green;")
                self.ui.label_color.setText("Allowed")
            else:
                stop = 1
                self.ui.label_color.setStyleSheet("background-color: red;")

                print(f'Экранировка нарушена')

            print(f'Результат{result}')

    def add_data_in_list(self,data):
        self.ui.lcd.display(data)
        self.measurement()
        if status == 0:
            open_list.append(data)
            if len(open_list) == 11:
                open_list.pop(0)
        if status == 1:
            close_list.append(data)
            if len(close_list) == 11:
                close_list.pop(0)

    def checkbox_state_control(self):
        global status, stop
        if self.ui.checkBox_door_status.isChecked():
            self.ui.checkBox_door_status.setText("Открыть дверь")
            close_list.clear()
            status = 1
        else:
            self.ui.checkBox_door_status.setText("Закрыть дверь")
            open_list.clear()
            close_list.clear()
            status = 0
            stop = 0
            self.ui.label_color.setStyleSheet("background-color: red;")
            self.ui.label_color.setText("Denied")
            self.ui.graph.clear()
            self.output_te.clear()


if __name__ == '__main__':
    win = MainWindow()
    pg.exec()
