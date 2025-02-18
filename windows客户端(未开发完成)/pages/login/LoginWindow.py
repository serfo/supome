# -*- coding: utf-8 -*-
import os
import json
import sys
import subprocess
from datetime import datetime
from configparser import ConfigParser
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from qfluentwidgets import BodyLabel, CheckBox, LineEdit, PrimaryPushButton
from function.login import login_status, login_get_cookies


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1275, 678)
        Form.setMinimumSize(QtCore.QSize(700, 500))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./../../static/img/background.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(360, 0))
        self.widget.setMaximumSize(QtCore.QSize(360, 16777215))
        self.widget.setStyleSheet("QLabel{\n"
                                  "    font: 13px \'Microsoft YaHei\'\n"
                                  "}")
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_2.setSpacing(9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(100, 100))
        self.label_2.setMaximumSize(QtCore.QSize(100, 100))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("./../../static/img/logo.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        self.label_5 = BodyLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.lineEdit_3 = LineEdit(self.widget)
        self.lineEdit_3.setClearButtonEnabled(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_2.addWidget(self.lineEdit_3)
        self.label_6 = BodyLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.lineEdit_4 = LineEdit(self.widget)
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_4.setClearButtonEnabled(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.verticalLayout_2.addWidget(self.lineEdit_4)
        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)
        self.checkBox = CheckBox(self.widget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_2.addWidget(self.checkBox)
        spacerItem3 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem3)
        self.pushButton = PrimaryPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        spacerItem4 = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.on_login_clicked)  # 连接按钮点击事件
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.load_saved_login_info()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_5.setText(_translate("Form", "用户名"))
        self.lineEdit_3.setPlaceholderText(_translate("Form", "username"))
        self.label_6.setText(_translate("Form", "密码"))
        self.lineEdit_4.setPlaceholderText(_translate("Form", "••••••••••••"))
        self.checkBox.setText(_translate("Form", "记住密码"))
        self.pushButton.setText(_translate("Form", "登录"))

    def load_saved_login_info(self):
        """加载已保存的登录信息"""
        login_info_path = './../../config/login_info.ini'
        if os.path.exists(login_info_path):
            config = ConfigParser()
            config.read(login_info_path)
            if 'login' in config:  # 注意这里的节名与保存时保持一致
                login_info = config['login']
                self.lineEdit_3.setText(login_info.get('username', ''))
                if self.checkBox.isChecked():  # 只有当记住密码选项被选中时才填充密码
                    self.lineEdit_4.setText(login_info.get('password', ''))
    def on_login_clicked(self):
        username = self.lineEdit_3.text()
        password = self.lineEdit_4.text()
        cookies = login_get_cookies(username, password)
        user, email = login_status(cookies)

        if user and user == username:
            QtWidgets.QMessageBox.information(self, "提示", f"登录成功！欢迎用户{user}，邮箱{email}")

            # 保存登录信息到INI文件
            config = ConfigParser()
            config['login'] = {
                'username': username,
                'password': password,  # 注意：这里应该对密码进行加密处理，而不是明文存储
                'cookies': cookies
            }
            with open('./../../config/login_info.ini', 'w') as configfile:
                config.write(configfile)

            self.close()
            home_main_path = os.path.join("..", "home", "home_main.py")
            python_executable = sys.executable
            try:
                process = subprocess.Popen([python_executable, home_main_path], stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "警告", "登录失败！")
        else:
            QtWidgets.QMessageBox.warning(self, "警告", "用户名或密码错误！")


def check_login_info():
    login_info_path = './../../config/login_info.ini'
    if os.path.exists(login_info_path):
        config = ConfigParser()
        config.read(login_info_path)
        if 'Login' in config:
            login_info = config['login']
            # 检查登录信息是否有效，例如通过调用login_status函数
            cookies = json.loads(login_info['cookies'])
            user, email = login_status(cookies)
            if user and user == login_info['username']:
                # 自动登录成功，跳转至主界面
                home_main_path = os.path.join("..", "home", "home_main.py")
                python_executable = sys.executable
                try:
                    process = subprocess.Popen([python_executable, home_main_path], stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                except Exception as e:
                    print(f"自动登录失败: {e}")
            else:
                # 登录信息无效，显示登录界面
                show_login_form()
    else:
        # 如果没有找到登录信息文件，直接显示登录界面
        show_login_form()


def show_login_form():
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    check_login_info()