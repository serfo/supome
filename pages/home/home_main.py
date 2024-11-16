# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont)
from qfluentwidgets import FluentIcon as FIF


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))



class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = Widget('信息中心', self)
        self.appInterface = Widget('创建隧道', self)
        self.videoInterface = Widget('隧道管理', self)
        self.peopleInterface = Widget('用户', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页中心', FIF.HOME_FILL)
        self.addSubInterface(self.appInterface, FIF.APPLICATION, '创建隧道')
        self.addSubInterface(self.videoInterface, FIF.VIDEO, '隧道管理')

        self.addSubInterface(self.peopleInterface, FIF.BOOK_SHELF, '用户', FIF.PEOPLE, NavigationItemPosition.BOTTOM)
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(1000, 650)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('速连内网穿透 - supo.me')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def showMessageBox(self):
        w = MessageBox(
            '速连内网穿透',
            '打开教程中心docs.supo.me寻找教程🚀',
            self
        )
        w.yesButton.setText('打开网站')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("http://supo.me"))


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
