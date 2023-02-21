import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QStatusBar
from PyQt5.QtCore import QTimer
import Menu
import WriteKey
import SM2
import SM4De
import SM4En
from PyQt5.QtCore import Qt

import serial
import serial.tools.list_ports
from time import sleep

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
        self.pushButton_return.clicked.connect(self.back)
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
            send_data = self.plainTextEdit.toPlainText()
            send_data += '\r\n'
            send_data = send_data.encode('UTF-8')
            self.ser.write(send_data)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                QMessageBox.warning(self, "错误", "接收数据错误")
            if num > 0:
                data = self.ser.read(num)
                self.statusbar.showMessage(data.decode('UTF-8'))

    def back(self):
        self.ser.close()
        self.close()

class SM2(SM2.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(SM2, self).__init__()
        self.setupUi(self)  # 初始化
        self.ser = serial.Serial()
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_data)
        self.uart_open()
        self.pushButton_return.clicked.connect(self.back)
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
            send_data = self.plainTextEdit.toPlainText()
            send_data += '\r\n'
            send_data = send_data.encode('UTF-8')
            self.ser.write(send_data)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                QMessageBox.warning(self, "错误", "接收数据错误")
            if num > 0:
                # 获取到text光标
                textCursor = self.textBrowser.textCursor()
                # 滚动到底部
                textCursor.movePosition(textCursor.End)
                # 设置光标到text中去
                self.textBrowser.setTextCursor(textCursor)
                data = self.ser.read(num)
                self.textBrowser.insertPlainText(data.decode('utf-8'))
                self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部

    def back(self):
        self.ser.close()
        self.close()

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
        self.pushButton_return.clicked.connect(self.back)
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
            send_data = self.plainTextEdit.toPlainText()
            send_data += '\r\n'
            send_data = send_data.encode('UTF-8')
            self.ser.write(send_data)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                QMessageBox.warning(self, "错误", "接收数据错误")
            if num > 0:
                # 获取到text光标
                textCursor = self.textBrowser.textCursor()
                # 滚动到底部
                textCursor.movePosition(textCursor.End)
                # 设置光标到text中去
                self.textBrowser.setTextCursor(textCursor)
                data = self.ser.read(num)
                self.textBrowser.insertPlainText(data.decode('utf-8'))
                self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部

    def back(self):
        self.ser.close()
        self.close()

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
        self.pushButton_return.clicked.connect(self.back)
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
            send_data = self.plainTextEdit.toPlainText()
            send_data += '\r\n'
            send_data = send_data.encode('UTF-8')
            self.ser.write(send_data)
            sleep(0.1)
            send_data = self.plainTextEdit_handle.toPlainText()
            send_data += '\r\n'
            send_data = send_data.encode('UTF-8')
            self.ser.write(send_data)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                QMessageBox.warning(self, "错误", "接收数据错误")
            # 获取到text光标
            textCursor = self.textBrowser.textCursor()
            # 滚动到底部
            textCursor.movePosition(textCursor.End)
            # 设置光标到text中去
            self.textBrowser.setTextCursor(textCursor)
            data = self.ser.read(num)
            self.textBrowser.insertPlainText(data.decode('utf-8'))
           # self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部

    def back(self):
        self.ser.close()
        self.close()

class Menu(Menu.Ui_Menu, QMainWindow):
    def __init__(self):
        super(Menu, self).__init__()
        self.setupUi(self)
        self.ser = serial.Serial()
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_data)
        self.uart_open()
        self.pushButton_WK.clicked.connect(self.writekey)
        self.pushButton_SM2_2.clicked.connect(self.sm2)
        self.pushButton_SM4D.clicked.connect(self.sm4de)
        self.pushButton_SM4E.clicked.connect(self.sm4en)
    def writekey(self):
        if not self.ser.isOpen():
            self.uart_open()
        send_data = '4'
        send_data += '\r\n'
        send_data = send_data.encode('UTF-8')
        self.ser.write(send_data)
        self.ser.close()
        self.WriteKey_window = WriteKey()
        self.WriteKey_window.show()

    def sm2(self):
        if not self.ser.isOpen():
            self.uart_open()
        send_data = '0'
        send_data+='\r\n'
        send_data = send_data.encode('UTF-8')
        self.ser.write(send_data)
        self.ser.close()
        self.SM2_window = SM2()
        self.SM2_window.show()
    def sm4en(self):
        if not self.ser.isOpen():
            self.uart_open()
        send_data = '2'
        send_data += '\r\n'
        send_data = send_data.encode('UTF-8')
        self.ser.write(send_data)
        self.ser.close()
        self.SM4En_window = SM4En()
        self.SM4En_window.show()
    def sm4de(self):
        if not self.ser.isOpen():
            self.uart_open()
        send_data = '3'
        send_data+='\r\n'
        send_data = send_data.encode('UTF-8')
        self.ser.write(send_data)
        self.ser.close()
        self.SM4De_window = SM4De()
        self.SM4De_window.show()
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

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                QMessageBox.warning(self, "错误", "接收数据错误")
            if num > 0:
                # 获取到text光标
                data = self.ser.read(num)
                data=data.decode('UTF-8')
                print(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Menu_window = Menu()
    Menu_window.show()
    sys.exit(app.exec_())