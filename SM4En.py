# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\SM4En.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(50, 30, 72, 15))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(50, 220, 91, 16))
        self.label_6.setObjectName("label_6")
        self.pushButton_return = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_return.setGeometry(QtCore.QRect(500, 490, 171, 51))
        self.pushButton_return.setObjectName("pushButton_return")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(140, 490, 171, 51))
        self.pushButton_start.setObjectName("pushButton_start")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(50, 240, 701, 121))
        self.textBrowser.setObjectName("textBrowser")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(50, 50, 701, 101))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(50, 380, 91, 16))
        self.label_7.setObjectName("label_7")
        self.textBrowser_handle = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_handle.setGeometry(QtCore.QRect(50, 400, 701, 31))
        self.textBrowser_handle.setObjectName("textBrowser_handle")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SM4加密"))
        self.label_5.setText(_translate("MainWindow", "明文："))
        self.label_6.setText(_translate("MainWindow", "密文："))
        self.pushButton_return.setText(_translate("MainWindow", "返回"))
        self.pushButton_start.setText(_translate("MainWindow", "加密"))
        self.plainTextEdit.setPlaceholderText(_translate("MainWindow", "请在此输入待加密明文"))
        self.label_7.setText(_translate("MainWindow", "句柄："))
