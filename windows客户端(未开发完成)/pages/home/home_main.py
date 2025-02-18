import os
import sys

import qfluentwidgets
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QIcon, QDesktopServices, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QSystemTrayIcon, QMenu, QAction, QTextBrowser, QWidget, \
    QTableWidgetItem, QLabel, QSizePolicy, QHeaderView, QHBoxLayout, QSpacerItem, QMenu, QAction, QApplication, \
    QTableWidget
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, TableWidget, RoundMenu, Action,
                            MenuAnimationType, FluentIcon)
from qfluentwidgets import FluentIcon as FIF
sys.path.append('../subpage')
import index, node_status, proxies_mn

class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0,0,0,0)  # 设置布局的边距为0
        self.setObjectName(text.replace(' ', '-'))  # 设置当前小部件的对象名称，将空格替换为破折号。

class HomeWidget(Widget):

    def __init__(self, parent=None):
        super().__init__('信息中心', parent)
        self.textBrowser = QTextBrowser(self)
        self.vBoxLayout.addWidget(self.textBrowser, stretch=1)  # 设置拉伸因子为1，使QTextBrowser填满整个布局

        # 获取并设置 Markdown 内容
        markdown_content = index.get_markdown_content()
        self.textBrowser.setMarkdown(markdown_content)

        # 设置字体
        font = QFont("Cambria", 12)  # 设置字体为 Cambria，大小为 12
        self.textBrowser.setFont(font)

        # 禁用滚动条
        self.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

class NodeWidget(Widget):

    def __init__(self, parent=None):
        super().__init__('节点状态', parent)
        self.textBrowser = QTextBrowser(self)
        self.vBoxLayout.addWidget(self.textBrowser, stretch=1)  # 设置拉伸因子为1，使QTextBrowser填满整个布局

        # 获取并设置初始 Markdown 内容
        self.update_markdown_content()

        # 设置字体
        font = QFont("Cambria", 12)  # 设置字体为 Cambria，大小为 12
        self.textBrowser.setFont(font)

        # 禁用滚动条
        self.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 设置定时器，每10秒更新一次内容
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_markdown_content)
        self.timer.start(10000)  # 10000毫秒 = 10秒

    def update_markdown_content(self):
        # 获取最新的 Markdown 内容
        markdown_content = node_status.get_markdown_content()
        self.textBrowser.setMarkdown(markdown_content)


class PrmnWidget(Widget):
    def __init__(self, parent=None):
        super().__init__('隧道管理', parent)

        # 设置主题
        setTheme(Theme.LIGHT)  # 可以选择 Theme.LIGHT 或 Theme.DARK

        # 创建表格
        self.tableWidget = TableWidget(self)
        self.vBoxLayout.addWidget(self.tableWidget, stretch=1)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID',  '名称','服务器节点', '地址', '端口','类型'])

        # 启用滚动条
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 禁止编辑
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        # 添加示例数据
        self.add_sample_data()

        # 连接点击事件
        self.tableWidget.cellClicked.connect(self.on_cell_clicked)

        # 连接右键菜单
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.open_proxies_info)


    def add_sample_data(self):
        # 示例数据
        proxies_list = proxies_mn.get_proxies()

        # 获取字典的键作为表头
        headers = list(proxies_list[0].keys()) if proxies_list else []

        # 设置表格的列数
        self.tableWidget.setColumnCount(len(headers))

        # 设置表头
        self.tableWidget.setHorizontalHeaderLabels(headers)

        # 设置表格的行数
        self.tableWidget.setRowCount(len(proxies_list))

        # 填充表格数据
        for row, data in enumerate(proxies_list):
            for col, key in enumerate(headers):
                value = data[key]
                if key == '主机名访问' and value != 'N/A':
                    label = QLabel(f'<a href="{value}">{value}</a>')
                    label.setOpenExternalLinks(True)
                    label.setAlignment(Qt.AlignCenter)
                    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    self.tableWidget.setCellWidget(row, col, label)
                else:
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)  # 居中显示
                    self.tableWidget.setItem(row, col, item)

        # 调整列宽
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setVerticalHeaderItem(i, QTableWidgetItem(""))
        # self.tableWidget.setColumnWidth(1, 400)

    def on_cell_clicked(self, row, column):
        # 获取表头
        headers = [self.tableWidget.horizontalHeaderItem(i).text() for i in range(self.tableWidget.columnCount())]

        # 检查是否点击了包含URL的列
        if headers[column] == '主机名访问':
            widget = self.tableWidget.cellWidget(row, column)
            if widget:
                url = widget.text().split('"')[1]  # 提取 URL
                QDesktopServices.openUrl(QUrl(url))
    def open_proxies_info(self, e):
        menu = RoundMenu()

        menu.addAction(Action(FluentIcon.COPY, '复制', triggered=lambda: print("复制成功")))
        menu.addAction(Action(FluentIcon.CUT, '剪切', triggered=lambda: print("剪切成功")))
        # 批量添加动作
        menu.addActions([
            Action(FluentIcon.PASTE, '粘贴'),
            Action(FluentIcon.CANCEL, '撤销')
        ])
        # 添加分割线
        menu.addSeparator()
        menu.addAction(QAction('全选', shortcut='Ctrl+A'))



class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.tray_icon = None  # 初始化系统托盘图标

        # 创建子界面
        self.homeInterface = HomeWidget(self)
        self.appInterface = Widget('创建隧道', self)
        self.proxies_mnInterface = PrmnWidget(self)
        self.nodeInterface = NodeWidget(self)
        self.peopleInterface = Widget('用户', self)

        self.initNavigation()
        self.initWindow()
        self.initTrayIcon()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '信息中心', FIF.HOME_FILL)
        self.addSubInterface(self.appInterface, FIF.APPLICATION, '创建隧道')
        self.addSubInterface(self.proxies_mnInterface, FIF.VIDEO, '隧道管理')
        self.addSubInterface(self.nodeInterface, FIF.CLOUD, '节点状态')
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
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def initTrayIcon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.windowIcon())
        self.tray_icon.setToolTip('速连内网穿透 - supo.me')

        menu = QMenu(self)
        restore_action = QAction('显示主窗口', self)
        restore_action.triggered.connect(self.showNormal)
        quit_action = QAction('退出程序', self)
        quit_action.triggered.connect(self.quitApp)

        menu.addAction(restore_action)
        menu.addAction(quit_action)
        self.tray_icon.setContextMenu(menu)

        # 连接激活事件
        self.tray_icon.activated.connect(self.onTrayIconActivated)

        self.tray_icon.show()

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.showNormal()  # 单击托盘图标时恢复主窗口

    def closeEvent(self, event):
        # 当尝试关闭窗口时，隐藏窗口并阻止窗口关闭
        event.ignore()
        self.hide()
        self.tray_icon.showMessage('速连内网穿透', '程序已最小化到系统托盘', QSystemTrayIcon.Information, 2000)

    def quitApp(self):
        # 完全退出程序
        self.tray_icon.hide()
        QApplication.quit()

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

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())