import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QStatusBar
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet
import serial
import serial.tools.list_ports

from src import Menu, SM2En, SM2De, SM2S, SM2V, WriteKey, SM4De, SM4En

class WriteKey(WriteKey.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(WriteKey, self).__init__()
        self.setupUi(self)  # 初始化
        self.ser = serial.Serial()
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_data)
        self.uart_open()
        self.pushButton_return.clicked.connect(self.close)
        self.pushButton_start.clicked.connect(self.send_data)

    def uart_open(self):
        self.ser.port = "COM5"
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = 'N'
        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "错误", "无法打开此串口！")
            return

        if self.ser.isOpen():
            # 打开串口接收定时器，周期为10ms
            self.timer.start(5)

    def send_data(self):
        if self.ser.isOpen():
            data = self.plainTextEdit.toPlainText()
            data_bytes = self.str2byte(data)
            data_len = int(len(data) / 2).to_bytes(2, byteorder='big', signed=False)
            algorithm_bytes = 0x01.to_bytes(1, byteorder="big", signed=False)

            send_data = algorithm_bytes + data_len + data_bytes
            self.ser.write(send_data)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                QMessageBox.warning(self, "错误", "接收数据错误")
            if num > 0:
                data = self.ser.read(num)
                if data == b'END':
                    QMessageBox.information(self, "提示", "注充完成")
                    self.close()

    def str2byte(self, data):
        data_arr = bytearray(data.encode("ASCII"))  # 将str类型转换为可变的bytearray
        data_int = list(data_arr)  # 再将其转换为int类型的List
        data_ok = list()  # 用来存放经过缩短后的数据
        # 将‘0’->0;'f'->15
        for index in range(len(data_int)):
            if data_int[index] >= 48 and data_int[index] <= 57:
                data_int[index] -= 0x30
            if data_int[index] >= 97 and data_int[index] <= 102:
                data_int[index] -= 0x57
        # 缩短数据
        for i in range(0, len(data_int), 2):
            data_ok.append(data_int[i] << 4 | data_int[i + 1])
        return bytes(data_ok)

    def closeEvent(self, event):
        self.ser.close()
        event.accept()


class SM2En(SM2En.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(SM2En, self).__init__()
        self.setupUi(self)  # 初始化
        self.ser = serial.Serial()
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_data)
        self.uart_open()
        self.pushButton_return.clicked.connect(self.close)
        self.pushButton_start.clicked.connect(self.send_data)
        self.datalen = 0
        self.numreceive = 0

    def uart_open(self):
        self.ser.port = "COM5"
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = 'N'
        try:
            self.ser.open()
        except:
            QMessageBox.warning(self, "错误", "无法打开此串口！")
            return

        if self.ser.isOpen():
            # 打开串口接收定时器，周期为10ms
            self.timer.start(5)

    def send_data(self):
        if self.ser.isOpen():
            data = self.plainTextEdit.toPlainText()
            data_bytes = self.str2byte(data)
            data_len = int(len(data) / 2).to_bytes(2, byteorder='big', signed=False)
            algorithm_bytes = 0x04.to_bytes(1, byteorder="big", signed=False)

            send_data = algorithm_bytes + data_len + data_bytes
            self.ser.write(send_data)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                QMessageBox.warning(self, "错误", "接收数据错误")
            if num > 0:
                if self.numreceive == 0:
                    # 获取到text光标
                    textCursor = self.textBrowser.textCursor()
                    # 滚动到底部
                    textCursor.movePosition(textCursor.End)
                    # 设置光标到text中去
                    self.textBrowser.setTextCursor(textCursor)
                    data = self.ser.read(num)
                    self.textBrowser_mode.insertPlainText(data[0].to_bytes(1, byteorder='big', signed=False).hex())
                    self.textBrowser_datalen.insertPlainText(data[1:3].hex())
                    self.textBrowser.insertPlainText(data[3:].hex())
                    self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部
                    self.numreceive = num
                    self.datalen = int(data[1:3].hex(), 16)
                else:
                    textCursor = self.textBrowser.textCursor()
                    # 滚动到底部
                    textCursor.movePosition(textCursor.End)
                    # 设置光标到text中去
                    self.textBrowser.setTextCursor(textCursor)
                    data = self.ser.read(num)
                    self.textBrowser.insertPlainText(data.hex())
                    self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部
                    self.numreceive += num
                    if self.numreceive >= self.datalen + 3:
                        self.datalen = 0
                        self.numreceive = 0

    def str2byte(self, data):
        data_arr = bytearray(data.encode("ASCII"))  # 将str类型转换为可变的bytearray
        data_int = list(data_arr)  # 再将其转换为int类型的List
        data_ok = list()  # 用来存放经过缩短后的数据
        # 将‘0’->0;'f'->15
        for index in range(len(data_int)):
            if data_int[index] >= 48 and data_int[index] <= 57:
                data_int[index] -= 0x30
            if data_int[index] >= 97 and data_int[index] <= 102:
                data_int[index] -= 0x57
        # 缩短数据
        for i in range(0, len(data_int), 2):
            data_ok.append(data_int[i] << 4 | data_int[i + 1])
        return bytes(data_ok)

    def closeEvent(self, event):
        self.ser.close()
        event.accept()


class SM2De(SM2De.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(SM2De, self).__init__()
        self.setupUi(self)  # 初始化
        self.ser = serial.Serial()
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_data)
        self.uart_open()
        self.pushButton_return.clicked.connect(self.close)
        self.pushButton_start.clicked.connect(self.send_data)
        self.datalen = 0
        self.numreceive = 0

    def uart_open(self):
        self.ser.port = "COM5"
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = 'N'
        try:
            self.ser.open()
        except:
            QMessageBox.warning(self, "错误", "无法打开此串口！")
            return

        if self.ser.isOpen():
            # 打开串口接收定时器，周期为10ms
            self.timer.start(5)

    def send_data(self):
        if self.ser.isOpen():
            data = self.plainTextEdit.toPlainText()
            data_bytes = self.str2byte(data)
            data_len = int(len(data) / 2).to_bytes(2, byteorder='big', signed=False)
            algorithm_bytes = 0x05.to_bytes(1, byteorder="big", signed=False)

            send_data = algorithm_bytes + data_len + data_bytes
            self.ser.write(send_data)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                QMessageBox.warning(self, "错误", "接收数据错误")
            if num > 0:
                if self.numreceive == 0:
                    # 获取到text光标
                    textCursor = self.textBrowser.textCursor()
                    # 滚动到底部
                    textCursor.movePosition(textCursor.End)
                    # 设置光标到text中去
                    self.textBrowser.setTextCursor(textCursor)
                    data = self.ser.read(num)
                    self.textBrowser_mode.insertPlainText(data[0].to_bytes(1, byteorder='big', signed=False).hex())
                    self.textBrowser_datalen.insertPlainText(data[1:3].hex())
                    self.textBrowser.insertPlainText(data[3:].hex())
                    self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部
                    self.numreceive = num
                    self.datalen = int(data[1:3].hex(), 16)
                else:
                    textCursor = self.textBrowser.textCursor()
                    # 滚动到底部
                    textCursor.movePosition(textCursor.End)
                    # 设置光标到text中去
                    self.textBrowser.setTextCursor(textCursor)
                    data = self.ser.read(num)
                    self.textBrowser.insertPlainText(data.hex())
                    self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部
                    self.numreceive += num
                    if self.numreceive >= self.datalen + 3:
                        self.datalen = 0
                        self.numreceive = 0

    def str2byte(self, data):
        data_arr = bytearray(data.encode("ASCII"))  # 将str类型转换为可变的bytearray
        data_int = list(data_arr)  # 再将其转换为int类型的List
        data_ok = list()  # 用来存放经过缩短后的数据
        # 将‘0’->0;'f'->15
        for index in range(len(data_int)):
            if data_int[index] >= 48 and data_int[index] <= 57:
                data_int[index] -= 0x30
            if data_int[index] >= 97 and data_int[index] <= 102:
                data_int[index] -= 0x57
        # 缩短数据
        for i in range(0, len(data_int), 2):
            data_ok.append(data_int[i] << 4 | data_int[i + 1])
        return bytes(data_ok)

    def closeEvent(self, event):
        self.ser.close()
        event.accept()


class SM2S(SM2S.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(SM2S, self).__init__()
        self.setupUi(self)  # 初始化
        self.ser = serial.Serial()
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_data)
        self.uart_open()
        self.pushButton_return.clicked.connect(self.close)
        self.pushButton_start.clicked.connect(self.send_data)
        self.datalen = 0
        self.numreceive = 0

    def uart_open(self):
        self.ser.port = "COM5"
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = 'N'
        try:
            self.ser.open()
        except:
            QMessageBox.warning(self, "错误", "无法打开此串口！")
            return

        if self.ser.isOpen():
            # 打开串口接收定时器，周期为10ms
            self.timer.start(5)

    def send_data(self):
        if self.ser.isOpen():
            data = self.plainTextEdit.toPlainText()
            data_bytes = self.str2byte(data)
            data_len = int(len(data) / 2).to_bytes(2, byteorder='big', signed=False)
            algorithm_bytes = 0x06.to_bytes(1, byteorder="big", signed=False)

            send_data = algorithm_bytes + data_len + data_bytes
            self.ser.write(send_data)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                QMessageBox.warning(self, "错误", "接收数据错误")
            if num > 0:
                if self.numreceive == 0:
                    # 获取到text光标
                    textCursor = self.textBrowser.textCursor()
                    # 滚动到底部
                    textCursor.movePosition(textCursor.End)
                    # 设置光标到text中去
                    self.textBrowser.setTextCursor(textCursor)
                    data = self.ser.read(num)
                    self.textBrowser_mode.insertPlainText(data[0].to_bytes(1, byteorder='big', signed=False).hex())
                    self.textBrowser_datalen.insertPlainText(data[1:3].hex())
                    self.textBrowser.insertPlainText(data[3:].hex())
                    self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部
                    self.numreceive = num
                    self.datalen = int(data[1:3].hex(), 16)
                else:
                    textCursor = self.textBrowser.textCursor()
                    # 滚动到底部
                    textCursor.movePosition(textCursor.End)
                    # 设置光标到text中去
                    self.textBrowser.setTextCursor(textCursor)
                    data = self.ser.read(num)
                    self.textBrowser.insertPlainText(data.hex())
                    self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部
                    self.numreceive += num
                    if self.numreceive >= self.datalen + 3:
                        self.datalen = 0
                        self.numreceive = 0

    def str2byte(self, data):
        data_arr = bytearray(data.encode("ASCII"))  # 将str类型转换为可变的bytearray
        data_int = list(data_arr)  # 再将其转换为int类型的List
        data_ok = list()  # 用来存放经过缩短后的数据
        # 将‘0’->0;'f'->15
        for index in range(len(data_int)):
            if data_int[index] >= 48 and data_int[index] <= 57:
                data_int[index] -= 0x30
            if data_int[index] >= 97 and data_int[index] <= 102:
                data_int[index] -= 0x57
        # 缩短数据
        for i in range(0, len(data_int), 2):
            data_ok.append(data_int[i] << 4 | data_int[i + 1])
        return bytes(data_ok)

    def closeEvent(self, event):
        self.ser.close()
        event.accept()


class SM2V(SM2V.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(SM2V, self).__init__()
        self.setupUi(self)  # 初始化
        self.ser = serial.Serial()
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_data)
        self.uart_open()
        self.pushButton_return.clicked.connect(self.close)
        self.pushButton_start.clicked.connect(self.send_data)

    def uart_open(self):
        self.ser.port = "COM5"
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = 'N'
        try:
            self.ser.open()
        except:
            QMessageBox.warning(self, "错误", "无法打开此串口！")
            return

        if self.ser.isOpen():
            # 打开串口接收定时器，周期为10ms
            self.timer.start(5)

    def send_data(self):
        if self.ser.isOpen():
            data = self.plainTextEdit.toPlainText()
            data_bytes = self.str2byte(data)
            data_len = int(len(data) / 2).to_bytes(2, byteorder='big', signed=False)
            algorithm_bytes = 0x07.to_bytes(1, byteorder="big", signed=False)

            send_data = algorithm_bytes + data_len + data_bytes
            self.ser.write(send_data)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                QMessageBox.warning(self, "错误", "接收数据错误")
            if num > 0:
                # 获取到text光标
                data = self.ser.read(num)
                if data == b'\x00':
                    QMessageBox.information(self, "提示", "验证成功！")
                    self.close()
                else:
                    QMessageBox.information(self, "提示", "验证失败！")
                    self.close()

    def str2byte(self, data):
        data_arr = bytearray(data.encode("ASCII"))  # 将str类型转换为可变的bytearray
        data_int = list(data_arr)  # 再将其转换为int类型的List
        data_ok = list()  # 用来存放经过缩短后的数据
        # 将‘0’->0;'f'->15
        for index in range(len(data_int)):
            if data_int[index] >= 48 and data_int[index] <= 57:
                data_int[index] -= 0x30
            if data_int[index] >= 97 and data_int[index] <= 102:
                data_int[index] -= 0x57
        # 缩短数据
        for i in range(0, len(data_int), 2):
            data_ok.append(data_int[i] << 4 | data_int[i + 1])
        return bytes(data_ok)

    def closeEvent(self, event):
        self.ser.close()
        event.accept()


class SM4En(SM4En.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(SM4En, self).__init__()
        self.setupUi(self)  # 初始化
        self.ser = serial.Serial()
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_data)
        self.uart_open()
        self.pushButton_return.clicked.connect(self.close)
        self.pushButton_start.clicked.connect(self.send_data)
        self.numreceive = 0
        self.datalen = 0

    def uart_open(self):
        self.ser.port = "COM5"
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = 'N'
        try:
            self.ser.open()
        except:
            QMessageBox.warning(self, "错误", "无法打开此串口！")
            return

        if self.ser.isOpen():
            # 打开串口接收定时器，周期为10ms
            self.timer.start(5)

    def send_data(self):
        if self.ser.isOpen():
            handle_bytes = 0x00000000.to_bytes(4, byteorder='big', signed=False)
            algorithm_bytes = 0x02.to_bytes(1, byteorder='big', signed=False)
            data = self.plainTextEdit.toPlainText()
            data_len = int(len(data) / 2).to_bytes(2, byteorder='big', signed=False)
            data_bytes = self.str2byte(data)

            send_data = algorithm_bytes + data_len + handle_bytes + data_bytes
            self.ser.write(send_data)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                QMessageBox.warning(self, "错误", "接收数据错误")
            if num > 0:
                if self.numreceive == 0:
                    # 获取到text光标
                    textCursor = self.textBrowser.textCursor()
                    # 滚动到底部
                    textCursor.movePosition(textCursor.End)
                    # 设置光标到text中去
                    self.textBrowser.setTextCursor(textCursor)
                    data = self.ser.read(num)
                    self.textBrowser_mode.insertPlainText(data[0].to_bytes(1, byteorder='big', signed=False).hex())
                    self.textBrowser_datalen.insertPlainText(data[1:3].hex())
                    self.textBrowser_handle.insertPlainText(data[3:7].hex())
                    self.textBrowser.insertPlainText(data[7:].hex())
                    self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部
                    self.numreceive = num
                    self.datalen = int(data[1:3].hex(), 16)
                else:
                    textCursor = self.textBrowser.textCursor()
                    # 滚动到底部
                    textCursor.movePosition(textCursor.End)
                    # 设置光标到text中去
                    self.textBrowser.setTextCursor(textCursor)
                    data = self.ser.read(num)
                    self.textBrowser.insertPlainText(data.hex())
                    self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部
                    self.numreceive += num
                    if self.numreceive >= self.datalen + 7:
                        self.datalen = 0
                        self.numreceive = 0

    def str2byte(self, data):
        data_arr = bytearray(data.encode("ASCII"))  # 将str类型转换为可变的bytearray
        data_int = list(data_arr)  # 再将其转换为int类型的List
        data_ok = list()  # 用来存放经过缩短后的数据
        # 将‘0’->0;'f'->15
        for index in range(len(data_int)):
            if data_int[index] >= 48 and data_int[index] <= 57:
                data_int[index] -= 0x30
            if data_int[index] >= 97 and data_int[index] <= 102:
                data_int[index] -= 0x57
        # 缩短数据
        for i in range(0, len(data_int), 2):
            data_ok.append(data_int[i] << 4 | data_int[i + 1])
        return bytes(data_ok)

    def closeEvent(self, event):
        self.ser.close()
        event.accept()


class SM4De(SM4De.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(SM4De, self).__init__()
        self.setupUi(self)  # 初始化
        self.ser = serial.Serial()
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_data)
        self.uart_open()
        self.pushButton_return.clicked.connect(self.close)
        self.pushButton_start.clicked.connect(self.send_data)
        self.datalen = 0
        self.numreceive = 0

    def uart_open(self):
        self.ser.port = "COM5"
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = 'N'
        try:
            self.ser.open()
        except:
            QMessageBox.warning(self, "错误", "无法打开此串口！")
            return

        if self.ser.isOpen():
            # 打开串口接收定时器，周期为10ms
            self.timer.start(5)

    def send_data(self):
        if self.ser.isOpen():
            data = self.plainTextEdit.toPlainText()
            handle = self.plainTextEdit_handle.toPlainText()
            data_bytes = self.str2byte(data)
            handle_bytes = self.str2byte(handle)
            data_len = int(len(data) / 2).to_bytes(2, byteorder='big', signed=False)
            algorithm_bytes = 0x03.to_bytes(1, byteorder='big', signed=False)

            send_data = algorithm_bytes + data_len + handle_bytes + data_bytes
            self.ser.write(send_data)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                QMessageBox.warning(self, "错误", "接收数据错误")
            if num > 0:
                if self.numreceive == 0:
                    # 获取到text光标
                    textCursor = self.textBrowser.textCursor()
                    # 滚动到底部
                    textCursor.movePosition(textCursor.End)
                    # 设置光标到text中去
                    self.textBrowser.setTextCursor(textCursor)
                    data = self.ser.read(num)
                    self.textBrowser_mode.insertPlainText(data[0].to_bytes(1, byteorder='big', signed=False).hex())
                    self.textBrowser_datalen.insertPlainText(data[1:3].hex())
                    self.textBrowser_handle.insertPlainText(data[3:7].hex())
                    self.textBrowser.insertPlainText(data[7:].hex())
                    self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部
                    self.numreceive = num
                    self.datalen = int(data[1:3].hex(), 16)
                else:
                    textCursor = self.textBrowser.textCursor()
                    # 滚动到底部
                    textCursor.movePosition(textCursor.End)
                    # 设置光标到text中去
                    self.textBrowser.setTextCursor(textCursor)
                    data = self.ser.read(num)
                    self.textBrowser.insertPlainText(data.hex())
                    self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部
                    self.numreceive += num
                    if self.numreceive >= self.datalen + 7:
                        self.datalen = 0
                        self.numreceive = 0

    def str2byte(self, data):
        data_arr = bytearray(data.encode("ASCII"))  # 将str类型转换为可变的bytearray
        data_int = list(data_arr)  # 再将其转换为int类型的List
        data_ok = list()  # 用来存放经过缩短后的数据
        # 将‘0’->0;'f'->15
        for index in range(len(data_int)):
            if data_int[index] >= 48 and data_int[index] <= 57:
                data_int[index] -= 0x30
            if data_int[index] >= 97 and data_int[index] <= 102:
                data_int[index] -= 0x57
        # 缩短数据
        for i in range(0, len(data_int), 2):
            data_ok.append(data_int[i] << 4 | data_int[i + 1])
        return bytes(data_ok)

    def closeEvent(self, event):
        self.ser.close()
        event.accept()


class Menu(Menu.Ui_Menu, QMainWindow):
    def __init__(self):
        super(Menu, self).__init__()
        self.setupUi(self)
        self.pushButton_WK.clicked.connect(self.writekey)
        self.pushButton_SM2E.clicked.connect(self.sm2en)
        self.pushButton_SM2D.clicked.connect(self.sm2de)
        self.pushButton_SM2S.clicked.connect(self.sm2s)
        self.pushButton_SM2V.clicked.connect(self.sm2v)
        self.pushButton_SM4D.clicked.connect(self.sm4de)
        self.pushButton_SM4E.clicked.connect(self.sm4en)

    def writekey(self):
        self.WriteKey_window = WriteKey()
        self.WriteKey_window.show()

    def sm2en(self):
        self.SM2En_window = SM2En()
        self.SM2En_window.show()

    def sm2de(self):
        self.SM2De_window = SM2De()
        self.SM2De_window.show()

    def sm2s(self):
        self.SM2S_window = SM2S()
        self.SM2S_window.show()

    def sm2v(self):
        self.SM2V_window = SM2V()
        self.SM2V_window.show()

    def sm4en(self):
        self.SM4En_window = SM4En()
        self.SM4En_window.show()

    def sm4de(self):
        self.SM4De_window = SM4De()
        self.SM4De_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    apply_stylesheet(app, theme='dark_cyan.xml')
    Menu_window = Menu()
    Menu_window.show()
    sys.exit(app.exec_())
