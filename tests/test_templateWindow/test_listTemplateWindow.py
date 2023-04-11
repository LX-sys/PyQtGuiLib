# -*- coding:utf-8 -*-
# @time:2023/4/1112:42
# @author:LX
# @file:test_listTemplateWindow.py
# @software:PyCharm
from PyQtGuiLib.header import (
    PYQT_VERSIONS,
    QApplication,
    sys,
    QWidget,
    QLabel,
    Qt
)

from random import randint
from PyQtGuiLib.templateWindow import ListTemplateWindow

'''
    测试 实际使用 模板窗口
'''

class myWidget(ListTemplateWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # 添加菜单
        self.addMenu({
            "text": "测试",
            "call": self.test,
        })

        # 添加头像
        self.setHeadPicture(r"D:\code\PyQtGuiLib\tests\temp_image\python1.png")

        # 添加页面
        self.addItem("首页",self.frist_page(),r"D:\code\PyQtGuiLib\tests\temp_image\python1.png")
        self.addItem("第二页",self.two_page(),r"D:\code\PyQtGuiLib\tests\temp_image\python1.png")

        # 头部窗口
        self.addHeadWidget(self.headWidget())

    def test(self):
        print("测试回调函数")

    def frist_page(self):
        widget = QLabel("我是首页")
        widget.setAlignment(Qt.AlignCenter)
        widget.setStyleSheet('''
background-color: rgb(229, 229, 229);
font: 22pt "黑体";
        ''')
        return widget

    def two_page(self):
        widget = QLabel("我是第二页")
        widget.setAlignment(Qt.AlignCenter)
        widget.setStyleSheet('''
        background-color: #ffd997;
        font: 22pt "黑体";
                ''')
        return widget

    def headWidget(self):
        widget = QLabel("头部窗口")
        widget.setAlignment(Qt.AlignCenter)
        widget.setStyleSheet('''
        font: 22pt "黑体";
                ''')
        return widget

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = myWidget()
    win.show()

    if PYQT_VERSIONS in ["PyQt6","PySide6"]:
        sys.exit(app.exec())
    else:
        sys.exit(app.exec_())
