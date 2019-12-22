# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\pytools\scrollui\untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QRegExpValidator, QIntValidator, QIcon
from server import runApp
import inspect
import ctypes
from threading import Thread
from setlog import Log

class MyThread(Thread):
    def __init__(self, port, address='0.0.0.0'):
        super().__init__()
        self.address = address
        self.port = port

    def run(self):
        runApp(self.address, self.port)

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)

class Ui_Form(object):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.count = 11
        self.scrollAreaBarHeight = 0
        self.log = Log()

    def start_server(self):
        self.start_button.setEnabled(False)
        self.server_thread = MyThread(self.port.text(), self.address.text())
        self.server_thread.start()
        self.stop_button.setEnabled(True)
        self.log.info('---------------start server---------------')
    
    def stop_server(self):
        self.stop_button.setEnabled(False)
        try:
            self.server_thread.stop_thread(self.server_thread)
            self.start_button.setEnabled(True)
            self.log.info('---------------stop server---------------')
        except Exception as e:
            self.log.error('启动flask服务报错:%s'%e)
    
    def addUrl(self):
        i = self.count
        if i <= 20:
            self.lab = QtWidgets.QLabel(self.gridLayoutWidget)
            self.lab.setMinimumSize(QtCore.QSize(15, 25))
            self.lab.setObjectName("lab" + str(i))
            self.gridLayout.addWidget(self.lab, i, 0, 1, 1, Qt.AlignTop)
            self.lab.setText(str(i))

            self.url = QtWidgets.QLineEdit(self.gridLayoutWidget)
            self.url.setPlaceholderText('请输入url')
            self.url.setMaximumSize(QtCore.QSize(200, 25))
            self.url.setMinimumHeight(25)
            self.url.setObjectName("url" + str(i))
            self.url.setValidator(self.url_reg_validator)
            self.url.setToolTip('输入格式:/[a-zA-Z/]*')
            self.gridLayout.addWidget(self.url, i, 1, 1, 1, Qt.AlignTop)

            self.result = QtWidgets.QLineEdit(self.gridLayoutWidget)
            self.result.setPlaceholderText('请输入返回json字符串')
            self.result.setMinimumSize(QtCore.QSize(600, 25))
            self.result.setObjectName("result" + str(i))
            self.gridLayout.addWidget(self.result, i, 2, 1, 1, Qt.AlignTop)
            self.scrollAreaWidgetContents.show()
            self.moveScrollBar('down')

        else:
            QMessageBox.information(self.scrollAreaWidgetContents, ('提示'), ('已达到上限20'))
            self.count = 20
        
        self.count += 1
        self.start_button.setEnabled(False)

    def deleteUrl(self):
        self.count -= 1
        i = self.count
        if i > 0:
            self.lab = self.gridLayoutWidget.findChild(QtWidgets.QLabel, 'lab' + str(i))
            self.lab.deleteLater()
            self.url = self.gridLayoutWidget.findChild(QtWidgets.QLineEdit, 'url' + str(i))
            self.url.deleteLater()
            self.result = self.gridLayoutWidget.findChild(QtWidgets.QLineEdit, 'result' + str(i))
            self.result.deleteLater()
            self.scrollAreaWidgetContents.show()
            self.moveScrollBar('up')
        else:
            QMessageBox.information(self.scrollAreaWidgetContents, ('提示'), ('已全部删除'))
            self.count = 1
        self.start_button.setEnabled(False)

    def saveOrUpdateData(self):
        data = {}
        urls_and_results = self.gridLayoutWidget.findChildren(QtWidgets.QLineEdit)
        text_data = [item.text() for item in urls_and_results]
        for i in range(0, len(urls_and_results), 2):
            data[text_data[i]] = text_data[i+1]
        data.pop('')
        try:
            with open('./data.ini', 'w') as f:
                f.write(str(data))
            if self.stop_button.isEnabled():
                self.start_button.setEnabled(False)
            else:
                self.start_button.setEnabled(True)
        except Exception as e:
            self.log.error('保存数据报错:%s'%e)

    def moveScrollBar(self, flag):
        self.scrollAreaBar = self.scrollArea.verticalScrollBar()
        if flag =='down':
            if self.count > 10:
                self.scrollAreaBarHeight += 50
                self.scrollAreaBar.setValue(self.scrollAreaBarHeight)
        elif flag =='up':
            if self.count > 10:
                self.scrollAreaBarHeight -= 50
                self.scrollAreaBar.setValue(self.scrollAreaBarHeight)
        
    def signalConnect(self):
        self.add_button.clicked.connect(self.addUrl)
        self.delete_button.clicked.connect(self.deleteUrl)
        self.start_button.clicked.connect(self.start_server)
        self.stop_button.clicked.connect(self.stop_server)
        self.save_button.clicked.connect(self.saveOrUpdateData)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(853, 650)
        Form.setMaximumSize(QtCore.QSize(853, 650))
        self.icon = QIcon('./resource/wings.png')
        Form.setWindowIcon(self.icon)

        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(20, 20, 800, 500))
        self.scrollArea.setMaximumSize(QtCore.QSize(800, 1000))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 800, 1000))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(800, 1000))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.gridLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 800, 1000))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")

        url_reg = QRegExp(r'^/[a-zA-Z0-9/]*$')
        self.url_reg_validator = QRegExpValidator(url_reg)
        for i in range(1, 11):
            self.lab = QtWidgets.QLabel(self.gridLayoutWidget)
            self.lab.setMinimumSize(QtCore.QSize(15, 25))
            self.lab.setObjectName("lab" + str(i))
            self.gridLayout.addWidget(self.lab, i, 0, 1, 1, Qt.AlignTop)

            self.lab.setText(str(i))

            self.url = QtWidgets.QLineEdit(self.gridLayoutWidget)
            self.url.setPlaceholderText('请输入url')
            self.url.setMaximumSize(QtCore.QSize(200, 25))
            self.url.setMinimumHeight(25)
            self.url.setObjectName("url" + str(i))
            self.url.setValidator(self.url_reg_validator)
            self.url.setToolTip('输入格式:/[a-zA-Z/]*')
            self.gridLayout.addWidget(self.url, i, 1, 1, 1, Qt.AlignTop)

            self.result = QtWidgets.QLineEdit(self.gridLayoutWidget)
            self.result.setPlaceholderText('请输入返回json字符串')
            self.result.setMinimumSize(QtCore.QSize(570, 25))
            self.result.setObjectName("result" + str(i))
            self.gridLayout.addWidget(self.result, i, 2, 1, 1, Qt.AlignTop)
        
        self.gridLayout.setVerticalSpacing(25)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)  #布局内部控件不填满，使用设定的size
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(20, 559, 800, 100))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 781, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.address = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.address.setMinimumSize(QtCore.QSize(200, 25))
        self.address.setObjectName("address")
        self.address.setText('0.0.0.0')
        self.address.setReadOnly(True)
        self.horizontalLayout.addWidget(self.address)

        self.port = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.port.setMaximumSize(QtCore.QSize(100, 25))
        self.port.setObjectName("port")
        self.port.setText('8080')
        #self.port.setMaxLength(5)
        self.port.setValidator(QIntValidator(0, 65536))
        self.horizontalLayout.addWidget(self.port)

        self.add_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.add_button.setMaximumSize(QtCore.QSize(50, 25))
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)

        self.save_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.save_button.setMaximumSize(QtCore.QSize(50, 25))
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)

        self.delete_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.delete_button.setMaximumSize(QtCore.QSize(50, 25))
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout.addWidget(self.delete_button)

        self.start_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.start_button.setMaximumSize(QtCore.QSize(50, 25))
        self.start_button.setObjectName("start_button")
        self.start_button.setEnabled(False)
        self.horizontalLayout.addWidget(self.start_button)

        self.stop_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.stop_button.setMaximumSize(QtCore.QSize(50, 25))
        self.stop_button.setObjectName("stop_button")
        self.stop_button.setEnabled(False)
        self.horizontalLayout.addWidget(self.stop_button)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.signalConnect()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Demo"))
        self.address.setPlaceholderText(_translate("Form", "请输入ip地址"))
        self.port.setPlaceholderText(_translate("Form", "请输入端口号"))
        self.add_button.setText(_translate("Form", "新增"))
        self.save_button.setText(_translate("Form", "保存"))
        self.delete_button.setText(_translate("Form", "删除"))
        self.start_button.setText(_translate("Form", "开始"))
        self.stop_button.setText(_translate("Form", "停止"))



if __name__ == '__main__':
    app = QApplication(sys.argv)  #
    MainWindow = QWidget() 
    ui = Ui_Form() 
    ui.setupUi(MainWindow) 
    MainWindow.show() 
    sys.exit(app.exec_())