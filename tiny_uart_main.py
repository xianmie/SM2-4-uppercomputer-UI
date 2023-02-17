import sys
import serial
import serial.tools.list_ports

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import QTimer
from Ui_tiny_uart import Ui_MainWindow
from time import sleep

APP_NAME = "Tiny Uart V1.0.0"


class Pyqt5_Serial(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Pyqt5_Serial, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.ser = serial.Serial()
        self.ser.setRTS(False)
        self.ser.setDTR(False)
        self.uart_refresh()
        self.init()

        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.rx_lcdNumber.setDigitCount(10)
        self.rx_lcdNumber.display(self.data_num_received)
        self.data_num_sended = 0
        self.tx_lcdNumber.setDigitCount(10)
        self.tx_lcdNumber.display(self.data_num_sended)

    def init(self):
        # 关联串口刷新按钮
        self.pushButton_refresh.clicked.connect(self.uart_refresh)
        # 关联打开串口按钮
        self.pushButton_open.clicked.connect(self.uart_open)
        # 关联发送数据按钮
        self.pushButton_send.clicked.connect(self.send_data)
        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receive_data)
        # 关联发送计数
        self.pushButton_clear_tx.clicked.connect(self.clear_send_num)
        # 关联接收计数
        self.pushButton_clear_rx.clicked.connect(self.clear_receive_num)

    def uart_refresh(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.comboBox_uart.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[1]] = "%s" % port[0]
            self.comboBox_uart.addItem(port[1])
        if len(self.Com_Dict) == 0:
            self.comboBox_uart.setCurrentText("")
            self.pushButton_open.setEnabled(False)
        else:
            self.pushButton_open.setEnabled(True)

    def uart_open(self):
        if self.pushButton_open.text() == '打开串口':
            self.ser.port = self.Com_Dict[self.comboBox_uart.currentText()]
            self.ser.baudrate = int(self.comboBox_baud.currentText())
            self.ser.bytesize = int(self.comboBox_data.currentText())
            self.ser.stopbits = int(self.comboBox_stop.currentText())
            self.ser.parity = self.comboBox_check.currentText()

            try:
                self.ser.open()
            except:
                QMessageBox.warning(self, "错误", "无法打开此串口！")
                return

            if self.ser.isOpen():
                self.pushButton_open.setText('关闭串口')
                # 打开串口接收定时器，周期为10ms
                self.timer.start(5)
        else:
            self.timer.stop()
            try:
                self.ser.close()
            except:
                pass

            if self.ser.isOpen() == False:
                self.pushButton_open.setText('打开串口')

    def send_data(self):
        if self.ser.isOpen():
            send_data = self.tx_plainTextEdit.toPlainText()
            send_data+='\r\n'
            send_data = send_data.encode('UTF-8')
            send_count = self.ser.write(send_data)
            self.data_num_sended += send_count
            self.tx_lcdNumber.display(self.data_num_sended)

    def receive_data(self):
        if self.ser.isOpen():
            try:
                num = self.ser.inWaiting()
            except:
                self.timer.stop()
                self.ser.close()
                self.pushButton_open.setText('打开串口')
                return
            if num > 0:
                # 获取到text光标
                textCursor = self.rx_textBrowser.textCursor()
                # 滚动到底部
                textCursor.movePosition(textCursor.End)
                # 设置光标到text中去
                self.rx_textBrowser.setTextCursor(textCursor)
                data = self.ser.read(num)
                if self.radioButton_hex.isChecked():
                    rev_data = ''
                    for i in range(0, len(data)):
                        rev_data = rev_data + '{:02X}'.format(data[i]) + ' '
                    self.rx_textBrowser.insertPlainText(rev_data)
                else:
                    self.rx_textBrowser.insertPlainText(data.decode('utf-8'))

                # 统计接收字符的数量
                self.data_num_received += num
                self.rx_lcdNumber.display(self.data_num_received)

                self.rx_textBrowser.moveCursor(self.rx_textBrowser.textCursor().End)  #文本框显示到底部

    def clear_send_num(self):
        self.data_num_sended = 0
        self.tx_lcdNumber.display(self.data_num_sended)
        self.tx_plainTextEdit.clear()

    def clear_receive_num(self):
        self.data_num_received = 0
        self.rx_lcdNumber.display(self.data_num_received)
        self.rx_textBrowser.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    tiny_uart = Pyqt5_Serial()
    tiny_uart.show()
    sys.exit(app.exec_())
